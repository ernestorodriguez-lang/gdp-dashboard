from utils import pagina_estandar

pagina_estandar(
    'seguimiento',
    dims=[
        ('entidad', 'Por entidad'), ('subsistema', 'Por subsistema'),
        ('actividad', 'Por actividad de seguimiento'), ('modulo', 'Por módulo'),
        ('contacto', 'Por tipo de contacto'), ('grupo_etareo', 'Por grupo etáreo'),
        ('plantel', 'Top 15 planteles'), ('asesor', 'Top 15 asesores'),
        ('sexo', 'Por sexo'), ('discapacidad', 'Por discapacidad'),
    ],
    kpi_cols=[('Estudiantes únicos', 'curp'), ('Asesores', 'asesor'), ('Planteles', 'plantel')],
    medias=[('Edad promedio', 'edad')],
)
