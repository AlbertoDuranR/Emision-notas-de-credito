import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .dynamics_functions import AuxiliaryFunctions # Para Django
# from dynamics_functions import AuxiliaryFunctions
from ..constans import CODIGO_DISPOSICION
from ..constans import SERIES_PARA_NOTA_CREDITO

def measure_time(func):
    ''' Decorator para medir tiempo de ejecución'''
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"La función {func.__name__} tardó {total_time:.2f} segundos en ejecutarse")
        return result
    return wrapper

load_dotenv()
is_development_mode = os.environ.get("ENVIRONMENT") == 'development'
is_production_mode = os.environ.get("ENVIRONMENT") == 'production'


class Dynamics_Bot:
    intentos = 0

    def __init__(self):
        # Credenciales
        if is_development_mode:
            print('--Modo desarrollo dynamics activado--')
            self.url = "https://mistr-master.sandbox.operations.dynamics.com/?cmp=TRV&mi=ReturnTableListPage" # Ir defrente a devoluciones master
        elif is_production_mode:
            print('--Modo producción dynamics activado--')
            self.url = "https://mistr.operations.dynamics.com/?cmp=TRV&mi=ReturnTableListPage" # Ir defrente a devoluciones en producccion
        print('Url RPA Dynamics:', self.url)
        self.usuario= os.environ.get("BOT_DYNAMICS_USER")
        self.contrasena = os.environ.get("BOT_DYNAMICS_PASSWORD")
        self.nro_pedido_venta_devolucion=''

        self.config_navigator()

        # XPaths
        self.xpath_siguiente = "//input[@type='submit']"
        self.xpath_input_login = '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]'
        self.xpath_input_contrasena = '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input'
        self.xpath_contrasena = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input"
        self.xpath_iniciar_sesion = "/html/body/div[1]/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[5]/div/div/div/div/input"
        self.xpath_mantener_sesion = "/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input"
        self.xpath_favoritos = "/html/body/div[2]/div/div[5]/div/div/div[2]/div[2]/span[2]"
        self.xpath_favoritos_diario_facturas = "/html/body/div[2]/div/div[5]/div/div[1]/div[2]/div[5]"
        self.xpath_favoritos_transacciones_tienda = "/html/body/div[2]/div/div[5]/div/div[1]/div[2]/div[14]"
        self.xpath_columna_factura = "/html/body/div[2]/div/div[6]/div/form[2]/div[5]/div/div[3]/div[2]/div[1]/div[4]/div/div[2]/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[3]/div/div/div/div"
        self.xpath_input_busqueda_diario_factura = "/html/body/div[22]/div[3]/div/div[3]/div/div/input"
        self.xpath_boton_buscar_diario_factura = "/html/body/div[22]/div[4]/button[1]"
        self.path_resultado_diario_factura = "/html/body/div[2]/div/div[6]/div/form[2]/div[5]/div/div[3]/div[2]/div[1]/div[4]/div/div[2]/div/div/div/div[1]/div[3]/div/div/div[1]/div[2]/div/div[3]/div/div/div/div/div/div/input"
        self.xpath_columna_numero_recibo = "/html/body/div[2]/div/div[6]/div/form/div[5]/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[3]/div/div/div/div"
        self.xpath_input_busqueda_transacciones_tienda = "/html/body/div[21]/div[3]/div/div[3]/div/div/input"
        self.xpath_boton_buscar_transacciones_tienda = "/html/body/div[21]/div[4]/button[1]"
        self.xpath_resultado_transacciones_tienda = "/html/body/div[2]/div/div[6]/div/form/div[5]/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div/div/div/div/div/input"
        self.xpath_modulos='//*[@id="navPaneModuleID"]' # si uso el full path se confunde si el modulo esta en otra posición
        self.xpath_ventas_marketing='//*[@id="mainPane"]/div[5]/div/div[1]/div[2]/a[37]'
        self.xpath_devolucion_ventas='/html/body/div[2]/div/div[5]/div/div[2]/div/div[2]/a[8]'
        self.xpath_contenedor_ventas_marketing='//*[@id="mainPane"]/div[5]/div/div[2]/div/div[2]'
        self.xpath_todos_pedidos_de_devolucion='//*[@id="mainPane"]/div[5]/div/div[2]/div/div[2]/div[1]/a[1]'
        self.xpath_expadir_todo='//*[@id="mainPane"]/div[5]/div/div[2]/div/div[1]/button[1]'

        # Crear nuevo pedido
        self.xpath_boton_nuevo_pedido='//*[contains(@id, "returntablelistpage") and contains(@id, "SystemDefinedNewButton")]' # XPAT que contenga subcadenas 'returntablelistpage' y 'SystemDefinedNewButton'
        self.xpath_combobox_buscar_por='//*[contains(@id, "SalesCreateOrder") and contains(@id, "MCRCustSearchType")]/div'
        self.xpath_combobox_item_pedido_ventas='//*[contains(@id, "SalesCreateOrder") and contains(@id, "MCRCustSearchType_list_item1")][1]'
        self.xpath_input_num_pedido='//*[contains(@id, "SalesCreateOrder") and contains(@id, "MCRSearchText_input")]'
        self.xpath_buscar_cliente='//*[contains(@id, "SalesCreateOrder") and contains(@id, "MCRCustomerSearch")]' # //*[@id="SalesCreateOrder_9_MCRCustomerSearch"]
        self.xpath_table_row_cliente='//*[contains(@id, "MCRCustSearch") and contains(@id, "Grid")]/div/div/div/div/div[3]/div[1]'
        self.xpath_boton_seleccionar_cliente='//*[contains(@id, "MCRCustSearch") and contains(@id, "ButtonSelect")]'
        self.xpath_input_codigo_motivo_devolucion='//*[contains(@id, "SalesCreateOrder") and contains(@id, "SalesTable_ReturnReasonCodeId_input")]' # //*[@id="SalesCreateOrder_26_SalesTable_ReturnReasonCodeId_input"]
        self.xpath_input_almacen='//*[contains(@id, "SalesCreateOrder") and contains(@id, "SalesTable_InventLocationId_input")]'
        self.xpath_input_sitio='//*[contains(@id, "SalesCreateOrder") and contains(@id, "SalesTable_InventSiteId_input")]'
        self.xpath_boton_crear_pedido_devolucion='//*[contains(@id, "SalesCreateOrder") and contains(@id, "OK")]'

        # Enlazar pedido origen a pedido devolución
        """ Test avances """
        self.xpath_boton_buscar_pedido_ventas='//*[contains(@id, "ReturnTable") and contains(@id, "ReturnFindSalesOrder")]' # correcto
        # self.xpath_boton_buscar_pedido_ventas='//*[contains(@id, "returntableforedit") and contains(@id, "ReturnFindSalesOrder")]' # test
        self.xpath_columna_pedido_ventas='//*[contains(@id, "SalesCopying") and contains(@id, "Invoice_Heading")]/div/div/div/div/div[2]/div/div/div[2]/div/div[2]'
        self.xpath_input_columna_pedido_ventas= '//input[@id="__FilterField_CustInvoiceJour_SalesNum_SalesId_Input_0_0_input"]'
        self.xpath_boton_aplicar_pedido_ventas='//button[@id="__CustInvoiceJour_SalesNum_ApplyFilters"]'

        # seleccionar articulos buscando en tabla
        self.xpath_columna_articulo='//div[contains(@id, "Invoice_Lines") and contains(@id, "_0_grid")]/div[1]/div[2]/div/div[1]/div[2]/div/div[2]'
        self.xpath_input_columna_articulo='//input[@id="__FilterField_CustInvoiceTrans_ItemId_ItemId_Input_0_0_input"]'
        self.xpath_boton_aplicar_articulo='//button[@id="__CustInvoiceTrans_ItemId_ApplyFilters"]'

        ## seleccionar articulos si es parcial
        self.xpath_div_lineas_articulos='//div[contains(@id, "Invoice_Lines") and contains(@id, "row")]' # Selecciona todas las lineas del Invoice
        self.xpath_boton_aceptar_enlazar_ventas='//button[contains(@id, "SalesCopying") and contains(@id, "OK")]'
        self.xpath_contenedor_enlazar_articulos_footer='//*[contains(@id, "SalesCopying") and contains(@id, "TabPageTreeControl")]' # Usado para scroll a este elemento

        ## seleccionar articulos si es total
        self.xpath_div_primer_pedido='//div[contains(@id, "Invoice_Heading") and contains(@id, "row-0")]'

        # Confirmar registro
        self.xpath_cantidad_filas='//*[contains(@id, "SalesLineGrid")]//span[contains(text(), "filas")]' # 1 filas
        self.div_lineas_articulos_para_registro='//div[contains(@id, "SalesLineGrid") and contains(@id, "row")]'
        self.xpath_actualizar_linea='//*[contains(@id, "ReturnTable") and contains(@id, "Update_button")]'
        self.xpath_registro_inventario='//button[contains(@id, "ReturnTable") and contains(@id, "InventTransRegister")]'
        self.xpath_input_codigo_disposicion='//input[contains(@id, "Dialog") and contains(@id, "_Fld3_1_input")]'
        self.xpath_boton_aceptar_codigo_disposicion='//button[contains(@id, "Dialog") and contains(@id, "OkButton")]'
        self.xpath_agregar_linea_registro='//button[contains(@id, "InventTransRegister") and contains(@id, "AddRegistrationLinesButton")]' # //*[@id="InventTransRegister_5_AddRegistrationLinesButton"]
        self.xpath_confirmar_registro='//button[contains(@id, "InventTransRegister") and contains(@id, "ctrlUpdateButton")]' # Esto verificar q < disabled != "disabled" />
        self.xpath_input_estado_recepcion='//input[contains(@id, "InventTrans_StatusReceipt") and contains(@id, "0_0_input")]'
        self.xpath_boton_salir_registro='//button[contains(@id, "InventTransRegister") and contains(@id, "SystemDefinedCloseButton")]'

        ## Registrar articulos buscando en tabla
        self.xpath_columna_articulo_confirmar='//div[contains(@id, "SalesLine_ItemIdGrid") and contains(@id, "header")]'
        self.xpath_input_columna_articulo_confirmar='//input[@id="__FilterField_SalesLine_ItemIdGrid_ItemId_Input_0_0_input"]'
        self.xpath_button_aplicar_articulo_confirmar='//button[@id="__SalesLine_ItemIdGrid_ApplyFilters"]'

        # Cambios en nuevo pedido de devolucióon
        self.xpath_input_num_pedido_devolucion='//*[contains(@id, "ReturnTable") and contains(@id, "ReturnOrder_SalesId_input")]'
        self.xpath_edit_icon='//*[contains(@id, "SalesTable") and contains(@id, "SalesTable_DeliveryNameHeaderOverview")]/span[2]' # Para poder editar todo.
        self.xpath_input_numero_cuenta_cliente='//input[contains(@id, "SalesTable") and contains(@id, "CarrierCustomerAccountNumber_input")]' # usamos para luego llgar con tab a la forma de pago
        self.xpath_button_vistas_globales='//button[contains(@id, "alesTable") and contains(@id, "SystemDefinedManageViewFilters")]'
        # self.xpath_vista_estandar='//div[contains(@id, "ViewButtons")]/div[2]/button[1]'
        self.xpath_vista_formulario_pedido_venta='//div[contains(@id, "ViewButtons")]/div[2]/button[3]'
        self.xpath_vista_estandar='//div[contains(@id, "ViewButtons")]/div[2]/button[1]'
        self.xpath_span_actualizar_lineas_pedido='//*[contains(@id, "Dialog") and contains(@id, "DeliveryDate_toggle")]'
        self.xpath_button_aceptar_actualizar='//button[contains(@id, "Dialog") and contains(@id, "OkButton")]'
        self.xpath_encabezado_pedidos_ventas='//button[contains(@id, "SalesTable") and contains(@id, "LineViewHeader_caption")]'
        self.xpath_input_fecha_envio_solicitada='//input[contains(@id, "SalesTable") and contains(@id, "Delivery_ShippingDateRequestedHeader_input")]'
        self.xpath_input_fecha_recepcion_solicitada='//input[contains(@id, "SalesTable") and contains(@id, "Delivery_ReceiptDateRequestedHeader_input")]'
        self.xpath_input_tipo_documento='//*[@id="SalesTable_80_DMPCFieldsPeruPE_DMPCCodTypeDocPay_PE_input"]'
        self.xpath_button_info_resumen='//button[contains(@id, "SalesTable") and contains(@id, "FactBoxToggleExpand")]'
        self.xpath_button_totales_pedido_venta='//button[contains(@id, "SalesTable")  and contains(@id, "DMPCSalesTotalSummaryPart_PE_caption")]'
        self.xpath_refresh_resumen='//a[contains(@id, "DMPCSalesTotalSummaryPart_PE") and contains(@id, "Refresh")]'
        self.xpath_importe_total_resumen='//input[contains(@id, "DMPCSalesTotalSummaryPart_PE") and contains(@id, "DMPCSalesTotalSummary_PE_TotalAmount_input")]'
        self.xpath_messagebar_error='//div[contains(@id, "SalesTable") and contains(@class, "messageBarSection-Error")]'
        # Generar Factura
        self.xpath_button_factura='//button[contains(@id, "SalesTable") and contains(@id, "Invoice_button")]'
        self.xpath_button_generar_factura='//button[contains(@id, "SalesTable") and contains(@id, "buttonUpdateInvoice")]'
        self.xpath_open_seleccion_tipo_documento='//*[contains(@id, "SalesParmTable_DPCodTypeDocPay_PE") and contains(@id, "_0")]/div/div'
        self.xpath_input_tipo_documento_en_factura='//input[contains(@id, "SalesParmTable") and contains(@id, "_DPCodTypeDocPay_PE") and contains(@id, "input")]'
        self.xpath_input_serie_documento_en_factura='//input[contains(@id, "SalesParmTable_DPNumberSequenceGroup_PE") and contains(@id, "input")]'
        self.xpath_input_tipo_de_nota_en_factura='//input[contains(@id, "SalesParmTable") and contains( @id, "DPIdTypeNote_PE") and contains(@id, "input")]'
        self.xpath_input_fecha_de_factura='//input[contains(@id, "SalesEditLines") and  contains(@id, "SalesParmTable_Transdate_input")]'
        self.xpath_input_fecha_documento_en_factura='//input[contains(@id, "SalesEditLines") and contains(@id, "SalesParmTable_DocumentDate_input")]'
        self.xpath_input_fecha_de_vencimiento='//input[contains(@id, "SalesEditLines") and contains(@id,"SalesParmTable_FixedDueDate_input")]'
        self.xpath_button_aceptar_en_factura='//button[contains(@id, "SalesEditLines") and contains(@id, "OK")]'
        self.xpath_button_confirmar_factura='//button[contains(@id, "SysBoxForm") and contains(@id, "Ok")]'

        # Reintentar
        self.xpath_button_buscar_rma='//*[contains(@id, "returntablelistpage") and contains(@id, "QuickFilterControl")]/button'

    def config_navigator(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        options.add_argument("--headless=new") # =new Despues de la versión 109
        # options.add_argument("--no-sandbox") # Ejecutar en entornos con sandboxing, como Docker Averiguar

        options = self.set_download_folter(options)
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1440, 900)  # Resolution Laptop L Aprox.
        # self.driver.maximize_window()
        get_size = self.driver.get_window_size()
        print('get_size', get_size)
        self.wait = WebDriverWait(self.driver , 10)
        self.wait_20 = WebDriverWait(self.driver , 20)

    def ir_a_url_inicial(self):
        self.driver.get(self.url)

    def set_download_folter(self, options):
        # Configura la ruta de descarga
        download_dir = os.path.join(os.getcwd(),  'static\\downloads')
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False, # establece si quieres que el navegador solicite confirmación para cada descarga
            "download.directory_upgrade": True, #  indica si quieres que el navegador permita la descarga en la carpeta especificada
            # "safebrowsing.enabled": False # habilita o deshabilita la función de navegación segura.
            }
        # print('prefs: ', prefs)
        options.add_experimental_option('prefs', prefs)
        return options

    @measure_time
    def iniciar_sesion(self):
        try:
            self.ir_a_url_inicial()
            print('Iniciar Sesion')
            # ingresar usuario
            #self._ingresar_valor_en_input_id("i0116", self.usuario)
            self._ingresar_valor_en_input_xpath(self.xpath_input_login, self.usuario)
            # boton siguiente
            self._hacer_clic_xpath(self.xpath_siguiente)
            # ingresar contraseña
            #self._ingresar_valor_en_input_id("i0118", self.contrasena)
            self._ingresar_valor_en_input_xpath(self.xpath_input_contrasena, self.contrasena)
            # boton iniciar sesion
            self._hacer_clic_xpath(self.xpath_iniciar_sesion)
            # boton mantener sesion abierta
            self._hacer_clic_xpath(self.xpath_mantener_sesion)
            self.driver.implicitly_wait(10)
        except (WebDriverException, NoSuchElementException) as e:
            print(f"Error al iniciar sesión: {str(e)}")

    def crear_nuevo_pedido(self, data, codigo_motivo_devolucion):
        try:
            print(">>> START crear nuevo pedido")
            self._hacer_clic_xpath(self.xpath_boton_nuevo_pedido)
            self._wait_hide_div_bloking(15)
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_combobox_buscar_por)
            self._hacer_clic_xpath(self.xpath_combobox_item_pedido_ventas)
            self._ingresar_valor_en_input_xpath(self.xpath_input_num_pedido, data["num_pedido_origen"])
            self._hacer_clic_xpath(self.xpath_buscar_cliente)
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_boton_seleccionar_cliente)
            time.sleep(2)
            self._scroll_a_elemento_xpath(self.xpath_input_codigo_motivo_devolucion)
            self._esperar_n_segundos(2)
            self._ingresar_valor_en_input_xpath(self.xpath_input_codigo_motivo_devolucion, codigo_motivo_devolucion[data["metodo"]])
            time.sleep(1)
            self._ingresar_valor_en_input_xpath(self.xpath_input_almacen, data["almacen"])
            self._hacer_clic_xpath(self.xpath_input_sitio)
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_boton_crear_pedido_devolucion)
            print(">>> Fin crear nuevo pedido")
            self._esperar_n_segundos(1)
            input_num_pedido_devolucion = self.wait.until(EC.element_to_be_clickable((By.XPATH,  self.xpath_input_num_pedido_devolucion)))
            self.nro_pedido_venta_devolucion=input_num_pedido_devolucion.get_attribute("value")
            time.sleep(1)
        except Exception as e:
                raise ValueError (f'Error: Al momento de crear el nuevo pedido: {e}')

    def enlazar_pedido_origen_a_pedido_devolucion(self, data):
        # START Enlazar pedido origen a pedido devolución
        print('>>> START enlazar pedidos')
        self._hacer_clic_xpath(self.xpath_boton_buscar_pedido_ventas)
        time.sleep(1)
        self._hacer_clic_xpath(self.xpath_columna_pedido_ventas)
        self._ingresar_valor_en_input_xpath(self.xpath_input_columna_pedido_ventas, data['num_pedido_origen'])
        self._hacer_clic_xpath(self.xpath_boton_aplicar_pedido_ventas)
        time.sleep(1)

        if data['metodo'] == 'total':
            try:
                self._esperar_n_segundos('2')
                self._hacer_clic_xpath(f'{self.xpath_div_primer_pedido}//div/span')
            except Exception as e:
                print('Error: Al momento de seleccionar todos los productos solicitados')
                return
        else:
            # Seleccionar productos, si es metodo parcial
            """
            # PRIMER METODO - Problema si hay mas de 8 productos no se muestran todos se tiene que hacer scroll
            # div_articulos=self.driver.find_elements(By.XPATH, self.xpath_div_lineas_articulos)
            # print('>> Cantidad de articulos: ', len(div_articulos))
            # # for fila in range(len(div_articulos)):
            # #     try:
            # #         # print("Fila: ", fila, div_articulos[fila])
            # #         xpath_fila=f'//div[contains(@id, "Invoice_Lines") and contains(@id, "row-{fila}")]' # "Invoice_Lines_3345_0-row-0" <- Formato para recorrer filas
            # #         input_elements = self.driver.find_elements(By.XPATH, f'{xpath_fila}//input')
            # #         # for input_element in input_elements:
            # #         #     print("Text input:", input_element.get_attribute("value"))
            # #         if data['metodo'].lower() == "total":
            # #             # Selecciona todos los productos
            # #             self._hacer_clic_xpath(f'{xpath_fila}//div/span')
            # #             continue
            # #         if(input_elements[1].get_attribute("value") in data['productos']):
            # #             self._hacer_clic_xpath(f'{xpath_fila}//div/span') # se tiene un error -> Qu si no se hacer scroll no selecciona el producto
            # #             print("Select: ", input_elements[1].get_attribute("value"))
            # #     except Exception as e:
            # #         print(f"Error al seleccionar producto a enlazar: {str(e)}")
            """
            # SEGUNDO METODO: Buscar uno por uno y seleccionar
            try:
                self._esperar_n_segundos(2)
                # Desplazarse a una elemento
                contenedor_tabla_articulos = self.driver.find_element(By.XPATH, self.xpath_contenedor_enlazar_articulos_footer)
                ActionChains(self.driver)\
                    .scroll_to_element(contenedor_tabla_articulos)\
                    .perform()
                div_articulos=self.driver.find_elements(By.XPATH, self.xpath_div_lineas_articulos)
                for articulo in  data['productos']:
                    self._hacer_clic_xpath(self.xpath_columna_articulo)
                    self._ingresar_valor_en_input_xpath(self.xpath_input_columna_articulo, articulo['codigo'])
                    self._esperar_n_segundos(1)
                    self._hacer_clic_xpath(self.xpath_boton_aplicar_articulo)
                    time.sleep(1)
                    counter = 0
                    while len(div_articulos) > 0:
                        counter += 1
                        self._esperar_n_segundos(1)
                        div_articulos=self.driver.find_elements(By.XPATH, self.xpath_div_lineas_articulos)
                        if len(div_articulos) == 1:
                            self._esperar_n_segundos(1)
                            xpath_fila=f'//div[contains(@id, "Invoice_Lines") and contains(@id, "row-0")]' # "Invoice_Lines_3345_0-row-0"
                            input_elements = self.driver.find_elements(By.XPATH, f'{xpath_fila}//input')
                            # for input_element in input_elements:
                            #     print("Text input:", input_element.get_attribute("value"))
                            self._esperar_n_segundos('1')
                            print("Select articulo: ", input_elements[1].get_attribute("value"))
                            # Artificio para borrar este input. No era posible con .clear()
                            input_elements[3].click()
                            input_elements[3].send_keys(Keys.DELETE * len(input_elements[3].get_attribute("value")))
                            input_elements[3].send_keys(articulo['cantidad'])
                            self._hacer_clic_xpath(f'{xpath_fila}//div/span')
                            print("Select cantidad: ", input_elements[3].get_attribute("value"))
                            break
                        if counter > 3:
                            print("No se muestra la fila del articulo")
                            break
            except Exception as e:
                print(f"Error al seleccionar producto a enlazar: {str(e)}")
                raise

        time.sleep(1)
        self._hacer_clic_xpath(self.xpath_boton_aceptar_enlazar_ventas)
        self._wait_hide_div_bloking(30)
        print('END enlazar pedidos')
        return 'ENLAZAR'

    def registrar_articulo_para_devolucion(self):
        try:
            self._hacer_clic_xpath(self.xpath_actualizar_linea)
            self._hacer_clic_xpath(self.xpath_registro_inventario)
            self._wait_hide_div_bloking(10)
            time.sleep(1)
            self._ingresar_valor_en_input_xpath(self.xpath_input_codigo_disposicion, CODIGO_DISPOSICION)
            self._hacer_clic_xpath(self.xpath_input_codigo_disposicion) # Para obtener datos del codigo ingresado
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_boton_aceptar_codigo_disposicion)
            self._hacer_clic_xpath(self.xpath_agregar_linea_registro)

            # Verificar si esta habilitado el boton para confirmar registro de pedido
            self._esperar_n_segundos(2)
            is_enabled_buton_confirmar_registro=self.driver.find_element(By.XPATH, self.xpath_confirmar_registro).is_enabled()
            counter=0
            while not is_enabled_buton_confirmar_registro:
                time.sleep(1)
                is_enabled_buton_confirmar_registro=self.driver.find_element(By.XPATH, self.xpath_confirmar_registro).is_enabled()
                counter = counter + 1
                if is_enabled_buton_confirmar_registro:
                    break
                if counter > 3: # Si es es disabled en 5 intentos sale del bucle
                    raise ValueError ("No enabled el boton confirmar registro")
            self._hacer_clic_xpath(self.xpath_confirmar_registro)

            self._esperar_n_segundos(1)
            estado_recepcion=self.driver.find_element(By.XPATH, self.xpath_input_estado_recepcion)
            atributo_value=estado_recepcion.get_attribute("value")
            counter=0
            while atributo_value.lower() == 'pedido':
                time.sleep(1)
                estado_recepcion=self.driver.find_element(By.XPATH, self.xpath_input_estado_recepcion)
                atributo_value=estado_recepcion.get_attribute("value")
                counter = counter + 1
                if(atributo_value.lower() == "registrado"):
                    break
                if counter > 3:
                    raise ValueError("Estado de la recepción no registrado")
            self._hacer_clic_xpath(self.xpath_boton_salir_registro)
        except Exception as e:
                    print(f"Error al registrar articulo para devolución: {str(e)}")
                    raise

    def registrar_articulos_para_devolucion(self, data):
        estado=None
        print('>> START Registrar Confirmar Articulos')
        time.sleep(1)
        # Verificar que cantidad de articulos seleccionados se igual a los solicitados a devolución
        try:
            self._esperar_n_segundos(10)
            cantidad_text = (self.driver.find_element(By.XPATH, self.xpath_cantidad_filas)).text
            print('cantidad_text', cantidad_text)
            cantidad_articulos_registrar = int(cantidad_text.strip().split(' ')[0])
            print('cantidad_articulos_registrar' ,cantidad_articulos_registrar)
        except Exception as e:
            # Segunda validación siempre y cuando no sean mas de 7 productos. Ya que en este metodo no se muestran mas productos en la tabla. Los demas estan ocultos
            if len(data['productos']) < 7:
                cantidad_articulos_registrar=len(self.driver.find_elements(By.XPATH, self.div_lineas_articulos_para_registro))
                count = 0
                while not cantidad_articulos_registrar == len(data['productos']):
                    # print('>> Cantidad de articulos a registrar: ', len(div_articulos_registrar))
                    time.sleep(1)
                    self._esperar_n_segundos(1)
                    cantidad_articulos_registrar=len(self.driver.find_elements(By.XPATH, self.div_lineas_articulos_para_registro))
                    print('Cantidad: Articulos Solicitados para devolución:', len(data['productos']), ' | Articulos a registrar ', cantidad_articulos_registrar)
                    count += 1
                    if count > 4:
                        raise ValueError('Error: Cantidad de articulos Seleccionados no son iguales a los solicitados')
            else:
                print('Error: Al obtener cantidad de articulos a registrar', e)
                # raise ValueError('Error: Al obtener cantidad de articulos a registrar', e)
        print('Cantidad: Articulos Solicitados para devolución:', len(data['productos']), ' | Articulos a registrar ', cantidad_articulos_registrar)
        count = 0
        while not cantidad_articulos_registrar == len(data['productos']):
            time.sleep(1)
            cantidad_text = (self.driver.find_element(By.XPATH, self.xpath_cantidad_filas)).text
            cantidad_articulos_registrar = int(cantidad_text.strip().split(' ')[0])
            count += 1
            if count > 4:
                raise ValueError('Error: Cantidad de articulos Seleccionados no son iguales a los solicitados')


        ## Registrar Articulos
        try:
            self._wait_hide_div_bloking(20)
            print('Scroll al contenedor de articulos')
            xpath_contenedor_articulos_para_confirmar='//div[contains(@id, "ReturnTable") and contains(@id, "SalesLineGrid")]'
            self._scroll_a_elemento_xpath(xpath_contenedor_articulos_para_confirmar)
            self._wait_hide_div_bloking(10)
            for articulo in  data['productos']:
                self._esperar_n_segundos(2)
                self._hacer_clic_xpath(self.xpath_columna_articulo_confirmar)
                self._esperar_n_segundos(2)
                self._ingresar_valor_en_input_xpath(self.xpath_input_columna_articulo_confirmar, articulo['codigo'])
                self._esperar_n_segundos(2)
                self._hacer_clic_xpath(self.xpath_button_aplicar_articulo_confirmar)
                time.sleep(1)
                xpath_primera_fila=f'//div[contains(@id, "SalesLineGrid") and contains(@id, "row-0")]' # Primera Fila
                self._esperar_n_segundos(5)
                input_elements = self.driver.find_elements(By.XPATH, f'{xpath_primera_fila}//input')
                estado_devolucion_articulo= input_elements[8].get_attribute("value")
                # for input_element in input_elements:
                #     print("Text input:", input_element.get_attribute("value"))
                print("-- Articulo a registrar:", articulo['codigo'], "Estado devolución:", estado_devolucion_articulo)
                if estado_devolucion_articulo.lower() == 'previsto':
                    self._esperar_n_segundos(2)
                    self._hacer_clic_xpath(xpath_primera_fila)
                    time.sleep(1)
                    print('Registrando Articulo')
                    self._esperar_n_segundos(1)
                    self.registrar_articulo_para_devolucion()
        except IndexError as ie:
            # Manejar el error de índice fuera de rango
            print("Error: Índice fuera de rango al acceder a la lista de elementos.", ie)
            self.intentos+=1
            if self.intentos > 1:
                self.intentos = 0
                raise ValueError (f"Error al recorrer articulos a registrar: {str(e)}")
            estado = self.enlazar_pedido_origen_a_pedido_devolucion(data=data)
            self.registrar_articulos_para_devolucion(data=data)
        except Exception as e:
            raise ValueError (f"Error al recorrer articulos a registrar: {str(e)}")
        print(">> END Confirmado")
        estado = 'REGISTRAR'
        return estado

    def set_data_pedido_devolucion(self, data):
        """
            Establecer al pedido de devolución:
            - fecha de solicitud
            - forma de pago
            - pago
            - Codigo de Nota de Crédito
        """
        # START Poner fecha de solicitud
        print(">> START Poner data al pedido de devolucion")
        self._esperar_n_segundos(2)
        self._hacer_clic_xpath(self.xpath_input_num_pedido_devolucion)
        self._wait_hide_div_bloking(15)
        ## Activar edición de campos
        try:
            time.sleep(1)
            # Ingresar a la vista estándar
            self._esperar_n_segundos(2)
            self._hacer_clic_xpath(self.xpath_button_vistas_globales)
            self._wait_hide_div_bloking(10)
            self._hacer_clic_xpath(self.xpath_vista_estandar)
            print('Entrando a la Vista estandar')
            ##
            try:
                self._wait_hide_div_bloking(20)
                self._esperar_n_segundos(4)
                edit_icon=self.driver.find_element(By.XPATH, self.xpath_edit_icon)
                print('Find edit_icon in: ', edit_icon.get_attribute("title")) # print() Ayuda para despues poder cambiar su class
            except:
                self._hacer_clic_xpath(self.xpath_encabezado_pedidos_ventas)
                self._esperar_n_segundos(4)
                edit_icon=self.driver.find_element(By.XPATH, self.xpath_edit_icon)
                print('Find edit_icon in: ', edit_icon.get_attribute("title"))
            self._esperar_n_segundos(4) # se le da ese tiempo para espera que se vea el icon
            self.driver.execute_script("arguments[0].classList.add('fieldOptionsShowIsFocusedControl')", edit_icon)
            self._esperar_n_segundos(3)
            self._hacer_clic_xpath(self.xpath_edit_icon)
        except Exception as e:
            print('Error click en icon edit', e)
            time.sleep(5)
            raise ValueError("Error al hacer click icon editar pedido", e)
        # START Ingresar Fechas
        try:
            try:
                self._esperar_n_segundos(2)
                valor_input_fecha=self.driver.find_element(By.XPATH, self.xpath_input_fecha_envio_solicitada)
                print('Antes de ingresar fecha_envio_solicitada', valor_input_fecha.get_attribute("value"))
                self._hacer_clic_xpath(self.xpath_input_fecha_envio_solicitada)
            except:
                print("Mostrando encabezado de pedidos de ventas...")
                self._hacer_clic_xpath(self.xpath_encabezado_pedidos_ventas)
                self._esperar_n_segundos(2)
                valor_input_fecha=self.driver.find_element(By.XPATH, self.xpath_input_fecha_envio_solicitada)
                print('Antes de ingresar fecha_envio_solicitada', valor_input_fecha.get_attribute("value"))
                self._hacer_clic_xpath(self.xpath_input_fecha_envio_solicitada)
            self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_envio_solicitada, data["fecha_solicitud"])
            self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_recepcion_solicitada, data["fecha_solicitud"])
            self._esperar_n_segundos(2)
            valor_input_fecha_recepcion_solicitada=self.driver.find_element(By.XPATH, self.xpath_input_fecha_envio_solicitada)
            print('Despues de ingresar fecha_envio_solicitada y fecha_recepcion_solicitada',
                  valor_input_fecha.get_attribute("value"), valor_input_fecha_recepcion_solicitada.get_attribute("value"))
        except Exception as e:
            print('Error cambiar fechas: ', e)
            raise
        # START ingresar forma  de pago y pago
        try:
            # Ingresar a la vista FORMULARIO DE PEDIDO DE VENTA
            self._esperar_n_segundos(2)
            self._hacer_clic_xpath(self.xpath_button_vistas_globales)
            if self._is_displayed_messagebar_error():
                self.validar_importe_resumen_con_importe_solicitud(data)
                print('Click en vistas globales')
                self._hacer_clic_xpath(self.xpath_button_vistas_globales)
            try:
                print('Click en Vista formulario de pedido de venta')
                self._esperar_n_segundos(1)
                self._hacer_clic_xpath(self.xpath_vista_formulario_pedido_venta)
            except:
                try:
                    self._wait_hide_div_bloking(15)
                    print('Click en Vista formulario de pedido de venta despues del bloking')
                    self._esperar_n_segundos(2)
                    self._hacer_clic_xpath(self.xpath_vista_formulario_pedido_venta)
                except:
                    print('Click panel actualizar lineas de pedido')
                    self._hacer_clic_xpath(self.xpath_span_actualizar_lineas_pedido)
                    self._hacer_clic_xpath(self.xpath_button_aceptar_actualizar)
                    print('Click en Vista formulario de pedido de venta')
                    self._esperar_n_segundos(2)
                    self._hacer_clic_xpath(self.xpath_vista_formulario_pedido_venta)

            print('Entro a la vista FORMULARIO DE PEDIDO DE VENTA')
            self._wait_hide_div_bloking(30)
            input_numero_cuenta_cliente = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.xpath_input_numero_cuenta_cliente)))
            input_numero_cuenta_cliente.click()
            input_numero_cuenta_cliente.send_keys(Keys.TAB)
            self._esperar_n_segundos(2)
            input_focus_forma_pago = self.driver.switch_to.active_element  # Obtiene el elemento actualmente enfocado
            input_focus_forma_pago.clear()
            input_focus_forma_pago.send_keys(data['forma_pago'])
            input_focus_forma_pago.send_keys(Keys.TAB)
            print(f'Forma de Pago: {input_focus_forma_pago.get_attribute("value")}')
            self._esperar_n_segundos(2)
            input_focus_pago = self.driver.switch_to.active_element
            input_focus_pago.clear()
            input_focus_pago.send_keys(data['pago'])
            input_focus_pago.send_keys(Keys.TAB)
            print(f'Pago: {input_focus_pago.get_attribute("value")}')
            # time.sleep(1)
            self._esperar_n_segundos(2)
            input_perfil_contabilizacion = self.driver.switch_to.active_element
            input_perfil_contabilizacion.send_keys(Keys.TAB)
            # time.sleep(2)
            self._esperar_n_segundos(2)
            input_tipo_documento = self.driver.switch_to.active_element
            input_tipo_documento.clear()
            input_tipo_documento.send_keys('07') # Nota de Crédito es 07
            print(f'Codigo nota de crédito: {input_tipo_documento.get_attribute("value")}')
            time.sleep(2)
        except Exception as e:
            print('Error al ingresar forma de pago, pago o codigo nota de crédito', e)
            raise
        return

    def validar_importe_resumen_con_importe_solicitud(self, data):
        # Siempre tener visible el DIV "Informacion relacionada" en las vistas del usuario.
        # START Verificar Ingualdad entre resumen y  monto total de solicitud
        try:
            try:
                self._esperar_n_segundos(2)
                self._hacer_clic_xpath(self.xpath_refresh_resumen)
            except:
                # self._hacer_clic_xpath(self.xpath_button_info_resumen)
                self._hacer_clic_xpath(self.xpath_button_totales_pedido_venta)
                print('xpath button totales pedido venta')
                self._esperar_n_segundos(2)
                self._hacer_clic_xpath(self.xpath_refresh_resumen)
            time.sleep(2)
            # Para verificar si el monto del resumen es igual al solicitado. SI ES IGUAL IR A FACTURAR
            self._esperar_n_segundos(4)
            importe_total_resumen = self.driver.find_element(By.XPATH, self.xpath_importe_total_resumen)
            importe_total_resumen_value = abs(round(float(importe_total_resumen.get_attribute("value")), 2))
            importe_total_nota_credito = abs(round(float(data['monto_total_nota_credito']), 2))
            count=0
            while importe_total_nota_credito != importe_total_resumen_value:
                print('Importe total', importe_total_nota_credito, importe_total_resumen_value)
                time.sleep(1)
                importe_total_resumen = self.driver.find_element(By.XPATH, self.xpath_importe_total_resumen)
                importe_total_resumen_value = abs(round(float(importe_total_resumen.get_attribute("value")), 2))
                count += 1
                if count > 5:
                    print('Error Importe de nota credito diferente al Importe de resumen')
                    raise ValueError("Importe de Nota credito diferente a Importe de resumen")
            print('Importe total Nota: ', importe_total_nota_credito, 'Importe total Resumen:', importe_total_resumen_value)
            time.sleep(2)
        except Exception as e:
            print('Error al verificar resumen: ', e)
            raise
         # END Verificar Ingualdad entre resumen y  monto total de solicitud

    def get_serie_documento(self, invoice_number: str) -> str:
        '''
            input: invoice_number "BB01-00080858"
            output: 'T_BC20'
        '''
        # print('get_Serie_documento: ', invoice_number)
        serie = invoice_number.split("-")[0]
        # codigo_base = serie[0] + serie[-2:]  # Obtener la primera letra y los dos últimos caracteres del código
        if serie in SERIES_PARA_NOTA_CREDITO:
            return SERIES_PARA_NOTA_CREDITO[serie]
        else:
            return None

    def generar_factura(self, data, codigo_motivo_devolucion):
        try:
            print('START Generar Factura - Nota de crédito')
            self._hacer_clic_xpath(self.xpath_button_factura)
            self._hacer_clic_xpath(self.xpath_button_generar_factura)
            if self._is_displayed_messagebar_error():
                self.validar_importe_resumen_con_importe_solicitud(data)
                self._hacer_clic_xpath(self.xpath_button_generar_factura)
            self._wait_hide_div_bloking(10)
            self._hacer_clic_xpath(self.xpath_open_seleccion_tipo_documento)
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_input_serie_documento_en_factura)
            self._ingresar_valor_en_input_xpath(self.xpath_input_serie_documento_en_factura, self.get_serie_documento(invoice_number=data['num_comprobante_origen']))
            time.sleep(1)
            self._ingresar_valor_en_input_xpath(self.xpath_input_tipo_de_nota_en_factura, codigo_motivo_devolucion[data['metodo']])
            time.sleep(1)
            print('Despues de codigo_motivo_devolucion')
            try:
                self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_de_factura,  data["fecha_solicitud"])
                self._hacer_clic_xpath(self.xpath_input_fecha_de_vencimiento) # Recien cambia la fecha de solicitud
                self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_documento_en_factura,  data["fecha_solicitud"])
            except:
                print('FALTO MOSTRAR CONFIGURAR')
                self._hacer_clic_xpath('//button[contains(@id, "SalesEditLines") and contains(@id, "TabSetup_caption")]')
                self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_de_factura,  data["fecha_solicitud"])
                self._hacer_clic_xpath(self.xpath_input_fecha_de_vencimiento) # Recien cambia la fecha de solicitud
                self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_documento_en_factura,  data["fecha_solicitud"])
            print('Despues de ingresar fechas de factura')
            self._esperar_n_segundos(1)
            self._hacer_clic_xpath(self.xpath_button_aceptar_en_factura)
            time.sleep(2)
            self._esperar_n_segundos(2)
            self._hacer_clic_xpath(self.xpath_button_confirmar_factura)
            time.sleep(5)
            try:
                print('Esperar descargar .txt')
                self._wait_hide_div_bloking(90)
            except e:
                print(e)
            print('END Generar Factura')
            return 'FACTURAR'
        except Exception as e:
            # print('Exception crear nota de credito: ', e)
            raise ValueError ('Error al crear la factura', e)

    @measure_time
    def crear_nota_de_credito(self, data):
        '''
            :params
                data = {'num_comprobante_origen': 'BG01-00054368', 'num_pedido_origen': 'TRV-02752003', 'metodo': 'parcial', 'almacen': 'MD05_CRZ', 'productos': [{'codigo': '109168', 'cantidad': 1}], 'forma_pago': 'FP015', 'pago': 'CONT', 'fecha_solicitud': '22/01/2024', 'monto_total_nota_credito': 4.2, 'sol_tipo_nc': 'PDV', 'sol_estado': 'VALIDADO', 'step_rpa': '', 'sol_id': 110}
        '''
        codigo_motivo_devolucion={
            "parcial": "07",
            "total": "06"
        }
        resultado = {
            "estado": "CREADO",
            "nro_pedido_venta_devolucion": None,
            "step_rpa": None,
            "error": None,
            "sol_id": data['sol_id']
        }
        print('START Crear_nota_de_credito')
        try:
            self.crear_nuevo_pedido(data=data, codigo_motivo_devolucion=codigo_motivo_devolucion)
            resultado["nro_pedido_venta_devolucion"] = self.nro_pedido_venta_devolucion
            if not self.nro_pedido_venta_devolucion:
                raise ValueError('No Exite número de pedido de venta para devolución con en el RPA')
            resultado["step_rpa"] = 'PEDIDO'
            resultado["step_rpa"] = self.enlazar_pedido_origen_a_pedido_devolucion(data=data)
            resultado["step_rpa"] = self.registrar_articulos_para_devolucion(data=data)
            # Establecer Fecha de solicitud, Forma de pago, pago, codigo Nota de crédito
            self.set_data_pedido_devolucion(data=data)
            resultado["step_rpa"] = self.generar_factura(data=data, codigo_motivo_devolucion=codigo_motivo_devolucion)
        except Exception as e:
            print('Exception crear nota de credito: ', e)
            resultado["estado"] = "ERROR"
            resultado["error"] = {
                "mensaje": str(e),
                "donde": "Crear nota de crédito"
            }
            return  resultado
        time.sleep(2)
        print('END Proceso Crear Nota de Credito')
        return resultado

    @measure_time
    def reintentar_crear_nota_de_credito(self, data: dict, nro_rma: str, nro_pedido_nota_credito:str):
        """
         :params
            data: {'num_comprobante_origen': 'BB01-00095300', 'num_pedido_origen': 'TRV-02756273', 'metodo': 'parcial', 'almacen': 'MD02_JRC', 'productos': [{'codigo': '109023', 'cantidad': 1}, {'codigo': '106239', 'cantidad': 2}], 'forma_pago': 'FP015', 'pago': 'CONT', 'fecha_solicitud': '01/30/2024', 'monto_total_nota_credito': 11.2, 'sol_tipo_nc': 'PDV', 'sol_estado': 'ERROR', 'step_rpa': 'REGISTRAR'}
            rma: 'TRV-02756273'
        """
        if data['sol_estado'] == 'CREADO':
            print('Pedido con estado CREADO')
            return
        if not nro_rma:
            print('Sin Nro RMA')
            return

        self.iniciar_sesion()
        print('START Reintentar_crear_nota_de_credito', data, nro_rma )
        step_rpa = data['step_rpa'] if data['step_rpa'] else 'PEDIDO'
        codigo_motivo_devolucion={
            "parcial": "07",
            "total": "06"
        }
        resultado = {
            "estado": "CREADO",
            "nro_pedido_venta_devolucion": nro_pedido_nota_credito,
            "error": None,
            "step_rpa":  step_rpa,
        }

        try:
            # start Reintentar - Si falla podriamos renovar al pedido de esta forma
            print('Reintentar Continuar')
            self.xpath_input_buscar_rma='//*[contains(@id, "returntablelistpage") and contains(@id, "QuickFilterControl_Input_input")]'
            self._ingresar_valor_en_input_xpath(self.xpath_input_buscar_rma, nro_rma) # Solo es para el ejemplo
            print('Click en buscar rma')
            self._hacer_clic_xpath(self.xpath_button_buscar_rma)
            self._esperar_n_segundos(2)
            input_buscar_rma = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.xpath_input_buscar_rma)))
            input_buscar_rma.click()
            input_buscar_rma.send_keys(Keys.TAB)
            self._esperar_n_segundos(1)
            pedido_devolucion_rma = self.driver.switch_to.active_element
            pedido_devolucion_rma.send_keys(Keys.ENTER)
            # end

            print('>> step_rpa:', step_rpa)

            if step_rpa == 'PEDIDO':
               step_rpa = resultado["step_rpa"] = self.enlazar_pedido_origen_a_pedido_devolucion(data=data)
            if step_rpa == 'ENLAZAR':
                resultado["step_rpa"] = self.registrar_articulos_para_devolucion(data=data)

            # Establecer Fecha de solicitud, Forma de pago, pago, codigo Nota de crédito
            self.set_data_pedido_devolucion(data=data)
            resultado["step_rpa"] = self.generar_factura(data=data, codigo_motivo_devolucion=codigo_motivo_devolucion)
        except Exception as e:
            print('Exception crear nota de credito: ', e)
            resultado["estado"] = "ERROR"
            resultado["error"] = {
                "mensaje": str(e),
                "donde": "Crear factura para la nota de crédito"
            }
            return  resultado
        time.sleep(2)
        print('END Proceso Reintentar Crear Nota de Credito')
        self.driver.quit()
        return resultado

    def crear_individual_nota_de_credito(self, data):
        self.iniciar_sesion()
        result_rpa= self.crear_nota_de_credito(data)
        self.driver.quit()
        return result_rpa

    def crear_masivo_nota_de_credito(self, data_solicitudes: list):
        estados_rpa = [] # [{}, {}, {}]
        self.iniciar_sesion()
        for data in data_solicitudes:
            print(f'Crear Data {data}, {data["sol_id"]}')
            estado_rpa = self.crear_nota_de_credito(data)
            estados_rpa.append(estado_rpa)
            if estado_rpa['estado'] == 'ERROR':
                break
            time.sleep(1)
            self.ir_a_url_inicial()
            time.sleep(1)
        self.driver.quit()
        return estados_rpa

    def _ingresar_valor_en_input_id(self, xpath, valor):
        AuxiliaryFunctions.ingresar_valor_en_input_id(self.driver, self.wait, xpath, valor)

    def _ingresar_valor_en_input_name(self, xpath, valor):
        AuxiliaryFunctions.ingresar_valor_en_input_name(self.driver, self.wait, xpath, valor)

    def _ingresar_valor_en_input_xpath(self, xpath, valor):
        AuxiliaryFunctions.ingresar_valor_en_input_xpath(self.driver, self.wait, xpath, valor)

    def _hacer_clic_class_name(self, class_name):
        AuxiliaryFunctions.hacer_clic_class_name(self.driver, self.wait, class_name)

    def _hacer_clic_xpath(self, xpath):
        AuxiliaryFunctions.hacer_clic_xpath(self.driver, self.wait, xpath)

    def _esperar_n_segundos(self, seg):
        """
         Tiempo de espera implícito de forma inteligente y dinámica,
         Selenium verificará periódicamente si el elemento está disponible
         durante el tiempo de espera especificado antes de continuar con la siguiente instrucción
        """
        self.driver.implicitly_wait(seg) # Espera n segundos
        # Ojo: time.sleep(1) es un pausa estática que detiene el script sin ninguna verificación.

    def _is_displayed_messagebar_error(self):
        try:
            self._esperar_n_segundos(2)
            messagebar_error = self.driver.find_element(By.XPATH, self.xpath_messagebar_error)
            print('messagebar_error',  messagebar_error.is_displayed())
            return messagebar_error.is_displayed()
        except NoSuchElementException:
            print("El elemento 'messagebar_error' no se pudo encontrar en la página web.")
            return False

    def _wait_hide_div_bloking(self, segundos=3):
        div_blocking=self.driver.find_element(By.XPATH, '//*[@id="ShellBlockingDiv"]')
        is_visible_blocking_div=div_blocking.is_displayed()
        counter = 0
        while is_visible_blocking_div:
            time.sleep(1) # Pausa explicita
            div_blocking=self.driver.find_element(By.XPATH, '//*[@id="ShellBlockingDiv"]')
            is_visible_blocking_div=div_blocking.is_displayed()
            print(f'is_visible_blocking_div {div_blocking.is_displayed()} {counter} Seg')
            if not is_visible_blocking_div:
                break
            counter += 1
            if counter > segundos:
                print (f'>>>>>>>> Visible DIV BLOCKING "Espera mientras procesamos..." por mas de {segundos} segundos')
                break

    def _scroll_a_elemento_xpath(self, xpath):
        # Desplazarse a una elemento
        self._esperar_n_segundos(2)
        elemento = self.driver.find_element(By.XPATH, xpath)
        ActionChains(self.driver)\
            .scroll_to_element(elemento)\
            .perform()

# ---------------------------------------------------------------------------------
# ---- data Ejemplos ---
data_parcial={
    "num_comprobante_origen": 'BF02-00153614',
    "PaymentTermsName": 'CONT',
    # Sale del orden de pedido
    "SalesOrderNumber": "TRV-02755697",
    "DefaultShippingWarehouseId": 'MD04_SUC',
    "CustomerPaymentMethodName": 'FP015',
    'num_pedido_origen': 'TRV-02755697',
    'metodo': 'parcial',
    'almacen': 'MD04_SUC',
    'productos': [
        {'codigo': '101196', 'cantidad': '1'}, # 'codigo : cantidad
        {'codigo': '103271', 'cantidad': '1'}
    ],
    'forma_pago':'FP015',
    'pago': 'CONT',
    'fecha_solicitud': '1/21/2024',
    'monto_total_nota_credito': '3.9'
}
data_total = {
    "num_comprobante_origen": "BB03-00080858",
    "PaymentTermsName": "CONT",
    # Sale del orden de pedido
    "SalesOrderNumber": "TRV-02750046",
    "CustomerPaymentMethodName": "FP015",
    "DefaultShippingWarehouseId": "MD02_JRC",
    "InvoiceDate": "2024-01-20T12:00:00Z",
    "TotalInvoiceAmount": 24.0,
    'num_pedido_origen': 'TRV-02750046',
    'metodo': 'total',
    'almacen': 'MD02_JRC',
    'productos': [  # Si es TOTAL tener todos los productos desde la base de datos
        {'codigo': '100827', 'cantidad': '1'},
        {'codigo': '102345', 'cantidad': '1'},
        {'codigo': '102337', 'cantidad': '1'},
        {'codigo': '105351', 'cantidad': '2'},
        {'codigo': '100130', 'cantidad': '1'},
        {'codigo': '102088', 'cantidad': '1'},
        {'codigo': '102171', 'cantidad': '2'},
    ],
    'forma_pago':'FP015',
    'pago': 'CONT',
    'fecha_solicitud': '1/20/2024',
    'monto_total_nota_credito': 24.0
}

# Crear instancia de AceptaFunctions
# dynamic_bot = Dynamics_Bot()
# INIT
# dynamic_bot.iniciar_sesion()
# dynamic_bot.crear_nota_de_credito(data=data_parcial)
