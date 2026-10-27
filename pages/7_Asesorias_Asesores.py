import re

import pandas as pd
import streamlit as st

from utils import BASES, cargar_base, iniciar

iniciar('Comportamiento')
st.title('Comportamiento por módulo')
st.caption('Estas bases solo traen el año, por lo que la vista es anual.')


def mostrar(clave: str):
    df = cargar_base(clave, detener=False)
    if df is None:
        st.info(f'Sube la base de **{BASES[clave]["titulo"]}** en la barra lateral '
                f'(o colócala en `data/{clave}.xlsx`).')
        return

    modulos = [c for c in df.columns if re.fullmatch(r'm\d{2}', c)]
    ids = [c for c in ('anio', 'discapacidad') if c in df.columns]
    largo = df.melt(id_vars=ids, value_vars=modulos, var_name='modulo', value_name='valor')
    largo['modulo'] = largo['modulo'].str.upper()
    largo['valor'] = pd.to_numeric(largo['valor'], errors='coerce')

    if 'discapacidad' in largo.columns:
        opciones = sorted(largo['discapacidad'].dropna().astype(str).unique())
        sel = st.multiselect('Discapacidad', opciones, key=f'disc_{clave}')
        if sel:
            largo = largo[largo['discapacidad'].astype(str).isin(sel)]

    todos = sorted(largo['modulo'].unique())
    elegidos = st.multiselect('Módulos', todos, default=todos[:5], key=f'mod_{clave}')
    largo = largo[largo['modulo'].isin(elegidos)]
    if largo.empty:
        st.warning('Sin datos para esta selección.')
        return

    tabla = largo.pivot_table(index='modulo', columns='anio', values='valor', aggfunc='mean')

    st.subheader('Evolución por año', divider='gray')
    st.line_chart(tabla.T)

    st.subheader('Último año disponible', divider='gray')
    ultimo = tabla.columns.max()
    st.caption(f'Año {ultimo}')
    st.bar_chart(tabla[ultimo])

    st.subheader('Tabla módulo × año', divider='gray')
    st.dataframe(tabla)
    st.download_button('Descargar CSV', tabla.to_csv().encode('utf-8-sig'),
                       file_name=f'{clave}.csv', mime='text/csv', key=f'dl_{clave}')


tabs = st.tabs(['Tasa de reprobación (TR)', 'Tasa de acreditación (TA)', 'Reprobación por intentos (TRI)'])
for tab, clave in zip(tabs, ['comportamiento_tr', 'comportamiento_ta', 'comportamiento_tri']):
    with tab:
        mostrar(clave)
