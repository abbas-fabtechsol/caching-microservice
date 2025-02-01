from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select, SQLModel
from models import CachedResult, Payload
from database import get_session, engine
from contextlib import asynccontextmanager
from utils import transform_string
from pydantic import BaseModel
from typing import List
import uuid
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create tables at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Caching Microservice",lifespan=lifespan)



class PayloadRequest(BaseModel):
    list_1: List[str]
    list_2: List[str]

class PayloadResponse(BaseModel):
    output: str

@app.post("/payload", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_payload(payload: PayloadRequest, session: Session = Depends(get_session)):
    if len(payload.list_1) != len(payload.list_2):
        raise HTTPException(status_code=400, detail="Lists must be of the same length")

    transformed_list = []
    for s1, s2 in zip(payload.list_1, payload.list_2):
        for s in [s1, s2]:
            # Check cache for s
            cached_s = session.exec(select(CachedResult).where(CachedResult.original_string == s)).first()
            if not cached_s:
                logger.info(f"Cache miss for string: {s}")
                transformed_s = transform_string(s)
                cached_s = CachedResult(original_string=s, transformed_string=transformed_s)
                session.add(cached_s)
                try:
                    session.commit()
                    session.refresh(cached_s)
                except Exception as e:
                    session.rollback()
                    logger.error(f"Database error: {e}")
                    raise HTTPException(status_code=500, detail="Internal server error")
            transformed_list.append(cached_s.transformed_string)

    # Generate a unique ID for the payload
    payload_id = str(uuid.uuid4())
    payload_output = ", ".join(transformed_list)

    # Check if a payload with the same output already exists.
    statement = select(Payload).where(Payload.output == payload_output)
    existing_payload = session.exec(statement).first()
    if existing_payload:
        return {"id": str(existing_payload.id)}
    
    # Store the payload in the database
    payload = Payload(id=payload_id, output=payload_output)
    session.add(payload)
    try:
        session.commit()
        session.refresh(payload)
    except Exception as e:
        session.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"id": str(payload_id)}

@app.get("/payload/{id}", response_model=PayloadResponse, status_code=status.HTTP_200_OK)
async def read_payload(id: str, session: Session = Depends(get_session)):
    payload = session.exec(select(Payload).where(Payload.id == id)).first()
    if not payload:
        raise HTTPException(status_code=404, detail="Payload not found")
    return {"output": payload.output}

