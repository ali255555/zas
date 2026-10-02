#!/usr/bin/env python3
"""
Recetas españolas y europeas de verdad, del recetario libre de Wikibooks.

es.wikibooks.org tiene «Artes culinarias/Recetas»: más de mil recetas escritas
por gente de aquí —potaje conquense, gachas manchegas, migas, alajú— con una
plantilla fija: comensales, tiempo, dificultad, ingredientes y procedimiento.
Eso se puede leer a máquina sin inventar nada.

Licencia: CC BY-SA 3.0. Hay que citar el título, el enlace y la licencia en cada
receta; la aplicación lo hace en la pantalla de la receta.

Salida: datos/recetas_wikibooks.json

    python3 datos/descargar_recetas_wikibooks.py
"""

import json
import re
import ssl
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import certifi
    CONTEXTO = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CONTEXTO = ssl.create_default_context()

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI / "recetas_wikibooks.json"
CACHE = AQUI / "cache_wikibooks_recetas.json"
API = "https://es.wikibooks.org/w/api.php"
AGENTE = "ZasApp/1.0 (https://github.com/alitalaint; recetario offline)"
LOTE = 40

# Texto de relleno de la plantilla vacía: no es ni ingrediente ni paso.
RELLENO = re.compile(
    r"^(enumerar|explicar|escrib|describ|indicar|a[nñ]ad[ei]r? aqu[ií]|"
    r"ingrediente\s*\d|paso\s*\d|poner los ingredientes|lista de ingredientes|"
    r"opcional(es)?$|sin especificar)", re.I)

# ---------------------------------------------------------------------------
# Lo que NO entra en la aplicación, por mucho que esté en el recetario.
#
# Esto no es remilgo: es que la aplicación la puede abrir un crío. No se dan
# instrucciones para hacer bebidas alcohólicas, ni para curar aceitunas con sosa
# cáustica, ni para envasar conservas en casa —que es como se produce el
# botulismo—. Aquí solo entra comida que se cocina y se come.

# Las categorías de la propia Wikibooks dicen de dónde es cada receta y si es
# comida o bebida. Es mejor guía que adivinar por el título.
CACHE_CATEGORIAS = AQUI / "cache_categorias_recetas.json"

# Cocina de aquí y del resto de Europa. Lo demás, fuera: el usuario pidió
# recetas europeas, y una bandeja paisa no lo es por muy buena que esté.
EUROPEAS = (
    "gastronomía de españa", "cocina de la guardia de jaén", "cocina castellano manchega",
    "cocina aragonesa", "cocina de ayerbe", "cocina de alpuente", "cocina de potries",
    "cocina andaluza", "cocina asturiana", "cocina castellano leonesa", "cocina catalana",
    "cocina alicantina", "cocina de colmenar de oreja", "cocina de la provincia de ávila",
    "cocina gallega", "cocina de ayora", "cocina murciana", "cocina navarra",
    "cocina riojana", "cocina de sot de chera", "cocina de la comunidad valenciana",
    "cocina madrileña", "cocina cántabra", "cocina leonesa", "cocina de niharra",
    "cocina de santo tomé de zabarcos", "gastronomía de la provincia de lérida",
    "gastronomía de la provincia de sevilla", "gastronomía de vizcaya",
    "gastronomía de italia", "gastronomía de francia", "gastronomía de portugal",
    "gastronomía de alemania", "gastronomía de austria", "gastronomía de hungría",
    "gastronomía de polonia", "gastronomía de letonia", "gastronomía de suiza",
    "gastronomía de grecia", "gastronomía de serbia", "gastronomía de macedonia",
    "gastronomía de reino unido", "gastronomía de irlanda", "cocina navideña",
)

# Ni bebidas ni alcohol: la aplicación la puede abrir un menor.
NO_SON_COMIDA_CAT = ("bebidas", "bebidas alcohólicas", "bebidas de venezuela", "bebidas de perú")

# Por el título: lo que la receta ES.
NO_ES_COMIDA = re.compile(
    r"(?<![a-zñáéíóú])("
    r"aguardiente|licor(es)?|orujo|ponche|sangr[ií]a|c[oó]cteles?|c[oó]ctel|"
    r"chupito|hidromiel|kalimotxo|calimocho|vermut|"
    r"agua de \w+|agua ardiente|horchata|refresco|batido|zumo|smoothie|"
    r"infusi[oó]n|mate terer[eé]|chilate|chicha|"
    r"conservas?|encurtidos?|salaz[oó]n|adobado|"
    r"mermeladas?|confituras?|jaleas?|"
    r"tinto de verano|rebujito|clarea|zurra|queimada|carajillo|"
    r"leche merengada|granizado|limonada|mojito|caipirinha|margarita|"
    r"taboul[eé]|tabul[eé]"
    r")(?![a-zñáéíóú])", re.I)

# Por el título, cuando el plato ES el propio proceso de curar, encurtir o
# macerar. Nada de esto se cocina y se come en el momento: son conservas, y
# una conserva mal hecha en casa es botulismo.
CURADOS = re.compile(
    r"aceitunas?\b|"
    r"habicholillas curadas|curad[oa]s al sol|salm?uera|"
    r"\ben (aceite|vinagre|salaz[oó]n|orza)\b|"
    r"anchoas\b|boquerones en vinagre|\bchucrut\b|"
    r"^alcaparras?$|aliñado de aceites|berenjenas aliñadas|^ajo$|"
    r"lomo de orza", re.I)

# Postres que consisten en empapar algo en alcohol. La aplicación la puede
# abrir un crío: aquí no se enseña a emborrachar un bizcocho.
EMPAPADOS_EN_ALCOHOL = re.compile(
    r"\bborrach[oa]s?\b|con vino\b|al vino\b(?!.*(guisad|estofad|salsa))|"
    r"empapad[oa]s? en (vino|licor|ron|co[ñn]ac)|bab[áa] \(", re.I)

# Por los pasos: procesos peligrosos en casa o que no son de cocina.
PELIGROSOS = re.compile(
    r"sosa c[aá]ustica|hidr[oó]xido de sodio|lej[ií]a|destilar|alambique|"
    r"fermentar durante \d+ (semanas|meses)|esterilizar los botes|"
    r"ba[nñ]o mar[ií]a durante \d+ (horas|h)", re.I)

# Lo que no es una receta aunque esté en la categoría.
NO_SON_RECETAS = re.compile(r"/Recetas/[A-ZÁÉÍÓÚÑ]$|Categoría|Plantilla|Anexo", re.I)


def consultar(parametros):
    parametros = dict(parametros, format="json", formatversion="2", utf8="1")
    url = API + "?" + urllib.parse.urlencode(parametros)
    peticion = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    for intento in range(4):
        try:
            with urllib.request.urlopen(peticion, timeout=45, context=CONTEXTO) as r:
                return json.load(r)
        except Exception as e:
            if intento == 3:
                print(f"  fallo: {e}", flush=True)
                return {}
            time.sleep(2 * (intento + 1))
    return {}


def titulos_de_recetas():
    titulos, cont = [], {}
    while True:
        d = consultar(dict(action="query", list="categorymembers",
                           cmtitle="Categoría:Recetas", cmlimit="500",
                           cmtype="page", **cont))
        titulos += [m["title"] for m in d.get("query", {}).get("categorymembers", [])]
        if "continue" not in d:
            break
        cont = d["continue"]
    return [t for t in titulos if not NO_SON_RECETAS.search(t)]


def wikitextos(titulos):
    d = consultar(dict(action="query", prop="revisions", rvprop="content",
                       rvslots="main", titles="|".join(titulos)))
    salida = {}
    for p in d.get("query", {}).get("pages", []):
        if p.get("missing"):
            continue
        revs = p.get("revisions") or []
        if not revs:
            continue
        salida[p["title"]] = revs[0]["slots"]["main"]["content"]
    return salida


def limpiar(texto):
    """Quita el marcado de wiki y deja texto llano."""
    t = texto
    t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "", t)
    # {{ing|huevo}} es el ingrediente, no un adorno: se queda «huevo». Igual con
    # {{ute|sartén}}. Si no se hace antes de borrar plantillas, la receta pierde
    # justo la palabra que importa y queda «2 dientes de».
    for _ in range(3):
        t = re.sub(r"\{\{\s*[a-zA-ZñÑ ]+\s*\|\s*([^{}|]+?)\s*(?:\|[^{}]*)?\}\}", r"\1", t)
    t = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", t)   # [[enlace|texto]]
    t = re.sub(r"\[https?://\S+\s+([^\]]*)\]", r"\1", t)
    t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = t.replace("'''", "").replace("''", "")
    t = re.sub(r"&nbsp;", " ", t)
    return re.sub(r"[ \t]+", " ", t).strip()


def campos_de_plantilla(wiki):
    """Saca los campos de {{Artes culinarias/Datos de receta | a = ... }}."""
    inicio = wiki.find("{{Artes culinarias/Datos de receta")
    if inicio == -1:
        return {}
    # buscar el cierre equilibrado
    nivel, i = 0, inicio
    while i < len(wiki):
        if wiki.startswith("{{", i):
            nivel += 1; i += 2; continue
        if wiki.startswith("}}", i):
            nivel -= 1; i += 2
            if nivel == 0:
                break
            continue
        i += 1
    cuerpo = wiki[inicio + 2:i - 2]

    campos, clave, acumulado = {}, None, []
    profundidad = 0
    for linea in cuerpo.splitlines():
        profundidad += linea.count("{{") + linea.count("[[")
        profundidad -= linea.count("}}") + linea.count("]]")
        m = re.match(r"\s*\|\s*([a-zA-ZñÑáéíóú ]+?)\s*=\s*(.*)$", linea)
        if m and profundidad <= 0:
            if clave:
                campos[clave] = "\n".join(acumulado).strip()
            clave = m.group(1).strip().lower()
            acumulado = [m.group(2)]
        elif clave:
            acumulado.append(linea)
    if clave:
        campos[clave] = "\n".join(acumulado).strip()
    return campos


def lista_de(texto):
    """Convierte una lista con *, # o «1.» en una lista de líneas limpias."""
    lineas = []
    for bruto in texto.splitlines():
        linea = limpiar(bruto).strip()
        linea = re.sub(r"^[\*#:;]+\s*", "", linea)
        linea = re.sub(r"^\d+[.)]\s*", "", linea)
        if len(linea) >= 3 and not RELLENO.match(linea):
            lineas.append(linea)
    return lineas


def entero(texto, por_defecto):
    """«4», «6/8», «2/3 horas», «30 min» -> un número razonable."""
    if not texto:
        return por_defecto
    t = limpiar(texto).lower()
    horas = re.search(r"(\d+)\s*(?:h|hora)", t)
    minutos = re.search(r"(\d+)\s*(?:min|m\b)", t)
    if horas or minutos:
        return int(horas.group(1)) * 60 if horas else int(minutos.group(1))
    m = re.search(r"\d+", t)
    return int(m.group(0)) if m else por_defecto


def identificador(titulo):
    base = titulo.split("/")[-1]
    s = unicodedata.normalize("NFD", base.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return "wb-" + s[:60]


# Ingredientes y palabras que delatan una cocina que no es la de aquí. Sirven
# para las recetas que no traen categoría de país: si no dice de dónde es, se
# mira lo que lleva.
DE_FUERA = re.compile(
    r"\b(arepa|masarepa|choclo|elote|frijol|frijoles|poroto|aj[ií] (amarillo|panca|pereirano)|"
    r"palta|yuca|mandioca|panela|chancho|mole poblano|achiote|epazote|chipotle|jalape[nñ]o|"
    r"poblano|tamal|tamales|pupusa|baleada|gandules|malanga|[nñ]ame|jitomate|arracacha|"
    r"quinua|cuy|chuchoca|merken|dulce de leche|manjar blanco|tortillas de ma[ií]z|"
    r"curry|garam masala|nori|miso|kimchi|wasabi|tahini|falafel|biscuits|bourbon|"
    r"maple|buttermilk|bagel|pretzel)\b", re.I)

# Y los platos que se llaman por su nombre y no son de aquí, para las recetas
# que no traen categoría de país.
PLATOS_DE_FUERA = re.compile(
    r"\b(sushi|sashimi|ramen|tempura|teriyaki|yakisoba|gyoza|wonton|dim sum|"
    r"chow mein|chaufa|pad thai|curry|tandoori|tikka|biryani|samosa|"
    r"baklava|baba ?ghanoush|hummus|falafel|tabul[eé]|shawarma|kebap|kebab|"
    r"cuscús|couscous|tayín|tajine|"
    r"brownie|club sandwich|cheesecake|muffin|donut|pancake|waffle|"
    r"enchilada|taco|burrito|quesadilla|guacamole|ceviche|arepa|tamal|pupusa|"
    r"gallopinto|golfeado|anticucho|ajiaco|chip[aá]|chocotorta|botana|"
    r"knish|lajmayin|jal[aá]|leicaj|"
    r"licuado|leche de (avena|arroz|almendra|soja)|bebida de|agua fresca|"
    r"smoothie|milkshake|"
    # Los que se cuelan por el nombre y no son de aquí, uno a uno.
    r"arequipe|capirotada|calzones rotos|boyacense|zambito|arreglos frutales|"
    r"cha chi kay|farfalaj|carajito|cherele|culeca|choj[ií]n|chuañe|chapaleles|"
    r"buseca|changua|chanclas|chilenitos|cachitos|golfeado|acemita"
    r")(s|es)?\b", re.I)


# Si lo que se prepara es básicamente alcohol con algo, es una copa, no un plato.
ALCOHOL = re.compile(
    r"\b(vino|vermut|cerveza|ron|ginebra|whisky|vodka|co[ñn]ac|brandy|licor|"
    r"aguardiente|orujo|anís|cava|champ[aá]n|sidra|tequila|pisco|ginebra)\b", re.I)


def es_una_copa(ingredientes):
    """Pocos ingredientes y uno de ellos es alcohol: eso es una bebida."""
    if len(ingredientes) > 5:
        return False
    return any(ALCOHOL.search(i) for i in ingredientes[:3])


def es_de_aqui(categorias, nombre, texto):
    """
    Se queda si la categoría dice que es europea, o si no dice nada de dónde es
    pero no lleva nada que delate otra cocina. Nunca si es una bebida.
    """
    bajas = [c.lower() for c in categorias]
    if any(c in NO_SON_COMIDA_CAT for c in bajas):
        return False
    if any(c in EUROPEAS for c in bajas):
        return True
    # ¿Trae categoría de país y no es europea? Entonces no es de aquí.
    if any(c.startswith("gastronomía de") or c.startswith("cocina ") for c in bajas):
        return False
    if PLATOS_DE_FUERA.search(nombre):
        return False
    return not DE_FUERA.search(nombre) and not DE_FUERA.search(texto)


def main():
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    categorias = (json.loads(CACHE_CATEGORIAS.read_text())
                  if CACHE_CATEGORIAS.exists() else {})
    if cache:
        titulos = list(cache)
        print(f"páginas en caché: {len(titulos)}")
    else:
        titulos = titulos_de_recetas()
        print(f"páginas en la categoría: {len(titulos)}")

    recetas, sin_plantilla, fuera = [], 0, []
    for i in range(0, len(titulos), LOTE):
        lote = titulos[i:i + LOTE]
        pendientes = [t for t in lote if t not in cache]
        if pendientes:
            cache.update(wikitextos(pendientes))
            CACHE.write_text(json.dumps(cache, ensure_ascii=False))
        for titulo in lote:
            wiki = cache.get(titulo)
            if not wiki:
                continue
            campos = campos_de_plantilla(wiki)
            ingredientes = lista_de(campos.get("ingredientes", ""))
            pasos = lista_de(campos.get("procedimiento", "") or campos.get("preparacion", ""))
            # Una receta con un solo paso o dos palabras no sirve de nada.
            if len(ingredientes) < 3 or len(pasos) < 2 or sum(len(x) for x in pasos) < 80:
                sin_plantilla += 1
                continue
            nombre = titulo.split("/")[-1].strip()

            texto_pasos = " ".join(pasos)
            if (NO_ES_COMIDA.search(nombre) or CURADOS.search(nombre)
                    or EMPAPADOS_EN_ALCOHOL.search(nombre)
                    or es_una_copa(ingredientes)
                    or PELIGROSOS.search(texto_pasos)
                    or not es_de_aqui(
                        categorias.get(titulo, []), nombre,
                        " ".join(ingredientes) + " " + texto_pasos,
                    )):
                fuera.append(nombre)
                continue
            recetas.append({
                "id": identificador(titulo),
                "nombre": nombre,
                "raciones": max(1, min(12, entero(campos.get("comensales"), 4))),
                "minutos": max(5, min(600, entero(campos.get("tiempo"), 45))),
                "ingredientes": ingredientes[:25],
                "pasos": pasos[:20],
                "fuente": "Wikibooks",
                "url": "https://es.wikibooks.org/wiki/" + urllib.parse.quote(titulo.replace(" ", "_")),
                "licencia": "CC BY-SA 3.0",
            })
        if pendientes:
            print(f"  {min(i + LOTE, len(titulos))}/{len(titulos)} · válidas {len(recetas)}", flush=True)
            time.sleep(0.4)

    # Sin repetidas por nombre, y ordenadas
    vistas, limpias = set(), []
    for r in sorted(recetas, key=lambda x: x["nombre"].lower()):
        clave = r["nombre"].lower()
        if clave in vistas:
            continue
        vistas.add(clave)
        limpias.append(r)

    SALIDA.write_text(json.dumps(limpias, ensure_ascii=False, indent=1))
    (AQUI / "recetas_descartadas.txt").write_text("\n".join(sorted(fuera)))
    print(f"recetas guardadas: {len(limpias)} | sin ingredientes o pasos: "
          f"{sin_plantilla} | fuera por no ser comida: {len(fuera)}")


if __name__ == "__main__":
    main()
