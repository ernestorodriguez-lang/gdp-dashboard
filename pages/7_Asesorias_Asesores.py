from utils import pagina_estandar

pagina_estandar(
    'asesores',
    dims=[
        ('asesor', 'Top 15 asesores (por asesorías)'), ('plantel', 'Top 15 planteles'),
        ('entidad', 'Por entidad'), ('actividad', 'Por actividad'),
        ('contacto', 'Por tipo de contacto'), ('modulo', 'Por módulo'),
        ('sexo_asesor', 'Asesores por sexo'),
    ],
    kpi_cols=[('Asesores', 'curp_asesores'), ('Estudiantes atendidos', 'curp'), ('Planteles', 'plantel')],
)
