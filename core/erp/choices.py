gender_choices = (
    ('hombre','Hombre'),
    ('mujer','Mujer')
)
tipo_concepto_choice = (
    ('EN', 'Entrada'),
    ('SA', 'Salida'),
    ('TR', 'traslado'),
    ('DS', 'Desincorporación')
)
salida_grupo_bienes_choice = (
    ('BMS', 'Bienes Muebles'),
    ('MTC', 'Materiales de Consumo'),
    ('AMB', 'Ambos!'),
)

#Solicitud de Servicio Técnico
tipo_servicio_choices = (
    ('MP', 'Mantenimiento Preventivo'),
    ('MC', 'Mantenimiento Correctivo'),
    ('OT', 'Otros')
)
unidamedida_choice = (
    ('unidad', 'Unidad'),
    ('pieza', 'Pieza'),
    ('equipo', 'Equipo'),
    ('caja', 'Caja'),
    ('bulto', 'Bulto'),
    ('paquete', 'Paquete'),
    ('servicio', 'Servicio'),
    ('metro', 'Metro'),
    ('centimetro', 'Centimetro'),
    ('milimetro', 'Milimetro'),
    ('pulgada', 'Pulgada'),
    ('litro', 'Litro'),
    ('mililitro', 'Mililitro'),
    ('galon', 'Galon'),
    ('gramo', 'Gramo'),
    ('kilogramo', 'Kilogramo'),
    ('tonelada', 'Tonelada'),
    ('libra', 'Libra')
)
#estado del documento solo para q el analista seleccione estas dos, bien saea ingreso ó salida de producto
status_choices = (
    ('EN CREACIÓN','En creación'),
    ('POR APROBAR','Por aprobar'),    
)

#estado del documento con todas las opciones, bien saea ingreso ó salida de producto
# estadoDocutodos_choices = (
#     ('ANU','Anulado'), # distribucion anulada
#     ('ENT','Entregado'), # ya fue entregado
#     ('PEN','Por entregar'), # ya esta aprobado pero aun no se a entregado
#     ('PAP','Por aprobar'), # ya se envio por aprobacion pero aun no se a aprobado
#     ('DIS','En creación')  # la distribucion esta en diseño o en proceso
# )

#especialmente para las autoridades ò en cualquier otra necesidad
activo_choices = (
    ('ACT','Activo'), 
    ('INA','Inactivo')
)

estadoCodigobien_choices = (
    ('ASI','Asignado'),
    ('SAS','Sin asignar'),
    ('ANU','Anulado')
)

#tipo de ingreso
condicionproducto_choices = (
    ('BNO','Bueno'),
    ('REG','Regular'),
    ('MAL','Malo'),
    ('OTR','Especificar')
)

tipocomprobante_choices = (
    ('FAC','Factura'),
    ('NTD','Nota debito'),
    ('NTE','Nota entrega'),
    ('MEM','Memorandum')
)
tipounidad_choices = (
    ('UADMC','Unidad Administrativa Central'),
    ('UADML','Unidad Administrativa Local'),
    ('UASIC','Unidad ASIC'),
)

tipoproduc_choices = (
    ('BM','Bienes mueble de uso'),
    ('BI','Bienes inmueble'),
    ('MC','Material de consumo'),
    ('SV','Servicio')
)

#tipo de documento Idenbtificacion
tipodocuidentif_choices = (
    ('CED','Cédula'),
    ('PAS','Pasaporte'),
    ('RIF','Rif'),
    ('NIT','Nit')
)