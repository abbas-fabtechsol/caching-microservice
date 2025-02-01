FastAPI Caching Microservice
============================

This is a FastAPI-based microservice that provides a simple caching mechanism for transforming and interleaving strings from two input lists. The service caches the results of the transformation function to improve performance for repeated requests.

Features
--------

*   **Create Payload**: Submit two lists of strings to generate a payload. The service caches the transformed strings for future use.
    
*   **Retrieve Payload**: Fetch a previously generated payload by its unique ID.
    
*   **Caching**: Transformed strings are cached in a database to avoid redundant computations.
    
*   **Database Integration**: Uses SQLite for persistent storage of cached results and payloads.
    
*   **Docker Support**: The application can be containerized for easy deployment.
    

Prerequisites
-------------

*   Python 3.9 or higher
    
*   Docker (optional, for containerized deployment)
    

Setup
-----

### 1\. Clone the Repository

```
git clone https://github.com/abbas-fabtechsol/caching-microservice.git
cd caching-microservice
```

### 2\. Install Dependencies

Create a virtual environment and install the required packages:

```
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  
pip install -r requirements.txt   
```
### 3\. Configure the Database

By default, the application uses SQLite. If you want to use PostgreSQL, update the DATABASE\_URL in the .env file:

```
DATABASE_URL=postgresql://user:password@localhost/dbname
```
### 4\. Run the Application

Start the FastAPI server:
```
uvicorn main:app --reload
```

The application will be available at http://127.0.0.1:8000.

API Endpoints
-------------

### 1. **Create a Payload**

*   **Endpoint**: POST /payload
    
*   **Description**: Submit two lists of strings to generate a payload. The service caches the transformed strings.
    
*   **Request Body**:
```
{
  "list_1": ["first string", "second string"],
  "list_2": ["other string", "another string"]
}
```    
*   **Response**:
```
{
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
``` 

### 2. **Retrieve a Payload**

*   **Endpoint**: GET /payload/{id}
    
*   **Description**: Fetch a previously generated payload by its unique ID.
    
*   **Response:**
```
{
  "output": "FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING"
}
``` 

Running with Docker
-------------------

### 1\. Build the Docker Image

``` 
docker-compose build 
```

### 2\. Start the Container

```
docker-compose up
```

The application will be available at http://localhost:8000.

Testing
-------

### Run Unit Tests

To run the test suite, use the following command:

```
pytest test_utils.py test_models.py test_main.py -v
```

Project Structure
-----------------
```
caching-microservice/
├── database.py
├── docker-compose.yml
├── Dockerfile
├── main.py
├── models.py
├── README.md
├── requirements.txt
├── test_main.py
└── utils.py
```

Technologies Used
-----------------

*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
    
*   **SQLModel**: A library for interacting with SQL databases using Python models.
    
*   **SQLite**: A lightweight, file-based database (default).
    
*   **Docker**: A platform for containerizing applications.
    

Contributing
------------

Contributions are welcome! If you find a bug or want to suggest an improvement, please open an issue or submit a pull request.

Contact
-------

For questions or feedback, please contact [Muhammad Abbas](mailto:mehar725@gmail.com).