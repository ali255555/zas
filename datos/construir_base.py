#!/usr/bin/env python3
"""
Construye catalogo.db, la base de datos que se empaqueta en la app.

Entradas (todas de Open Food Facts, ODbL 1.0):
  espana.tsv             productos vendidos en Espana (ver filtrar_espana.py)
  additives.json         taxonomia de aditivos
  additives_classes.json nombres de las funciones de los aditivos
  allergens.full.json    alergenos con sinonimos por idioma
  ingredients.full.json  ingredientes con sinonimos y origen vegano/vegetariano

Salida: app/src/main/assets/catalogo.db

Reglas: no se inventa ni se estima ningun dato. Lo que no viene en la fuente
se queda vacio y la app dira "no disponible".
"""
import csv, json, os, re, sqlite3, sys, unicodedata
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)  # para importar aditivos_riesgo.py
RAIZ = os.path.dirname(AQUI)
ESQUEMA = None  # se resuelve con ruta_esquema()
DESTINO = os.path.join(RAIZ, "app/src/main/assets/catalogo.db")

csv.field_size_limit(10_000_000)

FUENTE_OFF = "Open Food Facts"
URL_OFF = "https://openfoodfacts.org"


def sin_tildes(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def normalizar_tags(bruto: str) -> str:
    """'en:milk,en:gluten' -> 'en:milk,en:gluten' (limpio, sin huecos)."""
    if not bruto:
        return ""
    partes = [p.strip() for p in bruto.replace(";", ",").split(",")]
    return ",".join(p for p in partes if p)


def normalizar_aditivos(bruto: str) -> str:
    """'en:e120,en:e330' -> 'e120,e330'."""
    if not bruto:
        return ""
    salida = []
    for p in bruto.split(","):
        p = p.strip().lower()
        if not p:
            continue
        p = p.split(":")[-1].replace("-", "").replace(" ", "")
        if p:
            salida.append(p)
    return ",".join(dict.fromkeys(salida))


def ruta_esquema():
    """El esquema más nuevo que haya exportado Room. Así una subida de version
    no deja los scripts apuntando a un fichero viejo."""
    carpeta = os.path.join(RAIZ, "app/schemas/com.alitalaint.etiqueta.data.catalogo.CatalogoDatabase")
    numeros = [int(f[:-5]) for f in os.listdir(carpeta) if f.endswith(".json") and f[:-5].isdigit()]
    return os.path.join(carpeta, f"{max(numeros)}.json")


# Lo que se mide además de lo de la nota (Composicion.Nutriente en la app). Se
# guarda en GRAMOS por 100 g/100 ml, tal cual lo da Open Food Facts, como
# «clave=valor;clave=valor». Sin tocar ni completar nada.
EXTRA = ["carbohydrates", "trans-fat", "cholesterol", "sodium", "potassium", "calcium",
         "magnesium", "iron", "bicarbonate", "chloride", "sulphate", "fluoride", "silica",
         "nitrate", "phosphorus", "zinc", "iodine", "caffeine", "vitamin-c", "vitamin-d",
         "vitamin-b12", "folates", "ph"]


def extra(fila):
    partes = []
    for k in EXTRA:
        try:
            v = float(fila.get(k + "_100g") or "")
        except ValueError:
            continue
        # El pH va de 0 a 14; lo demás no puede pasar de 100 g en 100 g.
        if v < 0 or (k == "ph" and v > 14) or (k != "ph" and v > 100):
            continue
        partes.append(f"{k}={round(v, 6):g}")
    return ";".join(partes) or None


def crear_esquema(con):
    d = json.load(open(ruta_esquema()))["database"]
    for e in d["entities"]:
        con.execute(e["createSql"].replace("${TABLE_NAME}", e["tableName"]))
        for i in e.get("indices", []):
            con.execute(i["createSql"].replace("${TABLE_NAME}", e["tableName"]))
    con.execute("CREATE TABLE IF NOT EXISTS room_master_table (id INTEGER PRIMARY KEY, identity_hash TEXT)")
    con.execute("INSERT OR REPLACE INTO room_master_table (id, identity_hash) VALUES (42, ?)", (d["identityHash"],))
    con.execute(f"PRAGMA user_version = {d['version']}")
    return d["identityHash"]


def cargar_productos(con):
    ruta = os.path.join(AQUI, "espana.tsv")
    total = guardados = 0
    lote = []
    with open(ruta, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f, delimiter="\t")
        for fila in lector:
            total += 1
            codigo = (fila.get("code") or "").strip()
            if not codigo or not codigo.isdigit() or len(codigo) < 6:
                continue
            nombre = (fila.get("product_name") or "").strip() or (fila.get("generic_name") or "").strip()
            ingredientes = (fila.get("ingredients_text") or "").strip()
            alergenos = normalizar_tags(fila.get("allergens") or "")
            aditivos = normalizar_aditivos(fila.get("additives_tags") or "")
            # Un producto sin nombre y sin ninguna informacion util no aporta nada.
            if not nombre and not ingredientes and not alergenos and not aditivos:
                continue
            try:
                gramos = float(fila.get("product_quantity") or "")
                if gramos <= 0 or gramos > 100000:
                    gramos = None
            except ValueError:
                gramos = None
            try:
                nova = int(float(fila.get("nova_group") or ""))
            except ValueError:
                nova = None
            def numero(clave, tope=None):
                try:
                    v = float(fila.get(clave) or "")
                except ValueError:
                    return None
                if v < 0 or (tope is not None and v > tope):
                    return None
                return round(v, 2)

            try:
                aditivos_n = int(float(fila.get("additives_n") or ""))
            except ValueError:
                aditivos_n = None

            lote.append((
                codigo,
                nombre or None,
                (fila.get("brands") or "").strip() or None,
                (fila.get("quantity") or "").strip() or None,
                gramos,
                ingredientes or None,
                alergenos or None,
                normalizar_tags(fila.get("traces_tags") or "") or None,
                aditivos or None,
                normalizar_tags(fila.get("categories_tags") or "") or None,
                normalizar_tags(fila.get("labels_tags") or "") or None,
                normalizar_tags(fila.get("ingredients_analysis_tags") or "") or None,
                (fila.get("nutriscore_grade") or "").strip().lower() or None,
                nova,
                numero("energy-kcal_100g", 2000),
                numero("fat_100g", 100),
                numero("saturated-fat_100g", 100),
                numero("sugars_100g", 100),
                numero("salt_100g", 100),
                numero("fiber_100g", 100),
                numero("proteins_100g", 100),
                aditivos_n,
                extra(fila),
            ))
            guardados += 1
            if len(lote) >= 5000:
                con.executemany(
                    "INSERT OR REPLACE INTO producto VALUES (" + ",".join("?" * 23) + ")", lote)
                lote.clear()
    if lote:
        con.executemany("INSERT OR REPLACE INTO producto VALUES (" + ",".join("?" * 23) + ")", lote)
    print(f"productos: leidos {total:,}, guardados {guardados:,}")
    return guardados


def recortar(texto, maximo=190):
    """Una o dos frases: lo justo para saber qué es y de dónde sale."""
    frases = re.split(r"(?<=[a-záéíóúñ0-9)])\.\s+(?=[A-ZÁÉÍÓÚÑ])", texto)
    salida = ""
    for f in frases:
        if salida and len(salida) + len(f) + 2 > maximo:
            break
        # El punto se lo come el separador: hay que devolverlo al juntar, o
        # salen dos frases pegadas («…food coloring It is also known…»).
        salida = (salida + ". " + f).strip() if salida else f.strip()
        if len(salida) >= maximo * 0.55:
            break
    if len(salida) > maximo:
        salida = salida[:maximo].rsplit(" ", 1)[0].rstrip(",;: ") + "…"
    return salida if salida.endswith((".", "…")) else salida + "."


# Los que la ley NO autoriza, con la ley que lo dice. El Reglamento (CE)
# 1333/2008, anexo II, es la lista de la Unión: lo que no está en ella no se
# puede usar en un alimento en la UE.
NO_AUTORIZADOS = {
    "e103": "Reglamento (CE) 1333/2008, anexo II (no figura en la lista de la Unión)",
}


def traducir(mapa, texto):
    """El inglés de un texto nuestro. Si falta, se para: mejor no publicar que
    publicar media aplicación en español."""
    if texto is None:
        return None
    if texto not in mapa:
        raise SystemExit(f"falta el ingles de: «{texto[:70]}…»")
    return mapa[texto]


def cargar_aditivos(con):
    adi = json.load(open(os.path.join(AQUI, "additives.json")))
    clases = json.load(open(os.path.join(AQUI, "additives_classes.json")))
    # De qué está hecho cada aditivo, SOLO según la ley: el Reglamento (UE)
    # 231/2012 fija las especificaciones de todos los aditivos autorizados y
    # dice de qué está hecho cada uno, en castellano y en inglés (EUR-Lex). Lo
    # que el reglamento no describe se queda sin descripción.
    # Orden de Ali (1-oct-2026): nada de Wikipedia, que la escribe cualquiera.
    ruta_ley = os.path.join(AQUI, "aditivos_definicion.json")
    ruta_ley_en = os.path.join(AQUI, "aditivos_definicion_en.json")
    descripciones = json.load(open(ruta_ley, encoding="utf-8"))
    descripciones_en = json.load(open(ruta_ley_en, encoding="utf-8"))
    from aditivos_riesgo import (RIESGO, ESCALA, TOXICIDAD_POR_DEFECTO,
                                 EFECTO_EN, TEXTO_EN, a_diario_en, POR_DEFECTO_EN,
                                 EFECTO_POR_DEFECTO, a_diario)

    def nombre_clase(tag):
        c = clases.get(tag, {}).get("name", {})
        return c.get("es") or c.get("en") or tag.split(":")[-1].replace("-", " ")

    filas = []
    for clave, v in adi.items():
        ident = clave.split(":")[-1].lower().replace("-", "")
        if not ident.startswith("e"):
            continue
        numero = (v.get("e_number", {}) or {}).get("en")
        numero_e = f"E{numero}" if numero else ident.upper()
        nombres = v.get("name", {}) or {}
        bruto = nombres.get("es") or nombres.get("en") or numero_e
        # Los nombres vienen como "E120 - Cochinilla": nos quedamos con la parte util.
        nombre = bruto.split(" - ", 1)[1].strip() if " - " in bruto else bruto.strip()
        # El nombre inglés sale de la misma taxonomia, no de una traducción.
        bruto_en = nombres.get("en") or ""
        nombre_en = bruto_en.split(" - ", 1)[1].strip() if " - " in bruto_en else bruto_en.strip()
        if re.fullmatch(r"e[\w()]* food additive", nombre_en, re.I) or not nombre_en:
            nombre_en = numero_e
        # La taxonomia no siempre trae nombre en espanol y cuela el relleno
        # ingles "E411 food additive". Antes que un nombre en otro idioma o
        # inventado, se ensena el numero E a secas.
        if re.fullmatch(r"e[\w()]* food additive", nombre, re.I) or not nombre:
            nombre = numero_e
        funciones = []
        for campo in ("mandatory_additive_class", "additives_classes"):
            valor = (v.get(campo, {}) or {}).get("en")
            if valor:
                funciones += [nombre_clase(t.strip()) for t in valor.split(",") if t.strip()]
        funciones = list(dict.fromkeys(funciones))
        efsa_url = (v.get("efsa_evaluation_url", {}) or {}).get("en")
        efsa_txt = (v.get("efsa_evaluation", {}) or {}).get("en")
        if efsa_url:
            # Solo "EFSA": el titular del dictamen viene en inglés y no pinta nada
            # en una pantalla en español. El enlace lleva al documento entero.
            fuente_nombre = "EFSA"
            fuente_url = efsa_url
        else:
            fuente_nombre = "Taxonomía de aditivos de Open Food Facts"
            fuente_url = f"https://world.openfoodfacts.org/additive/{ident}"
        desc = descripciones.get(ident) or {}
        if desc.get("texto"):
            desc = dict(desc, texto=recortar(desc["texto"]))
        riesgo = RIESGO.get(ident)
        # Si la ley no lo autoriza, eso manda sobre todo lo demás.
        prohibido = riesgo is None and ident in NO_AUTORIZADOS
        filas.append((
            ident, numero_e, nombre,
            ", ".join(funciones) or None,
            None,  # explicacion: OFF no publica descripcion en espanol; la app la compone con los datos
            (v.get("vegan", {}) or {}).get("en"),
            (v.get("vegetarian", {}) or {}).get("en"),
            fuente_nombre[:300], fuente_url,
            desc.get("texto"), desc.get("fuente"), desc.get("url"),
            riesgo[0] if riesgo else None,      # alto / medio
            riesgo[3] if riesgo else None,      # qué le pasa
            riesgo[4] if riesgo else None,      # quién lo dice
            riesgo[5] if riesgo else None,      # enlace
            ESCALA[riesgo[1]] if riesgo else (100 if prohibido else TOXICIDAD_POR_DEFECTO),
            riesgo[2] if riesgo else (
                "No se puede usar en la Unión Europea." if prohibido else EFECTO_POR_DEFECTO
            ),
            "No se puede tomar: no está autorizado en la UE." if prohibido
            else (a_diario(ident) or (None, None))[0],
            NO_AUTORIZADOS[ident] if prohibido else (a_diario(ident) or (None, None))[1],
            # --- lo mismo en ingles ---
            nombre_en,
            # recortar() de un texto vacio devuelve un punto suelto: eso en
            # pantalla es un parrafo con un punto y nada mas.
            (lambda t: recortar(t) if t else None)(
                (descripciones_en.get(ident) or {}).get("texto")),
            traducir(TEXTO_EN, riesgo[3]) if riesgo else None,
            (traducir(EFECTO_EN, riesgo[2]) if riesgo else
             ("It cannot be used in the European Union." if prohibido
              else traducir(EFECTO_EN, EFECTO_POR_DEFECTO))),
            ("You cannot take it: it is not authorised in the EU." if prohibido
             else a_diario_en(ident)),
        ))
    con.executemany(
        "INSERT OR REPLACE INTO aditivo VALUES (" + ",".join("?" * 25) + ")", filas)
    con_desc = sum(1 for f in filas if f[9])
    con_riesgo = sum(1 for f in filas if f[12])
    con_diario = sum(1 for f in filas if f[18])
    print(f"aditivos: {len(filas):,} | con descripcion: {con_desc:,} | "
          f"señalados: {con_riesgo} | a diario: {con_diario}")
    return len(filas)


# Alergenos de declaracion obligatoria en la UE (Reglamento 1169/2011, anexo II)
ALERGENOS_UE = [
    "en:gluten", "en:crustaceans", "en:eggs", "en:fish", "en:peanuts", "en:soybeans",
    "en:milk", "en:nuts", "en:celery", "en:mustard", "en:sesame-seeds",
    "en:sulphur-dioxide-and-sulphites", "en:lupin", "en:molluscs",
]


def cargar_alergenos(con, marcadores):
    al = json.load(open(os.path.join(AQUI, "allergens.full.json")))
    filas = []
    for clave, v in al.items():
        if clave == "en:none":
            continue
        nombres = v.get("name", {}) or {}
        nombre = nombres.get("es") or nombres.get("en") or clave.split(":")[-1].replace("-", " ")
        nombre_en = nombres.get("en") or clave.split(":")[-1].replace("-", " ")
        sinonimos = [s for s in (v.get("synonyms", {}) or {}).get("es", []) if s]
        sinonimos_en = [s for s in (v.get("synonyms", {}) or {}).get("en", []) if s]
        filas.append((clave, nombre, ", ".join(sinonimos) or None, nombre_en))
        # Los marcadores llevan las dos listas: una etiqueta inglesa dice
        # «milk», no «leche», y tiene que saltar igual.
        for s in set(sinonimos + sinonimos_en + [nombre, nombre_en]):
            marcadores.append((clave, sin_tildes(s), nombre, "Taxonomía de alérgenos de Open Food Facts"))
    con.executemany("INSERT OR REPLACE INTO alergeno VALUES (?,?,?,?)", filas)
    print(f"alergenos: {len(filas)}")
    return len(filas)


def descendientes(ing, raiz):
    """Todos los nodos que cuelgan de 'raiz' en la taxonomia de ingredientes."""
    vistos, pila = set(), [raiz]
    while pila:
        n = pila.pop()
        if n in vistos:
            continue
        vistos.add(n)
        pila += (ing.get(n, {}).get("children", []) or [])
    return vistos


def cargar_marcadores(con, marcadores):
    ing = json.load(open(os.path.join(AQUI, "ingredients.full.json")))
    fuente = "Taxonomía de ingredientes de Open Food Facts"

    def anadir(clave, nodo, etiqueta_por_defecto=None):
        v = ing.get(nodo)
        if not v:
            return
        nombres = v.get("name", {}) or {}
        etiqueta = nombres.get("es") or nombres.get("en") or etiqueta_por_defecto or nodo.split(":")[-1]
        terminos = set((v.get("synonyms", {}) or {}).get("es", []) or [])
        if nombres.get("es"):
            terminos.add(nombres["es"])
        for t in terminos:
            t = t.strip()
            if len(t) >= 3:
                marcadores.append((clave, sin_tildes(t), etiqueta, fuente))

    # Origen animal segun la propia taxonomia
    for nodo, v in ing.items():
        if (v.get("vegan", {}) or {}).get("en") == "no":
            anadir("dieta:vegano", nodo)
        if (v.get("vegetarian", {}) or {}).get("en") == "no":
            anadir("dieta:vegetariano", nodo)

    # Filtros de ingrediente pedidos expresamente
    for nodo in descendientes(ing, "en:pork"):
        anadir("sin:cerdo", nodo)
    for nodo in descendientes(ing, "en:alcohol"):
        anadir("sin:alcohol", nodo)
    for nodo in ("en:gelatin", "en:pork-gelatin", "en:beef-gelatin"):
        anadir("sin:gelatina-animal", nodo)

    unicos = {}
    for clave, patron, etiqueta, f in marcadores:
        if patron and len(patron) >= 3:
            unicos[(clave, patron)] = (clave, patron, etiqueta, f)
    filas = list(unicos.values())
    con.executemany(
        "INSERT INTO marcador (clave, patron, etiqueta, fuente, nivel) VALUES (?,?,?,?,'excluir')",
        filas)
    print(f"marcadores: {len(filas):,}")
    return len(filas)


def main():
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    if os.path.exists(DESTINO):
        os.remove(DESTINO)
    con = sqlite3.connect(DESTINO)
    con.execute("PRAGMA journal_mode = DELETE")
    con.execute("PRAGMA synchronous = OFF")
    identidad = crear_esquema(con)

    marcadores = []
    n_prod = cargar_productos(con)
    n_adi = cargar_aditivos(con)
    n_ale = cargar_alergenos(con, marcadores)
    n_mar = cargar_marcadores(con, marcadores)
    # El índice de texto se llena al final, cuando ya están los productos.
    from indice_de_texto import construir as construir_indice
    construir_indice(con)
    print("Índice de texto hecho.")

    meta = [
        ("version_datos", date.today().isoformat()),
        ("fuente", FUENTE_OFF),
        ("fuente_url", URL_OFF),
        ("licencia", "Open Database License (ODbL) v1.0"),
        ("licencia_url", "https://opendatacommons.org/licenses/odbl/1-0/"),
        ("atribucion", "Datos de Open Food Facts (openfoodfacts.org), bajo licencia ODbL 1.0"),
        ("ambito", "Productos vendidos en España: los que lo declaran, los de empresa española (prefijo 84) y los que traen la etiqueta en español"),
        ("productos", str(n_prod)),
        ("aditivos", str(n_adi)),
        ("alergenos", str(n_ale)),
        ("marcadores", str(n_mar)),
        ("identidad_room", identidad),
    ]
    con.executemany("INSERT OR REPLACE INTO meta VALUES (?,?)", meta)
    con.commit()
    con.execute("VACUUM")
    con.commit()
    con.close()
    print(f"\n{DESTINO}: {os.path.getsize(DESTINO)/1e6:.1f} MB")


if __name__ == "__main__":
    main()
