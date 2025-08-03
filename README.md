# GOST Search Application

A web application for searching through GOST technical documentation.

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Place your RTF documents in `data/GOST Р ТК 164/`

## Running the Application

1. First, process the documents (if needed):
   ```python
   from app.models.vectorizer import Vectorizer
   vectorizer = Vectorizer()
   vectorizer.process_documents("data/GOST Р ТК 164")
   vectorizer.save()
2. Start the web server:

    ```bash
    python run.py

3. Access the API at http://localhost:8000
