import os

import psycopg
from dotenv import load_dotenv
from flask import Flask
from flask import Flask, request

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

@app.post("/cities")
def create_city():
    data = request.get_json(silent=True) or {}

    city_id = data.get("id")
    name = data.get("name", "").strip()
    country_code = data.get("country_code", "").strip().upper()
    district = data.get("district", "").strip()
    population = data.get("population")

    if (
        city_id is None
        or not name
        or not country_code
        or not district
        or population is None
    ):
        return {
            "error": (
                "ID, name, country_code, district, "
                "and population are required"
            )
        }, 400

    if population < 0:
        return {
            "error": "Population cannot be negative"
        }, 400

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO city (
                        id,
                        name,
                        country_code,
                        district,
                        population
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING
                        id,
                        name,
                        country_code,
                        district,
                        population
                    """,
                    (
                        city_id,
                        name,
                        country_code,
                        district,
                        population
                    )
                )

                new_city = cursor.fetchone()

    except psycopg.errors.UniqueViolation:
        return {
            "error": "A city with this ID already exists"
        }, 409

    except psycopg.errors.ForeignKeyViolation:
        return {
            "error": "The country code does not exist"
        }, 400

    return {
        "id": new_city[0],
        "name": new_city[1],
        "country_code": new_city[2],
        "district": new_city[3],
        "population": new_city[4]
    }, 201

@app.put("/cities/<int:city_id>")
def update_city(city_id):
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    country_code = data.get("country_code", "").strip().upper()
    district = data.get("district", "").strip()
    population = data.get("population")

    if (
        not name
        or not country_code
        or not district
        or population is None
    ):
        return {
            "error": (
                "Name, country_code, district, "
                "and population are required"
            )
        }, 400

    if population < 0:
        return {
            "error": "Population cannot be negative"
        }, 400

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE city
                    SET
                        name = %s,
                        country_code = %s,
                        district = %s,
                        population = %s
                    WHERE id = %s
                    RETURNING
                        id,
                        name,
                        country_code,
                        district,
                        population
                    """,
                    (
                        name,
                        country_code,
                        district,
                        population,
                        city_id
                    )
                )

                updated_city = cursor.fetchone()

    except psycopg.errors.ForeignKeyViolation:
        return {
            "error": "The country code does not exist"
        }, 400

    if updated_city is None:
        return {
            "error": "City not found"
        }, 404

    return {
        "id": updated_city[0],
        "name": updated_city[1],
        "country_code": updated_city[2],
        "district": updated_city[3],
        "population": updated_city[4]
    }