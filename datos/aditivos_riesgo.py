#!/usr/bin/env python3
"""
Qué tan señalado está cada aditivo, por quién, y qué provoca.

Esto NO es una opinión nuestra ni una nota de un blog. Cada entrada es un
pronunciamiento de un organismo con nombre y fecha: la EFSA (la agencia
europea), el IARC (la agencia del cáncer de la OMS) o el propio reglamento
europeo. El texto dice lo que dijeron, no lo que nos parece.

El número de 0 a 100 tampoco se inventa: sale de una escala fija según QUIÉN lo
ha señalado y por qué. La escala está aquí a la vista y es la misma para todos:

    100  prohibido en la Unión Europea
     90  el IARC lo clasifica como cancerígeno para las personas (grupo 1)
     75  el IARC lo clasifica como probablemente cancerígeno (grupo 2A)
     70  la ley obliga a avisar en la etiqueta
     60  el IARC lo clasifica como posiblemente cancerígeno (grupo 2B)
     45  la EFSA le ha puesto o rebajado el límite diario, o pidió más datos
     40  es alérgeno de declaración obligatoria
      5  autorizado en la UE y sin señalar por nadie

Los que no están en esta lista se quedan en 5: autorizados y sin señalamientos.
La aplicación lo dice así, sin adornos.
"""

# La escala, en un solo sitio.
ESCALA = {
    "prohibido": 100,
    "iarc1": 90,
    "iarc2a": 75,
    "aviso_ley": 70,
    "iarc2b": 60,
    "efsa_limite": 45,
    "alergeno": 40,
}
TOXICIDAD_POR_DEFECTO = 5
EFECTO_POR_DEFECTO = "Ningún organismo lo ha señalado."

# id -> (nivel, motivo de la escala, qué provoca, qué le pasa, quién lo dice, enlace)
RIESGO = {
    # --- Prohibido en la UE -------------------------------------------------
    "e171": (
        "alto", "prohibido", "La EFSA no descartó daño en el material genético.",
        "Prohibido en la Unión Europea desde 2022: la EFSA no pudo descartar que "
        "dañe el material genético.",
        "Reglamento (UE) 2022/63 · EFSA 2021",
        "https://eur-lex.europa.eu/eli/reg/2022/63/oj",
    ),

    # --- Advertencia obligatoria por ley (los seis colorantes de Southampton) -
    "e102": ("alto", "aviso_ley", "Puede afectar a la actividad y la atención de los niños.", "La etiqueta tiene que avisar por ley: puede afectar a la actividad y la atención de los niños.", "Reglamento (CE) 1333/2008, anexo V", "https://eur-lex.europa.eu/eli/reg/2008/1333/oj"),
    "e104": ("alto", "aviso_ley", "Puede afectar a la actividad y la atención de los niños.", "La etiqueta tiene que avisar por ley: puede afectar a la actividad y la atención de los niños.", "Reglamento (CE) 1333/2008, anexo V", "https://eur-lex.europa.eu/eli/reg/2008/1333/oj"),
    "e110": ("alto", "aviso_ley", "Puede afectar a la actividad y la atención de los niños.", "La etiqueta tiene que avisar por ley: puede afectar a la actividad y la atención de los niños.", "Reglamento (CE) 1333/2008, anexo V", "https://eur-lex.europa.eu/eli/reg/2008/1333/oj"),
    "e122": ("alto", "aviso_ley", "Puede afectar a la actividad y la atención de los niños.", "La etiqueta tiene que avisar por ley: puede afectar a la actividad y la atención de los niños.", "Reglamento (CE) 1333/2008, anexo V", "https://eur-lex.europa.eu/eli/reg/2008/1333/oj"),
    "e124": ("alto", "aviso_ley", "Puede afectar a la actividad y la atención de los niños.", "La etiqueta tiene que avisar por ley: puede afectar a la actividad y la atención de los niños.", "Reglamento (CE) 1333/2008, anexo V", "https://eur-lex.europa.eu/eli/reg/2008/1333/oj"),
    "e129": ("alto", "aviso_ley", "Puede afectar a la actividad y la atención de los niños.", "La etiqueta tiene que avisar por ley: puede afectar a la actividad y la atención de los niños.", "Reglamento (CE) 1333/2008, anexo V", "https://eur-lex.europa.eu/eli/reg/2008/1333/oj"),

    # --- Nitritos y nitratos (carnes curadas) -------------------------------
    "e249": ("alto", "iarc1", "En la carne curada puede formar nitrosaminas.", "En la carne curada puede formar nitrosaminas. El IARC clasifica la carne procesada como cancerígena para las personas (grupo 1).", "IARC, monografía 114 (2018) · EFSA 2017", "https://publications.iarc.fr/564"),
    "e250": ("alto", "iarc1", "En la carne curada puede formar nitrosaminas.", "En la carne curada puede formar nitrosaminas. El IARC clasifica la carne procesada como cancerígena para las personas (grupo 1).", "IARC, monografía 114 (2018) · EFSA 2017", "https://publications.iarc.fr/564"),
    "e251": ("medio", "efsa_limite", "En el cuerpo puede pasar a nitrito.", "Nitrato: en el cuerpo puede pasar a nitrito. La EFSA rebajó la dosis diaria admisible en 2017.", "EFSA 2017, reevaluación de nitratos", "https://doi.org/10.2903/j.efsa.2017.4787"),
    "e252": ("medio", "efsa_limite", "En el cuerpo puede pasar a nitrito.", "Nitrato: en el cuerpo puede pasar a nitrito. La EFSA rebajó la dosis diaria admisible en 2017.", "EFSA 2017, reevaluación de nitratos", "https://doi.org/10.2903/j.efsa.2017.4787"),

    # --- Señalados por el IARC ----------------------------------------------
    "e951": ("medio", "iarc2b", "Posiblemente cancerígeno según el IARC (2023).", "El IARC lo clasificó en 2023 como posiblemente cancerígeno (grupo 2B). La OMS mantiene el límite diario de 40 mg por kilo de peso.", "IARC/JECFA, julio de 2023", "https://www.who.int/news/item/14-07-2023-aspartame-hazard-and-risk-assessment-results-released"),
    "e320": ("medio", "iarc2b", "Posiblemente cancerígeno según el IARC.", "El IARC lo clasificó como posiblemente cancerígeno (grupo 2B).", "IARC, monografía 40", "https://publications.iarc.fr/48"),
    "e150c": ("medio", "iarc2b", "Al fabricarlo aparece 4-metilimidazol (IARC 2B).", "Al fabricarlo aparece 4-metilimidazol, que el IARC clasifica como posiblemente cancerígeno (grupo 2B).", "IARC, monografía 101 · EFSA 2011", "https://publications.iarc.fr/103"),
    "e150d": ("medio", "iarc2b", "Al fabricarlo aparece 4-metilimidazol (IARC 2B).", "Al fabricarlo aparece 4-metilimidazol, que el IARC clasifica como posiblemente cancerígeno (grupo 2B).", "IARC, monografía 101 · EFSA 2011", "https://publications.iarc.fr/103"),

    # --- La EFSA les puso o rebajó la dosis diaria --------------------------
    "e621": ("medio", "efsa_limite", "Dolor de cabeza y tensión alta al pasarse de la dosis.", "La EFSA le puso en 2017 un límite diario (30 mg por kilo de peso) que algunas personas superan.", "EFSA 2017, glutamatos", "https://doi.org/10.2903/j.efsa.2017.4910"),
    "e622": ("medio", "efsa_limite", "Mismo límite diario de grupo que el glutamato.", "Mismo límite diario de grupo que el glutamato: 30 mg por kilo de peso.", "EFSA 2017, glutamatos", "https://doi.org/10.2903/j.efsa.2017.4910"),
    "e623": ("medio", "efsa_limite", "Mismo límite diario de grupo que el glutamato.", "Mismo límite diario de grupo que el glutamato: 30 mg por kilo de peso.", "EFSA 2017, glutamatos", "https://doi.org/10.2903/j.efsa.2017.4910"),
    "e624": ("medio", "efsa_limite", "Mismo límite diario de grupo que el glutamato.", "Mismo límite diario de grupo que el glutamato: 30 mg por kilo de peso.", "EFSA 2017, glutamatos", "https://doi.org/10.2903/j.efsa.2017.4910"),
    "e625": ("medio", "efsa_limite", "Mismo límite diario de grupo que el glutamato.", "Mismo límite diario de grupo que el glutamato: 30 mg por kilo de peso.", "EFSA 2017, glutamatos", "https://doi.org/10.2903/j.efsa.2017.4910"),
    "e321": ("medio", "efsa_limite", "Límite diario bajo: 0,25 mg por kilo de peso.", "La EFSA le fijó una dosis diaria admisible baja: 0,25 mg por kilo de peso.", "EFSA 2012, BHT", "https://doi.org/10.2903/j.efsa.2012.2588"),
    "e211": ("medio", "efsa_limite", "Con vitamina C puede formar benceno en la bebida.", "Junto con vitamina C puede formar benceno en la bebida. La EFSA revisó su seguridad en 2016.", "EFSA 2016, benzoatos", "https://doi.org/10.2903/j.efsa.2016.4433"),
    "e210": ("medio", "efsa_limite", "Con vitamina C puede formar benceno en la bebida.", "Junto con vitamina C puede formar benceno en la bebida. La EFSA revisó su seguridad en 2016.", "EFSA 2016, benzoatos", "https://doi.org/10.2903/j.efsa.2016.4433"),
    "e407": ("medio", "efsa_limite", "Sin confirmar que sea seguro para los lactantes.", "La EFSA no pudo confirmar en 2018 que sea seguro para los lactantes y pidió más datos.", "EFSA 2018, carragenanos", "https://doi.org/10.2903/j.efsa.2018.5238"),
    "e338": ("medio", "efsa_limite", "Exceso de fósforo en la dieta.", "Fosfato: la EFSA fijó en 2019 un límite diario conjunto para todos los fosfatos, que ya se supera en parte de la población.", "EFSA 2019, fosfatos", "https://doi.org/10.2903/j.efsa.2019.5674"),
    "e339": ("medio", "efsa_limite", "Exceso de fósforo en la dieta.", "Fosfato: la EFSA fijó en 2019 un límite diario conjunto para todos los fosfatos, que ya se supera en parte de la población.", "EFSA 2019, fosfatos", "https://doi.org/10.2903/j.efsa.2019.5674"),
    "e340": ("medio", "efsa_limite", "Exceso de fósforo en la dieta.", "Fosfato: la EFSA fijó en 2019 un límite diario conjunto para todos los fosfatos, que ya se supera en parte de la población.", "EFSA 2019, fosfatos", "https://doi.org/10.2903/j.efsa.2019.5674"),
    "e341": ("medio", "efsa_limite", "Exceso de fósforo en la dieta.", "Fosfato: la EFSA fijó en 2019 un límite diario conjunto para todos los fosfatos, que ya se supera en parte de la población.", "EFSA 2019, fosfatos", "https://doi.org/10.2903/j.efsa.2019.5674"),
    "e450": ("medio", "efsa_limite", "Exceso de fósforo en la dieta.", "Fosfato: la EFSA fijó en 2019 un límite diario conjunto para todos los fosfatos, que ya se supera en parte de la población.", "EFSA 2019, fosfatos", "https://doi.org/10.2903/j.efsa.2019.5674"),
    "e451": ("medio", "efsa_limite", "Exceso de fósforo en la dieta.", "Fosfato: la EFSA fijó en 2019 un límite diario conjunto para todos los fosfatos, que ya se supera en parte de la población.", "EFSA 2019, fosfatos", "https://doi.org/10.2903/j.efsa.2019.5674"),
    "e452": ("medio", "efsa_limite", "Exceso de fósforo en la dieta.", "Fosfato: la EFSA fijó en 2019 un límite diario conjunto para todos los fosfatos, que ya se supera en parte de la población.", "EFSA 2019, fosfatos", "https://doi.org/10.2903/j.efsa.2019.5674"),

    # --- Sulfitos: alérgeno de declaración obligatoria ----------------------
    "e220": ("medio", "alergeno", "Puede dar reacción a personas asmáticas.", "Sulfito: alérgeno de declaración obligatoria en la UE. Puede dar reacción a personas asmáticas.", "Reglamento (UE) 1169/2011, anexo II", "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),
    "e221": ("medio", "alergeno", "Puede dar reacción a personas asmáticas.", "Sulfito: alérgeno de declaración obligatoria en la UE.", "Reglamento (UE) 1169/2011, anexo II", "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),
    "e222": ("medio", "alergeno", "Puede dar reacción a personas asmáticas.", "Sulfito: alérgeno de declaración obligatoria en la UE.", "Reglamento (UE) 1169/2011, anexo II", "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),
    "e223": ("medio", "alergeno", "Puede dar reacción a personas asmáticas.", "Sulfito: alérgeno de declaración obligatoria en la UE.", "Reglamento (UE) 1169/2011, anexo II", "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),
    "e224": ("medio", "alergeno", "Puede dar reacción a personas asmáticas.", "Sulfito: alérgeno de declaración obligatoria en la UE.", "Reglamento (UE) 1169/2011, anexo II", "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),
    "e226": ("medio", "alergeno", "Puede dar reacción a personas asmáticas.", "Sulfito: alérgeno de declaración obligatoria en la UE.", "Reglamento (UE) 1169/2011, anexo II", "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),
    "e227": ("medio", "alergeno", "Puede dar reacción a personas asmáticas.", "Sulfito: alérgeno de declaración obligatoria en la UE.", "Reglamento (UE) 1169/2011, anexo II", "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),
    "e228": ("medio", "alergeno", "Puede dar reacción a personas asmáticas.", "Sulfito: alérgeno de declaración obligatoria en la UE.", "Reglamento (UE) 1169/2011, anexo II", "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),

    # --- Fenilcetonuria: aviso obligatorio ----------------------------------
    "e962": ("medio", "aviso_ley", "Lleva fenilalanina: peligroso con fenilcetonuria.", "Lleva fenilalanina: la etiqueta tiene que avisar por las personas con fenilcetonuria.", "Reglamento (UE) 1169/2011, anexo III", "https://eur-lex.europa.eu/eli/reg/2011/1169/oj"),
}


# ---------------------------------------------------------------------------
# Qué le pasa al cuerpo si se toma TODOS LOS DÍAS.
#
# Aquí no se dice nunca «sin límite», porque se lee como «puedes tomarlo
# siempre» y eso no lo dice nadie. Cuando la EFSA pone la IDA «no especificada»
# está hablando de las cantidades que hacen falta para que el aditivo cumpla su
# función dentro de un alimento, no de tomar de más (definición del JECFA,
# recogida en el Codex CXS 192-1995). Así que cada ficha contesta dos cosas:
# cuánto es el tope, si lo hay, y qué le pasa al cuerpo si se toma mucho.
#
# Formato: id -> (qué pasa a diario, quién lo dice)

# Se repite en muchos aditivos: se escribe una vez.
SIN_TOPE = "Sin tope numérico, pero no es barra libre: vale para lo que lleva un alimento."
NO_ESTUDIADO = "Tomar mucho, cada día, no está estudiado."
FIBRA = "En cantidad, gases y heces blandas: es fibra."
# Para los que no tienen ningún dictamen publicado. No decir nada equivale a
# decir «puedes tomarlo siempre», y eso no lo sabe nadie.
POR_DEFECTO = (
    "Nadie ha publicado qué pasa tomándolo todos los días. "
    "Es un aditivo, no comida: cuanto menos, mejor."
)

A_DIARIO = {
    "e465": (f"{SIN_TOPE} De golpe y en cantidad, laxa.", "EFSA 2018, celulosas"),
    "e464": (f"{SIN_TOPE} De golpe y en cantidad, laxa.", "EFSA 2018, celulosas"),
    "e463": (f"{SIN_TOPE} De golpe y en cantidad, laxa.", "EFSA 2018, celulosas"),
    "e461": (f"{SIN_TOPE} De golpe y en cantidad, laxa.", "EFSA 2018, celulosas"),
    "e460": (f"{SIN_TOPE} De golpe y en cantidad, laxa.", "EFSA 2018, celulosas"),
    # --- Sin límite diario: la EFSA no vio necesidad de ponérselo ----------
    "e330": (f"{SIN_TOPE} En cantidad es ácido y desgasta el esmalte de los dientes.", "EFSA 2022, ácido cítrico"),
    "e331": (f"{SIN_TOPE} En cantidad es ácido y desgasta el esmalte de los dientes.", "EFSA 2022, citratos"),
    "e332": (f"{SIN_TOPE} En cantidad es ácido y desgasta el esmalte de los dientes.", "EFSA 2022, citratos"),
    "e300": (f"{SIN_TOPE} Es vitamina C: mucha cada día da diarrea y favorece las piedras de riñón.", "EFSA 2015, ascorbatos"),
    "e301": (f"{SIN_TOPE} Es una sal de la vitamina C: mucha cada día da diarrea.", "EFSA 2015, ascorbatos"),
    "e322": (f"{SIN_TOPE} {NO_ESTUDIADO}", "EFSA 2017, lecitinas"),
    "e471": (f"{SIN_TOPE} {NO_ESTUDIADO}", "EFSA 2017, mono y diglicéridos"),
    "e412": (f"{SIN_TOPE} {FIBRA}", "EFSA 2017, goma guar"),
    "e410": (f"{SIN_TOPE} {FIBRA}", "EFSA 2017, garrofín"),
    "e415": (f"{SIN_TOPE} {FIBRA}", "EFSA 2017, goma xantana"),
    "e414": (f"{SIN_TOPE} {FIBRA}", "EFSA 2017, goma arábiga"),
    "e440": (f"{SIN_TOPE} {FIBRA}", "EFSA 2017, pectinas"),
    "e466": (f"{SIN_TOPE} De golpe y en cantidad, laxa.", "EFSA 2018, celulosas"),
    "e500": (f"{SIN_TOPE} Es bicarbonato: en cantidad, gases y sodio de más.", "EFSA 2011, carbonatos de sodio"),
    "e503": (f"{SIN_TOPE} En cantidad, molestias de estómago.", "EFSA 2011, carbonatos de amonio"),
    "e270": (f"{SIN_TOPE} Es el ácido del yogur. {NO_ESTUDIADO}", "EFSA 2019, ácido láctico"),
    "e296": (f"{SIN_TOPE} Es el ácido de la manzana. En cantidad es ácido y desgasta el esmalte.", "EFSA 2018, ácido málico"),
    "e262": (f"{SIN_TOPE} Es el vinagre en sal: suma sodio al día.", "EFSA 2018, acetatos"),
    "e14xx": (f"{SIN_TOPE} {FIBRA}", "EFSA 2017, almidones modificados"),
    "e160a": (f"{SIN_TOPE} En cantidad y a diario, la piel se pone anaranjada.", "EFSA 2012, carotenos"),
    "e306": ("Límite diario de 4 mg por kilo: es vitamina E.", "EFSA 2015, tocoferoles"),

    # --- Con límite diario: pasarse todos los días es lo que hay que evitar -
    "e200": (f"Tope de 3 mg por kilo al día. {NO_ESTUDIADO}", "EFSA 2015, ácido sórbico"),
    "e202": (f"Tope de 3 mg por kilo al día. {NO_ESTUDIADO}", "EFSA 2015, sorbato potásico"),
    "e211": ("Límite diario de 5 mg por kilo. Con vitamina C puede formar benceno.", "EFSA 2016"),
    "e210": ("Límite diario de 5 mg por kilo.", "EFSA 2016, benzoatos"),
    "e120": ("Límite diario de 5 mg por kilo de peso.", "EFSA 2015, ácido carmínico"),
    "e100": ("Límite diario de 3 mg por kilo de peso.", "EFSA 2010, curcumina"),
    "e160c": ("Límite diario de 1,7 mg por kilo de peso.", "EFSA 2015, extracto de pimentón"),
    "e407": ("Límite diario de 75 mg por kilo. Sin confirmar en lactantes.", "EFSA 2018, carragenanos"),
    "e102": ("Límite diario de 7,5 mg por kilo. La etiqueta avisa por los niños.", "EFSA 2009 · Reglamento 1333/2008"),
    "e104": ("Límite diario de 0,5 mg por kilo. La etiqueta avisa por los niños.", "EFSA 2009 · Reglamento 1333/2008"),
    "e110": ("Límite diario de 4 mg por kilo. La etiqueta avisa por los niños.", "EFSA 2014 · Reglamento 1333/2008"),
    "e122": ("Límite diario de 4 mg por kilo. La etiqueta avisa por los niños.", "EFSA 2009 · Reglamento 1333/2008"),
    "e124": ("Límite diario de 0,7 mg por kilo. La etiqueta avisa por los niños.", "EFSA 2009 · Reglamento 1333/2008"),
    "e129": ("Límite diario de 7 mg por kilo. La etiqueta avisa por los niños.", "EFSA 2009 · Reglamento 1333/2008"),
    "e250": ("Límite diario de 0,07 mg por kilo, y de los más fáciles de superar comiendo embutido a diario.", "EFSA 2017, nitritos"),
    "e249": ("Límite diario de 0,07 mg por kilo.", "EFSA 2017, nitritos"),
    "e251": ("Límite diario de 3,7 mg por kilo.", "EFSA 2017, nitratos"),
    "e252": ("Límite diario de 3,7 mg por kilo.", "EFSA 2017, nitratos"),
    "e621": ("Límite diario de 30 mg por kilo, y una parte de la población lo supera.", "EFSA 2017, glutamatos"),
    "e951": ("Límite diario de 40 mg por kilo. El IARC lo puso en 2023 como posiblemente cancerígeno.", "JECFA/IARC 2023"),
    "e955": ("Límite diario de 5 mg por kilo de peso.", "EFSA 2000, sucralosa"),
    "e320": ("Límite diario de 1 mg por kilo de peso.", "EFSA 2011, BHA"),
    "e321": ("Límite diario de 0,25 mg por kilo de peso.", "EFSA 2012, BHT"),
    "e385": ("Límite diario de 1,9 mg por kilo de peso.", "EFSA 2018, EDTA"),
    "e960": ("Límite diario de 4 mg por kilo de peso.", "EFSA 2010, glucósidos de esteviol"),
    "e223": ("Sulfito: límite diario de 0,7 mg por kilo. Alérgeno de declaración obligatoria.", "EFSA 2016, sulfitos"),
    "e220": ("Sulfito: límite diario de 0,7 mg por kilo. Alérgeno de declaración obligatoria.", "EFSA 2016, sulfitos"),
    "e224": ("Sulfito: límite diario de 0,7 mg por kilo. Alérgeno de declaración obligatoria.", "EFSA 2016, sulfitos"),

    # --- Fosfatos: el exceso de fósforo del día a día ----------------------
    "e338": ("Cuenta para el límite diario de fósforo (40 mg por kilo), que ya se supera en parte de la población.", "EFSA 2019, fosfatos"),
    "e339": ("Cuenta para el límite diario de fósforo (40 mg por kilo).", "EFSA 2019, fosfatos"),
    "e340": ("Cuenta para el límite diario de fósforo (40 mg por kilo).", "EFSA 2019, fosfatos"),
    "e341": ("Cuenta para el límite diario de fósforo (40 mg por kilo).", "EFSA 2019, fosfatos"),
    "e450": ("Cuenta para el límite diario de fósforo (40 mg por kilo).", "EFSA 2019, fosfatos"),
    "e451": ("Cuenta para el límite diario de fósforo (40 mg por kilo).", "EFSA 2019, fosfatos"),
    "e452": ("Cuenta para el límite diario de fósforo (40 mg por kilo).", "EFSA 2019, fosfatos"),

    # --- Polialcoholes: efecto laxante, y la ley obliga a decirlo ----------
    "e420": ("Tomado a diario y en cantidad, laxa y da gases. La etiqueta tiene que avisarlo.", "Reglamento (UE) 1169/2011, anexo III"),
    "e421": ("Tomado a diario y en cantidad, laxa y da gases. La etiqueta tiene que avisarlo.", "Reglamento (UE) 1169/2011, anexo III"),
    "e422": (f"{SIN_TOPE} En cantidad, laxa y da dolor de tripa.", "EFSA 2018, glicerol"),
    "e953": ("Tomado a diario y en cantidad, laxa y da gases. La etiqueta tiene que avisarlo.", "Reglamento (UE) 1169/2011, anexo III"),
    "e965": ("Tomado a diario y en cantidad, laxa y da gases. La etiqueta tiene que avisarlo.", "Reglamento (UE) 1169/2011, anexo III"),
    "e966": ("Tomado a diario y en cantidad, laxa y da gases. La etiqueta tiene que avisarlo.", "Reglamento (UE) 1169/2011, anexo III"),
    "e967": ("Tomado a diario y en cantidad, laxa y da gases. La etiqueta tiene que avisarlo.", "Reglamento (UE) 1169/2011, anexo III"),
    "e968": ("Tomado a diario y en cantidad, laxa y da gases. La etiqueta tiene que avisarlo.", "Reglamento (UE) 1169/2011, anexo III"),

    # --- Los demás que salen mucho en el súper español ---------------------
    "e950": ("Límite diario de 9 mg por kilo de peso.", "Comité Científico de la Alimentación (UE), acesulfamo K"),
    "e428": (f"{SIN_TOPE} Es proteína animal. {NO_ESTUDIADO}", "EFSA, gelatina"),
    "e282": (f"{SIN_TOPE} {NO_ESTUDIADO}", "EFSA 2014, propionatos"),
    "e316": ("Límite diario de 6 mg por kilo de peso.", "JECFA, eritorbatos"),
    "e150d": ("Límite diario de grupo de 300 mg por kilo. Al fabricarlo aparece 4-metilimidazol.", "EFSA 2011, caramelos"),
    "e150a": ("Límite diario de grupo de 300 mg por kilo.", "EFSA 2011, caramelos"),
    "e150b": ("Límite diario de grupo de 300 mg por kilo.", "EFSA 2011, caramelos"),
    "e150c": ("Límite diario de 100 mg por kilo. Al fabricarlo aparece 4-metilimidazol.", "EFSA 2011, caramelos"),
    "e476": ("Límite diario de 25 mg por kilo de peso.", "EFSA 2017, PGPR"),
    "e481": ("Límite diario de 20 mg por kilo de peso.", "EFSA 2016, estearoil lactilatos"),
    "e307": ("Límite diario de 4 mg por kilo: es vitamina E.", "EFSA 2015, tocoferoles"),
    "e392": (f"{SIN_TOPE} Es extracto de romero. {NO_ESTUDIADO}", "EFSA 2008, extracto de romero"),
    # --- Prohibido -----------------------------------------------------------
    "e171": ("No se puede tomar: está prohibido en la UE desde 2022.", "Reglamento (UE) 2022/63"),

    # --- Fenilcetonuria ------------------------------------------------------
    "e962": ("Lleva fenilalanina: quien tenga fenilcetonuria no puede tomarlo.", "Reglamento (UE) 1169/2011, anexo III"),
}

# A un tope numérico le falta la mitad de la respuesta: qué pasa si te lo saltas.
_PASARSE = "Pasar de ahí cada día es salirse de lo comprobado."
A_DIARIO = {
    k: ((v[0] + " " + _PASARSE)
        if v[0].startswith(("Límite diario", "Tope de")) and len(v[0]) < 60
        else v[0], v[1])
    for k, v in A_DIARIO.items()
}

# Los subtipos heredan del padre: «e500ii» dice lo mismo que «e500».
def a_diario(ident):
    """Lo que le pasa al cuerpo a diario, para un aditivo y sus subtipos."""
    if ident in A_DIARIO:
        return A_DIARIO[ident]
    import re as _re
    base = _re.match(r"^(e\d{3,4}[a-z]?)", ident)
    if base and base.group(1) in A_DIARIO:
        return A_DIARIO[base.group(1)]
    corto = _re.match(r"^(e\d{3,4})", ident)
    if corto and corto.group(1) in A_DIARIO:
        return A_DIARIO[corto.group(1)]
    # Sin dictamen también es una respuesta, y hay que darla.
    return (POR_DEFECTO, None)


# ---------------------------------------------------------------------------
# LO MISMO EN INGLÉS
#
# No es una traducción automática: son las mismas piezas escritas en inglés y
# recompuestas igual, con las mismas cifras. Si una clave de A_DIARIO no tiene
# su pareja aquí, el generador de la base se para: así no puede salir una
# versión inglesa a medias.

SIN_TOPE_EN = ("No numerical limit, but that is not a free pass: it applies to "
               "the amounts a food actually carries.")
NO_ESTUDIADO_EN = "Taking a lot of it, every day, has not been studied."
FIBRA_EN = "In quantity, wind and loose stools: it is fibre."
POR_DEFECTO_EN = ("Nobody has published what happens if you take it every day. "
                  "It is an additive, not food: the less the better.")
_PASARSE_EN = "Going over that every day means leaving what has been tested."

_LAXA_EN = "In a large single dose, it has a laxative effect."
_ESMALTE_EN = "In quantity it is acidic and wears down tooth enamel."


def _tope_en(cantidad, extra=""):
    base = f"Daily limit of {cantidad} per kilo of body weight."
    if extra:
        return base + " " + extra
    return base + " " + _PASARSE_EN


A_DIARIO_EN = {
    # --- Sin tope numérico ---
    "e460": f"{SIN_TOPE_EN} {_LAXA_EN}",
    "e461": f"{SIN_TOPE_EN} {_LAXA_EN}",
    "e463": f"{SIN_TOPE_EN} {_LAXA_EN}",
    "e464": f"{SIN_TOPE_EN} {_LAXA_EN}",
    "e465": f"{SIN_TOPE_EN} {_LAXA_EN}",
    "e466": f"{SIN_TOPE_EN} {_LAXA_EN}",
    "e330": f"{SIN_TOPE_EN} {_ESMALTE_EN}",
    "e331": f"{SIN_TOPE_EN} {_ESMALTE_EN}",
    "e332": f"{SIN_TOPE_EN} {_ESMALTE_EN}",
    "e300": f"{SIN_TOPE_EN} It is vitamin C: a lot of it every day causes diarrhoea and favours kidney stones.",
    "e301": f"{SIN_TOPE_EN} It is a salt of vitamin C: a lot of it every day causes diarrhoea.",
    "e322": f"{SIN_TOPE_EN} {NO_ESTUDIADO_EN}",
    "e471": f"{SIN_TOPE_EN} {NO_ESTUDIADO_EN}",
    "e410": f"{SIN_TOPE_EN} {FIBRA_EN}",
    "e412": f"{SIN_TOPE_EN} {FIBRA_EN}",
    "e414": f"{SIN_TOPE_EN} {FIBRA_EN}",
    "e415": f"{SIN_TOPE_EN} {FIBRA_EN}",
    "e440": f"{SIN_TOPE_EN} {FIBRA_EN}",
    "e14xx": f"{SIN_TOPE_EN} {FIBRA_EN}",
    "e500": f"{SIN_TOPE_EN} It is bicarbonate: in quantity, wind and extra sodium.",
    "e503": f"{SIN_TOPE_EN} In quantity, stomach discomfort.",
    "e270": f"{SIN_TOPE_EN} It is the acid in yoghurt. {NO_ESTUDIADO_EN}",
    "e296": f"{SIN_TOPE_EN} It is the acid in apples. {_ESMALTE_EN}",
    "e262": f"{SIN_TOPE_EN} It is vinegar as a salt: it adds to your sodium for the day.",
    "e160a": f"{SIN_TOPE_EN} In quantity and every day, the skin turns orange.",
    "e422": f"{SIN_TOPE_EN} In quantity it laxates and gives stomach ache.",
    "e428": f"{SIN_TOPE_EN} It is animal protein. {NO_ESTUDIADO_EN}",
    "e282": f"{SIN_TOPE_EN} {NO_ESTUDIADO_EN}",
    "e392": f"{SIN_TOPE_EN} It is rosemary extract. {NO_ESTUDIADO_EN}",

    # --- Con tope numérico ---
    "e200": f"Limit of 3 mg per kilo a day. {NO_ESTUDIADO_EN}",
    "e202": f"Limit of 3 mg per kilo a day. {NO_ESTUDIADO_EN}",
    "e100": _tope_en("3 mg"),
    "e120": _tope_en("5 mg"),
    "e160c": _tope_en("1.7 mg"),
    "e210": _tope_en("5 mg"),
    "e211": _tope_en("5 mg", "With vitamin C it can form benzene."),
    "e306": _tope_en("4 mg", "It is vitamin E. " + _PASARSE_EN),
    "e307": _tope_en("4 mg", "It is vitamin E. " + _PASARSE_EN),
    "e316": _tope_en("6 mg"),
    "e320": _tope_en("1 mg"),
    "e321": _tope_en("0.25 mg"),
    "e385": _tope_en("1.9 mg"),
    "e407": _tope_en("75 mg", "Not confirmed as safe for infants."),
    "e476": _tope_en("25 mg"),
    "e481": _tope_en("20 mg"),
    "e950": _tope_en("9 mg"),
    "e955": _tope_en("5 mg"),
    "e960": _tope_en("4 mg"),
    "e102": _tope_en("7.5 mg", "The label has to warn about children."),
    "e104": _tope_en("0.5 mg", "The label has to warn about children."),
    "e110": _tope_en("4 mg", "The label has to warn about children."),
    "e122": _tope_en("4 mg", "The label has to warn about children."),
    "e124": _tope_en("0.7 mg", "The label has to warn about children."),
    "e129": _tope_en("7 mg", "The label has to warn about children."),
    "e249": _tope_en("0.07 mg"),
    "e250": _tope_en("0.07 mg", "One of the easiest to exceed if you eat cured meat every day."),
    "e251": _tope_en("3.7 mg"),
    "e252": _tope_en("3.7 mg"),
    "e621": _tope_en("30 mg", "Part of the population goes over it."),
    "e951": _tope_en("40 mg", "IARC listed it in 2023 as possibly carcinogenic."),
    "e150a": _tope_en("300 mg", "Group limit. " + _PASARSE_EN),
    "e150b": _tope_en("300 mg", "Group limit. " + _PASARSE_EN),
    "e150c": _tope_en("100 mg", "4-methylimidazole appears when it is made."),
    "e150d": _tope_en("300 mg", "Group limit. 4-methylimidazole appears when it is made."),
    "e220": "Sulphite: daily limit of 0.7 mg per kilo. Allergen that must be declared.",
    "e223": "Sulphite: daily limit of 0.7 mg per kilo. Allergen that must be declared.",
    "e224": "Sulphite: daily limit of 0.7 mg per kilo. Allergen that must be declared.",

    # --- Fosfatos ---
    "e338": ("Counts towards the daily phosphorus limit (40 mg per kilo), "
             "which part of the population already exceeds."),
    "e339": "Counts towards the daily phosphorus limit (40 mg per kilo).",
    "e340": "Counts towards the daily phosphorus limit (40 mg per kilo).",
    "e341": "Counts towards the daily phosphorus limit (40 mg per kilo).",
    "e450": "Counts towards the daily phosphorus limit (40 mg per kilo).",
    "e451": "Counts towards the daily phosphorus limit (40 mg per kilo).",
    "e452": "Counts towards the daily phosphorus limit (40 mg per kilo).",

    # --- Polialcoholes ---
    "e420": "Taken every day and in quantity, it laxates and gives wind. The label has to say so.",
    "e421": "Taken every day and in quantity, it laxates and gives wind. The label has to say so.",
    "e953": "Taken every day and in quantity, it laxates and gives wind. The label has to say so.",
    "e965": "Taken every day and in quantity, it laxates and gives wind. The label has to say so.",
    "e966": "Taken every day and in quantity, it laxates and gives wind. The label has to say so.",
    "e967": "Taken every day and in quantity, it laxates and gives wind. The label has to say so.",
    "e968": "Taken every day and in quantity, it laxates and gives wind. The label has to say so.",

    # --- Prohibido y fenilcetonuria ---
    "e171": "You cannot take it: it has been banned in the EU since 2022.",
    "e962": "It carries phenylalanine: anyone with PKU must not take it.",
}


def a_diario_en(ident):
    """El «tomándolo a diario» en inglés, con la misma herencia de subtipos."""
    import re as _re
    if ident in A_DIARIO_EN:
        return A_DIARIO_EN[ident]
    base = _re.match(r"^(e\d{3,4}[a-z]?)", ident)
    if base and base.group(1) in A_DIARIO_EN:
        return A_DIARIO_EN[base.group(1)]
    corto = _re.match(r"^(e\d{3,4})", ident)
    if corto and corto.group(1) in A_DIARIO_EN:
        return A_DIARIO_EN[corto.group(1)]
    return POR_DEFECTO_EN


# Lo que provoca, en una línea, y el porqué largo. Mismas fuentes, en inglés.
EFECTO_EN = {
    "Al fabricarlo aparece 4-metilimidazol (IARC 2B).":
        "4-methylimidazole appears when it is made (IARC 2B).",
    "Con vitamina C puede formar benceno en la bebida.":
        "With vitamin C it can form benzene in the drink.",
    "Dolor de cabeza y tensión alta al pasarse de la dosis.":
        "Headache and raised blood pressure when the dose is exceeded.",
    "En el cuerpo puede pasar a nitrito.":
        "In the body it can turn into nitrite.",
    "En la carne curada puede formar nitrosaminas.":
        "In cured meat it can form nitrosamines.",
    "Exceso de fósforo en la dieta.":
        "Too much phosphorus in the diet.",
    "La EFSA no descartó daño en el material genético.":
        "EFSA could not rule out damage to genetic material.",
    "Lleva fenilalanina: peligroso con fenilcetonuria.":
        "It carries phenylalanine: dangerous with PKU.",
    "Límite diario bajo: 0,25 mg por kilo de peso.":
        "Low daily limit: 0.25 mg per kilo of body weight.",
    "Mismo límite diario de grupo que el glutamato.":
        "Same group daily limit as glutamate.",
    "Posiblemente cancerígeno según el IARC (2023).":
        "Possibly carcinogenic according to IARC (2023).",
    "Posiblemente cancerígeno según el IARC.":
        "Possibly carcinogenic according to IARC.",
    "Puede afectar a la actividad y la atención de los niños.":
        "May affect activity and attention in children.",
    "Puede dar reacción a personas asmáticas.":
        "May cause a reaction in people with asthma.",
    "Sin confirmar que sea seguro para los lactantes.":
        "Not confirmed as safe for infants.",
    "Ningún organismo lo ha señalado.":
        "No authority has flagged it.",
    "No se puede usar en la Unión Europea.":
        "It cannot be used in the European Union.",
}

TEXTO_EN = {
    "Al fabricarlo aparece 4-metilimidazol, que el IARC clasifica como posiblemente cancerígeno (grupo 2B).":
        "4-methylimidazole appears when it is made, which IARC classifies as possibly carcinogenic (group 2B).",
    "El IARC lo clasificó como posiblemente cancerígeno (grupo 2B).":
        "IARC classified it as possibly carcinogenic (group 2B).",
    "El IARC lo clasificó en 2023 como posiblemente cancerígeno (grupo 2B). La OMS mantiene el límite diario de 40 mg por kilo de peso.":
        "IARC classified it in 2023 as possibly carcinogenic (group 2B). WHO keeps the daily limit at 40 mg per kilo of body weight.",
    "En la carne curada puede formar nitrosaminas. El IARC clasifica la carne procesada como cancerígena para las personas (grupo 1).":
        "In cured meat it can form nitrosamines. IARC classifies processed meat as carcinogenic to humans (group 1).",
    "Fosfato: la EFSA fijó en 2019 un límite diario conjunto para todos los fosfatos, que ya se supera en parte de la población.":
        "Phosphate: in 2019 EFSA set a combined daily limit for all phosphates, which part of the population already exceeds.",
    "Junto con vitamina C puede formar benceno en la bebida. La EFSA revisó su seguridad en 2016.":
        "Together with vitamin C it can form benzene in the drink. EFSA reviewed its safety in 2016.",
    "La EFSA le fijó una dosis diaria admisible baja: 0,25 mg por kilo de peso.":
        "EFSA set it a low acceptable daily intake: 0.25 mg per kilo of body weight.",
    "La EFSA le puso en 2017 un límite diario (30 mg por kilo de peso) que algunas personas superan.":
        "In 2017 EFSA gave it a daily limit (30 mg per kilo of body weight) that some people exceed.",
    "La EFSA no pudo confirmar en 2018 que sea seguro para los lactantes y pidió más datos.":
        "In 2018 EFSA could not confirm it is safe for infants and asked for more data.",
    "La etiqueta tiene que avisar por ley: puede afectar a la actividad y la atención de los niños.":
        "The label has to warn by law: it may affect activity and attention in children.",
    "Lleva fenilalanina: la etiqueta tiene que avisar por las personas con fenilcetonuria.":
        "It carries phenylalanine: the label has to warn for people with PKU.",
    "Mismo límite diario de grupo que el glutamato: 30 mg por kilo de peso.":
        "Same group daily limit as glutamate: 30 mg per kilo of body weight.",
    "Nitrato: en el cuerpo puede pasar a nitrito. La EFSA rebajó la dosis diaria admisible en 2017.":
        "Nitrate: in the body it can turn into nitrite. EFSA lowered the acceptable daily intake in 2017.",
    "Prohibido en la Unión Europea desde 2022: la EFSA no pudo descartar que dañe el material genético.":
        "Banned in the European Union since 2022: EFSA could not rule out that it damages genetic material.",
    "Sulfito: alérgeno de declaración obligatoria en la UE.":
        "Sulphite: an allergen that must be declared in the EU.",
    "Sulfito: alérgeno de declaración obligatoria en la UE. Puede dar reacción a personas asmáticas.":
        "Sulphite: an allergen that must be declared in the EU. May cause a reaction in people with asthma.",
}
