from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime

## Models
from ..models.model_solicitud_nc import SolicitudNC
from ..models.model_producto_detalle import ProductoDetalle
from ..models.model_detalle_solicitud import DetalleSolicitud

class ServiceNotaCredito:
    def crear_nota_credito(data):
        print("CORRER EL BOT PARA CREAR LA NOTA DE CREDITO")