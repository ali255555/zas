#!/usr/bin/env python3
"""
Lo mismo, pero mejor: alternativas reales que se venden en España.

Yuka enseña alternativas y es lo que más se le agradece: el usuario no quiere
comparar dos botes él solo en el pasillo, quiere que le digan cuál coger. Aquí
se hace igual, pero con las cuentas a la vista y sin inventar nada: todos los
productos salen de Open Food Facts, con su código de barras, su Nutri-Score,
su grupo NOVA y sus aditivos.

El fichero que sale viaja dentro del APK, así que las alternativas salen sin
conexión, en el pasillo del supermercado y sin cobertura.

    python3 datos/alternativas.py

Fuente: Open Food Facts (ODbL 1.0). Se guarda el código de barras para poder
citar cada producto y para que el usuario pueda escanearlo y verlo entero.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time

DESTINO = pathlib.Path(__file__).resolve().parent.parent / "app/src/main/assets/alternativas.json"
AGENTE = "Zas/0.5 (escaner de alimentos sin animo de lucro; https://openfoodfacts.org)"
CAMPOS = "code,product_name,brands,nutriscore_grade,nova_group,additives_n,categories_tags"

# Las categorías de un supermercado español. Es la lista de lo que se compra,
# no una opinión sobre lo que se debería comprar.
CATEGORIAS = [
    "en:yogurts", "en:milk", "en:cheese", "en:breakfast-cereals", "en:biscuits",
    "en:chocolates", "en:sausages", "en:hams", "en:canned-fishes", "en:legume-and-derivatives",
    "en:pasta", "en:rice", "en:bread", "en:fruit-juices", "en:carbonated-drinks",
    "en:waters", "en:olive-oils", "en:sauces", "en:pizzas", "en:frozen-foods",
    "en:potato-crisps", "en:nuts", "en:jams", "en:honey", "en:coffees", "en:teas",
    "en:ice-creams", "en:baby-foods", "en:plant-based-milk-alternatives",
    "en:tofu", "en:hummus", "en:canned-legumes", "en:tuna", "en:sardines",
    "en:olives", "en:vinegars", "en:mayonnaises", "en:ketchup", "en:mustards",
    "en:margarines", "en:butters", "en:eggs", "en:flours", "en:sugars",
    "en:chips-and-fries", "en:cookies", "en:cakes", "en:croissants",
    "en:energy-drinks", "en:beers", "en:wines", "en:soups", "en:broths",
    "en:prepared-meals", "en:salads", "en:desserts", "en:puddings",
    "en:custards", "en:cereal-bars", "en:chocolate-bars", "en:candies",
    "en:chewing-gum", "en:dried-fruits", "en:seeds", "en:peanut-butter",
    "en:chocolate-spreads", "en:sandwiches", "en:burgers", "en:nuggets",
    "en:fish-fingers", "en:surimi", "en:smoked-salmon", "en:fresh-cheeses",
    "en:blue-cheeses", "en:yogurt-drinks", "en:kefir", "en:cream",
    "en:condensed-milks", "en:powdered-milks", "en:infant-formulae",
    "en:pasta-sauces", "en:pestos", "en:curries", "en:noodles", "en:couscous",
    "en:quinoa", "en:oats", "en:mueslis", "en:granolas", "en:corn-flakes",
    "en:rusks", "en:crackers", "en:breadsticks", "en:tortillas",
    "en:canned-vegetables", "en:canned-tomatoes", "en:frozen-vegetables",
    "en:frozen-fish", "en:ready-to-eat-meals", "en:vegetable-oils",
    "en:sunflower-oils", "en:cocoa-and-its-products", "en:hot-beverages",
    "en:iced-teas", "en:lemonades", "en:syrups", "en:sweeteners",
    "en:protein-bars", "en:sports-drinks", "en:charcuterie", "en:bacons",
    "en:chorizos", "en:salamis", "en:pates", "en:meat-preparations",
    "en:chicken-breasts", "en:turkey-breasts", "en:cooked-hams",
]

CUANTAS_POR_CATEGORIA = 8

# Por debajo de esto no es una alternativa, es otro producto malo. Si en una
# categoría entera no hay nada decente —el chorizo, por ejemplo— no se guarda
# nada, y la aplicación no enseña nada. Es más honesto que ofrecer «el chorizo
# menos malo» detrás de un cartel que dice que no te lo comas.
NOTA_MINIMA = 1.0
PAGINA = 100


def baja(url: str, intentos: int = 3) -> dict:
    """
    Con reintentos: Open Food Facts contesta 503 cuando va cargado, y eso no
    significa que no haya productos. Sin esto, media lista se quedaba vacía.
    """
    ultimo = ""
    for intento in range(intentos):
        hecho = subprocess.run(
            ["curl", "-sS", "--fail", "--max-time", "60", "-A", AGENTE, url],
            capture_output=True,
        )
        if hecho.returncode == 0:
            try:
                return json.loads(hecho.stdout.decode("utf-8", "replace"))
            except json.JSONDecodeError as e:
                ultimo = f"respuesta que no es JSON: {e}"
        else:
            ultimo = hecho.stderr.decode("utf-8", "replace").strip()[:120]
        time.sleep(5 * (intento + 1))
    raise RuntimeError(ultimo)


def nota(p: dict) -> float:
    """
    Cuanto más alto, mejor. Es la misma idea que la nota de la aplicación:
    manda el grado de procesado, después el Nutri-Score y después los aditivos.
    """
    nova = p.get("nova_group")
    puntos = {1: 6.0, 2: 4.0, 3: 1.0, 4: -3.0}.get(nova, 0.0)
    puntos += {"a": 4.0, "b": 2.0, "c": 0.0, "d": -2.0, "e": -4.0}.get(
        (p.get("nutriscore_grade") or "").lower(), 0.0
    )
    puntos -= min(p.get("additives_n") or 0, 6) * 0.5
    return puntos


def vale(p: dict) -> bool:
    """Sin datos no entra: una alternativa sin nota no es una alternativa."""
    if not (p.get("code") or "").isdigit():
        return False
    if not (p.get("product_name") or "").strip():
        return False
    if p.get("nova_group") is None and not p.get("nutriscore_grade"):
        return False
    return True


def de_la_categoria(categoria: str) -> list[dict]:
    url = (
        "https://world.openfoodfacts.org/api/v2/search"
        f"?countries_tags_en=spain&categories_tags={categoria}"
        f"&fields={CAMPOS}&page_size={PAGINA}"
    )
    productos = [p for p in baja(url).get("products", []) if vale(p)]
    productos.sort(key=nota, reverse=True)
    mejores = []
    marcas = set()
    for p in productos:
        if nota(p) < NOTA_MINIMA:
            continue
        marca = (p.get("brands") or "").split(",")[0].strip().lower()
        # Una por marca: ocho yogures de la misma marca no son ocho opciones.
        if marca and marca in marcas:
            continue
        marcas.add(marca)
        mejores.append({
            "codigo": p["code"],
            "nombre": p["product_name"].strip()[:70],
            "marca": (p.get("brands") or "").split(",")[0].strip()[:40],
            "nutriscore": (p.get("nutriscore_grade") or "").lower() or None,
            "nova": p.get("nova_group"),
            "aditivos": p.get("additives_n"),
            "nota": round(nota(p), 2),
        })
        if len(mejores) >= CUANTAS_POR_CATEGORIA:
            break
    return mejores


def main() -> int:
    salida = {}
    fallos = []
    for i, categoria in enumerate(CATEGORIAS, 1):
        try:
            mejores = de_la_categoria(categoria)
        except Exception as e:
            fallos.append((categoria, str(e)[:80]))
            continue
        if mejores:
            salida[categoria] = mejores
        print(f"[{i}/{len(CATEGORIAS)}] {categoria}: {len(mejores)}", flush=True)
        time.sleep(1.0)  # una petición por segundo: no se castiga a Open Food Facts

    if not salida:
        print("Open Food Facts no ha devuelto nada: no se toca el fichero.", file=sys.stderr)
        return 1

    DESTINO.write_text(
        json.dumps(
            {
                "fuente": "Open Food Facts",
                "licencia": "ODbL 1.0",
                "url": "https://openfoodfacts.org",
                "descargado": time.strftime("%Y-%m-%d"),
                "categorias": salida,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    cuantos = sum(len(v) for v in salida.values())
    print(f"{len(salida)} categorías, {cuantos} alternativas → {DESTINO}")
    if fallos:
        print(f"Sin datos en {len(fallos)}: {[f[0] for f in fallos][:8]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
