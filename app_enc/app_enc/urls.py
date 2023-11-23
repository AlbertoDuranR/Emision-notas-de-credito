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

urlpatterns = [
    ## Path Index
    path('', views.index),
    
    ## Path View Solicitudes
    path('solicitud_nota_credito/punto_venta/', ViewNCPDV.notaPDV,name="new_nc_pdv"),
    path('solicitud_nota_credito/financieros/', ViewNCFinanciero.notaFinanciero),
    path('solicitud_nota_credito/servicios/', ViewNCServicios.notaServicios),
    ###
    
    ## Path View Consolidacion
    path('consolidacion_nota_credito/punto_venta/', ViewNCPDV.cnotaPDV),
    path('consolidacion_nota_credito/financieros/', ViewNCFinanciero.cnotaFinanciero),
    path('consolidacion_nota_credito/servicios/', ViewNCServicios.cnotaServicios),
    ###
    
    
    ## Path View Bandeja
    path('bandeja_nota_credito/punto_venta/', ViewNCPDV.bnotaPDV),
    path('bandeja_nota_credito/financieros/', ViewNCFinanciero.bnotaFinanciero),
    path('bandeja_nota_credito/servicios/', ViewNCServicios.bnotaServicios),
    ###

    ## Create NC
    path('solicitud_nota_credito/punto_venta/create/', ViewNCPDV.create_solicitud_pdv),
    path('solicitud_nota_credito/financieros/create/', ViewNCFinanciero.create_solicitud_financieras),
    path('solicitud_nota_credito/servicios/create/', ViewNCServicios.create_solicitud_servicios),
    ###

    ###
    path('admin/', admin.site.urls),
    path('oauth2/', include('django_auth_adfs.urls')),
    path('login/',views.login_successful,name='login-view')
    ####
]
