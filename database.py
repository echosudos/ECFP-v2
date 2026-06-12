import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg

"""
Todo:
- add docstring to initliaze
- database interaction functions
"""

def initialize() -> None:
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:

            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id serial PRIMARY KEY,
                name text
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS meters (
                id serial PRIMARY KEY,
                name text NOT NULL,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id serial PRIMARY KEY,
                meter_reading_kwh integer NOT NULL,
                reading_date DATE NOT NULL,
                meter_id INTEGER REFERENCES meters(id) ON DELETE CASCADE NOT NULL
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id serial PRIMARY KEY,
                total_consumption_kwh integer NOT NULL,
                current_meter_reading_kwh integer NOT NULL,
                meter_reading_date DATE NOT NULL,
                previous_reading integer,
                cycle_start DATE,
                cycle_end DATE,
                meter_id INTEGER REFERENCES meters(id) ON DELETE CASCADE NOT NULL
            )
            """)

            conn.commit()