#!/usr/bin/env python3
"""
Lee por la entrada estandar el volcado CSV (tabulado) de Open Food Facts y
escribe solo los productos vendidos en Espana, con las columnas que usa la app.

No transforma ni completa ningun dato: lo que no viene, se queda vacio.
Fuente: Open Food Facts, ODbL 1.0 - https://openfoodfacts.org
"""
import csv, re, sys

csv.field_size_limit(10_000_000)

COLUMNAS = [
    "code", "product_name", "generic_name", "brands", "quantity",
    "product_quantity", "ingredients_text", "allergens", "traces_tags",
    "additives_tags", "categories_tags", "labels_tags",
    "ingredients_analysis_tags", "countries_tags", "nutriscore_grade",
    "nova_group", "additives_n",
    # Lo que hace falta para avisar de azúcar, sal y grasas saturadas
    "energy-kcal_100g", "fat_100g", "saturated-fat_100g", "sugars_100g",
    "salt_100g", "fiber_100g", "proteins_100g",
    # 1-oct-2026: «que mida absolutamente todo». Van al FINAL para que las
    # columnas de antes no cambien de sitio. El agua también: sodio, calcio,
    # magnesio, bicarbonatos… es lo que la distingue de otra agua.
    "carbohydrates_100g", "trans-fat_100g", "cholesterol_100g",
    "sodium_100g", "potassium_100g", "calcium_100g", "magnesium_100g", "iron_100g",
    "bicarbonate_100g", "chloride_100g", "sulphate_100g", "fluoride_100g",
    "silica_100g", "nitrate_100g", "caffeine_100g", "ph_100g",
    "phosphorus_100g", "zinc_100g", "iodine_100g",
    "vitamin-d_100g", "vitamin-c_100g", "vitamin-b12_100g", "folates_100g",
]

lector = csv.reader(sys.stdin, delimiter="\t", quoting=csv.QUOTE_NONE)
cabecera = next(lector)
idx = {c: cabecera.index(c) for c in COLUMNAS if c in cabecera}
faltan = [c for c in COLUMNAS if c not in idx]
if faltan:
    print("AVISO columnas ausentes: " + ",".join(faltan), file=sys.stderr)

salida = csv.writer(sys.stdout, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
salida.writerow(COLUMNAS)

i_paises = idx.get("countries_tags")
i_code = idx["code"]

# QUÉ SE GUARDA Y POR QUÉ.
#
# Antes bastaba con que la ficha dijera «en:spain». El resultado, medido: de
# 4.535.553 productos se guardaban 354.697, y en el supermercado más de la
# mitad de lo que se escanea no aparece. La razón es que en Open Food Facts el
# país lo pone quien sube la ficha, y muchísimas fichas de productos que se
# venden aquí no lo llevan o llevan otro.
#
# Así que se guarda también por el CÓDIGO. El prefijo 84 lo da AECOC a las
# empresas registradas en España: un 84 significa que la empresa que registró
# ese producto es española. No dice dónde se cultivó ni dónde se fabricó —eso
# no lo dice ningún código de barras—, pero sí que es un producto de aquí, y
# es justo lo que hace falta para que el escáner encuentre la marca blanca de
# los supermercados españoles, que es casi todo lo que la gente compra.
ESPANA = ("en:spain", "es:espana", "es:españa")

# Y LA TERCERA PUERTA: LA ETIQUETA ESCRITA EN ESPAÑOL.
#
# Un producto importado —una crema de avellanas italiana, un refresco embotellado
# fuera— lleva su código de otro país y su ficha puede no decir España. Pero si la
# lista de ingredientes está en español, ese bote se vende aquí: la ley obliga a
# etiquetar en la lengua del país donde se vende. Medido sobre el volcado entero:
# 30.166 productos que hoy se quedaban fuera tienen la etiqueta en español.
ETIQUETA_ES = re.compile(
    r"\b(az[uú]car|aceite|leche|harina|conservador|colorante|emulgente|estabilizante|"
    r"sal|agua|almid[oó]n|huevo|trigo|cacao|aroma|aromas|edulcorante|antioxidante|"
    r"espesante|gluten|jarabe)\b",
    re.IGNORECASE,
)
PALABRAS_MINIMAS = 3


def es_de_aqui(paises: str, codigo: str, ingredientes: str) -> bool:
    bajo = paises.lower()
    if any(p in bajo for p in ESPANA):
        return True
    # EAN-13 con prefijo 84: empresa registrada en España.
    if len(codigo) == 13 and codigo.startswith("84"):
        return True
    # Etiqueta en español: se vende aquí, venga de donde venga.
    return len(ETIQUETA_ES.findall(ingredientes)) >= PALABRAS_MINIMAS


i_ing = idx.get("ingredients_text")
total = guardados = por_pais = por_codigo = por_etiqueta = 0
for fila in lector:
    total += 1
    if total % 500_000 == 0:
        print(f"leidos {total:,} guardados {guardados:,}", file=sys.stderr, flush=True)
    if len(fila) <= i_paises:
        continue
    paises = fila[i_paises]
    codigo = fila[i_code].strip()
    if not codigo or not codigo.isdigit():
        continue
    ingredientes = fila[i_ing] if i_ing is not None and i_ing < len(fila) else ""
    if not es_de_aqui(paises, codigo, ingredientes):
        continue
    if "en:spain" in paises.lower():
        por_pais += 1
    elif len(codigo) == 13 and codigo.startswith("84"):
        por_codigo += 1
    else:
        por_etiqueta += 1
    salida.writerow([fila[idx[c]] if c in idx and idx[c] < len(fila) else "" for c in COLUMNAS])
    guardados += 1

print(f"FIN leidos {total:,} guardados {guardados:,} (por pais {por_pais:,}, por codigo 84 {por_codigo:,}, por etiqueta en espanol {por_etiqueta:,})", file=sys.stderr, flush=True)
