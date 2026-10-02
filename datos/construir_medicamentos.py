"""
METE LOS MEDICAMENTOS DE LA AEMPS EN LA BASE DE LA APLICACIÓN.

Lee lo que dejó descargar_medicamentos.py en datos/cima/ y escribe dos tablas
en app/src/main/assets/catalogo.db:

  medicamento      un medicamento comercializado: nombre, laboratorio, si va
                   con receta, forma, vías, principios activos, la sección 6.1
                   de su ficha técnica (excipientes, uno por línea, literal) y
                   lo que la sección 2 dice de los excipientes con efecto
                   conocido y del origen de lo que lleva.
  medicamento_cn   cada caja (código nacional) → su medicamento.

QUIRÚRGICO: no reconstruye la base ni toca ninguna otra tabla. Comprueba que
el esquema que exporta Room solo cambia en estas dos tablas respecto al
anterior; si cambiara cualquier otra cosa, se para sin escribir nada.

Fuente de la información: Agencia Española de Medicamentos y Productos
Sanitarios www.aemps.gob.es (CIMA). Fecha de obtención: la de cada ficha.
"""
import html
import json
import os
import re
import sqlite3
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CIMA = os.path.join(AQUI, "cima")
BASE = os.path.join(RAIZ, "app/src/main/assets/catalogo.db")
ESQUEMAS = os.path.join(RAIZ, "app/schemas/com.alitalaint.etiqueta.data.catalogo.CatalogoDatabase")
NUEVAS = {"medicamento", "medicamento_cn"}


def esquema(n):
    return json.load(open(os.path.join(ESQUEMAS, f"{n}.json")))["database"]


def preparar_tablas(con):
    """Crea las dos tablas nuevas y deja la base en la versión nueva de Room."""
    numeros = sorted(int(f[:-5]) for f in os.listdir(ESQUEMAS) if f[:-5].isdigit())
    nueva, vieja = esquema(numeros[-1]), esquema(numeros[-2])
    actual = con.execute("PRAGMA user_version").fetchone()[0]
    if actual not in (vieja["version"], nueva["version"]):
        sys.exit(f"La base está en la versión {actual}; se esperaba {vieja['version']} o {nueva['version']}.")
    viejas = {e["tableName"]: e["createSql"] for e in vieja["entities"]}
    for e in nueva["entities"]:
        t = e["tableName"]
        if t in NUEVAS:
            continue
        if viejas.get(t) != e["createSql"]:
            sys.exit(f"La tabla {t} cambia entre esquemas: esto no es solo añadir medicamentos. Nada escrito.")
    for e in nueva["entities"]:
        if e["tableName"] not in NUEVAS:
            continue
        con.execute(f"DROP TABLE IF EXISTS `{e['tableName']}`")
        con.execute(e["createSql"].replace("${TABLE_NAME}", e["tableName"]))
        for i in e.get("indices", []):
            con.execute(i["createSql"].replace("${TABLE_NAME}", e["tableName"]))
    con.execute("UPDATE room_master_table SET identity_hash = ? WHERE id = 42", (nueva["identityHash"],))
    con.execute(f"PRAGMA user_version = {nueva['version']}")


# ── Del HTML de la ficha a líneas ─────────────────────────────────────────

FIN_DE_LINEA = re.compile(r"(?i)</p>|<br\s*/?>|</li>|</tr>|</h\d>|</div>")


def lineas_del_html(h):
    if not h:
        return []
    t = FIN_DE_LINEA.sub("\n", h)
    t = re.sub(r"(?i)</td>", " ", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t).replace("\xa0", " ")
    salida = []
    for linea in t.split("\n"):
        linea = re.sub(r"\s+", " ", linea).strip()
        if linea:
            salida.append(linea)
    return salida


def seccion_del_pdf(texto, desde, hasta):
    """Lo que hay entre dos encabezados de la ficha en PDF («6.1» y «6.2»)."""
    if not texto:
        return None
    m = re.search(desde, texto)
    if not m:
        return None
    resto = texto[m.end():]
    f = re.search(hasta, resto)
    return resto[: f.start()] if f else resto[:3000]


def partir_lista(texto):
    """«lactosa, celulosa (E460) y estearato de magnesio» → una por elemento,
    sin partir lo que va entre paréntesis."""
    trozos, actual, nivel = [], "", 0
    for ch in texto:
        if ch == "(":
            nivel += 1
        elif ch == ")":
            nivel = max(0, nivel - 1)
        if nivel == 0 and ch in ",;":
            trozos.append(actual)
            actual = ""
        else:
            actual += ch
    trozos.append(actual)
    salida = []
    for t in trozos:
        # « y » final de enumeración, solo fuera de paréntesis.
        partes = re.split(r"\s+y\s+(?![^()]*\))", t)
        salida += [x.strip(" .:") for x in partes if x.strip(" .:")]
    return salida


def del_prospecto(ficha):
    """
    Sin ficha técnica, el prospecto: «Los demás componentes (excipientes)
    son…», hasta «Aspecto del producto». Literal, partido por elementos.
    """
    bruto = ficha.get("prospecto") or ""
    if "<" in bruto:
        texto = " ".join(lineas_del_html(bruto))
    else:
        # Del PDF: las palabras partidas a final de línea llegan como «clo - ruro».
        texto = re.sub(r"\s+", " ", bruto)
        texto = re.sub(r"(?<=[a-záéíóúñ]) - (?=[a-záéíóúñ])", "", texto)
    m = re.search(
        r"(?i)(los demás componentes|los otros componentes|el otro componente|los demás ingredientes|"
        r"los excipientes)[^:.]{0,80}?(:|\bes\b|\bson\b)(.*?)"
        r"(aspecto del producto|aspecto de |contenido del envase|forma farmac|titular de la autorización|$)",
        texto,
    )
    if not m:
        # «Excipientes:» a secas, como encabezado de una lista.
        m = re.search(r"(?i)\bexcipientes\s*:()()(.*?)(forma farmac|aspecto|contenido del envase|\.\s+[A-ZÁÉÍÓÚ]{4,}|$)", texto)
    if not m:
        return []
    bloque = m.group(3)
    # Si lo que se ha cogido no parece una lista (demasiado largo), no se
    # inventa nada: mejor «no se pudo leer» que una lista equivocada.
    if len(bloque) > 700:
        return []
    lineas = partir_lista(bloque)
    if not lineas or any(len(l) > 120 for l in lineas):
        return []
    return lineas[:60]


def excipientes(ficha):
    if ficha.get("segmentada") and ficha.get("h6.1") and lineas_del_html(ficha.get("h6.1")):
        lineas = lineas_del_html(ficha.get("h6.1"))
    elif not ficha.get("pdf") and ficha.get("prospecto"):
        lineas = del_prospecto(ficha)
    else:
        bloque = seccion_del_pdf(
            ficha.get("pdf"),
            r"6\.1\.?\s*Lista de excipientes",
            r"\n\s*6\.2\.?\s",
        )
        lineas = [re.sub(r"\s+", " ", l).strip() for l in (bloque or "").split("\n")]
        lineas = [l for l in lineas if l]
    # Fuera los títulos de la sección, las viñetas y la puntuación que cierra
    # cada elemento de la lista («Sacarina sódica ,»).
    lineas = [l for l in lineas if not re.match(r"(?i)^6\.1\.?\s", l)]
    lineas = [re.sub(r"^[-•·*]\s*", "", l).strip().rstrip(" ,;.").strip() for l in lineas]
    # Un párrafo con toda la lista separada por comas se parte en elementos,
    # sin tocar lo que va entre paréntesis: así cada aviso señala solo el
    # excipiente exacto.
    partidas = []
    for l in lineas:
        partidas += partir_lista(l) if len(l) > 60 and "," in l else [l]
    lineas = [l for l in partidas if l]
    return "\n".join(lineas) if lineas else None


def composicion(ficha):
    if ficha.get("segmentada") and ficha.get("h2"):
        return " ".join(lineas_del_html(ficha.get("h2")))
    bloque = seccion_del_pdf(
        ficha.get("pdf"),
        r"2\.?\s*COMPOSICI[ÓO]N CUALITATIVA Y CUANTITATIVA",
        r"\n\s*3\.?\s*FORMA FARMAC",
    )
    return re.sub(r"\s+", " ", bloque or "").strip()


CIERRE = re.compile(r"(?i)para (consultar )?la lista completa de excipientes")


def efecto_conocido(texto):
    """El párrafo de «excipiente(s) con efecto conocido», literal y corto."""
    if not texto:
        return None
    m = re.search(r"(?i)excipientes? con efecto conocido", texto)
    if not m:
        return None
    resto = texto[m.start():]
    c = CIERRE.search(resto)
    trozo = resto[: c.start()] if c else resto[:600]
    trozo = trozo.strip(" .:;")
    return trozo[:600] or None


ORIGEN = re.compile(r"(?i)porcin|cerdo|bovin|vacun|ovin|pescado|origen animal|de huevo|de leche")


def origen(texto):
    """Las frases de la sección 2 que dicen de qué animal sale algo."""
    if not texto:
        return None
    frases = re.split(r"(?<=[.;])\s+", texto)
    halladas = [f.strip() for f in frases if ORIGEN.search(f)]
    return " ".join(halladas)[:600] or None


def main():
    if not os.path.isdir(os.path.join(CIMA, "fichas")):
        sys.exit("Falta datos/cima/: pasa antes descargar_medicamentos.py.")
    meds = []
    for f in sorted(os.listdir(os.path.join(CIMA, "listas"))):
        if f.startswith("medicamentos_"):
            meds += json.load(open(os.path.join(CIMA, "listas", f)))["resultados"]
    pres = []
    for f in sorted(os.listdir(os.path.join(CIMA, "listas"))):
        if f.startswith("presentaciones_"):
            pres += json.load(open(os.path.join(CIMA, "listas", f)))["resultados"]

    principios = {}
    for p in pres:
        if p.get("pactivos"):
            principios.setdefault(p["nregistro"], p["pactivos"])

    filas, sin_ficha, sin_excipientes = [], 0, 0
    for m in meds:
        nreg = m["nregistro"]
        ruta = os.path.join(CIMA, "fichas", f"{nreg}.json")
        ficha = json.load(open(ruta)) if os.path.exists(ruta) else {}
        if not ficha:
            sin_ficha += 1
        exc = excipientes(ficha) if ficha else None
        if ficha and not exc:
            sin_excipientes += 1
        comp = composicion(ficha) if ficha else ""
        url = next((d.get("url") for d in m.get("docs", []) if d.get("tipo") == 1), None)
        filas.append((
            nreg,
            m["nombre"],
            m.get("labtitular"),
            1 if m.get("receta") else 0,
            (m.get("formaFarmaceutica") or {}).get("nombre"),
            " | ".join(v["nombre"] for v in m.get("viasAdministracion", [])) or None,
            principios.get(nreg) or (m.get("vtm") or {}).get("nombre"),
            exc,
            efecto_conocido(comp),
            origen(comp),
            url,
            ficha.get("obtenido") or "",
        ))

    conocidos = {m["nregistro"] for m in meds}
    cajas = [(p["cn"], p["nregistro"], p.get("nombre")) for p in pres
             if p.get("cn") and p["nregistro"] in conocidos]

    destino = sys.argv[1] if len(sys.argv) > 1 else BASE  # una copia, para probar
    con = sqlite3.connect(destino)
    preparar_tablas(con)
    con.executemany("INSERT INTO medicamento VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", filas)
    con.executemany("INSERT OR REPLACE INTO medicamento_cn VALUES (?,?,?)", cajas)
    con.executemany("INSERT OR REPLACE INTO meta VALUES (?,?)", [
        ("fuente_medicamentos", "Agencia Española de Medicamentos y Productos Sanitarios www.aemps.gob.es"),
        ("medicamentos", str(len(filas))),
        ("medicamentos_obtenidos", max((f[-1] for f in filas if f[-1]), default="")),
    ])
    con.commit()
    con.execute("VACUUM")
    con.close()
    print(f"medicamentos: {len(filas)} · cajas: {len(cajas)} · sin ficha descargada: {sin_ficha} "
          f"· sin lista de excipientes legible: {sin_excipientes}")


if __name__ == "__main__":
    main()
