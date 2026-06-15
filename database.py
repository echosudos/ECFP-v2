import os
from datetime import date
import psycopg

"""
Todo:
- database interaction functions (add docstrings too once discord bot related code is added in)
- give power to admin
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
    - users (id, unique name)
    - meters (id, name, user_id)
    - readings (id, meter_reading, reading_date, meter_id)
    - bills 
        > id 
        > total_consumption
        > current_meter_reading 
        > prev_meter_reading
        > cycle_start
        > cycle_end
        > meter_id
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
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL
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

def del_user(conn: psycopg.Connection, name: str, user_id: int) -> None:
   
    with conn.cursor() as cur:

        cur.execute("""
        DELETE FROM users WHERE (name, id) = (%s, %s)
        """, (name, user_id))

        if cur.rowcount == 0:
            # TODO: Bring err to bot directly not caller
            print(f"User '{name}' not found")
            return ValueError("Error: Delete op failed, user not found")

        conn.commit()

def add_meter(conn: psycopg.Connection, name: str, user_id: int) -> None:
    
    with conn.cursor() as cur:

        try:
            # Add meter
            cur.execute("""
                INSERT INTO meters (name, user_id) VALUES (%s, %s)
            """, (name, user_id))

            print(f"Added meter {name} owned by {user_id}")
            conn.commit()
        
        except psycopg.errors.ForeignKeyViolation:
            # TODO: Bring err to bot directly not caller
            print(f"{user_id} does not exist")
            conn.rollback()
            return psycopg.errors.ForeignKeyViolation

    

def del_meter(conn: psycopg.Connection, meter_id: int, user_id: int) -> None:
    
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM meters WHERE id = %s
            AND user_id = %s
        """, (meter_id, user_id))
        
        if cur.rowcount == 0:
            # TODO: Bring err to bot directly not caller
            print(f"Meter '{meter_id}' not found")
            return ValueError("Error: Delete op failed, meter not found in user")
        
        conn.commit()

def add_reading(
    conn: psycopg.Connection, 
    meter_reading: int,
    reading_date: date,
    meter_id: int, 
) -> None:

    with conn.cursor() as cur:
        try:
            # Try to add reading entry
            cur.execute("""
                INSERT INTO readings (meter_reading, reading_date, meter_id) VALUES (%s, %s, %s)
            """, (meter_reading, reading_date, meter_id))
            
            conn.commit()
        except psycopg.errors.ForeignKeyViolation:
            # TODO: Bring err to bot directly not caller
            print(f"{meter_id} does not exist")
            conn.rollback()
            return psycopg.errors.ForeignKeyViolation

def del_reading(
    conn: psycopg.Connection, 
    reading_id: int, 
    user_id: int
) -> None:
    
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM readings WHERE id = %s 
            AND meter_id IN (
                SELECT id FROM meters WHERE user_id = %s
            ) 
        """, (reading_id, user_id))

        if cur.rowcount == 0:
            print(f"Reading '{reading_id}' or User '{user_id}' not found")
            return ValueError("Error: Delete op failed, reading/user id invalid")

        conn.commit()


def add_bill():
    pass

def del_bill():
    pass