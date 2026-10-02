#!/usr/bin/env python3
"""
De qué está hecho cada aditivo, según la ley europea.

El Reglamento (UE) 231/2012 fija las especificaciones de todos los aditivos
autorizados en la Unión, y de cada uno da una «Definición» que dice exactamente
de qué está hecho y de dónde sale:

    E 120 · «Los carmines y el ácido carmínico se obtienen a partir de extractos
    acuosos, alcohólicos o acuoso-alcohólicos de la cochinilla, que consiste en
    los cuerpos desecados de la hembra del insecto Dactylopius coccus Costa.»

Esa es la fuente que hay que enseñar en una tienda de aplicaciones: un acto
jurídico de la Unión Europea, publicado en el Diario Oficial y en castellano.
El texto de EUR-Lex se puede reutilizar citando la fuente (Decisión 2011/833/UE).

Salida: datos/aditivos_definicion.json (y, con «en», la versión inglesa del
mismo reglamento en datos/aditivos_definicion_en.json).

    python3 datos/descargar_aditivos_reglamento.py
    python3 datos/descargar_aditivos_reglamento.py en
"""

import html
import sys
import json
import re
import ssl
import urllib.request
from pathlib import Path

try:
    import certifi
    CONTEXTO = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CONTEXTO = ssl.create_default_context()

AQUI = Path(__file__).resolve().parent
# El mismo acto jurídico, publicado por la UE en cada lengua oficial.
INGLES = len(sys.argv) > 1 and sys.argv[1] == "en"
CACHE = AQUI / ("cache_reglamento_231_en.html" if INGLES else "cache_reglamento_231.html")
SALIDA = AQUI / ("aditivos_definicion_en.json" if INGLES else "aditivos_definicion.json")

URL = f"https://eur-lex.europa.eu/legal-content/{'EN' if INGLES else 'ES'}/TXT/HTML/?uri=CELEX:32012R0231"
FUENTE = ("Regulation (EU) No 231/2012, additive specifications" if INGLES
          else "Reglamento (UE) 231/2012, especificaciones de aditivos")
AGENTE = "Mozilla/5.0 (compatible; ZasApp/1.0; app de etiquetas alimentarias)"

# En el reglamento los subtipos se escriben «E 331 i) CITRATO MONOSÓDICO», con
# el paréntesis de cierre y sin el de apertura. Si no se contempla esa forma se
# pierden el E 500, el E 331, los fosfatos y media tabla.
CABECERA = re.compile(
    r'^E\s?(\d{3,4})\s?([a-z]?)\s*(?:\(?\s*([ivx]{1,4})\s*\)?)?\s+'
    r'([A-ZÁÉÍÓÚÑÜ0-9][^a-z]{2,90})$')

# Los rótulos de la ficha de cada aditivo en el reglamento.
ROTULOS = {
    "Synonyms", "Definition", "Chemical name", "Chemical formula", "Molecular weight",
    "Assay", "Description", "Identification", "Purity", "Solubility", "Class",
    "Colour Index No", "CAS number", "CAS No", "Impurities", "Particle size", "Content",
    "Sinónimos", "Definición", "Einecs", "EINECS", "Nombre químico", "Fórmula química",
    "Peso molecular", "Denominación química", "Contenido", "Descripción", "Identificación",
    "Pureza", "Solubilidad", "Criterios de pureza", "Clase", "Número de índice de color",
    "Número CAS", "Ensayo", "Impurezas", "Tamaño de partícula",
}

# Líneas que son códigos y no explican nada.
SOLO_CODIGO = re.compile(
    r'^(EINECS|Einecs|CAS|N\.º CAS|C\d|[A-Z][a-z]?\d|\d|No más|No menos|Máx|Mín|Not more|Not less)', )


def bajar():
    if CACHE.exists():
        return CACHE.read_text(encoding="utf-8", errors="ignore")
    peticion = urllib.request.Request(URL, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(peticion, timeout=180, context=CONTEXTO) as r:
        texto = r.read().decode("utf-8", errors="ignore")
    CACHE.write_text(texto, encoding="utf-8")
    return texto


def lineas_de(bruto):
    """
    El HTML de EUR-Lex marca en cursiva los nombres científicos —«Curcuma longa
    L.», «Candida spp.»— con etiquetas por dentro del párrafo. Si se cambian por
    saltos de línea, el nombre del bicho se pierde y queda «se obtiene de L.».
    Por eso las etiquetas de dentro del texto se cambian por nada y solo se
    parte por las que de verdad terminan un bloque.
    """
    texto = bruto
    texto = re.sub(r"(?i)</(p|td|tr|div|table|h\d)>|<br\s*/?>", "\n", texto)
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = html.unescape(texto)
    return [re.sub(r"\s+", " ", l).strip() for l in texto.split("\n") if l.strip()]


def bloque(lineas, desde):
    """Las líneas que hay debajo de un rótulo, hasta el siguiente rótulo."""
    partes = []
    for x in lineas[desde:desde + 8]:
        if x in ROTULOS or CABECERA.match(x):
            break
        partes.append(x)
    return partes


def limpiar(partes):
    """Quita los códigos y deja la prosa, que es lo que entiende una persona."""
    prosa = [p for p in partes if not SOLO_CODIGO.match(p) and len(p) > 25]
    if not prosa:
        return None
    texto = " ".join(prosa)
    texto = re.sub(r"\s*EINECS.*$", "", texto).strip(" .;,")
    texto = re.sub(r"\s{2,}", " ", texto)
    return texto + "." if texto and not texto.endswith(".") else texto


def main():
    lineas = lineas_de(bajar())
    entradas, actual = {}, None
    for i, l in enumerate(lineas):
        m = CABECERA.match(l)
        if m:
            base = ("e" + m.group(1) + m.group(2)).lower()
            actual = base + (m.group(3) or "").lower()
            entradas.setdefault(actual, {"definicion": None, "descripcion": None, "base": base})
            continue
        if not actual:
            continue
        if l in ("Definición", "Definition") and not entradas[actual]["definicion"]:
            entradas[actual]["definicion"] = limpiar(bloque(lineas, i + 1))
        elif l in ("Descripción", "Description") and not entradas[actual]["descripcion"]:
            entradas[actual]["descripcion"] = limpiar(bloque(lineas, i + 1))

    salida = {}
    for ident, v in entradas.items():
        texto = v["definicion"] or v["descripcion"]
        if not texto:
            continue
        ficha = {
            "texto": texto[:400],
            "fuente": FUENTE,
            "url": "https://eur-lex.europa.eu/eli/reg/2012/231/oj",
        }
        salida[ident] = ficha
        # Muchas etiquetas ponen «E 500» a secas, sin el subtipo: el texto del
        # primer subtipo sirve, porque es el mismo compuesto.
        salida.setdefault(v["base"], ficha)
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1))
    print(f"aditivos en el reglamento: {len(entradas)} | con texto: {len(salida)}")


if __name__ == "__main__":
    main()
