import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, './scripts/.env'))

DATABASE = {
    'dbname': env('DATABASE_NAME'),
    'user': env('DATABASE_USER'),
    'password': env('DATABASE_PASSWORD'),
    'host': env('DATABASE_HOST'),
    'port': env('DATABASE_PORT'),
}