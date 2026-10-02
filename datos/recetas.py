# -*- coding: utf-8 -*-
"""
Recetas de la aplicación.

El texto de cada receta es propio. Los datos nutricionales NO se escriben aquí:
se calculan sumando los ingredientes con la composición de USDA FoodData Central.
Las etiquetas ("alto en proteínas", "fuente de fibra"...) tampoco se deciden a mano:
salen de aplicar los umbrales del Reglamento (CE) 1924/2006.

Las cantidades están en gramos del alimento tal y como lo describe USDA
(las legumbres, el arroz y la pasta, ya cocidos).
"""

def r(id, nombre, descripcion, raciones, minutos, ingredientes, pasos):
    return dict(id=id, nombre=nombre, descripcion=descripcion, raciones=raciones,
                minutos=minutos, ingredientes=ingredientes, pasos=pasos)

RECETAS = [
    r("lentejas-verduras", "Lentejas con verduras",
      "El guiso de toda la vida, sin chorizo.", 4, 45,
      [("lentejas", 800, "800 g de lentejas cocidas"), ("cebolla", 150, "1 cebolla"),
       ("zanahoria", 120, "2 zanahorias"), ("pimiento", 100, "1 pimiento rojo"),
       ("ajo", 10, "2 dientes de ajo"), ("tomate-triturado", 200, "200 g de tomate triturado"),
       ("aceite-oliva", 30, "2 cucharadas de aceite de oliva"), ("pimenton", 3, "1 cucharadita de pimentón"),
       ("laurel", 1, "1 hoja de laurel"), ("sal", 1.2, "sal, una pizca")],
      ["Pica la cebolla, la zanahoria, el pimiento y el ajo.",
       "Sofríelos en el aceite a fuego medio unos 10 minutos.",
       "Añade el pimentón, remueve 10 segundos y echa el tomate. Cocina 5 minutos.",
       "Incorpora las lentejas, el laurel y agua hasta cubrir. Cuece 20 minutos a fuego suave.",
       "Sala al final y retira el laurel."]),

    r("garbanzos-espinacas", "Garbanzos con espinacas",
      "Plato de cuchara de media hora.", 4, 30,
      [("garbanzos", 700, "700 g de garbanzos cocidos"), ("espinacas", 300, "300 g de espinacas"),
       ("ajo", 10, "2 dientes de ajo"), ("cebolla", 120, "1 cebolla"),
       ("tomate-triturado", 150, "150 g de tomate triturado"), ("pan", 30, "1 rebanada de pan"),
       ("aceite-oliva", 30, "2 cucharadas de aceite de oliva"), ("pimenton", 3, "1 cucharadita de pimentón"),
       ("comino", 2, "1 pizca de comino"), ("sal", 1.2, "sal, una pizca")],
      ["Fríe el pan y el ajo en el aceite y reserva.",
       "En la misma sartén, pocha la cebolla picada 8 minutos.",
       "Añade el tomate, el pimentón y el comino. Cocina 5 minutos.",
       "Echa los garbanzos y las espinacas y remueve hasta que bajen.",
       "Tritura el pan con el ajo y un poco de caldo, y añádelo para espesar."]),

    r("alubias-puerro", "Alubias blancas con puerro",
      "Suave y barata.", 4, 35,
      [("alubias-blancas", 700, "700 g de alubias blancas cocidas"), ("puerro", 200, "2 puerros"),
       ("zanahoria", 100, "1 zanahoria"), ("patata", 200, "1 patata"),
       ("aceite-oliva", 25, "2 cucharadas de aceite de oliva"), ("laurel", 1, "1 hoja de laurel"),
       ("sal", 1.2, "sal, una pizca"), ("pimienta", 1, "pimienta")],
      ["Pocha el puerro en rodajas con el aceite, 10 minutos.",
       "Añade la zanahoria y la patata en dados, el laurel y agua hasta cubrir.",
       "Cuece 15 minutos hasta que la patata esté tierna.",
       "Incorpora las alubias y cuece 5 minutos más.",
       "Salpimienta y retira el laurel."]),

    r("ensalada-garbanzos-atun", "Ensalada de garbanzos y atún",
      "Sin encender el fuego.", 2, 10,
      [("garbanzos", 300, "300 g de garbanzos cocidos"), ("atun-lata", 120, "2 latas de atún al natural"),
       ("tomate", 150, "1 tomate"), ("cebolla", 50, "1/2 cebolla"),
       ("pimiento", 80, "1/2 pimiento"), ("aceite-oliva", 20, "1 cucharada y media de aceite"),
       ("vinagre", 10, "1 cucharada de vinagre"), ("sal", 0.6, "sal, una pizca")],
      ["Escurre los garbanzos y el atún.",
       "Pica el tomate, la cebolla y el pimiento en dados pequeños.",
       "Mezcla todo con el aceite, el vinagre y la sal.",
       "Mejor si reposa 20 minutos en la nevera."]),

    r("arroz-pollo", "Arroz con pollo y verduras",
      "Una sartén y se acabó.", 4, 35,
      [("arroz-blanco", 600, "600 g de arroz cocido"), ("pollo", 400, "400 g de pechuga de pollo"),
       ("pimiento", 150, "1 pimiento"), ("guisantes", 120, "120 g de guisantes"),
       ("cebolla", 120, "1 cebolla"), ("ajo", 10, "2 dientes de ajo"),
       ("tomate-triturado", 150, "150 g de tomate triturado"),
       ("aceite-oliva", 25, "2 cucharadas de aceite de oliva"), ("pimenton", 3, "pimentón"), ("sal", 1.2, "sal, una pizca")],
      ["Dora el pollo en dados con el aceite y reserva.",
       "Pocha la cebolla, el ajo y el pimiento 10 minutos.",
       "Añade el tomate y el pimentón, cocina 5 minutos.",
       "Incorpora el arroz, los guisantes y el pollo. Remueve 3 minutos.",
       "Sala y deja reposar 5 minutos antes de servir."]),

    r("arroz-champinones", "Arroz integral con champiñones",
      "Barato y con fibra.", 4, 30,
      [("arroz-integral", 600, "600 g de arroz integral cocido"), ("champinones", 300, "300 g de champiñones"),
       ("cebolla", 120, "1 cebolla"), ("ajo", 10, "2 dientes de ajo"),
       ("aceite-oliva", 25, "2 cucharadas de aceite de oliva"), ("caldo-verduras", 200, "200 ml de caldo de verduras"),
       ("pimienta", 1, "pimienta"), ("sal", 1.2, "sal, una pizca")],
      ["Saltea los champiñones laminados a fuego fuerte hasta que suelten el agua.",
       "Añade la cebolla y el ajo picados y pocha 8 minutos.",
       "Echa el arroz y el caldo y remueve hasta que se absorba.",
       "Salpimienta."]),

    r("pasta-atun", "Pasta con tomate y atún",
      "Quince minutos de reloj.", 2, 15,
      [("pasta", 350, "350 g de pasta cocida"), ("atun-lata", 120, "2 latas de atún al natural"),
       ("tomate-triturado", 250, "250 g de tomate triturado"), ("ajo", 5, "1 diente de ajo"),
       ("aceite-oliva", 20, "1 cucharada y media de aceite"), ("oregano", 2, "orégano"), ("sal", 0.6, "sal, una pizca")],
      ["Dora el ajo picado en el aceite.",
       "Añade el tomate y el orégano y cocina 8 minutos.",
       "Incorpora el atún escurrido y remueve.",
       "Mezcla con la pasta cocida y sala."]),

    r("pasta-brocoli", "Pasta integral con brócoli y ajo",
      "Verde y rápida.", 2, 20,
      [("pasta-integral", 350, "350 g de pasta integral cocida"), ("brocoli", 300, "300 g de brócoli"),
       ("ajo", 10, "2 dientes de ajo"), ("aceite-oliva", 25, "2 cucharadas de aceite de oliva"),
       ("queso-curado", 30, "30 g de queso curado rallado"), ("sal", 0.6, "sal, una pizca"), ("pimienta", 1, "pimienta")],
      ["Cuece el brócoli en ramilletes 5 minutos.",
       "Dora el ajo laminado en el aceite sin que se queme.",
       "Añade el brócoli y aplástalo un poco con el tenedor.",
       "Mezcla con la pasta, ralla el queso por encima y salpimienta."]),

    r("espaguetis-nueces", "Espaguetis con champiñones y nueces",
      "Sin carne y con mucho sabor.", 2, 20,
      [("pasta", 350, "350 g de espaguetis cocidos"), ("champinones", 250, "250 g de champiñones"),
       ("nueces", 40, "40 g de nueces"), ("ajo", 10, "2 dientes de ajo"),
       ("aceite-oliva", 25, "2 cucharadas de aceite de oliva"), ("oregano", 2, "orégano"), ("sal", 0.6, "sal, una pizca")],
      ["Saltea los champiñones laminados a fuego fuerte.",
       "Añade el ajo picado y las nueces troceadas, 2 minutos.",
       "Mezcla con la pasta, el orégano y la sal."]),

    r("ensalada-pasta", "Ensalada de pasta fría",
      "Para llevar al trabajo.", 2, 15,
      [("pasta", 300, "300 g de pasta cocida"), ("tomate", 150, "1 tomate"),
       ("atun-lata", 60, "1 lata de atún al natural"), ("maiz-dulce", 80, "80 g de maíz"),
       ("aceitunas", 40, "40 g de aceitunas"), ("huevo", 50, "1 huevo cocido"),
       ("aceite-oliva", 20, "1 cucharada y media de aceite"), ("sal", 0.6, "sal, una pizca")],
      ["Cuece la pasta y enfríala bajo el grifo.",
       "Pica el tomate y el huevo cocido.",
       "Mezcla todo con el aceite y la sal."]),

    r("tortilla-patata", "Tortilla de patata",
      "La de siempre, con cebolla.", 4, 40,
      [("patata", 600, "600 g de patata"), ("huevo", 300, "6 huevos"),
       ("cebolla", 150, "1 cebolla"), ("aceite-oliva", 60, "aceite de oliva"), ("sal", 1.2, "sal, una pizca")],
      ["Corta la patata en láminas finas y la cebolla en juliana.",
       "Confítalas a fuego suave en el aceite unos 20 minutos. Escurre.",
       "Bate los huevos con sal y mezcla con la patata. Deja reposar 5 minutos.",
       "Cuaja en la sartén 3 minutos por cada lado."]),

    r("tortilla-calabacin", "Tortilla de calabacín",
      "Más ligera que la de patata.", 2, 20,
      [("calabacin", 400, "2 calabacines"), ("huevo", 200, "4 huevos"),
       ("cebolla", 80, "media cebolla"), ("aceite-oliva", 20, "1 cucharada y media de aceite"), ("sal", 0.6, "sal, una pizca")],
      ["Ralla o corta fino el calabacín y pocha con la cebolla 10 minutos.",
       "Bate los huevos con sal y mezcla.",
       "Cuaja 3 minutos por cada lado."]),

    r("huevos-tomate", "Huevos al plato con tomate",
      "Cena de emergencia.", 2, 20,
      [("huevo", 200, "4 huevos"), ("tomate-triturado", 300, "300 g de tomate triturado"),
       ("cebolla", 100, "1 cebolla"), ("ajo", 5, "1 diente de ajo"),
       ("aceite-oliva", 20, "1 cucharada y media de aceite"), ("pimenton", 2, "pimentón"),
       ("pan", 60, "2 rebanadas de pan"), ("sal", 0.6, "sal, una pizca")],
      ["Pocha la cebolla y el ajo 8 minutos.",
       "Añade el tomate y el pimentón, cocina 8 minutos.",
       "Haz cuatro huecos y casca un huevo en cada uno.",
       "Tapa y cocina 5 minutos, hasta que cuaje la clara. Sirve con pan."]),

    r("revuelto-gambas", "Revuelto de espinacas y gambas",
      "Diez minutos y mucha proteína.", 2, 10,
      [("huevo", 200, "4 huevos"), ("espinacas", 200, "200 g de espinacas"),
       ("gambas", 150, "150 g de gambas peladas"), ("ajo", 5, "1 diente de ajo"),
       ("aceite-oliva", 15, "1 cucharada de aceite"), ("sal", 0.6, "sal, una pizca")],
      ["Saltea el ajo y las gambas 2 minutos.",
       "Añade las espinacas hasta que bajen.",
       "Echa los huevos batidos y remueve a fuego suave hasta cuajar. Sala."]),

    r("pollo-horno", "Pollo al horno con patata y zanahoria",
      "Se hace solo.", 4, 55,
      [("pollo", 600, "600 g de pechuga de pollo"), ("patata", 600, "600 g de patata"),
       ("zanahoria", 200, "2 zanahorias"), ("cebolla", 150, "1 cebolla"),
       ("aceite-oliva", 30, "2 cucharadas de aceite de oliva"), ("oregano", 2, "orégano"),
       ("sal", 1.2, "sal, una pizca"), ("pimienta", 1, "pimienta")],
      ["Corta la patata en rodajas y la zanahoria y la cebolla en tiras.",
       "Ponlo todo en la bandeja con el aceite, el orégano, sal y pimienta.",
       "Hornea a 200 grados 25 minutos.",
       "Añade el pollo encima y hornea 20 minutos más."]),

    r("pechuga-ensalada", "Pechuga a la plancha con ensalada",
      "Lo más simple que hay.", 2, 15,
      [("pollo", 300, "300 g de pechuga de pollo"), ("lechuga", 150, "150 g de lechuga"),
       ("tomate", 150, "1 tomate"), ("cebolla", 40, "1/4 de cebolla"),
       ("aceite-oliva", 20, "1 cucharada y media de aceite"), ("vinagre", 10, "vinagre"), ("sal", 0.6, "sal, una pizca")],
      ["Salpimienta la pechuga y hazla a la plancha 4 minutos por lado.",
       "Aliña la lechuga, el tomate y la cebolla con aceite, vinagre y sal.",
       "Sirve la pechuga en tiras sobre la ensalada."]),

    r("pavo-arroz-brocoli", "Pavo con arroz y brócoli",
      "El clásico del gimnasio, pero comestible.", 2, 25,
      [("pavo", 300, "300 g de pechuga de pavo"), ("arroz-integral", 400, "400 g de arroz integral cocido"),
       ("brocoli", 250, "250 g de brócoli"), ("ajo", 5, "1 diente de ajo"),
       ("aceite-oliva", 20, "1 cucharada y media de aceite"), ("pimienta", 1, "pimienta"), ("sal", 0.6, "sal, una pizca")],
      ["Cuece el brócoli 5 minutos.",
       "Haz el pavo en tiras a la plancha con el ajo.",
       "Sirve con el arroz, salpimienta y riega con el aceite."]),

    r("bacalao-horno", "Bacalao al horno con patata",
      "Pescado sin complicaciones.", 2, 35,
      [("bacalao", 350, "350 g de bacalao"), ("patata", 400, "400 g de patata"),
       ("cebolla", 120, "1 cebolla"), ("limon", 30, "medio limón"),
       ("aceite-oliva", 25, "2 cucharadas de aceite de oliva"), ("sal", 0.6, "sal, una pizca"), ("pimienta", 1, "pimienta")],
      ["Corta la patata en rodajas finas y la cebolla en juliana.",
       "Hornea con aceite y sal a 200 grados 20 minutos.",
       "Coloca la merluza encima con limón y hornea 12 minutos más."]),

    r("salmon-brocoli", "Salmón al horno con brócoli",
      "Grasa buena y mucha proteína.", 2, 25,
      [("salmon", 300, "300 g de salmón"), ("brocoli", 300, "300 g de brócoli"),
       ("limon", 30, "medio limón"), ("aceite-oliva", 20, "1 cucharada y media de aceite"),
       ("ajo", 5, "1 diente de ajo"), ("sal", 0.6, "sal, una pizca")],
      ["Pon el brócoli en la bandeja con aceite, ajo y sal.",
       "Hornea a 200 grados 10 minutos.",
       "Añade el salmón con limón y hornea 12 minutos más."]),

    r("sardinas-tomate", "Sardinas con tomate y pan",
      "Barata y llena de omega 3.", 2, 10,
      [("sardinas", 150, "2 latas de sardinas"), ("tomate", 200, "2 tomates"),
       ("pan-integral", 120, "4 rebanadas de pan integral"), ("ajo", 5, "1 diente de ajo"),
       ("aceite-oliva", 15, "1 cucharada de aceite"), ("sal", 0.6, "sal, una pizca")],
      ["Tuesta el pan y frótalo con el ajo.",
       "Ralla el tomate por encima y riega con aceite y sal.",
       "Coloca las sardinas escurridas encima."]),

    r("mejillones-vapor", "Mejillones al vapor con limón",
      "Dos ingredientes y listo.", 2, 15,
      [("mejillones", 150, "500 g de mejillones con concha (unos 150 g de carne)"), ("limon", 50, "1 limón"),
       ("laurel", 1, "1 hoja de laurel"), ("aceite-oliva", 10, "un chorro de aceite")],
      ["Limpia los mejillones.",
       "Ponlos en una cazuela con un dedo de agua y el laurel.",
       "Tapa y cuece 5 minutos, hasta que se abran.",
       "Descarta los que no se hayan abierto. Sirve con limón."]),

    r("atun-judias", "Atún con judías verdes y patata",
      "Plato único de verdad.", 2, 25,
      [("atun-lata", 120, "2 latas de atún al natural"), ("judias-verdes", 300, "300 g de judías verdes"),
       ("patata", 300, "300 g de patata"), ("cebolla", 60, "media cebolla"),
       ("aceite-oliva", 20, "1 cucharada y media de aceite"), ("vinagre", 10, "vinagre"), ("sal", 0.6, "sal, una pizca")],
      ["Cuece las judías y la patata en dados 15 minutos.",
       "Escurre y deja templar.",
       "Mezcla con el atún, la cebolla picada, aceite, vinagre y sal."]),

    r("crema-calabaza", "Crema de calabaza",
      "Poco de todo menos sabor.", 4, 30,
      [("calabaza", 700, "700 g de calabaza"), ("patata", 200, "1 patata"),
       ("puerro", 150, "1 puerro"), ("zanahoria", 100, "1 zanahoria"),
       ("aceite-oliva", 20, "1 cucharada y media de aceite"), ("caldo-verduras", 400, "400 ml de caldo"),
       ("sal", 1.2, "sal, una pizca"), ("pimienta", 1, "pimienta")],
      ["Pocha el puerro en el aceite 8 minutos.",
       "Añade la calabaza, la patata y la zanahoria en dados y el caldo.",
       "Cuece 20 minutos y tritura.",
       "Salpimienta."]),

    r("crema-calabacin", "Crema de calabacín",
      "Ligera y en media hora.", 4, 25,
      [("calabacin", 700, "700 g de calabacín"), ("patata", 150, "1 patata pequeña"),
       ("cebolla", 120, "1 cebolla"), ("caldo-verduras", 400, "400 ml de caldo"),
       ("aceite-oliva", 20, "1 cucharada y media de aceite"), ("sal", 1.2, "sal, una pizca")],
      ["Pocha la cebolla 8 minutos.",
       "Añade el calabacín y la patata en dados y el caldo.",
       "Cuece 15 minutos y tritura. Sala."]),

    r("sopa-verduras", "Sopa de verduras con fideos",
      "Reconfortante y barata.", 4, 35,
      [("pasta", 200, "200 g de fideos cocidos"), ("zanahoria", 150, "2 zanahorias"),
       ("puerro", 150, "1 puerro"), ("apio", 80, "1 rama de apio"),
       ("patata", 200, "1 patata"), ("col", 150, "150 g de col"),
       ("caldo-verduras", 800, "800 ml de caldo de verduras"), ("aceite-oliva", 15, "1 cucharada de aceite"), ("sal", 1.2, "sal, una pizca")],
      ["Pica todas las verduras en dados pequeños.",
       "Rehógalas en el aceite 5 minutos.",
       "Añade el caldo y cuece 20 minutos.",
       "Echa los fideos los últimos minutos y sala."]),

    r("gazpacho", "Gazpacho",
      "Verdura cruda que apetece.", 4, 15,
      [("tomate", 800, "800 g de tomate maduro"), ("pepino", 150, "medio pepino"),
       ("pimiento", 100, "1 pimiento verde"), ("ajo", 5, "1 diente de ajo"),
       ("pan", 50, "50 g de pan del día anterior"), ("aceite-oliva", 40, "3 cucharadas de aceite"),
       ("vinagre", 15, "1 cucharada de vinagre"), ("sal", 1.2, "sal, una pizca")],
      ["Trocea el tomate, el pepino y el pimiento.",
       "Tritúralo todo con el ajo, el pan, el aceite, el vinagre y la sal.",
       "Cuela si lo quieres fino y enfría dos horas."]),

    r("pisto", "Pisto",
      "Verduras que saben a algo.", 4, 45,
      [("calabacin", 300, "1 calabacín"), ("berenjena", 250, "1 berenjena"),
       ("pimiento", 200, "2 pimientos"), ("cebolla", 150, "1 cebolla"),
       ("tomate-triturado", 400, "400 g de tomate triturado"),
       ("aceite-oliva", 40, "3 cucharadas de aceite"), ("sal", 1.2, "sal, una pizca")],
      ["Pica todas las verduras en dados del mismo tamaño.",
       "Pocha la cebolla y el pimiento 10 minutos.",
       "Añade el calabacín y la berenjena, 10 minutos más.",
       "Echa el tomate y cocina a fuego suave 20 minutos. Sala."]),

    r("ensalada-lentejas", "Ensalada de lentejas",
      "Legumbre en verano.", 2, 10,
      [("lentejas", 350, "350 g de lentejas cocidas"), ("tomate", 150, "1 tomate"),
       ("pimiento", 80, "medio pimiento"), ("cebolla", 50, "media cebolla"),
       ("aceitunas", 30, "30 g de aceitunas"), ("aceite-oliva", 20, "1 cucharada y media de aceite"),
       ("vinagre", 10, "vinagre"), ("sal", 0.6, "sal, una pizca")],
      ["Escurre bien las lentejas.",
       "Pica la verdura en dados pequeños.",
       "Mezcla con el aceite, el vinagre y la sal."]),

    r("yogur-avena-fruta", "Yogur con avena, fruta y nueces",
      "Sin cocinar nada.", 1, 5,
      [("yogur-griego", 200, "200 g de yogur griego natural"), ("avena", 40, "40 g de copos de avena"),
       ("fresas", 100, "100 g de fresas"), ("nueces", 20, "20 g de nueces"), ("miel", 10, "1 cucharadita de miel")],
      ["Mezcla el yogur con la avena.",
       "Añade las fresas troceadas, las nueces y la miel."]),

    r("tostada-tomate-jamon", "Tostada de tomate y jamón",
      "El desayuno de siempre.", 1, 5,
      [("pan", 60, "2 rebanadas de pan"), ("tomate", 100, "1 tomate"),
       ("jamon", 40, "40 g de jamón en lonchas"), ("aceite-oliva", 10, "un chorro de aceite"), ("sal", 0.3, "sal, una pizca")],
      ["Tuesta el pan.",
       "Ralla el tomate, extiéndelo y riega con aceite y sal.",
       "Coloca el jamón encima."]),

    r("requeson-fruta", "Requesón con fruta y miel",
      "Postre con proteína.", 1, 5,
      [("requeson", 200, "200 g de requesón"), ("pera", 150, "1 pera"),
       ("almendras", 20, "20 g de almendras"), ("miel", 10, "1 cucharadita de miel")],
      ["Pon el requesón en un bol.",
       "Añade la pera en dados, las almendras y la miel."]),

    r("ensalada-mixta", "Ensalada mixta",
      "La base de todo.", 2, 10,
      [("lechuga", 200, "200 g de lechuga"), ("tomate", 200, "2 tomates"),
       ("cebolla", 50, "media cebolla"), ("aceitunas", 40, "40 g de aceitunas"),
       ("atun-lata", 60, "1 lata de atún al natural"), ("huevo", 50, "1 huevo cocido"),
       ("aceite-oliva", 20, "1 cucharada y media de aceite"), ("vinagre", 10, "vinagre"), ("sal", 0.6, "sal, una pizca")],
      ["Lava y trocea la lechuga.",
       "Añade el tomate, la cebolla, las aceitunas, el atún y el huevo.",
       "Aliña con aceite, vinagre y sal."]),

    r("crema-champinones", "Crema de champiñones",
      "Sabe a más de lo que cuesta.", 4, 30,
      [("champinones", 500, "500 g de champiñones"), ("patata", 200, "1 patata"),
       ("cebolla", 120, "1 cebolla"), ("ajo", 5, "1 diente de ajo"),
       ("caldo-verduras", 500, "500 ml de caldo"), ("leche-desnatada", 150, "150 ml de leche"),
       ("aceite-oliva", 20, "1 cucharada y media de aceite"), ("sal", 1.2, "sal, una pizca"), ("pimienta", 1, "pimienta")],
      ["Saltea los champiñones a fuego fuerte y reserva unos pocos.",
       "Pocha la cebolla y el ajo, añade la patata y el caldo.",
       "Cuece 20 minutos, añade la leche y tritura.",
       "Salpimienta y sirve con los champiñones reservados."]),

    r("lentejas-arroz", "Lentejas con arroz",
      "Proteína completa por poco dinero.", 4, 30,
      [("lentejas", 600, "600 g de lentejas cocidas"), ("arroz-blanco", 400, "400 g de arroz cocido"),
       ("cebolla", 150, "1 cebolla"), ("ajo", 10, "2 dientes de ajo"),
       ("comino", 3, "comino"), ("aceite-oliva", 25, "2 cucharadas de aceite"), ("sal", 1.2, "sal, una pizca")],
      ["Dora la cebolla en juliana hasta que esté muy tostada.",
       "Añade el ajo y el comino.",
       "Mezcla con las lentejas y el arroz y calienta 5 minutos. Sala."]),

    r("berenjena-horno", "Berenjenas al horno con tomate y queso",
      "Vegetariano que llena.", 2, 40,
      [("berenjena", 500, "2 berenjenas"), ("tomate-triturado", 300, "300 g de tomate triturado"),
       ("mozzarella", 120, "120 g de mozzarella"), ("cebolla", 100, "1 cebolla"),
       ("ajo", 5, "1 diente de ajo"), ("oregano", 2, "orégano"),
       ("aceite-oliva", 25, "2 cucharadas de aceite"), ("sal", 0.6, "sal, una pizca")],
      ["Corta la berenjena en rodajas, sala y hornea 15 minutos a 200 grados.",
       "Haz una salsa con la cebolla, el ajo, el tomate y el orégano.",
       "Alterna capas de berenjena y salsa, cubre con la mozzarella.",
       "Hornea 15 minutos más."]),

    r("patatas-pollo-guiso", "Guiso de patata con pollo",
      "Cuchara de domingo.", 4, 45,
      [("patata", 700, "700 g de patata"), ("pollo", 400, "400 g de pollo"),
       ("cebolla", 150, "1 cebolla"), ("zanahoria", 150, "2 zanahorias"),
       ("pimiento", 100, "1 pimiento"), ("ajo", 10, "2 dientes de ajo"),
       ("pimenton", 4, "1 cucharadita de pimentón"), ("laurel", 1, "laurel"),
       ("aceite-oliva", 30, "2 cucharadas de aceite"), ("sal", 1.2, "sal, una pizca")],
      ["Dora el pollo en trozos y reserva.",
       "Pocha la cebolla, el ajo, la zanahoria y el pimiento 10 minutos.",
       "Añade el pimentón y las patatas cascadas.",
       "Cubre con agua, añade el laurel y el pollo y cuece 25 minutos. Sala."]),
]


# ---------------------------------------------------------------------------
# LAS MISMAS RECETAS EN INGLÉS
#
# Escritas, no traducidas a máquina: son las mismas cantidades y los mismos
# pasos, contados como los contaría alguien en una cocina inglesa. Las medidas
# se dejan en gramos y mililitros, que es lo que pone una balanza.
#
# id -> (nombre, descripción)
NOMBRES_EN = {
    "lentejas-verduras": ("Lentils with vegetables", "The everyday stew, without chorizo."),
    "garbanzos-espinacas": ("Chickpeas with spinach", "A half-hour bowl of comfort."),
    "alubias-puerro": ("White beans with leek", "Mild and cheap."),
    "ensalada-garbanzos-atun": ("Chickpea and tuna salad", "No cooking at all."),
    "arroz-pollo": ("Rice with chicken and vegetables", "One pan and you're done."),
    "arroz-champinones": ("Brown rice with mushrooms", "Cheap and full of fibre."),
    "pasta-atun": ("Pasta with tomato and tuna", "Fifteen minutes flat."),
    "pasta-brocoli": ("Wholewheat pasta with broccoli and garlic", "Green and quick."),
    "espaguetis-nueces": ("Spaghetti with mushrooms and walnuts", "No meat and plenty of flavour."),
    "ensalada-pasta": ("Cold pasta salad", "To take to work."),
    "tortilla-patata": ("Spanish potato omelette", "The usual one, with onion."),
    "tortilla-calabacin": ("Courgette omelette", "Lighter than the potato one."),
    "huevos-tomate": ("Baked eggs with tomato", "Emergency dinner."),
    "revuelto-gambas": ("Scrambled eggs with spinach and prawns", "Ten minutes and a lot of protein."),
    "pollo-horno": ("Roast chicken with potato and carrot", "It cooks itself."),
    "pechuga-ensalada": ("Griddled chicken breast with salad", "The simplest thing there is."),
    "pavo-arroz-brocoli": ("Turkey with rice and broccoli", "The gym classic, but edible."),
    "bacalao-horno": ("Baked cod with potato", "Fish without any fuss."),
    "salmon-brocoli": ("Baked salmon with broccoli", "Good fat and plenty of protein."),
    "sardinas-tomate": ("Sardines with tomato and bread", "Cheap and full of omega 3."),
    "mejillones-vapor": ("Steamed mussels with lemon", "Two ingredients and that's it."),
    "atun-judias": ("Tuna with green beans and potato", "A proper one-plate meal."),
    "crema-calabaza": ("Pumpkin soup", "Not much of anything except flavour."),
    "crema-calabacin": ("Courgette soup", "Light, and ready in half an hour."),
    "sopa-verduras": ("Vegetable soup with noodles", "Comforting and cheap."),
    "gazpacho": ("Gazpacho", "Raw vegetables you actually want."),
    "pisto": ("Pisto", "Vegetables that taste of something."),
    "ensalada-lentejas": ("Lentil salad", "Pulses in summer."),
    "yogur-avena-fruta": ("Yoghurt with oats, fruit and walnuts", "Nothing to cook."),
    "tostada-tomate-jamon": ("Tomato and ham on toast", "The usual breakfast."),
    "requeson-fruta": ("Ricotta with fruit and honey", "Pudding with protein."),
    "ensalada-mixta": ("Mixed salad", "The base of everything."),
    "crema-champinones": ("Mushroom soup", "Tastes like more than it costs."),
    "lentejas-arroz": ("Lentils with rice", "Complete protein for very little money."),
    "berenjena-horno": ("Baked aubergine with tomato and cheese", "Vegetarian and filling."),
    "patatas-pollo-guiso": ("Potato and chicken stew", "Sunday comfort food."),
}


# Lo que se cuenta por piezas, no por peso: (gramos por pieza, singular, plural).
# Los gramos son los mismos que usa la receta española, así que las dos
# versiones dicen exactamente la misma cantidad.
POR_UNIDAD = {
    "huevo": (50, "egg", "eggs"),
    "cebolla": (150, "onion", "onions"),
    "ajo": (5, "garlic clove", "garlic cloves"),
    "zanahoria": (60, "carrot", "carrots"),
    "pimiento": (100, "pepper", "peppers"),
    "calabacin": (200, "courgette", "courgettes"),
    "berenjena": (250, "aubergine", "aubergines"),
    "patata": (150, "potato", "potatoes"),
    "tomate": (120, "tomato", "tomatoes"),
    "puerro": (100, "leek", "leeks"),
    "manzana": (150, "apple", "apples"),
    "platano": (120, "banana", "bananas"),
    "naranja": (180, "orange", "oranges"),
    "limon": (100, "lemon", "lemons"),
    "pera": (160, "pear", "pears"),
    "aguacate": (150, "avocado", "avocados"),
    "pepino": (200, "cucumber", "cucumbers"),
}


def linea_en(ingrediente_id, gramos, texto_es):
    """
    La línea de un ingrediente en inglés.

    No se traduce la frase española: se vuelve a escribir desde los datos, que
    son los que mandan (el gramaje es lo que usa la aplicación para calcular la
    nutrición y el coste). Así no hay forma de que la versión inglesa diga una
    cantidad distinta de la española.
    """
    from ingredientes import EN as INGREDIENTES_EN
    nombre = INGREDIENTES_EN.get(ingrediente_id, ingrediente_id.replace("-", " "))
    nombre = nombre[0].lower() + nombre[1:]

    # Condimentos en cantidad pequeña: nadie pesa 1,2 g de sal.
    CONDIMENTOS = {"sal", "pimienta", "pimenton", "comino", "oregano", "laurel"}
    if ingrediente_id in CONDIMENTOS and gramos <= 5:
        if ingrediente_id == "laurel":
            return "1 bay leaf" if gramos <= 1.5 else "2 bay leaves"
        return f"{nombre}, a pinch"

    if gramos is None:
        return nombre

    # Lo que se cuenta, se cuenta: «6 eggs», no «300 g egg».
    unidad = POR_UNIDAD.get(ingrediente_id)
    if unidad:
        peso, singular, plural = unidad
        piezas = gramos / peso
        if abs(piezas - round(piezas)) < 0.01 and 1 <= round(piezas) <= 12:
            n = round(piezas)
            return f"1 {singular}" if n == 1 else f"{n} {plural}"

    if float(gramos).is_integer():
        return f"{int(gramos)} g {nombre}"
    return f"{gramos:g} g {nombre}"


# Los pasos, escritos en inglés de cocina. Mismos tiempos y mismas temperaturas.
PASOS_EN = {
"lentejas-verduras": [
 "Chop the onion, carrot, pepper and garlic.",
 "Soften them in the oil over a medium heat for about 10 minutes.",
 "Add the paprika, stir for 10 seconds and tip in the tomato. Cook for 5 minutes.",
 "Add the lentils, the bay leaf and water to cover. Simmer gently for 20 minutes.",
 "Salt at the end and take out the bay leaf.",
],
"garbanzos-espinacas": [
 "Fry the bread and the garlic in the oil and set aside.",
 "In the same pan, soften the chopped onion for 8 minutes.",
 "Add the tomato, the paprika and the cumin. Cook for 5 minutes.",
 "Tip in the chickpeas and the spinach and stir until the leaves wilt.",
 "Blend the bread with the garlic and a little stock, and stir it in to thicken.",
],
"alubias-puerro": [
 "Soften the sliced leek in the oil for 10 minutes.",
 "Add the diced carrot and potato, the bay leaf and water to cover.",
 "Simmer for 15 minutes, until the potato is tender.",
 "Add the beans and cook for 5 minutes more.",
 "Season and take out the bay leaf.",
],
"ensalada-garbanzos-atun": [
 "Drain the chickpeas and the tuna.",
 "Dice the tomato, the onion and the pepper small.",
 "Mix everything with the oil, the vinegar and the salt.",
 "Better if it rests 20 minutes in the fridge.",
],
"arroz-pollo": [
 "Brown the diced chicken in the oil and set aside.",
 "Soften the onion, garlic and pepper for 10 minutes.",
 "Add the tomato and the paprika, cook for 5 minutes.",
 "Stir in the rice, the peas and the chicken. Stir for 3 minutes.",
 "Salt and let it rest 5 minutes before serving.",
],
"arroz-champinones": [
 "Fry the sliced mushrooms over a high heat until they give up their water.",
 "Add the chopped onion and garlic and soften for 8 minutes.",
 "Tip in the rice and the stock and stir until it is absorbed.",
 "Season.",
],
"pasta-atun": [
 "Brown the chopped garlic in the oil.",
 "Add the tomato and the oregano and cook for 8 minutes.",
 "Stir in the drained tuna.",
 "Mix with the cooked pasta and salt.",
],
"pasta-brocoli": [
 "Boil the broccoli florets for 5 minutes.",
 "Brown the sliced garlic in the oil without letting it burn.",
 "Add the broccoli and crush it a little with a fork.",
 "Mix with the pasta, grate the cheese over the top and season.",
],
"espaguetis-nueces": [
 "Fry the sliced mushrooms over a high heat.",
 "Add the chopped garlic and the broken walnuts, 2 minutes.",
 "Mix with the pasta, the oregano and the salt.",
],
"ensalada-pasta": [
 "Cook the pasta and cool it under the tap.",
 "Chop the tomato and the boiled egg.",
 "Mix everything with the oil and the salt.",
],
"tortilla-patata": [
 "Cut the potato into thin slices and the onion into strips.",
 "Cook them gently in the oil for about 20 minutes. Drain.",
 "Beat the eggs with salt and mix with the potato. Let it stand 5 minutes.",
 "Set it in the pan, 3 minutes on each side.",
],
"tortilla-calabacin": [
 "Grate or finely slice the courgette and soften it with the onion for 10 minutes.",
 "Beat the eggs with salt and mix.",
 "Set it in the pan, 3 minutes on each side.",
],
"huevos-tomate": [
 "Soften the onion and the garlic for 8 minutes.",
 "Add the tomato and the paprika, cook for 8 minutes.",
 "Make four hollows and crack an egg into each one.",
 "Cover and cook for 5 minutes, until the white sets. Serve with bread.",
],
"revuelto-gambas": [
 "Fry the garlic and the prawns for 2 minutes.",
 "Add the spinach until it wilts.",
 "Pour in the beaten eggs and stir over a low heat until they set. Salt.",
],
"pollo-horno": [
 "Slice the potato and cut the carrot and onion into strips.",
 "Put it all in the tin with the oil, the oregano, salt and pepper.",
 "Roast at 200 degrees for 25 minutes.",
 "Lay the chicken on top and roast for 20 minutes more.",
],
"pechuga-ensalada": [
 "Season the chicken breast and griddle it 4 minutes a side.",
 "Dress the lettuce, tomato and onion with oil, vinegar and salt.",
 "Serve the breast in strips over the salad.",
],
"pavo-arroz-brocoli": [
 "Boil the broccoli for 5 minutes.",
 "Griddle the turkey in strips with the garlic.",
 "Serve with the rice, season and pour the oil over.",
],
"bacalao-horno": [
 "Cut the potato into thin slices and the onion into strips.",
 "Roast with oil and salt at 200 degrees for 20 minutes.",
 "Lay the cod on top with lemon and roast for 12 minutes more.",
],
"salmon-brocoli": [
 "Put the broccoli in the tin with oil, garlic and salt.",
 "Roast at 200 degrees for 10 minutes.",
 "Add the salmon with lemon and roast for 12 minutes more.",
],
"sardinas-tomate": [
 "Toast the bread and rub it with the garlic.",
 "Grate the tomato over it and pour on oil and salt.",
 "Lay the drained sardines on top.",
],
"mejillones-vapor": [
 "Clean the mussels.",
 "Put them in a pan with a finger of water and the bay leaf.",
 "Cover and cook for 5 minutes, until they open.",
 "Throw away any that have not opened. Serve with lemon.",
],
"atun-judias": [
 "Boil the beans and the diced potato for 15 minutes.",
 "Drain and let them cool a little.",
 "Mix with the tuna, the chopped onion, oil, vinegar and salt.",
],
"crema-calabaza": [
 "Soften the leek in the oil for 8 minutes.",
 "Add the diced pumpkin, potato and carrot, and the stock.",
 "Simmer for 20 minutes and blend.",
 "Season.",
],
"crema-calabacin": [
 "Soften the onion for 8 minutes.",
 "Add the diced courgette and potato, and the stock.",
 "Simmer for 15 minutes and blend. Salt.",
],
"sopa-verduras": [
 "Dice all the vegetables small.",
 "Soften them in the oil for 5 minutes.",
 "Add the stock and simmer for 20 minutes.",
 "Drop in the noodles for the last few minutes and salt.",
],
"gazpacho": [
 "Roughly chop the tomato, the cucumber and the pepper.",
 "Blend it all with the garlic, the bread, the oil, the vinegar and the salt.",
 "Sieve it if you want it smooth and chill for two hours.",
],
"pisto": [
 "Dice all the vegetables to the same size.",
 "Soften the onion and the pepper for 10 minutes.",
 "Add the courgette and the aubergine, 10 minutes more.",
 "Tip in the tomato and cook gently for 20 minutes. Salt.",
],
"ensalada-lentejas": [
 "Drain the lentils well.",
 "Dice the vegetables small.",
 "Mix with the oil, the vinegar and the salt.",
],
"yogur-avena-fruta": [
 "Mix the yoghurt with the oats.",
 "Add the chopped strawberries, the walnuts and the honey.",
],
"tostada-tomate-jamon": [
 "Toast the bread.",
 "Grate the tomato, spread it and pour on oil and salt.",
 "Lay the ham on top.",
],
"requeson-fruta": [
 "Put the ricotta in a bowl.",
 "Add the diced pear, the almonds and the honey.",
],
"ensalada-mixta": [
 "Wash and tear the lettuce.",
 "Add the tomato, the onion, the olives, the tuna and the egg.",
 "Dress with oil, vinegar and salt.",
],
"crema-champinones": [
 "Fry the mushrooms over a high heat and keep a few back.",
 "Soften the onion and the garlic, add the potato and the stock.",
 "Simmer for 20 minutes, add the milk and blend.",
 "Season and serve with the mushrooms you kept back.",
],
"lentejas-arroz": [
 "Brown the sliced onion until it is very well caramelised.",
 "Add the garlic and the cumin.",
 "Mix with the lentils and the rice and heat through for 5 minutes. Salt.",
],
"berenjena-horno": [
 "Slice the aubergine, salt it and roast for 15 minutes at 200 degrees.",
 "Make a sauce with the onion, garlic, tomato and oregano.",
 "Layer aubergine and sauce alternately, cover with the mozzarella.",
 "Roast for 15 minutes more.",
],
"patatas-pollo-guiso": [
 "Brown the chicken pieces and set aside.",
 "Soften the onion, garlic, carrot and pepper for 10 minutes.",
 "Add the paprika and the cracked potatoes.",
 "Cover with water, add the bay leaf and the chicken and simmer for 25 minutes. Salt.",
],
}
