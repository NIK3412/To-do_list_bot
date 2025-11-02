
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
dbname = os.getenv("dbname")
host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")

