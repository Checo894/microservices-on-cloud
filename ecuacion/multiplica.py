from fastapi import FastAPI
from pydantic import BaseModel
import requests
import mysql.connector
import os

app = FastAPI()

class Input(BaseModel):
    a: float
    b: float
    c: float
    d: float

def guardar_en_bd(a, b, c, d, resultado):
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "mysql"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "qwer1234"),
            database=os.getenv("DB_NAME", "microservicios_db"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        cursor = conexion.cursor()
        sql = """
        INSERT INTO resultados_operaciones (a, b, c, d, resultado)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (a, b, c, d, resultado)
        cursor.execute(sql, valores)
        print(f"✅ Datos insertados: a={a}, b={b}, c={c}, d={d}, resultado={resultado}")
        conexion.commit()
        cursor.close()
        conexion.close()
    except mysql.connector.Error as err:
        print(f"Error al insertar en MySQL: {err}")

@app.post("/resolver")
def resolver(valores: Input):
    try:
        suma_resp = requests.post(
            os.getenv("SUMA_URL", "http://suma:8000/sumar"),
            json={"a": valores.a, "b": valores.b}
        )
        resta_resp = requests.post(
            os.getenv("RESTA_URL", "http://resta:8000/restar"),
            json={"c": valores.c, "d": valores.d}
        )
        suma = suma_resp.json()["resultado"]
        resta = resta_resp.json()["resultado"]
        resultado = suma * resta

        guardar_en_bd(valores.a, valores.b, valores.c, valores.d, resultado)

        return {"resultado": resultado}
    except Exception as e:
        return {"error": str(e)}

