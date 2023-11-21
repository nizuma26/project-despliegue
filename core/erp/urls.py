from django.urls import path
from core.erp.views.category.views import *
from core.erp.views.marca.views import *
from core.erp.views.modelo.views import *
from core.erp.views.product.views import *
from core.erp.views.control_stock.views import *
from core.erp.views.ingresos_prod.views import *
from core.erp.views.salidas_prod.salidas.views import *
from core.erp.views.unidad.views import *
from core.erp.views.depart.views import *
from core.erp.views.almacen.views import *
from core.erp.views.grupo.views import *
from core.erp.views.subgrupo.views import *
from core.erp.views.traslados_prod.views import *
from core.erp.views.codbienes.views import *
from core.erp.views.desincorp.views import *
from core.erp.views.desincorp.desinc.views import *
from core.erp.views.concepmov.views import *
from core.erp.views.proveedor.views import *
from core.erp.views.empresa.views import *
from core.erp.views.respaldo_bd.views import *
from core.erp.views.servicio_tecnico.views import *
from core.erp.views.monedas.views import *

app_name = 'erp'

urlpatterns = [
    # product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    # control de stock
    path('stock/list/', StockListView.as_view(), name='stock_list'),

    # category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
     # marca
    path('marca/list/', MarcaListView.as_view(), name='marca_list'),
    # modelo
    path('modelo/list/', ModeloListView.as_view(), name='modelo_list'),

    # almacen
    path('almacen/list/', AlmacenListView.as_view(), name='almacen_list'),

    # grupo
    path('grupo/list/', GrupoListView.as_view(), name='grupo_list'),

    # subgrupo
    path('subgrupo/list/', SubGrupoListView.as_view(), name='subgrupo_list'),

    # codigo de bienes
    path('codbien/list/', CodBienListView.as_view(), name='codbien_list'),

    # salidas de productos
    path('salida/list/', SalidaListView.as_view(), name='salida_list'),
    path('salida/add/', SalidaCreateView.as_view(), name='salida_create'),
    path('salida/detail/<int:pk>/', SalidaDetailView.as_view(), name='salida_detail'),
    path('salida/update/<int:pk>/', SalidaUpdateView.as_view(), name='salida_update'),
    path('salida/factura/pdf/<int:pk>/', SalidaFacturaPdfView.as_view(), name='salida_factura_pdf'),
    path('salida/solicitud/<int:pk>/', SalidaSolicitudView.as_view(), name='salida_solicitud'),

    # ingresos de productos
    path('ingreso/list/', IngresoListView.as_view(), name='ingreso_list'),
    path('ingreso/add/', IngresoCreateView.as_view(), name='ingreso_create'),
    path('ingreso/detail/<int:pk>/', IncorpDetailView.as_view(), name='ingreso_detail'),
    path('ingreso/update/<int:pk>/', IngresoUpdateView.as_view(), name='ingreso_update'),
    path('ingreso/factura/pdf/<int:pk>/', IngresoFacturaPdfView.as_view(), name='ingreso_factura_pdf'),

    # traslados de productos
    path('traslado/list/', TrasladoListView.as_view(), name='traslado_list'),
    path('traslado/add/', TrasladoCreateView.as_view(), name='traslado_create'),
    path('traslado/update/<int:pk>/', TrasladoUpdateView.as_view(), name='traslado_update'),
    path('traslado/factura/pdf/<int:pk>/', TrasladoFacturaPdfView.as_view(), name='traslado_factura_pdf'),
    path('traslado/solicitud/<int:pk>/', TrasladoSolicitudView.as_view(), name='traslado_solicitud'),

     # desicorporación de productos en unidad
    path('desinc/list/', DesincListView.as_view(), name='desinc_list'),
    path('desinc/add/', DesincCreateView.as_view(), name='desinc_create'),
    path('desinc/update/<int:pk>/', DesincUpdateView.as_view(), name='desinc_update'),
    path('desinc/factura/pdf/<int:pk>/', DesincFacturaPdfView.as_view(), name='desinc_factura_pdf'),

    # desicorporación de productos en almacen
    path('desincorp/list/', DesincorpListView.as_view(), name='desincorp_list'),
    path('desincorp/add/', DesincorpCreateView.as_view(), name='desincorp_create'),
    path('desincorp/update/<int:pk>/', DesincorpUpdateView.as_view(), name='desincorp_update'),
    path('desincorp/factura/pdf/<int:pk>/', DesincorpFacturaPdfView.as_view(),name='desincorp_factura_pdf'),
    
     # unidad  - dependencias
    path('unidad/list/', UnidadListView.as_view(), name='unidad_list'),
    
    # Departamento
    path('depart/list/', DepartListView.as_view(), name='depart_list'),

    # Proveedores
    path('proveedor/list/', ProveedorListView.as_view(), name='proveedor_list'),

  # Conceptos
    path('concepto/list/', ConcepMovListView.as_view(), name='concepto_list'),

    #Empresa
    path('empresa/list/', EmpresaListView.as_view(), name='empresa_list'),
    path('empresa/update/', EmpresaUpdateView.as_view(), name='empresa_update'),

    #Respaldo bd
    path('respaldo_bd/', RespaldoDB.as_view(), name="respaldo_db"),
    path('respaldar_bd/', RespaldarBD.as_view(), name="respaldar_db"),
    
    #Servicio Tecnico
    path('recepcion_soporte/list/', SoporteListView.as_view(), name="soporte_list"),   
    path('recepcion_soporte/create/', SoporteCreateView.as_view(), name="soporte_create"), 

    # Monedas
    path('monedas/list/', MonedaListView.as_view(), name='monedas_list'),  
]
 