"""Aquí van tus funciones para transformar los datos.

Cada función recibe el DataFrame ya con columnas normalizadas
(minúsculas, sin acentos, con guion bajo) y debe regresar el DataFrame.
Se aplican automáticamente al cargar cada base.
"""
import pandas as pd

def transformar_seguimiento(df):
    
    return df
def Entidades(x):
  if x==1:
    return  "Aguascalientes"
  elif x==2:
    return "Baja California"
  elif x==3:
    return "Baja California Sur"
  elif x==4:
    return "Campeche"
  elif x==5:
    return "Coahuila de Zaragoza"
  elif x==6:
    return "Colima"
  elif x==7:
    return "Chiapas"
  elif x==8:
    return "Chihuahua"
  elif x==9:
    return "Ciudad de México"
  elif x==10:
    return "Durango"
  elif x==11:
    return "Guanajuato"
  elif x==12:
    return "Guerrero"
  elif x==13:
    return "Hidalgo"
  elif x==14:
    return "Jalisco"
  elif x==15:
    return "Estado de México"
  elif x==16:
    return "Michoacán de Ocampo"
  elif x==17:
    return "Morelos"
  elif x==18:
    return "Nayarit"
  elif x==19:
    return "Nuevo León"
  elif x==20:
    return  "Oaxaca"
  elif x==21:
    return "Puebla"
  elif x==22:
    return "Querétaro"
  elif x==23:
    return "Quintana Roo"
  elif x==24:
    return "San Luis Potosí"
  elif x==25:
    return "Sinaloa"
  elif x==26:
    return "Sonora"
  elif x==27:
    return "Tabasco"
  elif x==28:
    return "Tamaulipas"
  elif x==29:
    return "Tlaxcala"
  elif x==30:
    return "Veracruz de Ignacio de la Llave"
  elif x==31:
    return "Yucatán"
  elif x==32:
    return "Zacatecas"
  else:
    return "Sin entidad"

def Ajustes(df):
    for col in ('sexo', 'sexo_asesor', 'sexo_alumno'):
        if col in df.columns:
            df[col] = (
                df[col].str.strip().str.lower()
                .replace({'h': 'Hombres','hombre': 'Hombres','mujer': 'Mujeres', 'm': 'Mujeres', 'x': 'No binario'})
            )
    return df
  



def transformar_asesores(df):
    return df


def transformar_examenes(df):
    return df




SIGLAS_DG = {
    'DIRECCIÓN GENERAL DE EDUCACIÓN TECNOLÓGICA INDUSTRIAL': 'DGETI',
    'DIRECCIÓN GENERAL DE EDUCACIÓN EN CIENCIA Y TECNOLOGÍA DEL MAR': 'DGECyTM',
    'DIRECCIÓN GENERAL DE CENTROS DE FORMACIÓN PARA EL TRABAJO': 'DGCFT',
    'DIRECCIÓN GENERAL DEL BACHILLERATO' : 'DGB'
}


def normalizar_texto(texto):
    return (
        texto.astype('string')
        .str.upper()
        .str.normalize('NFKD')
        .str.replace(r'[\u0300-\u036f]', '', regex=True)
        .str.split()
        .str.join(' ')
    )


def abreviar_direccion(df):
    if 'direccion_general' not in df.columns:
        return df

    # Normalizar las claves del diccionario
    siglas_normalizadas = {
        normalizar_texto(pd.Series([nombre])).iloc[0]: sigla
        for nombre, sigla in SIGLAS_DG.items()
    }

    original = df['direccion_general']
    clave = normalizar_texto(original)

    df['direccion_general'] = clave.map(siglas_normalizadas).fillna(original)

    return df



def transformar_certificados(df):
    df = abreviar_direccion(df)   
    return df
  
def transformar_inscritos(df):
    df = abreviar_direccion(df) 
    return df



def transformar_egresados(df):
    return df


def transformar_comportamiento(df):
    return df


TRANSFORMS = {
    'seguimiento': transformar_seguimiento,
    'seguimiento': Ajustes,
    'asesores': transformar_asesores,
    'examenes': transformar_examenes,
    'certificados': transformar_certificados,
    
    'inscritos': transformar_inscritos,
    #'inscritos': Ajustes,
    #'inscritos': abreviar_direccion,
    'egresados': transformar_egresados,
    'comportamiento_tr': transformar_comportamiento,
    'comportamiento_ta': transformar_comportamiento,
    'comportamiento_tri': transformar_comportamiento,
}
