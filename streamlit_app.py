import unicodedata
from pathlib import Path
 
import pandas as pd
import streamlit as st
 
st.set_page_config(page_title='CAED - Seguimiento Académico', layout='wide')
 
# -----------------------------------------------------------------------------
# Carga y limpieza de datos
 
def _norm(s: str) -> str:
    """Minúsculas, sin acentos, sin espacios extra."""
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode()
    return ' '.join(s.lower().split())
 
 
RENAME = {
    'id seguimiento academico': 'id_seguimiento',
    'rfc': 'rfc',
    'periodo': 'periodo',
    'curp estudiante': 'curp',
    'dia': 'dia',
    'mes': 'mes',
    'ano': 'anio',
    'fecha de nacimiento': 'fecha_nacimiento',
    'edad': 'edad',
    'gpo etareo': 'grupo_etareo',
    'modulo': 'modulo',
    'unidad': 'unidad',
    'tema': 'tema',
    'actividad seguimiento': 'actividad',
    'contacto': 'contacto',
    'observaciones': 'observaciones',
    'fecha': 'fecha',
    'creacion': 'creacion',
    'modificacion': 'modificacion',
    'asesor': 'asesor',
    'alumno': 'alumno',
    'sexo': 'sexo',
    'discapacidad': 'discapacidad',
    'cct': 'cct',
    'nombre plantel': 'plantel',
    'no. entidad': 'no_entidad',
    'entidad': 'entidad',
    'subsistema': 'subsistema',
    'entidad2': 'entidad2',
    'mes de periodo': 'mes_periodo',
}
 
 
@st.cache_data(show_spinner='Cargando base...')
def load_data(source) -> pd.DataFrame:
    name = getattr(source, 'name', str(source)).lower()
    if name.endswith('.csv'):
        df = pd.read_csv(source, encoding='utf-8', low_memory=False)
    else:
        df = pd.read_excel(source)
 
    new_cols = {}
    for c in df.columns:
        n = _norm(c)
        if n.startswith('abrir columna'):
            new_cols[c] = 'no_entidad_formula'
        else:
            new_cols[c] = RENAME.get(n, n.replace(' ', '_'))
    df = df.rename(columns=new_cols)
 
    # Fechas
    for c in ['fecha', 'creacion', 'modificacion', 'fecha_nacimiento']:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors='coerce', dayfirst=True)
    if 'edad' in df.columns:
        df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
 
    # Mes (año-mes) para series de tiempo
    if 'fecha' in df.columns:
        df['anio_mes'] = df['fecha'].dt.to_period('M').astype(str)
 
    # Texto limpio en columnas categóricas
    for c in df.select_dtypes(include='object').columns:
        df[c] = df[c].astype(str).str.strip().replace({'nan': pd.NA, '': pd.NA})
    return df
 
 
# -----------------------------------------------------------------------------
# Origen de datos
 
st.title('📚 CAED · Dashboard de Seguimiento Académico')
 
DEFAULT_PATH = Path(__file__).parent / 'data' / 'seguimiento.xlsx'
 
uploaded = st.sidebar.file_uploader('Sube la base (.xlsx o .csv)', type=['xlsx', 'csv'])
 
if uploaded is not None:
    df = load_data(uploaded)
elif DEFAULT_PATH.exists():
    df = load_data(DEFAULT_PATH)
else:
    st.info('Sube tu base en la barra lateral (o colócala en `data/seguimiento.xlsx`).')
    st.stop()
 
# -----------------------------------------------------------------------------
# Filtros (lista vacía = sin filtrar)
 
st.sidebar.header('Filtros')
 
 
def multi_filter(frame: pd.DataFrame, col: str, label: str) -> pd.DataFrame:
    if col not in frame.columns:
        return frame
    opciones = sorted(frame[col].dropna().unique().tolist())
    sel = st.sidebar.multiselect(label, opciones)
    return frame[frame[col].isin(sel)] if sel else frame
 
 
filtered = df.copy()
 
if 'fecha' in filtered.columns and filtered['fecha'].notna().any():
    fmin, fmax = filtered['fecha'].min().date(), filtered['fecha'].max().date()
    rango = st.sidebar.date_input('Rango de fechas', value=(fmin, fmax), min_value=fmin, max_value=fmax)
    if isinstance(rango, tuple) and len(rango) == 2:
        filtered = filtered[
            (filtered['fecha'] >= pd.Timestamp(rango[0]))
            & (filtered['fecha'] <= pd.Timestamp(rango[1]) + pd.Timedelta(days=1))
        ]
 
for col, label in [
    ('periodo', 'Periodo'),
    ('entidad', 'Entidad'),
    ('subsistema', 'Subsistema'),
    ('plantel', 'Plantel'),
    ('modulo', 'Módulo'),
    ('actividad', 'Actividad de seguimiento'),
    ('asesor', 'Asesor'),
    ('sexo', 'Sexo'),
    ('grupo_etareo', 'Grupo etáreo'),
]:
    filtered = multi_filter(filtered, col, label)
 
if filtered.empty:
    st.warning('No hay registros con los filtros seleccionados.')
    st.stop()
 
# -----------------------------------------------------------------------------
# KPIs
 
 
def nunique(col):
    return filtered[col].nunique() if col in filtered.columns else 0
 
 
k = st.columns(5)
k[0].metric('Seguimientos', f'{len(filtered):,}')
k[1].metric('Estudiantes únicos', f'{nunique("curp"):,}')
k[2].metric('Asesores', f'{nunique("asesor"):,}')
k[3].metric('Planteles', f'{nunique("plantel"):,}')
if 'edad' in filtered.columns:
    k[4].metric('Edad promedio', f'{filtered["edad"].mean():.1f}')
 
if 'curp' in filtered.columns and nunique('curp'):
    st.caption(f'Promedio de {len(filtered) / nunique("curp"):.1f} seguimientos por estudiante.')
 
st.divider()
 
# -----------------------------------------------------------------------------
# Evolución en el tiempo
 
if 'anio_mes' in filtered.columns:
    st.header('Seguimientos por mes', divider='gray')
    serie = filtered.groupby('anio_mes').size().rename('Seguimientos').reset_index()
    st.line_chart(serie, x='anio_mes', y='Seguimientos')
 
 
# -----------------------------------------------------------------------------
# Distribuciones
 
 
def bar_count(col: str, titulo: str, top: int | None = None, container=st):
    if col not in filtered.columns:
        return
    container.subheader(titulo)
    conteo = filtered[col].value_counts()
    if top:
        conteo = conteo.head(top)
    container.bar_chart(conteo)
 
 
c1, c2 = st.columns(2)
bar_count('entidad', 'Por entidad', container=c1)
bar_count('subsistema', 'Por subsistema', container=c2)
 
c3, c4 = st.columns(2)
bar_count('actividad', 'Por actividad de seguimiento', container=c3)
bar_count('modulo', 'Por módulo', container=c4)
 
c5, c6, c7 = st.columns(3)
bar_count('sexo', 'Por sexo', container=c5)
bar_count('grupo_etareo', 'Por grupo etáreo', container=c6)
bar_count('contacto', 'Por tipo de contacto', container=c7)
 
c8, c9 = st.columns(2)
bar_count('plantel', 'Top 15 planteles', top=15, container=c8)
bar_count('asesor', 'Top 15 asesores', top=15, container=c9)
 
# -----------------------------------------------------------------------------
# Resumen por entidad (tarjetas, como en la plantilla)
 
if 'entidad' in filtered.columns:
    st.header('Resumen por entidad', divider='gray')
    resumen = (
        filtered.groupby('entidad')
        .agg(
            seguimientos=('entidad', 'size'),
            estudiantes=('curp', 'nunique') if 'curp' in filtered.columns else ('entidad', 'size'),
        )
        .sort_values('seguimientos', ascending=False)
    )
    cols = st.columns(4)
    for i, (ent, fila) in enumerate(resumen.head(8).iterrows()):
        cols[i % 4].metric(
            label=str(ent),
            value=f'{int(fila["seguimientos"]):,}',
            delta=f'{int(fila["estudiantes"]):,} estudiantes',
            delta_color='off',
        )
    with st.expander('Ver tabla completa por entidad'):
        st.dataframe(resumen, use_container_width=True)
 
# -----------------------------------------------------------------------------
# Detalle y descarga
 
st.header('Detalle de registros', divider='gray')
st.dataframe(filtered, use_container_width=True, height=400)
st.download_button(
    'Descargar datos filtrados (CSV)',
    data=filtered.to_csv(index=False).encode('utf-8-sig'),
    file_name='seguimiento_filtrado.csv',
    mime='text/csv',
)