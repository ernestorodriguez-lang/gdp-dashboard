from utils import pagina_estandar

pagina_estandar(
    'inscritos',
    dims=[
        ('entidad', 'Por entidad'), ('plantel', 'Top 15 planteles'),
        ('plan', 'Por plan de estudios'), ('direccion_general', 'Por dirección general'),
        ('sexo', 'Por sexo'), ('discapacidad', 'Por discapacidad'),
    ],
    dividir_plan=True,  # pestañas Todos / PA / PM
)
