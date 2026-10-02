"""
DESCARGA LOS MEDICAMENTOS COMERCIALIZADOS EN ESPAÑA DESDE CIMA (AEMPS).

Fuente: Centro de Información online de Medicamentos de la AEMPS, API REST
pública (https://cima.aemps.es/cima/rest/). La AEMPS permite reutilizar sus
datos citando «Fuente de la información: Agencia Española de Medicamentos y
Productos Sanitarios www.aemps.gob.es» y la fecha en que se obtuvieron.

Con cuidado de no saturar su servidor: UNA petición cada vez, con pausa entre
una y otra, y todo lo descargado se guarda en datos/cima/ para no volver a
pedirlo nunca (si se corta, se retoma donde se quedó).

  1. Lista de medicamentos comercializados (paginada, 200 por página).
  2. Lista de presentaciones comercializadas: el código nacional (CN) de cada
     caja, que es lo que va en su código de barras (847000 + CN).
  3. De cada medicamento, la sección 6.1 de su ficha técnica (lista completa
     de excipientes) y la sección 2 (composición: «excipientes con efecto
     conocido», donde figura el etanol y su cantidad). Si la ficha no está
     segmentada, se lee del PDF oficial de la ficha técnica.

Uso: python3 datos/descargar_medicamentos.py [listas|fichas|completar|todo]
"""
import io
import json
import os
import sys
import subprocess
import time
import urllib.parse

BASE = "https://cima.aemps.es/cima/rest/"
AQUI = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(AQUI, "cima")
PAUSA = 0.4  # segundos entre peticiones: nunca más de una a la vez (≈2 por segundo)
AGENTE = "Zas/1.0 (app de etiquetas; datos AEMPS reutilizados citando la fuente)"

_ultima = 0.0


def pedir(url, acepta="application/json", intentos=4):
    """Una petición, respetando la pausa. Reintenta despacio si falla la red.

    Va por curl y no por urllib: curl usa los certificados del sistema, y en
    este Mac Python no los ve.
    """
    global _ultima
    for n in range(intentos):
        espera = PAUSA - (time.time() - _ultima)
        if espera > 0:
            time.sleep(espera)
        _ultima = time.time()
        r = subprocess.run(
            ["curl", "-s", "-m", "90", "-A", AGENTE, "-H", "Accept: " + acepta,
             "-w", "\n%{http_code}", url],
            capture_output=True,
        )
        if r.returncode != 0:
            time.sleep(15 * (n + 1))
            continue
        cuerpo, _, codigo = r.stdout.rpartition(b"\n")
        estado = int(codigo or 0)
        if estado in (404, 204):
            return estado, b""
        if estado == 429 or estado >= 500 or estado == 0:
            time.sleep(30 * (n + 1))
            continue
        return estado, cuerpo
    raise RuntimeError("no responde: " + url)


def listas():
    os.makedirs(os.path.join(CACHE, "listas"), exist_ok=True)
    for recurso in ("medicamentos", "presentaciones"):
        pagina = 1
        while True:
            fichero = os.path.join(CACHE, "listas", f"{recurso}_{pagina:04d}.json")
            if not os.path.exists(fichero):
                url = BASE + recurso + "?" + urllib.parse.urlencode({"comerc": 1, "pagina": pagina})
                estado, cuerpo = pedir(url)
                if estado != 200:
                    raise RuntimeError(f"{recurso} página {pagina}: {estado}")
                with open(fichero + ".tmp", "wb") as f:
                    f.write(cuerpo)
                os.replace(fichero + ".tmp", fichero)
            d = json.load(open(fichero))
            total = d["totalFilas"]
            if pagina * d["tamanioPagina"] >= total:
                print(recurso, total, "en", pagina, "páginas")
                break
            pagina += 1


def medicamentos():
    salida = []
    for nombre in sorted(os.listdir(os.path.join(CACHE, "listas"))):
        if nombre.startswith("medicamentos_"):
            salida += json.load(open(os.path.join(CACHE, "listas", nombre)))["resultados"]
    return salida


def texto_del_pdf(cuerpo):
    from pypdf import PdfReader  # solo hace falta para fichas sin segmentar
    lector = PdfReader(io.BytesIO(cuerpo))
    return "\n".join((p.extract_text() or "") for p in lector.pages)


def fichas():
    carpeta = os.path.join(CACHE, "fichas")
    os.makedirs(carpeta, exist_ok=True)
    # Primero lo que se traga (vía oral, bucal, sublingual): es lo que más se
    # escanea y lo que importa para alergias y creencias.
    def se_traga(m):
        vias = " ".join(v.get("nombre", "") for v in m.get("viasAdministracion", [])).lower()
        return any(p in vias for p in ("oral", "bucal", "buccal", "sublingual", "orofar"))
    meds = sorted(medicamentos(), key=lambda m: 0 if se_traga(m) else 1)
    hechos = 0
    for m in meds:
        nreg = m["nregistro"]
        fichero = os.path.join(carpeta, f"{nreg}.json")
        if os.path.exists(fichero):
            continue
        segmentada = any(d.get("tipo") == 1 and d.get("secc") for d in m.get("docs", []))
        ficha = {"nregistro": nreg, "segmentada": segmentada}
        if segmentada:
            for seccion in ("2", "6.1"):
                url = BASE + "docSegmentado/contenido/1?" + urllib.parse.urlencode(
                    {"nregistro": nreg, "seccion": seccion})
                # En JSON llega el HTML de la sección, que conserva un excipiente
                # por párrafo; el texto plano los junta y no se pueden separar.
                estado, cuerpo = pedir(url)
                html = None
                if estado == 200 and cuerpo.strip():
                    d = json.loads(cuerpo)
                    d = d if isinstance(d, list) else [d]
                    html = "\n".join(x.get("contenido") or "" for x in d)
                ficha["h" + seccion] = html
        else:
            pdf = next((d.get("url") for d in m.get("docs", []) if d.get("tipo") == 1), None)
            if pdf:
                estado, cuerpo = pedir(pdf, acepta="application/pdf")
                if estado == 200 and cuerpo[:4] == b"%PDF":
                    try:
                        ficha["pdf"] = texto_del_pdf(cuerpo)
                    except Exception as e:  # PDF ilegible: se anota, no se inventa
                        ficha["error"] = str(e)[:200]
        ficha["obtenido"] = time.strftime("%Y-%m-%d")
        with open(fichero + ".tmp", "w") as f:
            json.dump(ficha, f, ensure_ascii=False)
        os.replace(fichero + ".tmp", fichero)
        hechos += 1
        if hechos % 100 == 0:
            print(hechos, "fichas nuevas", flush=True)
    print("fichas:", len(os.listdir(carpeta)), "de", len(meds))


def completar():
    """
    SEGUNDA PASADA, para las fichas que la primera no pudo leer:

     - Medicamentos europeos: CIMA redirige su ficha técnica a la de la EMA
       (Agencia Europea de Medicamentos, información de producto del EPAR).
       Se sigue la redirección y se guarda solo lo que hace falta (secciones 2
       y 6.1). Varias presentaciones comparten el mismo documento: se baja una
       vez.
     - Sin ficha técnica publicada: se lee el prospecto, cuya sección 6 dice
       «Los demás componentes (excipientes) son…».
    """
    carpeta = os.path.join(CACHE, "fichas")
    pdfs = os.path.join(CACHE, "pdf_ema")
    os.makedirs(pdfs, exist_ok=True)
    por_registro = {m["nregistro"]: m for m in medicamentos()}
    hechos = 0
    for nombre in sorted(os.listdir(carpeta)):
        ruta = os.path.join(carpeta, nombre)
        ficha = json.load(open(ruta))
        if ficha.get("segmentada") and ficha.get("h6.1"):
            continue
        if ficha.get("pdf") or ficha.get("prospecto") or ficha.get("completada"):
            continue
        m = por_registro.get(ficha["nregistro"], {})
        docs = m.get("docs", [])
        ft = next((d for d in docs if d.get("tipo") == 1), None)
        p = next((d for d in docs if d.get("tipo") == 2), None)
        if ft and ft.get("url") and not ft.get("secc"):
            clave = ft["url"].rsplit("/", 1)[-1]
            destino = os.path.join(pdfs, clave + ".txt")
            if not os.path.exists(destino):
                estado, cuerpo = pedir_siguiendo(ft["url"])
                texto = ""
                if estado == 200 and cuerpo[:4] == b"%PDF":
                    try:
                        texto = texto_del_pdf(cuerpo)
                    except Exception:
                        texto = ""
                with open(destino, "w") as f:
                    f.write(texto)
            ficha["pdf"] = open(destino).read() or None
        if not ficha.get("pdf") and p:
            if p.get("secc"):
                url = BASE + "docSegmentado/contenido/2?" + urllib.parse.urlencode(
                    {"nregistro": ficha["nregistro"], "seccion": "6"})
                estado, cuerpo = pedir(url)
                if estado == 200 and cuerpo.strip():
                    d = json.loads(cuerpo)
                    d = d if isinstance(d, list) else [d]
                    ficha["prospecto"] = "\n".join(x.get("contenido") or "" for x in d)
            elif p.get("url"):
                estado, cuerpo = pedir_siguiendo(p["url"])
                if estado == 200 and cuerpo[:4] == b"%PDF":
                    try:
                        ficha["prospecto"] = texto_del_pdf(cuerpo)
                    except Exception:
                        pass
        ficha["completada"] = time.strftime("%Y-%m-%d")
        with open(ruta + ".tmp", "w") as f:
            json.dump(ficha, f, ensure_ascii=False)
        os.replace(ruta + ".tmp", ruta)
        hechos += 1
        if hechos % 50 == 0:
            print(hechos, "completadas", flush=True)
    print("completadas:", hechos)


def pedir_siguiendo(url):
    """Como pedir(), pero siguiendo la redirección (CIMA → EMA) y aceptando PDF."""
    global _ultima
    espera = PAUSA - (time.time() - _ultima)
    if espera > 0:
        time.sleep(espera)
    _ultima = time.time()
    r = subprocess.run(
        ["curl", "-s", "-L", "--max-redirs", "3", "-m", "180", "-A", AGENTE, "-w", "\n%{http_code}", url],
        capture_output=True,
    )
    cuerpo, _, codigo = r.stdout.rpartition(b"\n")
    return int(codigo or 0), cuerpo


if __name__ == "__main__":
    que = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if que in ("listas", "todo"):
        listas()
    if que in ("fichas", "todo"):
        fichas()
    if que in ("completar", "todo"):
        completar()
