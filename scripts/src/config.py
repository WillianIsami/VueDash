import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DATABASE = {
    'dbname': env('DB_NAME'),
    'user': env('DB_USER'),
    'password': env('DB_PASSWORD'),
    'host': env('DB_HOST'),
    'port': env('DB_PORT'),
}