#!/usr/bin/env python3
"""
Añade a la base empaquetada el índice de texto de nombres y marcas.

Sin índice, buscar «gouda» obliga a SQLite a leerse los 336.667 productos:
casi un segundo de espera. Con él, la respuesta es inmediata (1 ms medido en
el emulador). El índice no copia los textos, solo los apunta, y ocupa unos
10 MB.

Se puede ejecutar suelto sobre la base que ya existe:

    python3 datos/indice_de_texto.py

o llamarse desde construir_base.py cuando se reconstruye todo.
"""
import json
import os
import sqlite3
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
BASE = os.path.join(RAIZ, "app/src/main/assets/catalogo.db")
ESQUEMAS = os.path.join(
    RAIZ, "app/schemas/com.alitalaint.etiqueta.data.catalogo.CatalogoDatabase"
)


def esquema():
    """El esquema más nuevo que haya exportado Room."""
    numeros = [int(f[:-5]) for f in os.listdir(ESQUEMAS) if f[:-5].isdigit()]
    with open(os.path.join(ESQUEMAS, f"{max(numeros)}.json")) as f:
        return json.load(f)["database"]


def tabla_del_indice(d):
    for e in d["entities"]:
        if e["tableName"] == "producto_texto":
            return e
    raise SystemExit("El esquema de Room no trae la tabla producto_texto.")


def construir(con, d=None):
    """Crea el índice tal y como lo espera Room y lo llena. Idempotente."""
    d = d or esquema()
    entidad = tabla_del_indice(d)
    con.execute("DROP TABLE IF EXISTS producto_texto")
    con.execute(entidad["createSql"].replace("${TABLE_NAME}", entidad["tableName"]))
    # Los disparadores los crea Room en su base; aquí se crean igual para que
    # la tabla empaquetada sea exactamente la que la aplicación espera.
    for disparador in entidad.get("contentSyncTriggers", []):
        con.execute(disparador)
    con.execute("INSERT INTO producto_texto(producto_texto) VALUES('rebuild')")


def sellar(con, d=None):
    """Deja en la base la versión y la huella del esquema de Room."""
    d = d or esquema()
    con.execute(
        "CREATE TABLE IF NOT EXISTS room_master_table (id INTEGER PRIMARY KEY, identity_hash TEXT)"
    )
    con.execute(
        "INSERT OR REPLACE INTO room_master_table (id, identity_hash) VALUES (42, ?)",
        (d["identityHash"],),
    )
    con.execute(f"PRAGMA user_version = {d['version']}")


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else BASE
    d = esquema()
    con = sqlite3.connect(ruta)
    construir(con, d)
    sellar(con, d)
    con.commit()
    cuantos = con.execute("SELECT COUNT(*) FROM producto").fetchone()[0]
    prueba = con.execute(
        "SELECT COUNT(*) FROM producto_texto WHERE producto_texto MATCH 'gouda*'"
    ).fetchone()[0]
    con.close()
    print(f"Índice hecho sobre {cuantos} productos. «gouda*» encuentra {prueba}.")
    print(f"Versión {d['version']}, huella {d['identityHash']}.")
    print("Tamaño: %.1f MB" % (os.path.getsize(ruta) / 1e6))
