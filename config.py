import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    AZURE_DATABASE_CONNECTION = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=tcp:tracker666.database.windows.net,1433;"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    SECRET_KEY = "supersecretkey"
