from utils import pagina_estandar

pagina_estandar(
    'egresados',
    dims=[
        ('entidad', 'Por entidad'), ('plantel', 'Top 15 planteles'),
        ('area_de_estudios', 'Por área de estudios'), ('estatus', 'Por estatus'),
        ('permanencia', 'Por permanencia'), ('sexo', 'Por sexo'), ('discapacidad', 'Por discapacidad'),
    ],
    medias=[('Promedio general', 'promedio_general'), ('Permanencia (años)', 'permanencia_anios')],
    dividir_plan=True,  # pestañas Todos / PA / PM
)
