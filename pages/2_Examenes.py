from utils import pagina_estandar

pagina_estandar(
    'examenes',
    dims=[
        ('entidad', 'Por entidad'), ('sede', 'Top 15 sedes'),
        ('modulo', 'Top 15 módulos'), ('clasificacion', 'Por clasificación'),
        ('etapa_de_solicitud', 'Por etapa de solicitud'), ('fase_de_solicitud', 'Por fase de solicitud'),
        ('sexo', 'Por sexo'), ('discapacidad', 'Por discapacidad'),
    ],
    kpi_cols=[('Personas únicas', 'curp'), ('Sedes', 'sede'), ('Entidades', 'entidad')],
    dividir_plan=True,  # pestañas Todos / PA / PM
)
