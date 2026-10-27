from utils import pagina_estandar

pagina_estandar(
    'certificados',
    dims=[
        ('entidad', 'Por entidad'), ('plantel', 'Top 15 planteles'),
        ('direccion_general', 'Por dirección general'), ('permanencia', 'Por permanencia'),
        ('sexo', 'Por sexo'), ('discapacidad', 'Por discapacidad'),
    ],
    medias=[('Edad promedio', 'edad')],
)
