# Bouq-It 🌹
This project was developed by students in the Ateneo de Manila University for their CSCI 42 (Introduction to Software Engineering) class.

Bouq-It (pronounced Book-It) is a flower delivery service. 
It is a play on words of “bouquet” and the act of booking a delivery order. 
The primary purpose of Bouq-It is to provide a convenient and user-friendly platform for purchasing and customizing flower arrangements. 
It aims to support floral shops by offering them an online marketplace while giving customers flexibility in selecting or designing bouquets.


# Installation Guide
1. Make a python virtual environment
    ```
    python -m venv .venv
    ```
2. Activate venv
    ```
    # Windows command prompt
    .venv\Scripts\activate.bat

    # Windows PowerShell
    .venv\Scripts\Activate.ps1

    # macOS and Linux
    source .venv/bin/activate
    ```
3. Install requirements
    ```
    pip install -r requirements.txt
    ```
4. Run PostgreSQL
    ```
    psql -U postgres
    ```
5. Setup database (In Postgres)
    ```
    \i 'db.sql'
    \i 'data.sql'
    ```
6. Setup `secrets.toml` file
    - Locate `secrets.toml.example` 
    - Change the user and password to your user and password in postgres.
    - Rename the file to `secrets.toml`
7. Run the app locally
    ```
    streamlit run app.py
    ```
