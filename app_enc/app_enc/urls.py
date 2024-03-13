"""
URL configuration for app_enc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .view.view_nc_punto_venta import ViewNCPDV
from .view.view_nc_financiero import ViewNCFinanciero
from .view.view_nc_servicios import ViewNCServicios
from .view.view_nota_credito import ViewNotaCredito
from .view.validation_view import ValidationView
from .view.download_view import DownloadView

urlpatterns = [
    ## Path Index
    path('', views.index),
    
    ## Path View Solicitudes
    path('solicitud_nota_credito/punto_venta/', ViewNCPDV.notaPDV,name="new_nc_pdv"),
    path('solicitud_nota_credito/financieros/', ViewNCFinanciero.notaFinanciero),
    path('solicitud_nota_credito/servicios/', ViewNCServicios.notaServicios),
    # Get Datos Solicitud
    path('solicitud_nota_credito/datos_solicitud/<int:sol_id>', ViewNCPDV.get_datos_solicitud),
    ###
    
    ## Path View Consolidacion
    path('consolidacion_nota_credito/punto_venta/', ViewNCPDV.cnotaPDV),
    path('consolidacion_nota_credito/financieros/', ViewNCFinanciero.cnotaFinanciero),
    path('consolidacion_nota_credito/servicios/', ViewNCServicios.cnotaServicios),
    ###
    
    ## Path View Edit Consolidacion
    path('solicitud_nota_credito/punto_venta/edit/<int:id>/<int:id_product>/', ViewNCPDV.notaPDVEdit,name="new_nc_pdv"),
    path('solicitud_nota_credito/financieros/edit/<int:id>/', ViewNCFinanciero.notaFinancieroEdit),
    path('solicitud_nota_credito/servicios/edit/<int:id>/', ViewNCServicios.notaServiciosEdit),
    ##
    
    
    ## Path Delete Consolidacion
    path('solicitud_nota_credito/punto_venta/delete/', ViewNCPDV.delete_consolidado,name="new_nc_pdv"),
    path('solicitud_nota_credito/financieros/delete/', ViewNCFinanciero.delete_consolidado),
    path('solicitud_nota_credito/servicios/delete/', ViewNCServicios.delete_consolidado),
    ##
     
    ## Path View Bandeja
    path('bandeja_nota_credito/punto_venta/', ViewNCPDV.bnotaPDV),
    path('bandeja_nota_credito/financieros/', ViewNCFinanciero.bnotaFinanciero),
    path('bandeja_nota_credito/servicios/', ViewNCServicios.bnotaServicios),
    ###
    
    ## Path View validacion Consolidacion
    path('solicitud_nota_credito/validar_comprobante/', ValidationView.validar_comprobante,name="new_nc_pdv"),
    path('solicitud_nota_credito/validar_comprobantes/', ValidationView.validar_comprobantes),
    path('solicitud_nota_credito/validar_notas/', ValidationView.validar_notas),
    path('solicitud_nota_credito/financieros/validar/', ViewNCFinanciero.validar_solicitud),
    path('solicitud_nota_credito/servicios/validar/', ViewNCServicios.notaServiciosEdit),
    ##

    ## Create Solicitud Nota de Credito
    path('solicitud_nota_credito/punto_venta/create/', ViewNCPDV.create_solicitud_pdv),
    path('solicitud_nota_credito/financieros/create/', ViewNCFinanciero.create_solicitud_financieras),
    path('solicitud_nota_credito/servicios/create/', ViewNCServicios.create_solicitud_servicios),
    ###
    
    ## Create Observacion
    path('solicitud_nota_credito/punto_venta/observacion/', ViewNCPDV.observar_solicitud_pdv),
    path('solicitud_nota_credito/financieros/observacion/', ViewNCFinanciero.observar_solicitud),
    path('solicitud_nota_credito/servicios/observacion/', ViewNCServicios.observar_solicitud),
    
    ## Update NC
    path('solicitud_nota_credito/punto_venta/edit/', ViewNCPDV.edit_solicitud_pdv),
    path('solicitud_nota_credito/financieros/edit/', ViewNCFinanciero.edit_solicitud_financieras),
    path('solicitud_nota_credito/servicios/edit/', ViewNCServicios.edit_solicitud_servicios),
    ##

    ## Create Nota de Credito
    path('nota_credito/punto_venta/create/', ViewNotaCredito.create_nota_credito),
    path('nota_credito/punto_venta/create_all/', ViewNotaCredito.create_all_notas_credito),
    path('nota_credito/punto_venta/retry/', ViewNotaCredito.retry_create_nota_credito),
    path('nota_credito/download/<str:nro_nota_credito>', DownloadView.getTxt),
    
    ## Get Datos Comprobante
    path('comprobante/get_datos_comprobante/<str:nro_comprobante>', ViewNCPDV.get_sales_invoice),
    path('comprobante/detalle_comprobante/<str:nro_comprobante>', ViewNCPDV.get_sales_invoice_details),

    ## Get datos de reniec
    path('solicitud_nota_credito/financieros/reniec/', ViewNCFinanciero.obtener_datos_personales),

    ## Get datos empleado
    path('solicitud_nota_credito/empleado/<str:dni>/<str:department_number>', ViewNCPDV.get_name_by_dni_and_department),
    ###
    # path('admin/', admin.site.urls),
    path('admin/',  ViewNCPDV.bnotaPDV),
    path('oauth2/', include('django_auth_adfs.urls')),
    path('login/',views.login_successful,name='login-view')
    ####
]
