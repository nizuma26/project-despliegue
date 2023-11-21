#Servicio Técnico
prioridad_choices = (
    ('MB', 'Muy baja'),
    ('BJ', 'Baja'),
    ('NM', 'Normal'),
    ('AL', 'Alta'),
    ('MA', 'Muy alta')
)
tipo_solic_soporte_choices = (
    ('REP', 'Reparacion y mantenimiento'),
    ('AST', 'Soporte técnico'),
)
tipo_solic_choices = (
    ('DIST', 'Solicitud de Distribución'),
    ('TRAS', 'Solicitud de Traslado'),
    ('DES_USO', 'Solicitud de Desincorporación de Bienes Muebles en Uso'),
    ('DES_DEPOSITO', 'Solicitud de Desincorporación de Bienes Muebles en Depósito y Materiales de Consumo')
)
status_choices = (
    ('ECR', 'En Creación'),
    ('PEN', 'Pendiente'),
    ('REC', 'Rechazada'),
    ('RES', 'Resuelta')
)
prod_solicitud_choices = (
    ('BMU', 'Bien mueble en uso'),
    ('BMD', 'Bien en deposito'),
)