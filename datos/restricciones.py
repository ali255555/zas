# -*- coding: utf-8 -*-
"""
Catálogo de restricciones que la aplicación ofrece.

Cada una dice de dónde sale. Las que se apoyan en una norma citan la norma;
las que se apoyan en la taxonomía de Open Food Facts lo dicen también.

IMPORTANTE: una restricción religiosa o ética NO se puede certificar leyendo
una lista de ingredientes. La aplicación solo puede decir si ha encontrado un
ingrediente incompatible; nunca puede decir que algo es halal o kosher. Por eso
esos grupos llevan aviso propio ("aviso" del registro).
"""

UE_1169 = "Reglamento (UE) 1169/2011, anexo II"
OFF_TAX = "Taxonomía de Open Food Facts"
UE_1333_V = "Reglamento (CE) 1333/2008, anexo V"
UE_1169_III = "Reglamento (UE) 1169/2011, anexo III"

AVISO_CREENCIA = "Miramos ingredientes. El sello lo da el fabricante."
AVISO_ALERGIA = "La etiqueta del envase manda."

# (id, grupo, nombre, descripcion, tipo, claves, fuente, aviso)
# La palabra de alarma de cada una va en PALABRAS, más abajo.
RESTRICCIONES = [
    # --- Alérgenos de declaración obligatoria en la UE ---
    ("gluten", "Alérgenos", "Gluten", "Trigo, centeno, cebada, avena y derivados", "ALERGENO", ["en:gluten"], UE_1169, AVISO_ALERGIA),
    ("crustaceos", "Alérgenos", "Crustáceos", "Gambas, langostinos, cangrejo", "ALERGENO", ["en:crustaceans"], UE_1169, AVISO_ALERGIA),
    ("huevos", "Alérgenos", "Huevo", "", "ALERGENO", ["en:eggs"], UE_1169, AVISO_ALERGIA),
    ("pescado", "Alérgenos", "Pescado", "", "ALERGENO", ["en:fish"], UE_1169, AVISO_ALERGIA),
    ("cacahuetes", "Alérgenos", "Cacahuete", "", "ALERGENO", ["en:peanuts"], UE_1169, AVISO_ALERGIA),
    ("soja", "Alérgenos", "Soja", "", "ALERGENO", ["en:soybeans"], UE_1169, AVISO_ALERGIA),
    ("leche", "Alérgenos", "Leche", "Incluye la lactosa y todos los lácteos", "ALERGENO", ["en:milk"], UE_1169, AVISO_ALERGIA),
    ("frutos-cascara", "Alérgenos", "Frutos de cáscara", "Almendra, avellana, nuez, anacardo, pistacho", "ALERGENO", ["en:nuts"], UE_1169, AVISO_ALERGIA),
    ("apio", "Alérgenos", "Apio", "", "ALERGENO", ["en:celery"], UE_1169, AVISO_ALERGIA),
    ("mostaza", "Alérgenos", "Mostaza", "", "ALERGENO", ["en:mustard"], UE_1169, AVISO_ALERGIA),
    ("sesamo", "Alérgenos", "Sésamo", "", "ALERGENO", ["en:sesame-seeds"], UE_1169, AVISO_ALERGIA),
    ("sulfitos", "Alérgenos", "Sulfitos", "E220 a E228. Vino, frutos secos, conservas", "ALERGENO",
     ["en:sulphur-dioxide-and-sulphites", "aditivo:e220", "aditivo:e221", "aditivo:e222", "aditivo:e223",
      "aditivo:e224", "aditivo:e226", "aditivo:e227", "aditivo:e228"], UE_1169, AVISO_ALERGIA),
    ("altramuz", "Alérgenos", "Altramuz", "", "ALERGENO", ["en:lupin"], UE_1169, AVISO_ALERGIA),
    ("moluscos", "Alérgenos", "Moluscos", "Mejillón, almeja, calamar, pulpo", "ALERGENO", ["en:molluscs"], UE_1169, AVISO_ALERGIA),

    # --- Dietas ---
    ("vegano", "Dieta", "Vegano", "Nada de origen animal, ni aditivos", "DIETA",
     ["dieta:vegano", "aditivo:origen-animal"], OFF_TAX, None),
    ("vegetariano", "Dieta", "Vegetariano", "Sin carne ni pescado. Admite huevo y leche", "DIETA",
     ["dieta:vegetariano", "aditivo:no-vegetariano"], OFF_TAX, None),
    ("ovolactovegetariano", "Dieta", "Ovolactovegetariano", "Igual que vegetariano, con huevo y lácteos", "DIETA",
     ["dieta:vegetariano", "aditivo:no-vegetariano"], OFF_TAX, None),
    ("pescetariano", "Dieta", "Pescetariano", "Sin carne. Admite pescado y marisco", "INGREDIENTE",
     ["sin:carne"], OFF_TAX, None),
    ("sin-carne-roja", "Dieta", "Sin carne roja", "Ternera, cerdo, cordero", "INGREDIENTE",
     ["sin:ternera", "sin:cerdo"], OFF_TAX, None),

    # --- Creencias y tradición ---
    ("halal", "Creencias", "Halal (ingredientes)", "Sin cerdo, alcohol, gelatina animal ni insectos", "INGREDIENTE",
     ["sin:cerdo", "sin:alcohol", "sin:gelatina-animal", "aditivo:origen-animal"], OFF_TAX, AVISO_CREENCIA),
    ("kosher", "Creencias", "Kosher (ingredientes)", "Sin cerdo, marisco, gelatina animal ni insectos", "INGREDIENTE",
     ["sin:cerdo", "sin:marisco", "sin:gelatina-animal"], OFF_TAX, AVISO_CREENCIA),
    ("sin-ternera", "Creencias", "Sin ternera ni vaca", "", "INGREDIENTE", ["sin:ternera"], OFF_TAX, AVISO_CREENCIA),
    ("sin-ajo-cebolla", "Creencias", "Sin ajo ni cebolla", "", "INGREDIENTE", ["sin:ajo-cebolla"], OFF_TAX, AVISO_CREENCIA),
    ("sin-cerdo", "Creencias", "Sin cerdo", "", "INGREDIENTE", ["sin:cerdo"], OFF_TAX, AVISO_CREENCIA),
    ("sin-alcohol", "Creencias", "Sin alcohol", "", "INGREDIENTE", ["sin:alcohol"], OFF_TAX, AVISO_CREENCIA),
    ("sin-gelatina", "Creencias", "Sin gelatina animal", "", "INGREDIENTE", ["sin:gelatina-animal"], OFF_TAX, AVISO_CREENCIA),

    # --- Intolerancias y condiciones ---
    ("lactosa", "Intolerancias", "Lactosa", "Leche y derivados con lactosa", "ALERGENO", ["en:milk"], UE_1169, AVISO_ALERGIA),
    ("fenilcetonuria", "Intolerancias", "Fenilalanina (fenilcetonuria)", "Aspartamo: E951 y E962", "ADITIVO",
     ["aditivo:e951", "aditivo:e962"], UE_1169_III, AVISO_ALERGIA),
    ("polioles", "Intolerancias", "Polioles", "Edulcorantes (sorbitol, manitol, maltitol, xilitol). No son alcohol; en exceso, laxantes", "ADITIVO",
     ["aditivo:e420", "aditivo:e421", "aditivo:e953", "aditivo:e965", "aditivo:e966", "aditivo:e967", "aditivo:e968"],
     UE_1169_III, None),
    ("marisco", "Intolerancias", "Marisco", "Crustáceos y moluscos", "ALERGENO",
     ["en:crustaceans", "en:molluscs"], UE_1169, AVISO_ALERGIA),

    # --- Aditivos ---
    ("aditivos-animales", "Aditivos", "Aditivos de origen animal", "Cochinilla, gelatina, goma laca y similares", "ADITIVO",
     ["aditivo:origen-animal"], OFF_TAX, None),
    ("e120", "Aditivos", "E120 (cochinilla)", "Colorante rojo de origen animal", "ADITIVO", ["aditivo:e120"], OFF_TAX, None),
    ("azoicos", "Aditivos", "Colorantes azoicos", "E102, E104, E110, E122, E124 y E129", "ADITIVO",
     ["aditivo:e102", "aditivo:e104", "aditivo:e110", "aditivo:e122", "aditivo:e124", "aditivo:e129"], UE_1333_V, None),
    ("edulcorantes", "Aditivos", "Edulcorantes", "Todos los de la clase edulcorante", "ADITIVO",
     ["aditivo:clase:edulcorante"], OFF_TAX, None),
    ("colorantes", "Aditivos", "Colorantes", "Todos los de la clase colorante", "ADITIVO",
     ["aditivo:clase:colorante"], OFF_TAX, None),
    ("conservantes", "Aditivos", "Conservantes", "Todos los de la clase conservante", "ADITIVO",
     ["aditivo:clase:conservante"], OFF_TAX, None),
    ("glutamato", "Aditivos", "Glutamato y potenciadores", "E620 a E650", "ADITIVO",
     ["aditivo:clase:potenciador"], OFF_TAX, None),
]

# Advertencias que la propia norma obliga a poner en la etiqueta.
# Se muestran cuando el producto lleva el aditivo, la active el usuario o no.
ADVERTENCIAS = [
    (["e102", "e104", "e110", "e122", "e124", "e129"],
     "Puede tener efectos negativos sobre la actividad y la atención de los niños.",
     UE_1333_V, "https://eur-lex.europa.eu/eli/reg/2008/1333/oj"),
    (["e951", "e962"],
     "Contiene una fuente de fenilalanina.",
     UE_1169_III, "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),
    (["e420", "e421", "e953", "e965", "e966", "e967", "e968"],
     "Un consumo excesivo puede producir efectos laxantes.",
     UE_1169_III, "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),
    (["e220", "e221", "e222", "e223", "e224", "e226", "e227", "e228"],
     "Los sulfitos son alérgeno de declaración obligatoria por encima de 10 mg/kg.",
     UE_1169, "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),
]

# Raíces de la taxonomía de ingredientes que definen cada filtro nuevo.
RAICES = {
    # Cuidado: en la taxonomia de Open Food Facts en:chicken y en:beef NO cuelgan
    # de en:meat. Hay que nombrarlos todos o el filtro deja pasar el pollo.
    "sin:carne": ["en:meat", "en:poultry", "en:beef", "en:beef-meat", "en:pork",
                  "en:pork-meat", "en:lamb", "en:lamb-meat", "en:veal", "en:chicken",
                  "en:turkey", "en:duck", "en:rabbit", "en:offal", "en:sausage",
                  "en:ham", "en:bacon", "en:goat-meat", "en:horse-meat"],
    "sin:ternera": ["en:beef", "en:beef-meat", "en:veal"],
    "sin:marisco": ["en:crustacean", "en:mollusc"],
    "sin:ajo-cebolla": ["en:garlic", "en:onion"],
}


# Lo que la aplicación dice y enseña en rojo cuando salta cada restricción.
# El usuario puede cambiar cualquiera desde los ajustes.
PALABRAS = {
    "gluten": "Lleva gluten",
    "crustaceos": "Lleva crustáceos",
    "huevos": "Lleva huevo",
    "pescado": "Lleva pescado",
    "cacahuetes": "Lleva cacahuete",
    "soja": "Lleva soja",
    "leche": "Lleva leche",
    "frutos-cascara": "Lleva frutos de cáscara",
    "apio": "Lleva apio",
    "mostaza": "Lleva mostaza",
    "sesamo": "Lleva sésamo",
    "sulfitos": "Lleva sulfitos",
    "altramuz": "Lleva altramuz",
    "moluscos": "Lleva moluscos",
    "vegano": "No es vegano",
    "vegetariano": "No es vegetariano",
    "ovolactovegetariano": "No es vegetariano",
    "pescetariano": "Lleva carne",
    "sin-carne-roja": "Lleva carne roja",
    "halal": "Haram",
    "kosher": "Tref",
    "sin-ternera": "Lleva ternera",
    "sin-ajo-cebolla": "Lleva ajo o cebolla",
    "sin-cerdo": "Lleva cerdo",
    "sin-alcohol": "Lleva alcohol",
    "sin-gelatina": "Lleva gelatina",
    "lactosa": "Lleva lactosa",
    "fenilcetonuria": "Lleva fenilalanina",
    "polioles": "Lleva polioles",
    "marisco": "Lleva marisco",
    "aditivos-animales": "Aditivo animal",
    "e120": "Lleva E120",
    "azoicos": "Colorante azoico",
    "edulcorantes": "Lleva edulcorante",
    "colorantes": "Lleva colorante",
    "conservantes": "Lleva conservante",
    "glutamato": "Lleva potenciador",
}


# ---------------------------------------------------------------------------
# Palabras en castellano que la taxonomía de Open Food Facts no trae.
#
# La taxonomía está pensada para etiquetas de producto, y en una etiqueta pone
# «harina de trigo». En una receta de aquí pone «harina», «pan rallado» o
# «chorizo», y un celíaco o un musulmán tienen que saltar igual. Para una
# alergia o una creencia, quedarse corto es el error grave: aquí se prefiere
# avisar de más y que la persona mire la etiqueta.
#
# Cada bloque cita en qué se apoya.
FUENTE_CASTELLANO = "Lista en castellano · Reglamento (UE) 1169/2011, anexo II"
FUENTE_COCINA = "Nombres de cocina en castellano"

MARCADORES_CASTELLANO = {
    # Anexo II del 1169/2011: «cereales que contengan gluten». En cocina
    # española eso es, casi siempre, harina, pan y pasta de trigo.
    "en:gluten": [
        "harina", "harinas", "pan", "pan rallado", "pan de molde", "miga de pan",
        "pasta", "macarrones", "espaguetis", "fideos", "tallarines", "lasana",
        "canelones", "semola", "cuscus", "bulgur", "galleta", "galletas",
        "bizcocho", "hojaldre", "empanada", "empanadilla", "masa quebrada",
        "rebozado", "pan tostado", "picatostes", "cerveza", "seitan",
        "levadura de cerveza", "malta", "magdalena", "magdalenas", "churros",
        "torta", "tortas", "obleas", "fideua", "salvado de trigo", "germen de trigo",
    ],
    "en:milk": [
        "requeson", "cuajada", "bechamel", "kefir", "crema de leche", "cuajo",
        "mantequilla clarificada", "manteca de vaca", "leche condensada",
        "leche evaporada", "leche entera", "leche desnatada", "queso rallado",
        "queso fresco", "queso curado", "nata liquida", "nata montada", "yogur",
    ],
    "en:eggs": [
        "huevo", "huevos", "yema", "yemas", "clara de huevo", "claras de huevo",
        "huevo duro", "huevo cocido", "mayonesa", "merengue", "tortilla francesa",
    ],
    # Carne de cerdo con los nombres del embutido español.
    "sin:cerdo": [
        "chorizo", "salchichon", "salchichas", "morcilla", "sobrasada",
        "butifarra", "fuet", "longaniza", "lomo embuchado", "salami",
        "mortadela", "manteca de cerdo", "careta", "secreto iberico",
        "presa iberica", "costilla de cerdo", "codillo", "chistorra",
        "jamon iberico", "jamon york", "bacon ahumado", "torreznos",
    ],
    "sin:alcohol": [
        "coñac", "aguardiente", "orujo", "anis", "pacharan", "cava", "moscatel",
        "vino de jerez", "vino dulce", "amaretto", "kirsch", "curacao",
        # Añadidos el 2-oct-2026 (orden de Ali: todos los alcoholes de beber).
        "vodka", "whisky", "whiskey", "bourbon", "grappa", "calvados", "mirin", "tequila",
        "mezcal", "wine", "beer", "rum", "liqueur", "vermouth", "sherry", "cider",
        "brandy de jerez", "licor de hierbas", "sangria",
    ],
    # Para quien evita todo lo animal: los nombres de cocina más habituales.
    "dieta:vegano": [
        "chorizo", "morcilla", "salchichon", "jamon", "bacon", "panceta",
        "pollo", "pavo", "conejo", "cordero", "cabrito", "buey", "cerdo",
        "chuleta", "solomillo", "costillas", "albondigas", "atun", "bacalao",
        "merluza", "sardina", "sardinas", "boquerones", "anchoas", "salmon",
        "gambas", "langostinos", "almejas", "mejillones", "calamares", "pulpo",
        "chipirones", "sepia", "caldo de carne", "caldo de pollo", "caldo de pescado",
        "manteca de cerdo", "mantequilla", "nata", "queso", "leche", "huevo",
        "huevos", "yema", "miel", "gelatina", "requeson", "yogur",
    ],
    "dieta:vegetariano": [
        "chorizo", "morcilla", "salchichon", "jamon", "bacon", "panceta",
        "pollo", "pavo", "conejo", "cordero", "cabrito", "buey", "cerdo",
        "chuleta", "solomillo", "costillas", "albondigas", "atun", "bacalao",
        "merluza", "sardina", "sardinas", "boquerones", "anchoas", "salmon",
        "gambas", "langostinos", "almejas", "mejillones", "calamares", "pulpo",
        "caldo de carne", "caldo de pollo", "caldo de pescado", "manteca de cerdo",
        "gelatina",
    ],
    "sin:carne": [
        "pollo", "pavo", "conejo", "cordero", "cabrito", "buey", "cerdo",
        "chorizo", "morcilla", "salchichon", "jamon", "bacon", "panceta",
        "chuleta", "solomillo", "costillas", "albondigas", "carne picada",
    ],
    "sin:marisco": [
        "gambas", "langostinos", "cigalas", "almejas", "mejillones", "berberechos",
        "calamares", "chipirones", "sepia", "pulpo", "navajas", "percebes",
        "bogavante", "cangrejo", "nécoras", "vieiras", "zamburinas",
    ],
    "en:fish": [
        "atun", "bacalao", "merluza", "sardina", "sardinas", "boquerones",
        "anchoas", "salmon", "lubina", "dorada", "rape", "trucha", "caballa",
        "bonito", "pescadilla", "rodaballo", "lenguado", "mero", "salmonete",
    ],
    "en:nuts": [
        "almendra", "almendras", "avellana", "avellanas", "nuez", "nueces",
        "pistacho", "pistachos", "anacardo", "anacardos", "pinones", "pipas de calabaza",
    ],
}


# Ingredientes que la etiqueta no aclara: pueden ser de origen animal o no.
# Aquí la aplicación avisa en ámbar («puede ser de origen animal») y no
# sentencia, porque una gelatina puede ser de cerdo, de ternera o de pescado.
FUENTE_DUDA = "Puede ser de origen animal según el fabricante"

MARCADORES_DE_DUDA = {
    "sin:gelatina-animal": ["gelatina", "grenetina", "gelificante"],
    "sin:cerdo": ["gelatina", "grenetina", "manteca", "grasa animal", "mono y digliceridos"],
    "dieta:vegano": [
        "gelatina", "grenetina", "cuajo", "mono y digliceridos", "e471",
        "estearato de magnesio", "glicerina", "glicerol", "aroma natural",
        "acido estearico", "acido lactico", "lecitina",
    ],
    "dieta:vegetariano": ["gelatina", "grenetina", "cuajo", "mono y digliceridos", "e471"],
    "en:milk": ["suero", "caseina", "caseinato", "lactosa"],
    "en:gluten": ["almidon", "almidon modificado", "fecula", "maltodextrina", "levadura"],
}


# ---------------------------------------------------------------------------
# El inglés.
#
# Va al lado del español y en el mismo fichero a propósito: si alguien añade
# una restricción y no le pone su inglés, la prueba de traducción lo canta.
#
# Los nombres de los catorce alérgenos son los del anexo II del Reglamento
# 1169/2011 en su versión inglesa, que es la que vale para una etiqueta
# británica o irlandesa. «Haram» y «Tref» no se traducen: son las palabras.

GRUPOS_EN = {
    "Alérgenos": "Allergens",
    "Dieta": "Diet",
    "Creencias": "Beliefs",
    "Intolerancias": "Intolerances",
    "Aditivos": "Additives",
    "Lo tuyo": "Yours",
}

AVISO_CREENCIA_EN = "We look at ingredients. Certification is the manufacturer's business."
AVISO_ALERGIA_EN = "The label on the pack is what counts."

# id -> (nombre, descripción, palabra de alarma)
EN = {
    "gluten": ("Gluten", "Wheat, rye, barley, oats and derivatives", "Contains gluten"),
    "crustaceos": ("Crustaceans", "Prawns, langoustines, crab", "Contains crustaceans"),
    "huevos": ("Egg", "", "Contains egg"),
    "pescado": ("Fish", "", "Contains fish"),
    "cacahuetes": ("Peanut", "", "Contains peanut"),
    "soja": ("Soya", "", "Contains soya"),
    "leche": ("Milk", "Includes lactose and all dairy", "Contains milk"),
    "frutos-cascara": ("Tree nuts", "Almond, hazelnut, walnut, cashew, pistachio", "Contains tree nuts"),
    "apio": ("Celery", "", "Contains celery"),
    "mostaza": ("Mustard", "", "Contains mustard"),
    "sesamo": ("Sesame", "", "Contains sesame"),
    "sulfitos": ("Sulphites", "E220 to E228. Wine, dried fruit, preserves", "Contains sulphites"),
    "altramuz": ("Lupin", "", "Contains lupin"),
    "moluscos": ("Molluscs", "Mussel, clam, squid, octopus", "Contains molluscs"),

    "vegano": ("Vegan", "Nothing of animal origin, additives included", "Not vegan"),
    "vegetariano": ("Vegetarian", "No meat, no fish. Egg and milk allowed", "Not vegetarian"),
    "ovolactovegetariano": ("Ovo-lacto vegetarian", "Same as vegetarian, with egg and dairy", "Not vegetarian"),
    "pescetariano": ("Pescatarian", "No meat. Fish and shellfish allowed", "Contains meat"),
    "sin-carne-roja": ("No red meat", "Beef, pork, lamb", "Contains red meat"),

    "halal": ("Halal (ingredients)", "No pork, alcohol, animal gelatine or insects", "HARAM"),
    "kosher": ("Kosher (ingredients)", "No pork, shellfish, animal gelatine or insects", "TREF"),
    "sin-ternera": ("No beef", "", "Contains beef"),
    "sin-ajo-cebolla": ("No garlic or onion", "", "Contains garlic or onion"),
    "sin-cerdo": ("No pork", "", "Contains pork"),
    "sin-alcohol": ("No alcohol", "", "Contains alcohol"),
    "sin-gelatina": ("No animal gelatine", "", "Contains gelatine"),

    "lactosa": ("Lactose", "Milk and dairy containing lactose", "Contains lactose"),
    "fenilcetonuria": ("Phenylalanine (PKU)", "Aspartame: E951 and E962", "Contains phenylalanine"),
    "polioles": ("Polyols", "Sorbitol, mannitol, maltitol, xylitol. Laxative effect", "Contains polyols"),
    "marisco": ("Shellfish", "Crustaceans and molluscs", "Contains shellfish"),

    "aditivos-animales": ("Additives of animal origin", "Cochineal, gelatine, shellac and the like", "Animal additive"),
    "e120": ("E120 (cochineal)", "Red colour of animal origin", "Contains e120"),
    "azoicos": ("Azo colours", "E102, E104, E110, E122, E124 and E129", "Azo colour"),
    "edulcorantes": ("Sweeteners", "Everything in the sweetener class", "Contains sweetener"),
    "colorantes": ("Colours", "Everything in the colour class", "Contains colour"),
    "conservantes": ("Preservatives", "Everything in the preservative class", "Contains preservative"),
    "glutamato": ("Glutamate and flavour enhancers", "E620 to E650", "Contains flavour enhancer"),
}


def en_de(ident, grupo, aviso):
    """El inglés de una restricción: nombre, descripción, aviso, palabra, grupo."""
    nombre, descripcion, palabra = EN.get(ident, (None, None, None))
    aviso_en = None
    if aviso == AVISO_CREENCIA:
        aviso_en = AVISO_CREENCIA_EN
    elif aviso == AVISO_ALERGIA:
        aviso_en = AVISO_ALERGIA_EN
    return nombre, (descripcion or None), aviso_en, palabra, GRUPOS_EN.get(grupo)


# La redacción EN INGLÉS es la del propio reglamento, no una traducción mía:
# es la frase que lleva impresa una etiqueta británica o irlandesa.
ADVERTENCIAS_EN = {
    "Puede tener efectos negativos sobre la actividad y la atención de los niños.":
        "May have an adverse effect on activity and attention in children.",
    "Contiene una fuente de fenilalanina.":
        "Contains a source of phenylalanine.",
    "Un consumo excesivo puede producir efectos laxantes.":
        "Excessive consumption may produce laxative effects.",
    "Los sulfitos son alérgeno de declaración obligatoria por encima de 10 mg/kg.":
        "Sulphites must be declared as an allergen above 10 mg/kg.",
}
