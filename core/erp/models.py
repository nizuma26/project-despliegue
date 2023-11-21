from datetime import date, datetime
# Django
from django.db import models
from django.utils.text import capfirst
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from configuracion.settings import MEDIA_URL, STATIC_URL, AUTH_USER_MODEL
from core.erp.choices import *
from core.audit_log.mixins import AuditMixin
from django.forms import model_to_dict

#INVENTARIO
class Categoria(AuditMixin, models.Model):
    nombre = models.CharField(max_length=250, unique=True, verbose_name="Nombre de la categoria")    
 
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        ordering=['-id']
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class Marca(AuditMixin, models.Model):
    marca=models.CharField(max_length=100, unique=True, verbose_name='Marca')
    created=models.DateTimeField(auto_now_add=True, verbose_name='Creación')
    updated=models.DateTimeField(auto_now_add=True, verbose_name='Ultima modificación')
   
    def __str__(self):
        return f'{self.id} - {self.marca}'
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        ordering=['marca']
        verbose_name='Marca'
        verbose_name_plural='Marcas'

class Modelo(AuditMixin, models.Model):
    marcas=models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True, related_name='marca_model_set', verbose_name='Marca')
    modelo=models.CharField(max_length=100, unique=True, verbose_name='Modelo')
    created=models.DateTimeField(auto_now_add=True, verbose_name='Creación')
    updated=models.DateTimeField(auto_now_add=True, verbose_name='Ultima Modificación')    

    def toJSON(self):
        item = model_to_dict(self)
        item['marcas'] = self.marcas.toJSON()
        return item

    class Meta:
        ordering=['modelo']
        verbose_name='Modelo'
        verbose_name_plural='Modelos' 

    def __str__(self):
        return self.modelo
      
class Unidad(AuditMixin, models.Model):
    nombre=models.CharField(max_length=150, unique=True, verbose_name='Nombre Unidad')
    direccion=models.CharField(max_length=200, null=True, blank=True, verbose_name='Dirección')
    rif=models.CharField(max_length=12, unique=True, null=True, blank=True, verbose_name='Rif')
    ced_resp=models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name='Cedula')
    nombrejefe=models.CharField(max_length=150, null=True, blank=True, verbose_name='Nombre Responsable')
    email=models.EmailField(max_length=50, null=True, blank=True, verbose_name='Email')
    tlf=models.CharField(max_length=26, null=True, blank=True, verbose_name='Telefonos')
    tipo_unidad= models.CharField(max_length=25, choices=tipounidad_choices, null=True, blank=True, verbose_name='Tipo de Unidad')
    solic_almacen=models.BooleanField(default=True, max_length=4, null=True, blank=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} / {}'.format(self.nombre, self.rif)

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo_unidad'] = {'id': self.tipo_unidad, 'name': self.get_tipo_unidad_display()}
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
        ordering = ['id']

class Almacen(AuditMixin, models.Model):
    codigo=models.CharField(max_length=12, unique=True, null=True, blank=True, verbose_name='Código Almacen')
    nombre=models.CharField(max_length=150, unique=True, verbose_name='Nombre Almacen')
    unidad=models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name='prod_almacen_set', null=True, blank=True, verbose_name='Pertenece a:')
    cedula=models.CharField(max_length=10, null=True, blank=True, verbose_name='Cedula')
    responsable=models.CharField(max_length=150, null=True, blank=True,  verbose_name='Responsable Almacen')

    def __str__(self):
         return self.get_full_name()


    def get_full_name(self):
        return '{} - {}'.format(self.codigo, self.nombre)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['unidad'] = self.unidad.toJSON()
        item['full_name'] = self.get_full_name()
        return item


    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        ordering=['nombre']
        verbose_name='Almacen'
        verbose_name_plural='Almacenes'

class GrupoCtaBienes(AuditMixin, models.Model):
    cod_grupo=  models.CharField(max_length=3, blank=True, null=True, verbose_name='Grupo')
    nombre= models.CharField(max_length=50, blank=True, null=True, verbose_name='Nombre Grupo')

    def __str__(self):
       return self.get_full_name()

    def get_full_name(self):
        return '{}-{}'.format(self.cod_grupo, self.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Concepto de Grupo'
        verbose_name_plural = 'Concepto de Grupos'
        ordering = ['id']

class SubGrupoCtaBienes(AuditMixin, models.Model):
    grupo= models.ForeignKey(GrupoCtaBienes, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Grupo cuenta')
    subgrupo= models.CharField(max_length=3, blank=True, null=True, verbose_name='Subgrupo cuenta')
    seccion= models.CharField(max_length=3, blank=True, null=True, verbose_name='Sección cuenta')
    cod_grusubgrusec= models.CharField(max_length=11, blank=True, null=True, verbose_name='Auto Código ')
    denominacion= models.CharField(max_length=120, blank=True, null=True, verbose_name='Denominación')

    def __str__(self):
       return self.get_full_name()

    def get_full_name(self):
        return '{}-{}'.format(self.cod_grusubgrusec, self.denominacion)

    def toJSON(self):
        item = model_to_dict(self)
        item['grupo'] = self.grupo.toJSON()
        return item

    class Meta:
        verbose_name = 'Concepto de SubGrupo'
        verbose_name_plural = 'Concepto de SubGrupos'
        ordering = ['grupo']

class Moneda(AuditMixin, models.Model):
    codigo = models.CharField(max_length=4, unique=True, verbose_name="Código Moneda")
    pais = models.CharField(max_length=120, verbose_name="Pais de la Moneda")
    moneda = models.CharField(max_length=100, verbose_name="Nombre Moneda")
    simbolo = models.CharField(max_length=3, verbose_name='Símbolo')
    tasa_cambio = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Tasa de Cambio')
    status=models.BooleanField(default=True, max_length=4, null=True, blank=True, verbose_name='Activo')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
       return '{} - {} - {}'.format(self.codigo, self.moneda, self.pais)
    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        ordering=['moneda']
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"
        
class Producto(models.Model):
    codigo=models.CharField(max_length=10, null=True, blank=True, verbose_name='Código')
    nombre=models.CharField(max_length=100, verbose_name='Nombre Producto')
    descripcion=models.CharField(max_length=250, null=True, blank=True, verbose_name='Descripción')
    componentes=models.CharField(max_length=250, null=True, blank=True, verbose_name='Componentes')
    unida_medida=models.CharField(max_length=14, choices=unidamedida_choice, default='unidad', null=True, blank=True, verbose_name='Unidad Medida')  
    activo=models.BooleanField(default=1, null=True, blank=True, verbose_name='Activo')
    grupobien=models.ForeignKey(GrupoCtaBienes, on_delete=models.CASCADE, verbose_name='Grupo Bienes')
    subgrupobien=models.ForeignKey(SubGrupoCtaBienes, on_delete=models.CASCADE, verbose_name='Cuenta Bienes')
    imagen=models.ImageField(upload_to='producto/%Y/%m/%d', default='producto/sin_imagen_2.png', null=True, blank=True, verbose_name='Insertar Imagen')    
    categorias=models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='prod_categ_set', verbose_name='Categoria')
    pagaimpuesto=models.BooleanField(default=True, max_length=4, null=True, blank=True, verbose_name='Paga Impuesto')
    inventariable=models.BooleanField(null=True, blank=True, verbose_name='Inventariable')
    lote=models.BooleanField(null=True, blank=True, verbose_name='Usa Lote')
    serie=models.BooleanField(null=True, blank=True, verbose_name='Solicita Nro de Serie')
    marca=models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='prod_marca_set', verbose_name='Marca')
    modelo=models.ForeignKey(Modelo, on_delete=models.CASCADE, related_name='prod_modelo_set', verbose_name='Modelo')
    moneda=models.ForeignKey(Moneda, on_delete=models.CASCADE, null=True, blank=True, related_name='prod_moneda_set', verbose_name='Moneda')
    usuario=models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prod_user_set', verbose_name='Usuario')
  
    def __str__(self):
         return self.get_full_name()

    def get_full_name(self):
        return '{} - {}'.format(self.codigo, self.nombre)
    
    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'producto/sin_imagen_2.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = '{} / {}'.format(self.nombre, self.categorias.nombre)
        item['unida_medida'] = {'id': self.unida_medida, 'name': self.get_unida_medida_display()}        
        item['imagen'] = self.get_imagen()
        item['categorias'] = self.categorias.toJSON()
        item['marca'] = self.marca.toJSON()
        item['modelo'] = self.modelo.toJSON()
        item['moneda'] = self.moneda.toJSON()
        item['grupo bien'] = self.grupobien.toJSON()
        item['subgrupobien'] = self.subgrupobien.toJSON()
        item['usuario'] = self.usuario.toJSON()
        return item

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['id']

class ControlStock(models.Model):
    productos=models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    almacenes=models.ForeignKey(Almacen, default=1, on_delete=models.CASCADE, blank=True, null=True, related_name='prod_almacen_set')
    stock_actual=models.PositiveIntegerField(default=0, null=True, blank=True)
    apartados=models.PositiveIntegerField(default=0, null=True, blank=True)
    precio=models.DecimalField(max_digits=14, decimal_places=2, default=0.00, null=True, blank=True)
    stock_min=models.PositiveIntegerField(default=0, null=True, blank=True)
    stock_max=models.PositiveIntegerField(default=0, null=True, blank=True)  

    def __str__(self):
        return self.almacenes.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['productos'] = self.productos.toJSON()
        item['almacenes'] = self.almacenes.toJSON()
        item['stock_actual'] = format(self.stock_actual, '.2f')
        item['precio'] = format(self.precio, '.2f')
        item['stock_min'] = format(self.stock_min, '.2f')
        item['stock_max'] = format(self.stock_max, '.2f')
        return item

    class Meta:
        verbose_name = "Control de Stock"
        verbose_name_plural = "Control de los Stock"
        ordering = ['id'] 

class Proveedor(AuditMixin, models.Model):
    empresa = models.CharField(max_length=150, verbose_name='Nombres Empresa')
    tipo_docu = models.CharField(max_length=3, choices=tipodocuidentif_choices, default='RIF', verbose_name='Tipo Documento')
    documento = models.CharField(max_length=14, unique=True, verbose_name='Documento')
    ramo = models.CharField(max_length=150, null=True, blank=True, verbose_name='Ramo - Dedicación')
    ced_repre=models.CharField(max_length=10, null=True, blank=True, verbose_name='Cedula representante')
    represen=models.CharField(max_length=150, null=True, blank=True, verbose_name='Representante de Negocio')
    tlf=models.CharField(max_length=26, null=True, blank=True, verbose_name='Telefonos')
    email=models.EmailField(max_length=50, null=True, blank=True, verbose_name='Email')
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} / {}'.format(self.empresa, self.ramo)

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo_docu'] = {'id': self.tipo_docu, 'name': self.get_tipo_docu_display()}
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']

class CodBienes(AuditMixin, models.Model):
    codbien=models.CharField(max_length=80, unique=True)    
    estado= models.CharField(max_length=12, choices=estadoCodigobien_choices, default='SAS', null=True, blank=True)   

    def toJSON(self):
        item = model_to_dict(self)
        item['estado'] = {'id': self.estado, 'name': self.get_estado_display()}
        return item

    class Meta:
        ordering=['codbien']
        verbose_name='Código de Bien'
        verbose_name_plural='Código de Bienes'

    def __str__(self):
         return self.codbien

class Departamento(AuditMixin, models.Model):
    nombre = models.CharField(max_length=250, unique=True, verbose_name="Nombre del Departamento")    
 
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        ordering=['nombre']
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

class ConcepMovimiento(AuditMixin, models.Model):
    codigo= models.CharField(max_length=3, unique=True, blank=True, null=True, verbose_name='Código')
    denominacion = models.CharField(max_length=120, blank=True, null=True, verbose_name='Denominación')
    estado= models.CharField(max_length=3, choices=activo_choices, default='ACT', null=True, blank=True, verbose_name='Estado del Concepto')
    tipo_conc= models.CharField(max_length=2, choices=tipo_concepto_choice, null=True, blank=True, verbose_name='Tipo de Movimiento')
    salida_bienes= models.CharField(max_length=6, choices=salida_grupo_bienes_choice, null=True, blank=True, verbose_name='Bienes que Despacha')   

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} - {}'.format(self.codigo, self.denominacion)

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo_conc'] = {'id': self.tipo_conc, 'name': self.get_tipo_conc_display()}
        item['tipo_bienes'] = {'id': self.salida_bienes, 'name': self.get_salida_bienes_display()}
        item['estado'] = {'id': self.estado, 'name': self.get_estado_display()}
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Concepto Movimiento'
        verbose_name_plural = 'Concepto Movimientos'
        ordering = ['codigo']

#MOVIMIENTOS
class SalidaProduc(models.Model):
    cod_salida= models.CharField(max_length=14, blank=True, null=True)
    origen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True, related_name='salidaproduc_almacen_set')
    respon_origen=models.CharField(max_length=120, null=True, blank=True)
    destino = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True, related_name='salidaproduc_destino_set')
    respon_destino=models.CharField(max_length=120, null=True, blank=True)
    tipo_salida= models.ForeignKey(ConcepMovimiento, on_delete=models.CASCADE)
    tipo_comprob = models.CharField(max_length=3, null=True, blank=True, choices=tipocomprobante_choices)
    num_comprob= models.CharField(max_length=24, null=True, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=14, decimal_places=2)
    iva = models.DecimalField(default=0.16, max_digits=14, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=14, decimal_places=2)
    fecha_salida = models.DateField(default=datetime.now)
    usuario=models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='salidaproduc_user_set')
    observ=models.CharField(max_length=200, null=True, blank=True)
    estado= models.CharField(max_length=25, choices=status_choices, default='EN CREACIÓN')
    
    def __str__(self):
        return self.destino.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['origen'] = self.origen.toJSON()
        item['destino'] = self.destino.toJSON()
        item['tipo_salida'] = self.tipo_salida.toJSON()
        item['tipo_comprob'] = {'id': self.tipo_comprob, 'name': self.get_tipo_comprob_display()}
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha_salida'] = self.fecha_salida.strftime('%Y-%m-%d')
        item['usuario'] = self.usuario.toJSON()
        item['estado'] = {'id': self.estado, 'name': self.get_estado_display()}
        item['det'] = [i.toJSON() for i in self.detsalidaprod_salida_set.all()]
        item['det_insumos'] = [i.toJSON() for i in self.det_salidainsumos_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detsalidaprod_salida_set.all():
            det.codbien.estado = 'SAS'
            det.codbien.save()
        super(SalidaProduc, self).delete()

    class Meta:
        verbose_name = 'Distribución de Producto'
        verbose_name_plural = 'Distribuciones de producto'
        ordering = ['id']

class DetSalidaProd(models.Model):
    salida = models.ForeignKey(SalidaProduc, on_delete=models.CASCADE, blank=True, null=True, related_name='detsalidaprod_salida_set', verbose_name='Código distribución')
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True, related_name='detsalidaprod_prod_set', verbose_name='Producto')
    codbien = models.ForeignKey(CodBienes, on_delete=models.CASCADE, blank=True, null=True, related_name='detsalidaprod_codbien_set', verbose_name='Código Bien')
    codubica = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=True, null=True, related_name='detsalidaprod_ubicafisi_set',verbose_name='Código ubicación')
    precio = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Precio')
    cant =  models.IntegerField(default=1.00, verbose_name='Cantidad')
    subtotal = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Sub total')

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['salida'])
        item['prod'] = self.prod.toJSON()
        item['codbien'] = self.codbien.toJSON()
        item['codubica'] = self.codubica.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['cant'] = format(self.cant, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Distribución'
        verbose_name_plural = 'Detalle de Distribuciónes'
        ordering = ['id']

class DetSalidaInsumos(models.Model):
    salida = models.ForeignKey(SalidaProduc, on_delete=models.CASCADE, blank=True, null=True, related_name='det_salidainsumos_set', verbose_name='Código distribución')
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True, related_name='det_salidainsumos_prod_set', verbose_name='Producto')
    nro_lote = models.CharField(max_length=20, null=True, blank=True, verbose_name='Número de Lote')
    fecha_venc = models.DateField(blank=True, null=True, verbose_name='Fecha de vencimiento')
    precio = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Precio')
    cant =  models.IntegerField(default=0.00, verbose_name='Cantidad')
    subtotal = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Sub total')

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['salida'])
        item['prod'] = self.prod.toJSON()        
        item['precio'] = format(self.precio, '.2f')
        item['cant'] = format(self.cant, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle Distribución de Suministros'
        verbose_name_plural = 'Detalle Distribuciónes de Suministros'
        ordering = ['id']

class IngresoProduc(models.Model):
    cod_ingreso= models.CharField(max_length=14, blank=True, null=True, verbose_name='Código ingreso')
    almacen=models.ForeignKey(Almacen, on_delete=models.CASCADE, related_name='ingresoproduc_almacen_set', verbose_name='Almacen')
    respon_almac=models.CharField(max_length=120, null=True, blank=True, verbose_name='Responsable Almacén')
    tipo_ingreso= models.ForeignKey(ConcepMovimiento, on_delete=models.CASCADE, verbose_name='Tipo ingreso')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, blank=True, null=True, related_name='ingresoproduc_prod_set', verbose_name='Proveedor')
    tipo_comprob = models.CharField(max_length=3, choices=tipocomprobante_choices, verbose_name='Tipo comprobante')
    num_comprob= models.CharField(max_length=24, unique=True, verbose_name='Numero Comprobante')
    subtotal = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Sub total')
    iva = models.DecimalField(default=0.16, max_digits=14, decimal_places=2, verbose_name='Impuesto IVA')
    total = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Total')
    fecha_ingreso = models.DateField(default=datetime.now, verbose_name='Fecha ingreso')
    usuario=models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='ingresoproduc_user_set', verbose_name='Usuario')
    observ=models.CharField(max_length=200, null=True, blank=True, verbose_name='Observación')
    estado= models.CharField(max_length=25, choices=status_choices, default='EN CREACIÓN')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} - {}'.format(self.cod_ingreso, self.almacen.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo_ingreso'] = self.tipo_ingreso.toJSON()        
        item['tipo_comprob'] = {'id': self.tipo_comprob, 'name': self.get_tipo_comprob_display()}
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['almacen'] = self.almacen.toJSON()
        item['fecha_ingreso'] = self.fecha_ingreso.strftime('%Y-%m-%d')
        item['usuario'] = self.usuario.toJSON()
        item['estado'] = {'id': self.estado, 'name': self.get_estado_display()}
        item['det'] = [i.toJSON() for i in self.detingresoproduc_ingresopro_set.all()]
        if self.proveedor:
            item['proveedor'] = self.proveedor.toJSON()
        else:
            item['proveedor'] = None
        return item
    # a traves de su relate_name creado por el programador ó el creado automaticamente por django
    # en el  video 64 minuto 11:16 describe como hacerlo 

    # def delete(self, using=None, keep_parents=False):
    #     for det in self.detingresoproduc_ingresopro_set.all():
    #         det.prod.stock_actual -= det.cant
    #         det.prod.save()
    #     super(IngresoProduc, self).delete()

    class Meta:
        verbose_name = 'Incorporación'
        verbose_name_plural = 'Incorporaciones'
        ordering = ['id']

class DetIngresoProduc(models.Model):
    ingresoPro = models.ForeignKey(IngresoProduc, on_delete=models.CASCADE, blank=True, null=True, related_name='detingresoproduc_ingresopro_set', verbose_name='Código distribución')
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True, related_name='detingresoproduc_prod_set', verbose_name='Producto')
    precio = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Precio del Producto')
    cant = models.IntegerField(default=0.00, verbose_name='Cantidad')
    iva = models.DecimalField(default=0.16, max_digits=14, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Sub total')

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['ingresoPro'])
        item['prod'] = self.prod.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['cant'] = format(self.cant, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Ingreso'
        verbose_name_plural = 'Detalle de Ingresos'
        ordering = ['id']

class TrasladoProduc(models.Model):
    cod_traslado= models.CharField(max_length=14, blank=True, null=True, verbose_name='Código Traslado')
    origen = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True, related_name='trasproducorigen_set', verbose_name='Origen Traslado')
    respon_origen=models.CharField(max_length=120, null=True, blank=True, verbose_name='Responsable Origen')
    destino = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True, related_name='trasprodubicfisdestino_set', verbose_name='Destino Producto')
    respon_destino=models.CharField(max_length=120, null=True, blank=True, verbose_name='Responsable Destino')
    tipo_traslado= models.ForeignKey(ConcepMovimiento, on_delete=models.CASCADE, verbose_name='Tipo de Traslado')
    fecha_traslado = models.DateField(default=datetime.now, verbose_name='Fecha traslado')
    usuario=models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='trasprod_user_set', verbose_name='Usuario')
    observ=models.CharField(max_length=250, null=True, blank=True, verbose_name='Observación')
    estado= models.CharField(max_length=25, choices=status_choices, default='POR APROBAR')
    soportedocum=models.FileField(upload_to='documsoporte/trasladoEquipo/', default='documsoporte/trasladoEquipo/uploadfile.png', null=True, blank=True, verbose_name='Subir Documento')
    salida = models.ForeignKey(SalidaProduc, on_delete=models.CASCADE, blank=True, null=True, related_name='trasSalproduc_set')
   # objects = SaleManager()

    def __str__(self):
        return self.destino.nombre
    
    # def get_soportedocum(self):
    #     if self.soportedocum:
    #         return '{}{}'.format(MEDIA_URL, self.soportedocum)
    #     return '{}{}'.format(STATIC_URL, 'documsoporte/trasladoEquipo/uploadfile.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['origen'] = self.origen.toJSON()
        item['destino'] = self.destino.toJSON()
        item['salida'] = self.salida.toJSON()
        item['tipo_traslado'] = self.tipo_traslado.toJSON()
        item['fecha_traslado'] = self.fecha_traslado.strftime('%Y-%m-%d')
        item['usuario'] = self.usuario.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')        
        # item['soportedocum'] = self.get_soportedocum()
        item['det'] = [i.toJSON() for i in self.dettrasprod_traslado_set.all()]
        return item

    class Meta:
        verbose_name = 'Traslado de Producto'
        verbose_name_plural = 'Traslado de productos'
        ordering = ['id']

class DetTrasladoProd(models.Model):
    trasproduc = models.ForeignKey(TrasladoProduc, on_delete=models.CASCADE, blank=True, null=True, related_name='dettrasprod_traslado_set', verbose_name='Código transferencia')
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True, related_name='dettrasprod_prod_set', verbose_name='Producto')
    codbien = models.ForeignKey(CodBienes, on_delete=models.CASCADE, blank=True, null=True, related_name='dettrasprod_codbien_set', verbose_name='Código Bien')    
    codubica = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=True, null=True, related_name='dettras_ubicorigen_set',verbose_name='Ubicación origen')
    ubica_destino = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=True, null=True, related_name='dettras_ubicdestino_set',verbose_name='Ubicación destino')

    #objects = SaleDetailManager()

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['trasproduc'])
        item['prod'] = self.prod.toJSON()
        item['codbien'] = self.codbien.toJSON()        
        item['codubica'] = self.codubica.toJSON()
        item['ubica_destino'] = self.ubica_destino.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle de traslado'
        verbose_name_plural = 'Detalle de traslados'
        ordering = ['id']

class DesincProduc(models.Model):
    cod_desinc= models.CharField(max_length=14, blank=True, null=True, verbose_name='Código desincorporación')
    origen = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True, related_name='desincproduc_unidad_set', verbose_name='Origen desincorporación')
    respon_origen=models.CharField(max_length=120, null=True, blank=True, verbose_name='Responsable Origen')
    tipo_desinc = models.ForeignKey(ConcepMovimiento, on_delete=models.CASCADE, related_name='tipo_desincorp_set', verbose_name='Tipo desincorporación')
    fecha_desinc = models.DateField(default=datetime.now, verbose_name='Fecha desincorporación')
    usuario=models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='desincproduc_user_set', verbose_name='Usuario')
    observ=models.CharField(max_length=200, null=True, blank=True, verbose_name='Observación')
    estado= models.CharField(max_length=25, choices=status_choices, default='EN CREACIÓN')
    soportedocum=models.FileField(upload_to='desincorporacionEquipo/', default='desincorporacionEquipo/uploadfile.png', null=True, blank=True, verbose_name='Subir Documento')

    def __str__(self):
        return self.origen.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['origen'] = self.origen.toJSON()
        item['tipo_desinc'] = self.tipo_desinc.toJSON()       
        item['fecha_desinc'] = self.fecha_salida.strftime('%Y-%m-%d')
        item['usuario'] = self.usuario.toJSON()
        item['estado'] = {'id': self.estado, 'name': self.get_estado_display()}
        item['det'] = [i.toJSON() for i in self.detdesincprod_desinc_set.all()]
        return item

    # def delete(self, using=None, keep_parents=False):
    #     for det in self.detdesincprod_desinc_set.all():
    #         det.prod.stock_actual -= det.cant
    #         det.prod.save()
    #     super(DesincProduc, self).delete()

    class Meta:
        verbose_name = 'Desincorporación de Producto'
        verbose_name_plural = 'Desincorporaciones de producto'
        ordering = ['id']

class DetDesincProd(models.Model):
    desinc = models.ForeignKey(DesincProduc, on_delete=models.CASCADE, blank=True, null=True, related_name='detdesincprod_desinc_set', verbose_name='Código desincorporación')
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True, related_name='detdesincprod_prod_set', verbose_name='Producto')
    codbien = models.ForeignKey(CodBienes, on_delete=models.CASCADE, blank=True, null=True, related_name='detdesincprod_codbien_set', verbose_name='Código Bien')
    codubica = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=True, null=True, related_name='detdesincprod_ubicafisi_set',verbose_name='Código ubicación')
    precio = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Precio')
    subtotal = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Sub total')

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['desinc'])
        item['prod'] = self.prod.toJSON()
        item['codbien'] = self.codbien.toJSON()
        item['codubica'] = self.codubica.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Desincorporación'
        verbose_name_plural = 'Detalle de Desincorporaciones'
        ordering = ['id']

class DesincAlmacen(models.Model):
    cod_desinc= models.CharField(max_length=14, blank=True, null=True, verbose_name='Código desincorporación')
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True, related_name='desincproduc_almacen_set', verbose_name='Ubicación desincorporación')
    respon_almac=models.CharField(max_length=120, null=True, blank=True, verbose_name='Responsable Almacén')
    tipo_desinc = models.ForeignKey(ConcepMovimiento, on_delete=models.CASCADE, related_name='tipo_desinc_set',  verbose_name='Tipo desincorporación')
    subtotal = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Sub total')
    iva = models.DecimalField(default=0.16, max_digits=14, decimal_places=2, verbose_name='Impuesto IVA')
    total = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Total')
    fecha_desinc = models.DateField(default=datetime.now, verbose_name='Fecha desincorporación')
    usuario=models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='desincalmacen_user_set', verbose_name='Usuario')
    observ=models.CharField(max_length=200, null=True, blank=True, verbose_name='Observación')
    estado= models.CharField(max_length=25, choices=status_choices, default='EN CREACIÓN')
    soportedocum=models.FileField(upload_to='desincorporacionEquipo/', default='desincorporacionEquipo/uploadfile.png', null=True, blank=True, verbose_name='Subir Documento')

    def __str__(self):
        return self.almacen.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['almacen'] = self.almacen.toJSON()
        item['tipo_desinc'] = self.tipo_desinc.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha_desinc'] = self.fecha_desinc.strftime('%Y-%m-%d')
        item['usuario'] = self.usuario.toJSON()
        item['estado'] = {'id': self.estado, 'name': self.get_estado_display()}
        item['det'] = [i.toJSON() for i in self.detdesinc_almacen_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detdesinc_almacen_set.all():
            det.prod.stock_actual += det.cant
            det.prod.save()
        super(DesincAlmacen, self).delete()


    class Meta:
        verbose_name = 'Desincorporación de Producto en almacen'
        verbose_name_plural = 'Desincorporaciones de producto en almacen'
        ordering = ['id']

class DetDesincAlmacen(models.Model):
    desincorp = models.ForeignKey(DesincAlmacen, on_delete=models.CASCADE, blank=True, null=True, related_name='detdesinc_almacen_set', verbose_name='Código desincorporación')
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True, related_name='detdesincprod_almacen_set', verbose_name='Producto')
    precio = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Precio')
    cant = models.IntegerField(default=0.00, verbose_name='Cantidad')
    subtotal = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Sub total')

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['desincorp'])
        item['prod'] = self.prod.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['cant'] = format(self.cant, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Desincorporación de Almacen'
        verbose_name_plural = 'Detalle de Desincorporaciones de Almacen'
        ordering = ['id']

#SERIALES Y LOTES
class Seriales(models.Model):
    stock = models.ForeignKey(ControlStock, on_delete=models.CASCADE, null=True, blank=True, related_name='stock_serial_set')
    incorp = models.ForeignKey(IngresoProduc, on_delete=models.CASCADE, null=True, blank=True, related_name='incorp_serial_set')
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True, related_name='prod_serial_set')
    disp = models.CharField(max_length=25, blank=True, null=True, verbose_name='Disponibilidad')
    serial = models.CharField(max_length=120, blank=True, null=True, verbose_name='Serial')

    def __str__(self):
        return self.serial

    def toJSON(self):
        item = model_to_dict(self)        
        item['stock'] = self.stock.toJSON()
        item['incorp'] = self.incorp.toJSON()
        item['prod'] = self.prod.toJSON()
        return item

    class Meta:
        verbose_name = "Serial de Producto"
        verbose_name_plural = "Seriales de Productos"
        ordering = ['id']

class Lotes(models.Model):
    stock = models.ForeignKey(ControlStock, on_delete=models.CASCADE, null=True, blank=True, related_name='stock_lote_set')    
    incorp = models.ForeignKey(IngresoProduc, on_delete=models.CASCADE, null=True, blank=True, related_name='incorp_lote_set')
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True, related_name='prod_lote_set')
    nro_lote = models.CharField(max_length=120, blank=True, null=True, verbose_name='Número de lote')
    fecha_venc = models.DateField(blank=True, null=True, verbose_name='Fecha de vencimiento')

    def __str__(self):
        return self.nro_lote

    def toJSON(self):
        item = model_to_dict(self)        
        item['stock'] = self.stock.toJSON()
        item['incorp'] = self.incorp.toJSON()
        item['prod'] = self.prod.toJSON()
        item['fecha_venc'] = self.fecha_venc.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = "Número de Lote del Producto"
        verbose_name_plural = "Números de Lote de Productos"
        ordering = ['id']

class InventarioBienes(models.Model):
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True, related_name='unida_invbienes_set', verbose_name='Unidad')
    ubica_fisica = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=True, null=True, related_name='ubica_invbienes_set',verbose_name='Ubicación del Bien')
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True, related_name='prod_invbienes_set', verbose_name='Producto')
    codbien = models.ForeignKey(CodBienes, on_delete=models.CASCADE, blank=True, null=True, related_name='codbien_invbienes_set', verbose_name='Código Bien')
    ult_proc=models.CharField(max_length=120, null=True, blank=True, verbose_name='Ultimo Proceso')
    tipo_proc = models.ForeignKey(ConcepMovimiento, on_delete=models.CASCADE, null=True, blank=True, related_name='tipo_proc_invbienes_set', verbose_name='Tipo de entrada')
    salida = models.ForeignKey(SalidaProduc, on_delete=models.CASCADE, blank=True, null=True, related_name='invBienesSalproduc_set')
    date_joined = models.DateField(default=datetime.now)
    created=models.DateTimeField(auto_now_add=True, verbose_name='Creación')
    updated=models.DateTimeField(auto_now_add=True, verbose_name='Última actualización')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} / {}'.format(self.unidad.nombre, self.ubica_fisica.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['unidad'] = self.unidad.toJSON()
        item['ubica_fisica'] = self.ubica_fisica.toJSON()
        item['prod'] = self.prod.toJSON()
        item['salida'] = self.salida.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['codbien'] = self.codbien.toJSON()
        item['tipo_proc'] = self.tipo_proc.toJSON()
        return item

    class Meta:
        verbose_name = 'Inventario de Bien'
        verbose_name_plural = 'Inventario de Bienes'
        ordering = ['id']

#Configuración
class Empresa(models.Model):
    codigo = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name="Código Empresa")
    nombre = models.CharField(max_length=250, unique=True, verbose_name="Nombre Empresa ó Institución")
    tipo_docu=models.CharField(max_length=3, choices=tipodocuidentif_choices, null=True, blank=True, default='RIF', verbose_name='Tipo Documento')
    documento=models.CharField(max_length=14, verbose_name='Documento')
    dedicacion=models.CharField(max_length=150, null=True, blank=True, verbose_name='Ramo - Dedicación')
    tlflocal=models.CharField(max_length=26, null=True, blank=True, verbose_name='Telefono Local')
    tlfmovil=models.CharField(max_length=26, null=True, blank=True, verbose_name='Telefono Movil')
    email=models.EmailField(max_length=70, null=True, blank=True, verbose_name='Email')
    web=models.EmailField(max_length=70, null=True, blank=True, verbose_name='Pagina Web')
    instagram=models.EmailField(max_length=70, null=True, blank=True, verbose_name='Instagram')
    facebook=models.EmailField(max_length=70, null=True, blank=True, verbose_name='Facebook')
    telegram=models.EmailField(max_length=70, null=True, blank=True, verbose_name='Telegram')
    whatsapp=models.EmailField(max_length=70, null=True, blank=True, verbose_name='Whatsapp')
    twitter=models.EmailField(max_length=70, null=True, blank=True, verbose_name='Twitter')
    mision=models.CharField(max_length=250, unique=True, blank=True, null=True, verbose_name="Mision")
    vision=models.CharField(max_length=250, unique=True, blank=True, null=True, verbose_name="Vision")
    direccion=models.CharField(max_length=200, null=True, blank=True, verbose_name='Dirección')
    logo=models.ImageField(upload_to='empresa', default='empresa/newlogompps.png', null=True, blank=True, verbose_name='Insertar Imagen')
    representante=models.CharField(max_length=150, null=True, blank=True, verbose_name="Nombre del representante")
    ced_repre=models.CharField(max_length=10, null=True, blank=True, verbose_name='Cédula representante')
    cuentadante=models.CharField(max_length=150, null=True, blank=True, verbose_name="Nombre del cuentadante")
    ced_ctadante=models.CharField(max_length=10, null=True, blank=True, verbose_name='Cédula cuentadante')
    nameimpuesto=models.CharField(max_length=12, null=True, blank=True, verbose_name='Nombre Impuesto')
    iva=models.DecimalField(max_digits=4, decimal_places=2, default=0.00, null=True, blank=True, verbose_name="Porcentaje Impuesto")
    almacen_principal = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True, related_name='empresa_almacen_set')
    created=models.DateTimeField(auto_now_add=True, verbose_name='Creación')
    updated=models.DateTimeField(auto_now_add=True, verbose_name='Última actualización')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{}'.format(self.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['tipo_docu'] = {'id': self.tipo_docu, 'name': self.get_tipo_docu_display()}
        item['logo'] = self.get_logo()
        item['iva'] = format(self.iva, '.2f')
        return item

    def get_logo(self):
        if self.logo:
            return '{}{}'.format(MEDIA_URL, self.logo)
        return '{}{}'.format(STATIC_URL, 'empresa/newlogompps.png')

    class Meta:
        ordering=['nombre']
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        