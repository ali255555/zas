# -*- coding: utf-8 -*-
"""
Añade a catalogo.db los ingredientes, las recetas, el catálogo de restricciones
y las advertencias obligatorias.

Reglas que se respetan aquí:
  - La composición de cada ingrediente sale de USDA FoodData Central (dominio
    público). No se ajusta ni se redondea a ojo.
  - El origen (vegano, vegetariano) y los alérgenos salen de la taxonomía de
    Open Food Facts, subiendo por los padres igual que hace Open Food Facts.
  - Las declaraciones ("alto contenido en proteínas"...) salen de aplicar los
    umbrales literales del Reglamento (CE) 1924/2006. No son opinión.
  - Si falta un dato, queda vacío y la aplicación dirá que no lo tiene.
"""
import csv, json, os, re, sqlite3, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from ingredientes import INGREDIENTES, EN as INGREDIENTES_EN
from recetas import RECETAS, NOMBRES_EN, PASOS_EN, linea_en
from restricciones import (RESTRICCIONES, ADVERTENCIAS, ADVERTENCIAS_EN, RAICES, PALABRAS, en_de,
                           MARCADORES_CASTELLANO, FUENTE_CASTELLANO,
                           MARCADORES_DE_DUDA, FUENTE_DUDA)

RAIZ = os.path.dirname(AQUI)
DESTINO = os.path.join(RAIZ, "app/src/main/assets/catalogo.db")
USDA = os.path.join(AQUI, "usda/FoodData_Central_sr_legacy_food_csv_2018-04/")

csv.field_size_limit(10_000_000)

FUENTE_USDA = "USDA FoodData Central (SR Legacy), dominio público"
FUENTE_OFF = "Taxonomía de ingredientes de Open Food Facts"
FUENTE_1924 = "Reglamento (CE) 1924/2006, anexo"

NUTRIENTES = {
    "1008": "kcal", "1003": "proteina", "1004": "grasa", "1258": "saturadas",
    "1005": "hidratos", "2000": "azucares", "1079": "fibra", "1093": "sodio",
}



def comprobar_columnas(con, tabla, columnas):
    """
    Que la tabla tenga EXACTAMENTE esas columnas, ni una más ni una menos.

    No compara el orden —para eso se escriben los nombres en el INSERT—, pero
    sí avisa a gritos si el esquema ha ganado o perdido una: si se añade una
    columna y nadie la rellena, la aplicación enseñaría un hueco sin que nada
    fallara.
    """
    reales = {f[1] for f in con.execute(f"PRAGMA table_info({tabla})")}
    faltan = reales - set(columnas)
    sobran = set(columnas) - reales
    if faltan or sobran:
        raise SystemExit(
            f"La tabla «{tabla}» no encaja con lo que escribe este script.\n"
            f"  sin rellenar: {sorted(faltan) or 'ninguna'}\n"
            f"  no existen:   {sorted(sobran) or 'ninguna'}"
        )


def sin_tildes(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


# ---------- Open Food Facts: herencia por la taxonomía ----------

OFF = json.load(open(os.path.join(AQUI, "ingredients.full.json"), encoding="utf-8"))


def heredar(nodo, campo, vistos=None, prof=0):
    if vistos is None:
        vistos = set()
    if nodo in vistos or prof > 12:
        return None
    vistos.add(nodo)
    v = OFF.get(nodo)
    if not v:
        return None
    propio = (v.get(campo, {}) or {}).get("en")
    if propio:
        return propio
    for p in (v.get("parents") or []):
        r = heredar(p, campo, vistos, prof + 1)
        if r:
            return r
    return None


def antepasados(nodo, vistos=None, prof=0):
    if vistos is None:
        vistos = set()
    if nodo in vistos or prof > 15:
        return vistos
    vistos.add(nodo)
    for p in (OFF.get(nodo, {}).get("parents") or []):
        antepasados(p, vistos, prof + 1)
    return vistos


# ---------- USDA ----------

def cargar_usda(descripciones):
    por_descripcion = {}
    for r in csv.DictReader(open(USDA + "food.csv", encoding="utf-8", errors="replace")):
        if r["description"] in descripciones:
            por_descripcion[r["description"]] = r["fdc_id"]
    quiero = set(por_descripcion.values())
    valores = {fid: {} for fid in quiero}
    for r in csv.DictReader(open(USDA + "food_nutrient.csv", encoding="utf-8", errors="replace")):
        if r["fdc_id"] in quiero and r["nutrient_id"] in NUTRIENTES:
            try:
                valores[r["fdc_id"]][NUTRIENTES[r["nutrient_id"]]] = float(r["amount"])
            except ValueError:
                pass
    return por_descripcion, valores


# ---------- Declaraciones del Reglamento (CE) 1924/2006 ----------

def declaraciones(kcal100, prot100, grasa100, sat100, azu100, fibra100, sal100):
    """Umbrales literales del anexo del Reglamento. Sólidos."""
    d = []
    if kcal100 is None:
        return d
    if kcal100 <= 40:
        d.append("bajo-energia")
    if grasa100 is not None and grasa100 <= 3:
        d.append("bajo-grasa")
    if sat100 is not None and sat100 <= 1.5:
        d.append("bajo-saturadas")
    if azu100 is not None and azu100 <= 5:
        d.append("bajo-azucares")
    if sal100 is not None and sal100 <= 0.3:
        d.append("bajo-sal")
    if fibra100 is not None:
        por_kcal = (fibra100 / kcal100 * 100) if kcal100 > 0 else 0
        if fibra100 >= 6 or por_kcal >= 3:
            d.append("alto-fibra")
        elif fibra100 >= 3 or por_kcal >= 1.5:
            d.append("fuente-fibra")
    if prot100 is not None and kcal100 > 0:
        parte = prot100 * 4 / kcal100
        if parte >= 0.20:
            d.append("alto-proteinas")
        elif parte >= 0.12:
            d.append("fuente-proteinas")
    return d


def recetas_de_fuera(con):
    """
    Las recetas del recetario libre de Wikibooks (CC BY-SA 3.0).

    No traen cantidades en gramos de todos los ingredientes, así que no se les
    calcula composición: eso sería inventarla. Lo que sí se puede hacer, y se
    hace, es mirar su lista de ingredientes con los mismos marcadores que se
    usan con los productos, para saber si chocan con lo que el usuario evita
    (cerdo, gluten, leche, algo de origen animal...).
    """
    ruta = os.path.join(AQUI, "recetas_wikibooks.json")
    if not os.path.exists(ruta):
        print("  (sin recetas_wikibooks.json: ejecuta descargar_recetas_wikibooks.py)")
        return []

    marcadores = [(clave, patron) for clave, patron in
                  con.execute("SELECT clave, patron FROM marcador")]
    filas = []
    for r in json.load(open(ruta, encoding="utf-8")):
        texto = sin_tildes(" , ".join(r["ingredientes"]).lower())
        choques = sorted({c for c, patron in marcadores if palabra_en(texto, patron)})
        filas.append((
            r["id"], r["nombre"], None, r["raciones"], r["minutos"],
            "|".join(r["pasos"]),
            None, None, None, None, None, None, None, None, None, None,  # sin números
            None,          # declaraciones
            None,          # puntos_sano
            ",".join(choques) or None,
            None,          # cobertura
            r["fuente"], r["url"], r["licencia"],
            "|".join(r["ingredientes"]),
            # Las del recetario libre están escritas en español y así se
            # quedan: traducirlas a máquina sería inventar cantidades y pasos.
            None, None, None, None,
        ))
    return filas


def palabra_en(texto, patron):
    """El patrón como palabra entera: «sal» no puede saltar dentro de «salmón»."""
    if len(patron) < 3:
        return False
    return re.search(r"(?<![a-z0-9])" + re.escape(patron) + r"(?![a-z0-9])", texto) is not None


def comprobar_que_cuadran(con):
    """
    Dos números que sabemos de memoria, mirados después de escribirlos.

    Si una columna se corre, el aceite de oliva deja de tener 884 kcal y la
    prueba lo dice AQUÍ, antes de empaquetar nada, no en el supermercado.
    """
    esperado = {"aceite-oliva": (884.0, 0.0), "lentejas": (116.0, 9.02)}
    for ident, (kcal, proteina) in esperado.items():
        fila = con.execute(
            "SELECT kcal, proteina FROM ingrediente WHERE id = ?", (ident,)
        ).fetchone()
        if fila is None:
            raise SystemExit(f"falta el ingrediente «{ident}»")
        if abs((fila[0] or 0) - kcal) > 1 or abs((fila[1] or 0) - proteina) > 0.5:
            raise SystemExit(
                f"«{ident}» tendría que tener {kcal} kcal y {proteina} g de "
                f"proteína, y tiene {fila[0]} y {fila[1]}. Alguna columna se ha corrido."
            )
    print("los números de los ingredientes cuadran.")


def main():
    con = sqlite3.connect(DESTINO)
    con.execute("PRAGMA foreign_keys = OFF")

    # --- Ingredientes ---
    descripciones = {u for _, _, u, _ in INGREDIENTES}
    por_descripcion, valores = cargar_usda(descripciones)
    faltan = [u for u in descripciones if u not in por_descripcion]
    if faltan:
        raise SystemExit("Sin coincidencia en USDA: " + str(faltan))

    filas_ing, claves_ing = [], {}
    for ident, nombre, usda, nodo in INGREDIENTES:
        fid = por_descripcion[usda]
        v = valores.get(fid, {})
        sodio = v.get("sodio")
        sal = round(sodio * 2.5 / 1000, 4) if sodio is not None else None
        vegano = heredar(nodo, "vegan")
        vegetariano = heredar(nodo, "vegetarian")

        claves = set()
        alergenos = heredar(nodo, "allergens")
        if alergenos:
            for a in alergenos.split(","):
                a = a.strip()
                if a:
                    claves.add(a)
        if vegano == "no":
            claves.add("dieta:vegano")
        if vegetariano == "no":
            claves.add("dieta:vegetariano")
        arriba = antepasados(nodo)
        for clave, raices in RAICES.items():
            if any(r in arriba for r in raices):
                claves.add(clave)
        for clave, raices in {"sin:cerdo": ["en:pork"], "sin:alcohol": ["en:alcohol"]}.items():
            if any(r in arriba for r in raices):
                claves.add(clave)
        claves_ing[ident] = claves

        filas_ing.append((
            ident, nombre, fid, usda,
            v.get("kcal"), v.get("proteina"), v.get("grasa"), v.get("saturadas"),
            v.get("hidratos"), v.get("azucares"), v.get("fibra"), sal,
            vegano, vegetariano, ",".join(sorted(claves)) or None,
            FUENTE_USDA, FUENTE_OFF,
            INGREDIENTES_EN.get(ident),
        ))
    # LAS COLUMNAS, POR SU NOMBRE. Antes iban por posición y el día que el
    # esquema ganó una columna («nombre_en», que entró la segunda) todos los
    # números se corrieron un sitio: el aceite de oliva pasó a tener 0 kcal y
    # 100 g de proteína. Con los nombres escritos, eso no puede repetirse.
    COLUMNAS_ING = (
        "id", "nombre", "usda_id", "usda_nombre",
        "kcal", "proteina", "grasa", "saturadas",
        "hidratos", "azucares", "fibra", "sal",
        "vegano", "vegetariano", "claves",
        "fuente_nutricion", "fuente_origen",
        "nombre_en",
    )
    comprobar_columnas(con, "ingrediente", COLUMNAS_ING)
    con.executemany(
        f"INSERT OR REPLACE INTO ingrediente ({','.join(COLUMNAS_ING)}) "
        f"VALUES ({','.join('?' * len(COLUMNAS_ING))})",
        filas_ing,
    )
    print(f"ingredientes: {len(filas_ing)}")

    porcien = {f[0]: dict(kcal=f[4], proteina=f[5], grasa=f[6], saturadas=f[7],
                          hidratos=f[8], azucares=f[9], fibra=f[10], sal=f[11]) for f in filas_ing}

    # --- Marcadores nuevos para los filtros de ingrediente ---
    fuente_marcador = FUENTE_OFF
    nuevos = []
    for clave, raices in RAICES.items():
        for nodo, v in OFF.items():
            if not any(rr in antepasados(nodo) for rr in raices):
                continue
            nombres = v.get("name", {}) or {}
            etiqueta = nombres.get("es") or nombres.get("en") or nodo.split(":")[-1]
            terminos = set((v.get("synonyms", {}) or {}).get("es", []) or [])
            if nombres.get("es"):
                terminos.add(nombres["es"])
            for t in terminos:
                t = t.strip()
                if len(t) >= 3:
                    nuevos.append((clave, sin_tildes(t), etiqueta, fuente_marcador, "excluir"))
    # Los nombres de cocina en castellano que la taxonomía no trae.
    for clave, patrones in MARCADORES_CASTELLANO.items():
        for t in patrones:
            nuevos.append((clave, sin_tildes(t.lower()), t, FUENTE_CASTELLANO, "excluir"))

    # Los que solo permiten dudar: avisan en ámbar, no sentencian.
    for clave, patrones in MARCADORES_DE_DUDA.items():
        for t in patrones:
            nuevos.append((clave, sin_tildes(t.lower()), t, FUENTE_DUDA, "revisar"))

    # Si un patrón está como "excluir" y como "revisar", manda el que sentencia.
    unicos = {}
    for a, b, c, d, nivel in nuevos:
        if (a, b) in unicos and unicos[(a, b)][4] == "excluir":
            continue
        unicos[(a, b)] = (a, b, c, d, nivel)
    existentes = {(c, p) for c, p in con.execute("SELECT clave, patron FROM marcador")}
    nuevos = [n for n in unicos.values() if (n[0], n[1]) not in existentes]
    con.executemany(
        "INSERT INTO marcador (clave, patron, etiqueta, fuente, nivel) VALUES (?,?,?,?,?)", nuevos)
    print(f"marcadores nuevos: {len(nuevos)}")

    # --- Recetas ---
    filas_rec, filas_ri = [], []
    for r in RECETAS:
        total = {k: 0.0 for k in ("kcal", "proteina", "grasa", "saturadas", "hidratos", "azucares", "fibra", "sal")}
        gramos_totales = 0.0
        gramos_con_dato = 0.0
        for ing, gramos, texto in r["ingredientes"]:
            filas_ri.append((None, r["id"], ing, float(gramos), texto))
            gramos_totales += gramos
            p = porcien[ing]
            if p["kcal"] is None:
                continue
            gramos_con_dato += gramos
            for k in total:
                if p[k] is not None:
                    total[k] += p[k] * gramos / 100.0

        raciones = r["raciones"]
        racion = {k: round(v / raciones, 2) for k, v in total.items()}
        gramos_racion = round(gramos_totales / raciones, 1)
        factor = 100.0 / gramos_totales if gramos_totales else 0
        cien = {k: v * factor for k, v in total.items()}
        decl = declaraciones(cien["kcal"], cien["proteina"], cien["grasa"], cien["saturadas"],
                             cien["azucares"], cien["fibra"], cien["sal"])
        puntos = sum(1 for d in ("bajo-saturadas", "bajo-azucares", "bajo-sal") if d in decl)
        if "alto-fibra" in decl or "fuente-fibra" in decl:
            puntos += 1

        choques = set()
        for ing, _, _ in r["ingredientes"]:
            choques |= claves_ing[ing]

        filas_rec.append((
            r["id"], r["nombre"], r["descripcion"], raciones, r["minutos"],
            "|".join(r["pasos"]), gramos_racion,
            racion["kcal"], racion["proteina"], racion["grasa"], racion["saturadas"],
            racion["hidratos"], racion["azucares"], racion["fibra"], racion["sal"],
            round(cien["kcal"], 2), ",".join(decl) or None, puntos,
            ",".join(sorted(choques)) or None,
            round(gramos_con_dato / gramos_totales, 3) if gramos_totales else 0.0,
        ))
    # Las nuestras llevan números calculados; las de fuera, no. Se marcan con
    # nulos en vez de con ceros, que sería mentir.
    # Las cuatro columnas nulas son la fuente y la licencia (solo las de fuera
    # las llevan). Detrás van el nombre, la descripción y los pasos en inglés.
    conIngles = []
    for f in filas_rec:
        nombre_en, desc_en = NOMBRES_EN.get(f[0], (None, None))
        pasos_en = PASOS_EN.get(f[0])
        if nombre_en is None or pasos_en is None:
            raise SystemExit(f"la receta «{f[0]}» no tiene su versión inglesa")
        conIngles.append(
            f + (None, None, None, None, nombre_en, desc_en, "|".join(pasos_en), None))
    filas_rec = conIngles
    propias = len(filas_rec)
    filas_rec += recetas_de_fuera(con)

    # Se vacían antes: si no, cada reconstrucción duplicaba los ingredientes y
    # las cuentas salían al doble o al triple.
    con.execute("DELETE FROM receta_ingrediente")
    con.execute("DELETE FROM receta")
    con.executemany(
        "INSERT OR REPLACE INTO receta VALUES (" + ",".join("?" * 28) + ")", filas_rec)
    con.executemany(
        "INSERT INTO receta_ingrediente (receta_id, ingrediente_id, gramos, texto, texto_en) "
        "VALUES (?,?,?,?,?)",
        [(f[1], f[2], f[3], f[4], linea_en(f[2], f[3], f[4])) for f in filas_ri])
    print(f"recetas: {len(filas_rec)} ({propias} propias con análisis, "
          f"{len(filas_rec) - propias} del recetario libre) | "
          f"líneas de ingrediente: {len(filas_ri)}")

    # --- Restricciones ---
    filas_res = []
    for i, (ident, grupo, nombre, desc, tipo, claves, fuente, aviso) in enumerate(RESTRICCIONES):
        nom_en, desc_en, aviso_en, palabra_en, grupo_en = en_de(ident, grupo, aviso)
        if nom_en is None:
            raise SystemExit(f"la restricción «{ident}» no tiene inglés en restricciones.EN")
        filas_res.append((
            ident, grupo, nombre, desc or None, tipo, ",".join(claves), fuente, aviso,
            PALABRAS.get(ident, nombre), i,
            nom_en, desc_en, aviso_en, palabra_en, grupo_en,
        ))
    con.executemany(
        "INSERT OR REPLACE INTO restriccion VALUES (" + ",".join("?" * 15) + ")", filas_res)
    print(f"restricciones: {len(filas_res)}")

    # --- Advertencias obligatorias ---
    filas_adv = []
    for aditivos, texto, fuente, url in ADVERTENCIAS:
        texto_en = ADVERTENCIAS_EN.get(texto)
        if texto_en is None:
            raise SystemExit(f"la advertencia «{texto[:40]}…» no tiene inglés")
        for a in aditivos:
            filas_adv.append((a, texto, fuente, url, texto_en))
    con.execute("DELETE FROM advertencia")
    con.executemany(
        "INSERT INTO advertencia (aditivo_id, texto, fuente, fuente_url, texto_en) "
        "VALUES (?,?,?,?,?)", filas_adv)
    print(f"advertencias: {len(filas_adv)}")


    # --- Identidad de Room y metadatos ---
    carpeta = os.path.join(RAIZ, "app/schemas/com.alitalaint.etiqueta.data.catalogo.CatalogoDatabase")
    ultima = max(int(f[:-5]) for f in os.listdir(carpeta) if f.endswith(".json") and f[:-5].isdigit())
    esquema = json.load(open(os.path.join(carpeta, f"{ultima}.json")))["database"]
    con.execute("INSERT OR REPLACE INTO room_master_table (id, identity_hash) VALUES (42, ?)", (esquema["identityHash"],))
    con.executemany("INSERT OR REPLACE INTO meta VALUES (?,?)", [
        ("recetas", str(len(filas_rec))),
        ("ingredientes", str(len(filas_ing))),
        ("restricciones", str(len(filas_res))),
        ("fuente_nutricion", FUENTE_USDA),
        ("fuente_nutricion_url", "https://fdc.nal.usda.gov"),
        ("fuente_declaraciones", FUENTE_1924),
        ("fuente_declaraciones_url", "https://eur-lex.europa.eu/eli/reg/2006/1924/oj"),
        ("identidad_room", esquema["identityHash"]),
    ])
    con.commit()
    comprobar_que_cuadran(con)
    con.execute("VACUUM")
    con.commit()
    con.close()
    print(f"\n{DESTINO}: {os.path.getsize(DESTINO)/1e6:.1f} MB")


if __name__ == "__main__":
    main()


