import os

import psycopg
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)
app.json.sort_keys = False


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@app.get("/countries/<country_code>")
def get_country(country_code):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT code, name, continent, population
                FROM country
                WHERE code = %s
                """,
                (country_code.upper(),)
            )

            country = cursor.fetchall()

    if country is None:
        return {"error": "Country not found"}, 404

    return {
        "code": country[0],
        "name": country[1],
        "continent": country[2],
        "population": country[3]
    }

@app.get("/countries")
def get_countries():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT code, name, continent, population
                FROM country
                ORDER BY name
                LIMIT 20
                """
            )

            rows = cursor.fetchall()

    countries = []

    for row in rows:
        countries.append({
            "code": row[0],
            "name": row[1],
            "continent": row[2],
            "population": row[3]
        })

    return countries