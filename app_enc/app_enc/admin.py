from django.contrib import admin

## Importando modelos
from .models.model_solicitud_nc import *
from .models.model_usuario import *
from .models.model_detalle_solicitud import *
from .models.model_market import *
from .models.model_menu_r_permisos import *
from .models.model_menu import *
from .models.model_permisos import *
from .models.model_producto_detalle import *
from .models.model_roles_permisos import *
from .models.model_roles import *
from .models.model_solicitante_detalle import *


## Registrando modelos
admin.site.register(SolicitudNC)
admin.site.register(Usuario)
admin.site.register(DetalleSolicitud)
admin.site.register(Market)
admin.site.register(MenuRPermisos)
admin.site.register(Menu)
admin.site.register(Permisos)
admin.site.register(ProductoDetalle)
admin.site.register(RolesPermisos)
admin.site.register(Roles)
admin.site.register(SolicitanteDet)