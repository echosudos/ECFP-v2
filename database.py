import os
from datetime import datetime
import psycopg

"""
Todo:
- add docstring to initliaze
- database interaction functions
"""

def connect_to_database(DATABASE_URL: str) -> psycopg.Connection:
    '''
    Connects to database and returns that connection
    '''
    conn = psycopg.connect(DATABASE_URL)

    return conn
    

def initialize(conn: psycopg.Connection) -> None:
    '''
    Initializes database tables
    '''
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            name text NOT NULL UNIQUE
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

        # Assumption
        # One bill corresponds to one meter
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

def add_user(conn: psycopg.Connection, name: str) -> None:
    with conn.cursor() as cur:

        try:
            cur.execute("""
            INSERT INTO users (name) VALUES (%s)
            """, (name,))

            print(f"Added user {name}")
            conn.commit()
        except psycopg.errors.UniqueViolation:
            # TODO: Bring err to bot directly not caller
            print(f"User '{name}' already exists")
            conn.rollback()
            return psycopg.errors.UniqueViolation

def del_user(conn: psycopg.Connection, name: str) -> None:
    with conn.cursor() as cur:

        cur.execute("""
        DELETE FROM users WHERE name = %s
        """, (name,))

        if cur.rowcount == 0:
            # TODO: Bring err to bot directly not caller
            print(f"User '{name}' not found")
            return ValueError("Error: Delete op failed, user not found")

        conn.commit()
