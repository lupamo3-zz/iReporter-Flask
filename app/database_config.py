import urllib.parse
import psycopg2
import os


db_url = os.getenv('DATABASE_URL')
testdb_url = os.getenv('TESTDATABASE_URL')


def connection(db_url):
    conn = psycopg2.connect(db_url)
    return conn


def init_db():
    con = connection(db_url)
    return con


def create_tables():
    conn = connection(db_url)
    curr = conn.cursor()
    queries = tables()

    for query in queries:
        curr.execute(query)
    conn.commit()


def destroy_tables():
    drop1 = [
        """DROP TABLE IF EXISTS users CASCADE""",

        """DROP TABLE IF EXISTS incidents CASCADE"""
    ]
    queries = [drop1]
    return queries


def tables():
    userstables = """CREATE TABLE IF NOT EXISTS Users (
        user_id serial PRIMARY KEY NOT NULL,
        firstname character varying(50) NOT NULL,
        lastname character varying(50) NOT NULL,
        othernames character varying(50),
        username character varying(50) NOT NULL UNIQUE,
        email character varying(50) UNIQUE,
        phonenumber character varying(50) UNIQUE,
        registered timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
        isAdmin boolean NOT NULL,
        password character varying(50) NOT NULL,
        confirm_password character varying(50) NOT NULL
    )"""

    incidentstables = """CREATE TABLE IF NOT EXISTS Incidents (
        incidents_id serial PRIMARY KEY NOT NULL,
        type character varying(20) NOT NULL,
        status character varying(100) NOT NULL,
        comment character varying(200) NOT NULL,
        createdBy character varying(200) NOT NULL,
        createdOn timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
        location character varying(200) NOT NULL,
        images character varying(200) NOT NULL,
        videos character varying(200) NOT NULL
    )"""

    queries = [userstables, incidentstables]
    return queries
