import streamlit as st

from utils import iniciar

iniciar('Inicio')

st.title('📚 CAED · Tablero de indicadores')
st.write(
    'Elige una sección. En cada una puedes subir la base desde la barra lateral, '
    'cambiar la vista del reporte (mensual, trimestral, semestral o anual), '
    'filtrar y descargar los datos del periodo en CSV o Excel.'
)

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.page_link('pages/1_Seguimiento.py', label='Seguimiento académico', icon='📋')
    st.page_link('pages/2_Examenes.py', label='Exámenes (PA y PM)', icon='📝')
    st.page_link('pages/3_Certificados.py', label='Certificados', icon='🎓')
    st.page_link('pages/4_Inscritos.py', label='Inscritos', icon='✍️')
with col2:
    st.page_link('pages/5_Egresadas.py', label='Personas egresadas (PA y PM)', icon='🏁')
    st.page_link('pages/6_Comportamiento.py', label='Comportamiento (TR, TA y TRI)', icon='📈')
    st.page_link('pages/7_Asesorias_Asesores.py', label='Asesorías y asesores', icon='🧑‍🏫')

    
