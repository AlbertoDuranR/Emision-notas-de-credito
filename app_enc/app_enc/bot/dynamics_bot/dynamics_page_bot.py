# acepta_functions.py
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import pandas as pd
from .dynamics_functions import AuxiliaryFunctions # Para Django
from ..constans import CODIGO_DISPOSICION
from ..constans import SERIES_PARA_NOTA_CREDITO
# from dynamics_functions import AuxiliaryFunctions
from selenium.webdriver.common.keys import Keys


class Dynamics_Bot:
    def __init__(self):
        # Credenciales
        self.url = "https://mistr-master.sandbox.operations.dynamics.com/?cmp=TRV&mi=ReturnTableListPage" # Ir defrente a devoluciones
        self.usuario = "robert.tolentino@terranovatrading.com.pe"
        self.contrasena = "huaraz2023.."
        self.nro_pedido_venta_devolucion=''

        # XPaths
        self.xpath_siguiente = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[4]/div/div/div/div/input"
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
        self.xpath_combobox_item_pedido_ventas='//*[contains(@id, "SalesCreateOrder") and contains(@id, "MCRCustSearchType_list_item1")]'
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
        self.xpath_button_vistas_globales='//button[contains(@id, "SalesTable") and contains(@id, "SystemDefinedManageViewFilters")]'
        self.xpath_vista_estandar='//div[contains(@id, "ViewButtons")]/descendant::button[contains(@id, "5637889366")]'
        self.xpath_input_fecha_envio_solicitada='//input[contains(@id, "SalesTable") and contains(@id, "Delivery_ShippingDateRequestedHeader_input")]'
        self.xpath_input_fecha_recepcion_solicitada='//input[contains(@id, "SalesTable") and contains(@id, "Delivery_ReceiptDateRequestedHeader_input")]'
        self.xpath_input_tipo_documento='//*[@id="SalesTable_80_DMPCFieldsPeruPE_DMPCCodTypeDocPay_PE_input"]'
        self.xpath_refresh_resumen='//a[contains(@id, "DMPCSalesTotalSummaryPart_PE") and contains(@id, "Refresh")]'
        self.xpath_importe_total_resumen='//input[contains(@id, "DMPCSalesTotalSummaryPart_PE") and contains(@id, "DMPCSalesTotalSummary_PE_TotalAmount_input")]'
        self.xpath_button_factura='//button[contains(@id, "SalesTable") and contains(@id, "Invoice_button")]'

        # Generar Factura
        self.xpath_button_generar_factura='//button[contains(@id, "SalesTable") and contains(@id, "buttonUpdateInvoice")]'
        self.xpath_open_seleccion_tipo_documento='//*[contains(@id, "SalesParmTable_DPCodTypeDocPay_PE") and contains(@id, "_0")]/div/div'
        self.xpath_input_tipo_documento_en_factura='//input[contains(@id, "SalesParmTable") and contains(@id, "_DPCodTypeDocPay_PE") and contains(@id, "input")]'
        self.xpath_input_serie_documento_en_factura='//input[contains(@id, "SalesParmTable_DPNumberSequenceGroup_PE") and contains(@id, "input")]'
        self.xpath_input_tipo_de_nota_en_factura='//input[contains(@id, "SalesParmTable") and contains( @id, "DPIdTypeNote_PE") and contains(@id, "input")]'
        self.xpath_input_fecha_de_factura='//input[contains(@id, "SalesEditLines") and  contains(@id, "SalesParmTable_Transdate_input")]'
        self.xpath_input_fecha_documento_en_factura='//input[contains(@id, "SalesEditLines") and contains(@id, "SalesParmTable_DocumentDate_input")]'
        self.xpath_button_aceptar_en_factura='//button[contains(@id, "SalesEditLines") and contains(@id, "OK")]'
        self.xpath_button_confirmar_factura='//button[contains(@id, "SysBoxForm") and contains(@id, "Ok")]'

        # Reintentar
        self.xpath_button_buscar_rma='//*[contains(@id, "returntablelistpage") and contains(@id, "QuickFilterControl")]/button'

    def config_navigator(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # options.add_argument("--window-size=1600,1024")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver , 10)
        self.wait_20 = WebDriverWait(self.driver , 20)
        self.driver.maximize_window()

    def iniciar_sesion(self):
        self.config_navigator()
        try:
            self.driver.get(self.url)
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
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_combobox_buscar_por)
            self._hacer_clic_xpath(self.xpath_combobox_item_pedido_ventas)
            time.sleep(1)
            self._ingresar_valor_en_input_xpath(self.xpath_input_num_pedido, data["num_pedido_origen"])
            self._hacer_clic_xpath(self.xpath_buscar_cliente)
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_boton_seleccionar_cliente)
            time.sleep(1)
            self._ingresar_valor_en_input_xpath(self.xpath_input_codigo_motivo_devolucion, codigo_motivo_devolucion[data["metodo"]])
            self._ingresar_valor_en_input_xpath(self.xpath_input_almacen, data["almacen"])
            self._hacer_clic_xpath(self.xpath_input_sitio)
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_boton_crear_pedido_devolucion)
            print(">>> Fin crear nuevo pedido")
            self._esperar_n_segundos(1)
            input_num_pedido_devolucion = self.wait.until(EC.element_to_be_clickable((By.XPATH,  self.xpath_input_num_pedido_devolucion)))
            self.nro_pedido_venta_devolucion=input_num_pedido_devolucion.get_attribute('value')
            time.sleep(1)
        except Exception as e:
                print('Error: Al momento de crear el nuevo pedido', e)
                return 

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
                # input_elements = self.driver.find_elements(By.XPATH, f'{self.xpath_div_primer_pedido}//input')
                # for input_element in input_elements:
                #     print("Text input:", input_element.get_attribute("value"))
                # print("Select articulo: ", input_elements[1].get_attribute("value"))
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
        print('END enlazar pedidos')

    def registrar_articulo_para_devolucion(self):
        try:
            self._hacer_clic_xpath(self.xpath_actualizar_linea)
            self._hacer_clic_xpath(self.xpath_registro_inventario)
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
        print('>> START Confirmar registro')
        time.sleep(2)
        # Verificar que cantidad de articulos seleccionados se igual a los solicitados a devolución
        try:
            # div_articulos_registrar=self.driver.find_elements(By.XPATH, self.div_lineas_articulos_para_registro)
            # cantidad_articulos_registrar=len(div_articulos_registrar)
            self._esperar_n_segundos(4)
            cantidad_articulos_registrar=len(self.driver.find_elements(By.XPATH, self.div_lineas_articulos_para_registro))
        except Exception as e:
            raise ValueError('Error: Al obtener cantidad de articulos a registrar', e)

        print('Cantidad: Articulos Solicitados para devolución:', len(data['productos']), ' | Articulos a registrar ', cantidad_articulos_registrar)
        count = 0
        while not cantidad_articulos_registrar == len(data['productos']):
            # print('>> Cantidad de articulos a registrar: ', len(div_articulos_registrar))
            time.sleep(1)
            self._esperar_n_segundos(1)
            cantidad_articulos_registrar=len(self.driver.find_elements(By.XPATH, self.div_lineas_articulos_para_registro))
            if count > 3:
                raise ValueError('Error: Cantidad de articulos Seleccionados no son iguales a los solicitados')
            count += 1
        print('Cantidad: Articulos Solicitados para devolución:', len(data['productos']), ' | Articulos a registrar ', cantidad_articulos_registrar)

        ## Registrar Articulos
        try:
            # self._esperar_n_segundos(1)
            # div_articulos_registrar=self.driver.find_elements(By.XPATH, self.div_lineas_articulos_para_registro)
            # cantidad_articulos_registrar=len(div_articulos_registrar)
            # print('Cantidad de articulos a registrar: ', cantidad_articulos_registrar) # Tiene q ser igual a los productos a registrar
            print('Scroll al contenedor de articulos')
            xpath_contenedor_articulos_para_confirmar='//div[contains(@id, "ReturnTable") and contains(@id, "SalesLineGrid")]'
            contenedor_tabla_articulos = self.driver.find_element(By.XPATH, xpath_contenedor_articulos_para_confirmar)
            ActionChains(self.driver)\
                .scroll_to_element(contenedor_tabla_articulos)\
                .perform()

            for articulo in  data['productos']:
                self._hacer_clic_xpath(self.xpath_columna_articulo_confirmar)
                self._ingresar_valor_en_input_xpath(self.xpath_input_columna_articulo_confirmar, articulo['codigo'])
                self._esperar_n_segundos(2)
                self._hacer_clic_xpath(self.xpath_button_aplicar_articulo_confirmar)
                time.sleep(1)
                xpath_primera_fila=f'//div[contains(@id, "SalesLineGrid") and contains(@id, "row-0")]' # Primera Fila
                self._esperar_n_segundos(3)
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
        except Exception as e:
            print(f"Error al recorrer articulos a registrar: {str(e)}")
            raise
        print(">> END Confirmado")

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
        ## Activar edición de campos
        try:
            time.sleep(1)
            self._esperar_n_segundos(4)
            edit_icon=self.driver.find_element(By.XPATH, self.xpath_edit_icon)
            print('Find edit_icon in: ', edit_icon.get_attribute("title")) # print() Ayuda para despues poder cambiar su class
            self._esperar_n_segundos(4) # se le da ese tiempo para espera que se vea el icon
            self.driver.execute_script("arguments[0].classList.add('fieldOptionsShowIsFocusedControl')", edit_icon)
            # print('After edit_icon > ', edit_icon.get_attribute("class"))
            self._esperar_n_segundos(2)
            self._hacer_clic_xpath(self.xpath_edit_icon)
        except Exception as e:
            print('Error click en icon edit', e)
            time.sleep(5)
            raise ValueError("Error al hacer click icon editar pedido", e)
        ## ingresar forma  de pago y pago
        try:
            self._esperar_n_segundos(1)
            input_numero_cuenta_cliente = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.xpath_input_numero_cuenta_cliente)))
            input_numero_cuenta_cliente.click()
            input_numero_cuenta_cliente.send_keys(Keys.TAB)
            self._esperar_n_segundos(1)
            input_focus_forma_pago = self.driver.switch_to.active_element  # Obtiene el elemento actualmente enfocado
            input_focus_forma_pago.clear()
            input_focus_forma_pago.send_keys(data['forma_pago'])
            # time.sleep(1)
            input_focus_forma_pago.send_keys(Keys.TAB)
            print(f'Forma de Pago: {input_focus_forma_pago.get_attribute('value')}')
            self._esperar_n_segundos(1)
            input_focus_pago = self.driver.switch_to.active_element
            input_focus_pago.clear()
            input_focus_pago.send_keys(data['pago'])
            input_focus_pago.send_keys(Keys.TAB)
            print(f'Pago: {input_focus_pago.get_attribute('value')}')
            # time.sleep(1)
            self._esperar_n_segundos(1)
            input_perfil_contabilizacion = self.driver.switch_to.active_element
            input_perfil_contabilizacion.send_keys(Keys.TAB)
            # time.sleep(2)
            self._esperar_n_segundos(1)
            input_tipo_documento = self.driver.switch_to.active_element
            input_tipo_documento.clear()
            input_tipo_documento.send_keys('07') # Nota de Crédito es 07
            print(f'Codigo nota de crédito: {input_tipo_documento.get_attribute('value')}')
            time.sleep(3)
        except Exception as e:
            print('Error al ingresar forma de pago, pago o codigo nota de crédito', e)
            raise

        self._esperar_n_segundos(2)
        self._hacer_clic_xpath(self.xpath_button_vistas_globales)
        self._esperar_n_segundos(1)
        self._hacer_clic_xpath(self.xpath_vista_estandar)

        try:
            # time.sleep(1)
            self._esperar_n_segundos(1)
            valor_input_fecha=self.driver.find_element(By.XPATH, self.xpath_input_fecha_envio_solicitada)
            print('before xpath_input_fecha_envio_solicitada', valor_input_fecha.get_attribute("value"))
            self._hacer_clic_xpath(self.xpath_input_fecha_envio_solicitada)
            self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_envio_solicitada, data["fecha_solicitud"])
            self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_recepcion_solicitada, data["fecha_solicitud"])
            print('after xpath_input_fecha_envio_solicitada', valor_input_fecha.get_attribute("value"))
        except Exception as e:
            print('Error cambiar fechas: ', e)
            raise
        # END Poner fecha de solicitud

    def validar_importe_resumen_con_importe_solicitud(self, data):
        # START Verificar Ingualdad entre resumen y  monto total de solicitud
        try:
            self._esperar_n_segundos(2)
            self._hacer_clic_xpath(self.xpath_refresh_resumen)
            time.sleep(2)
            # Para verificar si el monto del resumen es igual al solicitado. SI ES IGUAL IR A FACTURAR
            self._esperar_n_segundos(2)
            importe_total_resumen = self.driver.find_element(By.XPATH, self.xpath_importe_total_resumen)
            importe_total_resumen_value = abs(round(float(importe_total_resumen.get_attribute("value")), 2))
            importe_total_nota_credito = abs(round(float(data['monto_total_nota_credito']), 2))
            count=0
            while importe_total_nota_credito != importe_total_resumen_value:
                print('Importe total', importe_total_nota_credito, importe_total_resumen_value)
                time.sleep(1)
                importe_total_resumen = self.driver.find_element(By.XPATH, self.xpath_importe_total_resumen)
                importe_total_resumen_value = abs(round(float(importe_total_resumen.get_attribute("value")), 2))
                if count > 3:
                    print('Error Importe de nota credito diferente al Importe de resumen')
                    raise ValueError("Importe de Nota credito diferente a Importe de resumen")
            print('Importe total Nota: ', importe_total_nota_credito, 'Importe total Resumen:', importe_total_resumen_value)
            time.sleep(2)
            self._hacer_clic_xpath(self.xpath_button_factura)
            self._hacer_clic_xpath(self.xpath_button_generar_factura)
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

    def crear_nota_de_credito(self, data):
        codigo_motivo_devolucion={
            "parcial": "07",
            "total": "06"
        }
        resultado = {
            "estado": "CREADO",
            "nro_pedido_venta_devolucion": None,
            "error": None
        }
        # # # start TEST esta parte es temporal para no crear cada rato pedidos - Si falla podriamos renovar al pedido de esta forma
        # # print('Continuar 1')
        # # self.xpath_input_buscar_rma='//*[contains(@id, "returntablelistpage") and contains(@id, "QuickFilterControl_Input_input")]'
        # # self._ingresar_valor_en_input_xpath(self.xpath_input_buscar_rma, 'TRV-007954') # Solo es para el ejemplo
        # # print('Click en buscar rma')
        # # time.sleep(3)
        # # # end
        try:
            # Crear nuevo pedido
            self.crear_nuevo_pedido(data=data, codigo_motivo_devolucion=codigo_motivo_devolucion)
            resultado["nro_pedido_venta_devolucion"] = self.nro_pedido_venta_devolucion
            # print('num_pedido_devolucion: ',  resultado["nro_pedido_venta_devolucion"])
            # Enlazar pedidos
            self.enlazar_pedido_origen_a_pedido_devolucion(data=data)
            # registrar articulos para devolución
            self.registrar_articulos_para_devolucion(data=data)
            # Establecer Fecha de solicitud, Forma de pago, pago, codigo Nota de crédito
            self.set_data_pedido_devolucion(data=data)
            # Validar Si importe resumen es igual a importe solicitud continuar
            self.validar_importe_resumen_con_importe_solicitud(data=data)
            # START Generar Factura
            print('START Generar Factura - Nota de crédito')
            try:
                self._hacer_clic_xpath(self.xpath_open_seleccion_tipo_documento)
                time.sleep(1)
                self._hacer_clic_xpath(self.xpath_input_serie_documento_en_factura)
                self._ingresar_valor_en_input_xpath(self.xpath_input_serie_documento_en_factura, self.get_serie_documento(invoice_number=data['num_comprobante_origen']))
                time.sleep(1)
                self._ingresar_valor_en_input_xpath(self.xpath_input_tipo_de_nota_en_factura, codigo_motivo_devolucion[data['metodo']])
                time.sleep(1)
                self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_de_factura,  data["fecha_solicitud"])
                self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_documento_en_factura,  data["fecha_solicitud"])
                self._esperar_n_segundos(1)
                self._hacer_clic_xpath(self.xpath_button_aceptar_en_factura)
                time.sleep(1)
                self._esperar_n_segundos(2)
                self._hacer_clic_xpath(self.xpath_button_confirmar_factura)
                time.sleep(2)
            except Exception as e:
                # print('Exception crear nota de credito: ', e)
                raise 'Error al crear la factura'
            print('END Generar Factura')
        except Exception as e:
            print('Exception crear nota de credito: ', e)
            resultado["estado"] = "ERROR"
            resultado["error"] = {
                "mensaje": str(e),
                "donde": "Crear nota de crédito"
            }
            return  resultado
        time.sleep(20)
        return resultado

    def reintentar_crear_nota_de_credito(self, data: dict, nro_rma: str):
        print('reintentar_crear_nota_de_credito', data, nro_rma )
        codigo_motivo_devolucion={
            "parcial": "07",
            "total": "06"
        }
        resultado = {
            "estado": "CREADO",
            "nro_pedido_venta_devolucion": None,
            "error": None
        }

        try:
            # start Reintentar - Si falla podriamos renovar al pedido de esta forma
            print('Reintentar Continuar')
            self.xpath_input_buscar_rma='//*[contains(@id, "returntablelistpage") and contains(@id, "QuickFilterControl_Input_input")]'
            self._ingresar_valor_en_input_xpath(self.xpath_input_buscar_rma, nro_rma) # Solo es para el ejemplo
            print('Click en buscar rma')
            self._hacer_clic_xpath(self.xpath_button_buscar_rma)
            # time.sleep(1)
            self._esperar_n_segundos(2)
            input_buscar_rma = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.xpath_input_buscar_rma)))
            input_buscar_rma.click()
            input_buscar_rma.send_keys(Keys.TAB)
            self._esperar_n_segundos(1)
            pedido_devolucion_rma = self.driver.switch_to.active_element
            pedido_devolucion_rma.send_keys(Keys.ENTER)
            # end
            # Enlazar pedidos
            # self.enlazar_pedido_origen_a_pedido_devolucion(data=data)
            # registrar articulos para devolución
            self.registrar_articulos_para_devolucion(data=data)
            # Establecer Fecha de solicitud, Forma de pago, pago, codigo Nota de crédito
            self.set_data_pedido_devolucion(data=data)
            # Validar Si importe resumen es igual a importe solicitud continuar
            self.validar_importe_resumen_con_importe_solicitud(data=data)
            # START Generar Factura
            print('START Generar Factura - Nota de crédito')
            try:
                self._hacer_clic_xpath(self.xpath_open_seleccion_tipo_documento)
                time.sleep(1)
                self._hacer_clic_xpath(self.xpath_input_serie_documento_en_factura)
                self._ingresar_valor_en_input_xpath(self.xpath_input_serie_documento_en_factura, self.get_serie_documento(invoice_number=data['num_comprobante_origen']))
                time.sleep(1)
                self._ingresar_valor_en_input_xpath(self.xpath_input_tipo_de_nota_en_factura, codigo_motivo_devolucion[data['metodo']])
                time.sleep(1)
                self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_de_factura,  data["fecha_solicitud"])
                self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_documento_en_factura,  data["fecha_solicitud"])
                self._esperar_n_segundos(1)
                self._hacer_clic_xpath(self.xpath_button_aceptar_en_factura)
                time.sleep(1)
                self._esperar_n_segundos(2)
                self._hacer_clic_xpath(self.xpath_button_confirmar_factura)
                time.sleep(2)
            except Exception as e:
                print('Exception crear nota de credito: ', e)
                raise 'Error al crear la factura'
            print('END Generar Factura')
        except Exception as e:
            print('Exception crear nota de credito: ', e)
            resultado["estado"] = "ERROR"
            resultado["error"] = {
                "mensaje": str(e),
                "donde": "Crear factura para la nota de crédito"
            }
            return  resultado
        time.sleep(20)
        print('END Proceso Crear Nota de Credito')
        return resultado

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
