"""Aquí van tus funciones para transformar los datos.

Cada función recibe el DataFrame ya con columnas normalizadas
(minúsculas, sin acentos, con guion bajo) y debe regresar el DataFrame.
Se aplican automáticamente al cargar cada base.
"""


def transformar_seguimiento(df):
    return df


def transformar_asesores(df):
    return df


def transformar_examenes(df):
    return df


def transformar_certificados(df):
    return df


def transformar_inscritos(df):
    return df


def transformar_egresados(df):
    return df


def transformar_comportamiento(df):
    return df


TRANSFORMS = {
    'seguimiento': transformar_seguimiento,
    'asesores': transformar_asesores,
    'examenes': transformar_examenes,
    'certificados': transformar_certificados,
    'inscritos': transformar_inscritos,
    'egresados': transformar_egresados,
    'comportamiento_tr': transformar_comportamiento,
    'comportamiento_ta': transformar_comportamiento,
    'comportamiento_tri': transformar_comportamiento,
}
