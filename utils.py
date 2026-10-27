"""Funciones compartidas por todas las páginas del dashboard CAED."""
import io
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

GUINDA = '#9D2449'
DATA_DIR = Path(__file__).parent / 'data'
VISTAS = ['Mensual', 'Trimestral', 'Semestral', 'Anual']

# -----------------------------------------------------------------------------
# Estilo

CSS = f"""
<style>
    .block-container {{padding-top: 1.5rem; max-width: 1400px;}}
    [data-testid="stMetric"] {{
        background-color: {GUINDA};
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    }}
    [data-testid="stMetric"] * {{color: #FFFFFF !important;}}
    [data-testid="stMetric"] svg {{fill: #FFFFFF !important;}}
    [data-testid="stMetricValue"] {{font-size: 1.9rem; font-weight: 700;}}
    [data-testid="stMetricLabel"] p {{font-size: 0.95rem; opacity: 0.9;}}
</style>
"""


def iniciar(titulo: str):
    """Debe ser el primer comando de cada página."""
    st.set_page_config(page_title=f'CAED · {titulo}', layout='wide')
    st.markdown(CSS, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Configuración de cada base
# Los nombres de columna ya están normalizados (minúsculas, sin acentos, con _).
# 'mantener' elimina columnas para aligerar la base (nombres y apellidos no se cargan).

ALIAS = {
    'entidad_federativa': 'entidad',
    'nombre_plantel': 'plantel',
    'caed': 'plantel',
    'curp_estudiante': 'curp',
    'fecha_de_alta': 'fecha_alta',
    'fecha_de_expedicion': 'fecha_expedicion',
    'tipo_de_discapacidad': 'discapacidad',
    'plan_de_estudios': 'plan',
    'ano': 'anio',
    'mes_de_periodo': 'mes_periodo',
    'permanencia_en_anos': 'permanencia_anios',
    'gpo_etareo': 'grupo_etareo',
    'actividad_seguimiento': 'actividad',
    'id_seguimiento_academico': 'id_seguimiento',
}

_SEGUIMIENTO = [
    'id_seguimiento', 'periodo', 'curp', 'dia', 'mes', 'anio', 'fecha_nacimiento', 'edad',
    'grupo_etareo', 'modulo', 'unidad', 'tema', 'actividad', 'contacto', 'fecha', 'creacion',
    'modificacion', 'asesor', 'sexo', 'discapacidad', 'cct', 'plantel', 'no_entidad',
    'entidad', 'subsistema', 'entidad2', 'mes_periodo',
]

BASES = {
    'seguimiento': dict(
        titulo='Seguimiento académico', fecha='fecha',
        mantener=_SEGUIMIENTO,
        fechas=['fecha', 'creacion', 'modificacion', 'fecha_nacimiento'], numericas=['edad'],
        filtros=['entidad', 'subsistema', 'plantel', 'modulo', 'actividad', 'asesor', 'sexo', 'grupo_etareo'],
    ),
    'asesores': dict(
        titulo='Asesorías y asesores', fecha='fecha',
        renombrar={'sexo': 'sexo_asesor', 'sexo_1': 'sexo_alumno'},
        mantener=[c for c in _SEGUIMIENTO if c not in ('sexo', 'grupo_etareo')]
        + ['curp_asesores', 'sexo_asesor', 'sexo_alumno'],
        fechas=['fecha', 'creacion', 'modificacion', 'fecha_nacimiento'], numericas=['edad'],
        filtros=['entidad', 'plantel', 'asesor', 'modulo', 'actividad', 'contacto', 'sexo_asesor'],
    ),
    'examenes': dict(
        titulo='Exámenes', fecha='fecha_alta',
        mantener=['mes', 'direccion_general', 'entidad', 'sede', 'curp', 'matricula', 'discapacidad',
                  'sexo', 'plan', 'etapa_de_solicitud', 'fase_de_solicitud', 'clave_del_modulo',
                  'modulo', 'Fecha alta', 'clasificacion'],
        fechas=['fecha_alta'], numericas=[],
        filtros=['direccion_general', 'entidad', 'sede', 'modulo', 'etapa_de_solicitud',
                 'fase_de_solicitud', 'clasificacion', 'sexo'],
    ),
    'certificados': dict(
        titulo='Certificados', fecha='fecha_alta',
        mantener=['direccion_general', 'entidad', 'plantel', 'curp', 'edad', 'matricula', 'sexo',
                  'discapacidad', 'fecha_alta', 'mes_de_expedicion', 'anio', 'permanencia'],
        fechas=['fecha_alta'], numericas=['edad'],
        filtros=['direccion_general', 'entidad', 'plantel', 'sexo', 'permanencia'],
    ),
    'inscritos': dict(
        titulo='Inscritos', fecha='fecha_alta',
        mantener=['clave_oficina', 'clave_caed', 'plantel', 'direccion_general', 'plan', 'matricula',
                  'curp', 'sexo', 'mes_periodo', 'fecha_alta', 'discapacidad', 'entidad'],
        fechas=['fecha_alta'], numericas=[],
        filtros=['direccion_general', 'entidad', 'plantel', 'plan', 'sexo'],
    ),
    'egresados': dict(
        titulo='Personas egresadas', fecha='fecha_expedicion',
        mantener=['clave_del_caed', 'plantel', 'entidad', 'direccion_general', 'matricula', 'curp',
                  'sexo', 'discapacidad', 'fecha_alta', 'plan', 'area_de_estudios', 'estatus',
                  'total_de_modulos_acreditados', 'fecha_expedicion', 'anio', 'permanencia_anios',
                  'promedio_general', 'promedio_redondeo', 'permanencia'],
        fechas=['fecha_alta', 'fecha_expedicion'],
        numericas=['total_de_modulos_acreditados', 'permanencia_anios', 'promedio_general', 'promedio_redondeo'],
        filtros=['direccion_general', 'entidad', 'plantel', 'area_de_estudios', 'estatus', 'sexo'],
    ),
    # Comportamiento: formato ancho (anio, discapacidad, m01..m22). Solo tiene año.
    'comportamiento_tr': dict(titulo='Tasa de reprobación (TR)', fecha=None, mantener=None, fechas=[], numericas=[], filtros=[]),
    'comportamiento_ta': dict(titulo='Tasa de acreditación (TA)', fecha=None, mantener=None, fechas=[], numericas=[], filtros=[]),
    'comportamiento_tri': dict(titulo='Reprobación por intentos (TRI)', fecha=None, mantener=None, fechas=[], numericas=[], filtros=[]),
}

# -----------------------------------------------------------------------------
# Carga y limpieza


def _snake(c) -> str:
    s = unicodedata.normalize('NFKD', str(c)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '_', s).strip('_')


def _dedupe(cols):
    vistos, salida = {}, []
    for c in cols:
        if c in vistos:
            vistos[c] += 1
            salida.append(f'{c}_{vistos[c]}')
        else:
            vistos[c] = 0
            salida.append(c)
    return salida


def _normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    nuevas = []
    for c in df.columns:
        s = _snake(c)
        if s.startswith('abrir_columna'):
            s = 'no_entidad_formula'
        elif s == '':
            s = 'sin_nombre'
        nuevas.append(ALIAS.get(s, s))
    df.columns = _dedupe(nuevas)
    return df


def _transformaciones() -> dict:
    """Carga tus funciones de transformacion.py (si existe)."""
    try:
        import transformaciones
        return getattr(transformaciones, 'TRANSFORMS', {})
    except ImportError:
        return {}


@st.cache_data(show_spinner='Cargando base...')
def _leer(source, clave: str) -> pd.DataFrame:
    cfg = BASES[clave]
    nombre = getattr(source, 'name', str(source)).lower()
    if nombre.endswith('.parquet'):
        df = pd.read_parquet(source)
    elif nombre.endswith('.csv'):
        df = pd.read_csv(source, low_memory=False, encoding='utf-8-sig', encoding_errors='replace')
    else:
        df = pd.read_excel(source)

    df = _normalizar_columnas(df)
    if cfg.get('renombrar'):
        df = df.rename(columns=cfg['renombrar'])
    if cfg.get('mantener'):
        df = df[[c for c in cfg['mantener'] if c in df.columns]]

    for c in cfg['fechas']:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors='coerce', dayfirst=True)
    for c in cfg['numericas']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    for c in df.select_dtypes(include='object').columns:
        df[c] = df[c].astype('string').str.strip()

    funcion = _transformaciones().get(clave)
    if funcion:
        df = funcion(df)
    return df


def cargar_base(clave: str, detener: bool = True):
    """Muestra el cargador de archivos en la barra lateral; si no hay archivo
    busca data/<clave>.parquet|xlsx|csv."""
    cfg = BASES[clave]
    subido = st.sidebar.file_uploader(
        f'Base: {cfg["titulo"]}', type=['xlsx', 'csv', 'parquet'], key=f'up_{clave}'
    )
    fuente = subido
    if fuente is None:
        for ext in ('parquet', 'xlsx', 'csv'):
            ruta = DATA_DIR / f'{clave}.{ext}'
            if ruta.exists():
                fuente = ruta
                break
    if fuente is None:
        if detener:
            st.info(f'Sube la base de **{cfg["titulo"]}** en la barra lateral '
                    f'(o colócala en `data/{clave}.xlsx`).')
            st.stop()
        return None
    return _leer(fuente, clave)


def clasificar_plan(serie: pd.Series) -> pd.Series:
    """PA / PM según el texto de 'Plan de Estudios' (busca 'asig' o 'modul')."""
    txt = serie.astype('string').fillna('').str.lower()
    txt = txt.map(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode())
    return pd.Series(
        np.select([txt.str.contains('modul'), txt.str.contains('asig')], ['PM', 'PA'], 'Otro'),
        index=serie.index,
    )


# -----------------------------------------------------------------------------
# Periodos (mensual / trimestral / semestral / anual)


def agregar_periodo(df: pd.DataFrame, col_fecha: str, vista: str) -> pd.DataFrame:
    df = df[df[col_fecha].notna()].copy()
    f = df[col_fecha]
    anio = f.dt.year.astype(int).astype(str)
    if vista == 'Mensual':
        df['periodo_reporte'] = f.dt.strftime('%Y-%m')
    elif vista == 'Trimestral':
        df['periodo_reporte'] = anio + ' T' + f.dt.quarter.astype(str)
    elif vista == 'Semestral':
        df['periodo_reporte'] = anio + ' S' + (((f.dt.month - 1) // 6) + 1).astype(str)
    else:
        df['periodo_reporte'] = anio
    return df


def selector_periodo(df, col_fecha, clave, contenedor):
    """Devuelve (df del/los periodos elegidos, df con todos los periodos, vista, elegidos, anterior)."""
    with contenedor:
        vista = st.radio('Vista del reporte', VISTAS, index=1, key=f'vista_{clave}')
        df = agregar_periodo(df, col_fecha, vista)
        opciones = sorted(df['periodo_reporte'].unique())
        elegidos = st.multiselect('Periodo(s)', opciones, default=opciones[-1:], key=f'per_{clave}')
    anterior = None
    if len(elegidos) == 1:
        i = opciones.index(elegidos[0])
        anterior = opciones[i - 1] if i > 0 else None
    return df[df['periodo_reporte'].isin(elegidos)], df, vista, elegidos, anterior


def filtros_sidebar(df: pd.DataFrame, columnas, clave: str) -> pd.DataFrame:
    st.sidebar.header('Filtros')
    for col in columnas:
        if col in df.columns:
            opciones = sorted(df[col].dropna().astype(str).unique())
            sel = st.sidebar.multiselect(col.replace('_', ' ').capitalize(), opciones, key=f'f_{clave}_{col}')
            if sel:
                df = df[df[col].astype(str).isin(sel)]
    return df


# -----------------------------------------------------------------------------
# Componentes de la página estándar


def _barras(df, col, titulo, contenedor, top=15):
    if col in df.columns:
        contenedor.subheader(titulo)
        contenedor.bar_chart(df[col].value_counts().head(top))


def _cuerpo(sub_f, sub_c, clave, vista, elegidos, anterior, dims, kpi_cols, medias, etiqueta):
    if sub_f.empty:
        st.warning('Sin registros para esta selección.')
        return

    # KPIs
    columnas = st.columns(1 + len(kpi_cols) + len(medias))
    total = len(sub_f)
    previo = int((sub_c['periodo_reporte'] == anterior).sum()) if anterior else None
    columnas[0].metric(
        'Registros', f'{total:,}',
        delta=f'{total - previo:+,} vs {anterior}' if previo is not None else None,
        delta_color='off',
    )
    for i, (nombre, col) in enumerate(kpi_cols, start=1):
        valor = sub_f[col].nunique() if col in sub_f.columns else 0
        columnas[i].metric(nombre, f'{valor:,}')
    for j, (nombre, col) in enumerate(medias, start=1 + len(kpi_cols)):
        valor = sub_f[col].mean() if col in sub_f.columns else np.nan
        columnas[j].metric(nombre, '—' if pd.isna(valor) else f'{valor:.2f}')

    # Evolución en todos los periodos de la vista elegida
    st.subheader(f'Evolución {vista.lower()}', divider='gray')
    st.bar_chart(sub_c.groupby('periodo_reporte').size())

    # Distribuciones
    st.subheader('Distribución', divider='gray')
    for i in range(0, len(dims), 2):
        cols = st.columns(2)
        for cont, (col, titulo) in zip(cols, dims[i:i + 2]):
            _barras(sub_f, col, titulo, cont)

    # Detalle y descarga
    st.subheader('Detalle y descarga', divider='gray')
    st.dataframe(sub_f, height=350)
    nombre = f'{clave}_{vista.lower()}_{"_".join(elegidos)}{etiqueta}'.replace(' ', '')
    c1, c2 = st.columns(2)
    c1.download_button('Descargar CSV', sub_f.to_csv(index=False).encode('utf-8-sig'),
                       file_name=f'{nombre}.csv', mime='text/csv', key=f'csv_{clave}{etiqueta}')
    buf = io.BytesIO()
    sub_f.to_excel(buf, index=False)
    c2.download_button('Descargar Excel', buf.getvalue(), file_name=f'{nombre}.xlsx',
                       key=f'xlsx_{clave}{etiqueta}',
                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


def pagina_estandar(clave, dims, kpi_cols=None, medias=None, dividir_plan=False):
    """Página completa: carga, periodo, filtros, KPIs, gráficas y descarga."""
    cfg = BASES[clave]
    kpi_cols = kpi_cols or [('Personas únicas', 'curp'), ('Planteles', 'plantel'), ('Entidades', 'entidad')]
    medias = medias or []

    iniciar(cfg['titulo'])
    st.title(cfg['titulo'])

    df = cargar_base(clave)
    contenedor_periodo = st.sidebar.container()
    df = filtros_sidebar(df, cfg['filtros'], clave)

    if cfg['fecha'] not in df.columns:
        st.error(f'No encontré la columna de fecha `{cfg["fecha"]}` en la base.')
        st.stop()
    if df.empty:
        st.warning('No hay registros con los filtros seleccionados.')
        st.stop()

    filtrado, completo, vista, elegidos, anterior = selector_periodo(
        df, cfg['fecha'], clave, contenedor_periodo
    )
    if not elegidos:
        st.warning('Elige al menos un periodo.')
        st.stop()
    st.caption(f'Vista {vista.lower()} · {", ".join(elegidos)}')

    args = (clave, vista, elegidos, anterior, dims, kpi_cols, medias)
    if dividir_plan and 'plan' in df.columns:
        filtrado = filtrado.assign(tipo_plan=clasificar_plan(filtrado['plan']))
        completo = completo.assign(tipo_plan=clasificar_plan(completo['plan']))
        tabs = st.tabs(['Todos', 'Plan asignatura (PA)', 'Plan modular (PM)'])
        for tab, valor in zip(tabs, [None, 'PA', 'PM']):
            with tab:
                sf = filtrado if valor is None else filtrado[filtrado['tipo_plan'] == valor]
                sc = completo if valor is None else completo[completo['tipo_plan'] == valor]
                _cuerpo(sf, sc, *args, etiqueta=f'_{valor or "todos"}')
    else:
        _cuerpo(filtrado, completo, *args, etiqueta='')
