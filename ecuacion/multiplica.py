from fastapi import FastAPI
from pydantic import BaseModel
import requests
import mysql.connector

app = FastAPI()

class Input(BaseModel):
    a: float
    b: float
    c: float
    d: float

def guardar_en_bd(a, b, c, d, resultado):
    try:
        conexion = mysql.connector.connect(
            host="mysql",
            user="root",
            password="qwer1234",
            database="microservicios_db"
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
    suma_resp = requests.post("http://suma:8000/sumar", json={"a": valores.a, "b": valores.b})
    resta_resp = requests.post("http://resta:8000/restar", json={"c": valores.c, "d": valores.d})
    suma = suma_resp.json()["resultado"]
    resta = resta_resp.json()["resultado"]
    resultado = suma * resta

    # Guardar en base de datos
    guardar_en_bd(valores.a, valores.b, valores.c, valores.d, resultado)

    return {"resultado": resultado}
