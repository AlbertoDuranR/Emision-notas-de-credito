# acepta_functions.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import pandas as pd
from dynamics_functions import AuxiliaryFunctions
from selenium.webdriver.common.keys import Keys


class Dynamics_Bot:
    def __init__(self):
        
        # Configuración del navegador
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver , 10)
        self.wait_20 = WebDriverWait(self.driver , 10)
        self.driver.maximize_window() # Colocar dimensiones exactas

        # Credenciales
        self.url = "https://mistr-master.sandbox.operations.dynamics.com/?cmp=TRV&mi=ReturnTableListPage" # Ir defrente a devoluciones
        self.usuario = "robert.tolentino@terranovatrading.com.pe"
        self.contrasena = "huaraz2023.."

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
        # self.buscar_rma='//*[contains(@id, "returntablelistpage") and contains(@id, "QuickFilterControl")]/button'
        
        """ Test avances """
        self.xpath_boton_buscar_pedido_ventas='//*[contains(@id, "ReturnTable") and contains(@id, "ReturnFindSalesOrder")]' # correcto
        # self.xpath_boton_buscar_pedido_ventas='//*[contains(@id, "returntableforedit") and contains(@id, "ReturnFindSalesOrder")]' # test

        self.xpath_columna_pedido_ventas='//*[contains(@id, "SalesCopying") and contains(@id, "Invoice_Heading")]/div/div/div/div/div[2]/div/div/div[2]/div/div[2]'
        self.xpath_input_columna_pedido_ventas= '//*[@id="__FilterField_CustInvoiceJour_SalesNum_SalesId_Input_0_0_input"]'
        self.xpath_boton_aplicar_pedido_ventas='//*[@id="__CustInvoiceJour_SalesNum_ApplyFilters"]'
        # seleccionar articulos si es parcial
        self.xpath_div_lineas_articulos='//div[contains(@id, "Invoice_Lines") and contains(@id, "row")]' # Selecciona todas las lineas del Invoice
        self.xpath_checkbox_primera_linea_articulo= '//*[contains(@id, "CustInvoiceTrans_Copy") and contains(@id, "0_0_input")]'
        self.xpath_boton_aceptar_enlazar_ventas='//button[contains(@id, "SalesCopying") and contains(@id, "OK")]'

        # Confirmar registro
        self.div_lineas_articulos_para_registro='//div[contains(@id, "SalesLineGrid") and contains(@id, "row")]'
        self.xpath_actualizar_linea='//*[contains(@id, "ReturnTable") and contains(@id, "Update_button")]'
        self.xpath_registro_inventario='//button[contains(@id, "ReturnTable") and contains(@id, "InventTransRegister")]'
        self.xpath_input_codigo_disposicion='//input[contains(@id, "Dialog") and contains(@id, "_Fld3_1_input")]'
        self.xpath_boton_acptar_codigo_disposicion='//button[contains(@id, "Dialog") and contains(@id, "OkButton")]'
        self.xpath_agregar_linea_registro='//button[contains(@id, "InventTransRegister") and contains(@id, "AddRegistrationLinesButton")]' # //*[@id="InventTransRegister_5_AddRegistrationLinesButton"]
        self.xpath_confirmar_registro='//button[contains(@id, "InventTransRegister") and contains(@id, "ctrlUpdateButton")]' # Esto verificar q < disabled != "disabled" />
        self.xpath_input_estado_recepcion='//input[contains(@id, "InventTrans_StatusReceipt") and contains(@id, "0_0_input")]'
        self.xpath_boton_salir_registro='//button[contains(@id, "InventTransRegister") and contains(@id, "SystemDefinedCloseButton")]'

        # Cambios en nuevo pedido de devolucióon
        self.xpath_input_num_pedido_devolucion='//*[contains(@id, "ReturnTable") and contains(@id, "ReturnOrder_SalesId_input")]'
        self.xpath_button_vistas_globales='//button[contains(@id, "SalesTable") and contains(@id, "SystemDefinedManageViewFilters")]'
        # //*[@id="SalesTable_6_SystemDefinedManageViewFilters"]
        self.xpath_vista_estandar='//div[contains(@id, "ViewButtons")]/descendant::button[contains(@id, "5637889366")]'
        self.xpath_edit_icon='//*[contains(@id, "SalesTable") and contains(@id, "Delivery_ReceiptDateRequestedHeader")]/div/div[2]/div'
        self.xpath_input_fecha_envio_solicitada='//input[contains(@id, "SalesTable") and contains(@id, "Delivery_ShippingDateRequestedHeader_input")]'
        self.xpath_input_fecha_envio_solicitada_icon_editar='//input[contains(@id, "SalesTable") and contains(@id, "Delivery_ShippingDateRequestedHeader_input")]/div/div[1]/span[1]'
        self.xpath_input_fecha_recepcion_solicitada='//input[contains(@id, "SalesTable") and contains(@id, "Delivery_ReceiptDateRequestedHeader_input")]'

        # //*[@id="SalesTable_6_Delivery_ShippingDateRequestedHeader"]/div/div[1]/span[1]
    def iniciar_sesion(self):
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

    def seleccionar_ventas_marketing(self):
        try:
            self._hacer_clic_xpath(self.xpath_modulos)
            self._hacer_clic_xpath(self.xpath_ventas_marketing)
        except TimeoutError:
            print("No se encontraron elementos modulos o ventas y marketing.")

    def seleccionar_todos_los_pedidos_de_devolucion(self):
        try:
            div_contenedor = self.wait_10.until(EC.element_to_be_clickable((By.XPATH, self.xpath_contenedor_ventas_marketing)))
            print('div_contenedor: ', div_contenedor)
            # Encontrar todos los <a> dentro del div
            links = div_contenedor.find_elements_by_tag_name("a")
            print('link: ', links)
            # Iterar sobre los enlaces y obtener el texto y la URL
            for link in links:
                link_text = link.text
                link_url = link.get_attribute("href")  # Obtener el atributo href del enlace
                print(f"Texto del enlace: {link_text}, URL del enlace: {link_url}")
            time.sleep(5)


        except Exception as e:
            print(f"Error al clickear en la opción todos los pedidos de devolución: {str(e)}")

    def crear_nuevo_pedido(self):
        # input:
        data={
            'num_pedido_origen': 'TRV-02721425',
            'metodo': 'parcial',
            'almacen': 'MD03_CRH',
            'productos': ['108104', '103810', '104835'],
            'fecha_solicitud': '1/10/2024'
        }

        codigo_motivo_devolucion={
            "parcial": "07",
            "total": "06"
        }

        try:
            # # # start TEST esta parte es temporal para no crear cada rato pedidos
            # # print('Continuar 1')
            # # self.xpath_input_buscar_rma='//*[contains(@id, "returntablelistpage") and contains(@id, "QuickFilterControl_Input_input")]'
            # # self._ingresar_valor_en_input_xpath(self.xpath_input_buscar_rma, 'TRV-007851') # Solo es para el ejemplo
            # # print('Click en buscar rma')
            # # time.sleep(3)
            # # # end

            # Crear nuevo pedido
            print(">>> Inicia crear nuevo pedido")
            self._hacer_clic_xpath(self.xpath_boton_nuevo_pedido)
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_combobox_buscar_por)
            self._hacer_clic_xpath(self.xpath_combobox_item_pedido_ventas)
            time.sleep(1)
            self._ingresar_valor_en_input_xpath(self.xpath_input_num_pedido, data["num_pedido_origen"])
            # self.driver.find_element(By.XPATH, self.xpath_buscar_cliente).click()
            self._hacer_clic_xpath(self.xpath_buscar_cliente)
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_boton_seleccionar_cliente)
            time.sleep(1)
            print('before select motivo')
            self._ingresar_valor_en_input_xpath(self.xpath_input_codigo_motivo_devolucion, codigo_motivo_devolucion[data["metodo"]])
            print('after select motivo', self.xpath_input_codigo_motivo_devolucion)
            self._ingresar_valor_en_input_xpath(self.xpath_input_almacen, data["almacen"])
            self._hacer_clic_xpath(self.xpath_input_sitio)
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_boton_crear_pedido_devolucion)
            print(">>> Fin crear nuevo pedido")
            time.sleep(2)

            print(">>> Inicia enlazar pedidos")
            self.enlazar_pedido_origen_a_pedido_devolucion(data=data)
            print('>>> Fin enlazar pedidos')

            # START Confirmar registro
            print('>> Confirmar registro')
            time.sleep(4)
            div_articulos_registrar=self.driver.find_elements(By.XPATH, self.div_lineas_articulos_para_registro)
            print('>> Cantidad de articulos a registrar: ', len(div_articulos_registrar))
            try:
                for fila in range(len(div_articulos_registrar)):
                    print("Fila: ", fila, div_articulos_registrar[fila])
                    #//*[@id="SalesLineGrid_9928_0-row-0"]
                    xpath_fila=f'//div[contains(@id, "SalesLineGrid") and contains(@id, "row-{fila}")]' #//*[@id="SalesLineGrid_9928_0-row-0"] <- Formato para recorrer filas
                    input_elements = self.driver.find_elements(By.XPATH, f'{xpath_fila}//input')
                    # for input_element in input_elements:
                    #     print("Text input:", input_element.get_attribute("value"))
                    print("Estado devolución: ", input_elements[8].get_attribute("value"))
                    if (input_elements[8].get_attribute("value")).lower() == 'previsto':
                        self._hacer_clic_xpath(xpath_fila)
                        print('Se hizo click en la fila ', fila)
                        time.sleep(1)
                        print('Inicio Registrar Articulo: ', fila)
                        self.registrar_articulo_para_devolucion()
                        print('Fin Registrar Articulo: ', fila)
            except Exception as e:
                print(f"Error al crear nuevo pedido: {str(e)}")
            time.sleep(3)

            print("Confirmado")

            # START Poner fecha de solicitud
            print(">> Poner Fecha de Solicitud")
            self._hacer_clic_xpath(self.xpath_input_num_pedido_devolucion)
            time.sleep(2)
            print('after input numero pedido')
            self._hacer_clic_xpath(self.xpath_button_vistas_globales)
            print('after button_vistas_globales')
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_vista_estandar)
            print('after vista_estandar')
            time.sleep(1)

            # Falta poder modificar la fecha...
            # # try:
            # #     # self._hacer_clic_xpath(self.xpath_input_fecha_envio_solicitada_icon_editar)
            # #     # print('after edit_icon')
            # #     time.sleep(3)
            # #     valor_input_fecha=self.driver.find_element(By.XPATH, self.xpath_input_fecha_envio_solicitada)
            # #     print('xpath_input_fecha_envio_solicitada', valor_input_fecha.get_attribute("value"))
            # #     self._hacer_clic_xpath(self.xpath_input_fecha_envio_solicitada)

            # #     self._ingresar_valor_en_input_xpath(self.xpath_input_fecha_envio_solicitada, '2024-02-03')
            # #     valor_input_fecha=self.driver.find_element(By.XPATH, self.xpath_input_fecha_envio_solicitada)
            # #     print('xpath_input_fecha_envio_solicitada II', valor_input_fecha.get_attribute("value"))
            # # except Exception as e:
            # #     print(f'Error al editar fecha solicitud {e}')

            # # # Encuentra el elemento span oculto por su clase
            # # span_oculto = self.driver.find_elements(By.CLASS_NAME, 'timeZoneIndicator')
            # # print('span_oculto', span_oculto[0])
            # # # Haz clic en el elemento span oculto
            # # span_oculto[0].click()

            # END Poner fecha de solicitud
            time.sleep(7)
        except Exception as e:
            print(f"Error al crear nuevo pedido: {str(e)}")

    def enlazar_pedido_origen_a_pedido_devolucion(self, data):
        # START Enlazar pedido origen a pedido devolución
        self._hacer_clic_xpath(self.xpath_boton_buscar_pedido_ventas)
        time.sleep(1)
        self._hacer_clic_xpath(self.xpath_columna_pedido_ventas)
        self._ingresar_valor_en_input_xpath(self.xpath_input_columna_pedido_ventas, data['num_pedido_origen'])
        self._hacer_clic_xpath(self.xpath_boton_aplicar_pedido_ventas)
        time.sleep(2)
        # Seleccionar productos si tiene y  si es metodo parcial
        div_articulos=self.driver.find_elements(By.XPATH, self.xpath_div_lineas_articulos)
        print('>> Cantidad de articulos: ', len(div_articulos))
        try:
            for fila in range(len(div_articulos)):
                print("Fila: ", fila, div_articulos[fila])
                xpath_fila=f'//div[contains(@id, "Invoice_Lines") and contains(@id, "row-{fila}")]' # "Invoice_Lines_3345_0-row-0" <- Formato para recorrer filas
                input_elements = self.driver.find_elements(By.XPATH, f'{xpath_fila}//input')
                # for input_element in input_elements:
                #     print("Text input:", input_element.get_attribute("value"))
                if data['metodo'].lower() == "total":
                    # Selecciona todos los productos
                    self._hacer_clic_xpath(f'{xpath_fila}//div/span')
                    continue
                if(input_elements[1].get_attribute("value") in data['productos']):
                    self._hacer_clic_xpath(f'{xpath_fila}//div/span')
                    print("Select: ", input_elements[1].get_attribute("value"))
        except Exception as e:
            print(f"Error al seleccionar productos a enlazar: {str(e)}")
        # print("Productos seleccionados")
        time.sleep(1)
        self._hacer_clic_xpath(self.xpath_boton_aceptar_enlazar_ventas)
        # self._hacer_clic_xpath(self.xpath_columna_articulo)
        # self._ingresar_valor_en_input_xpath(self.xpath_input_columna_articulo, '108104')
        # self._hacer_clic_xpath(self.xpath_boton_aplicar_articulo)
        # END Enlazar pedido origen a pedido devolución

    def registrar_articulo_para_devolucion(self):
        try:
            self._hacer_clic_xpath(self.xpath_actualizar_linea)
            print('after click actualizar pedido')
            self._hacer_clic_xpath(self.xpath_registro_inventario)
            time.sleep(1)
            self._ingresar_valor_en_input_xpath(self.xpath_input_codigo_disposicion, 'CD001')
            self._hacer_clic_xpath(self.xpath_input_codigo_disposicion) # Para obtener datos del codigo ingresado
            time.sleep(1)
            self._hacer_clic_xpath(self.xpath_boton_acptar_codigo_disposicion)
            self._hacer_clic_xpath(self.xpath_agregar_linea_registro)

            # Verificar si esta habilitado el boton para confirmar registro de pedido
            is_enabled_buton_confirmar_registro=self.driver.find_element(By.XPATH, self.xpath_confirmar_registro).is_enabled()
            counter=0
            # print('Boton confirmar registro: ', is_enabled_buton_confirmar_registro)
            while not is_enabled_buton_confirmar_registro:
                time.sleep(1)
                is_enabled_buton_confirmar_registro=self.driver.find_element(By.XPATH, self.xpath_confirmar_registro).is_enabled()
                counter = counter + 1
                if is_enabled_buton_confirmar_registro:
                    self._hacer_clic_xpath(self.xpath_confirmar_registro)
                    break
                if counter > 5: # Si es es disabled en 5 intentos sale del bucle
                    print("No enabled el boton confirmar registro")
                    break

            estado_recepcion=self.driver.find_element(By.XPATH, self.xpath_input_estado_recepcion)
            atributo_value=estado_recepcion.get_attribute("value")
            counter=0
            while atributo_value.lower() == 'pedido':
                time.sleep(1)
                estado_recepcion=self.driver.find_element(By.XPATH, self.xpath_input_estado_recepcion)
                atributo_value=estado_recepcion.get_attribute("value")
                counter = counter + 1
                if(atributo_value.lower() == "registrado"):
                    self._hacer_clic_xpath(self.xpath_boton_salir_registro)
                    break
                if counter > 3: # Si es es disabled en 5 intentos sale del bucle
                    print("Estado recepcion no registrado")
                    break
        except Exception as e:
                    print(f"Error al registrar articulo para devolución: {str(e)}")

    def favoritos_transacciones_tienda(self):
        try:
            self._hacer_clic_xpath(self.xpath_favoritos)
            self._hacer_clic_xpath(self.xpath_favoritos_transacciones_tienda)
            
            #time.sleep(10)
        except (WebDriverException, NoSuchElementException) as e:
            print(f"Error al iniciar sesión: {str(e)}")  
      
    def busqueda_transacciones_tienda(self, lista_boletas):
        try:
            # resuñtado de las boletas buscadas
            resultados_boletas = {}
            
            for boleta in lista_boletas:
                self._hacer_clic_xpath(self.xpath_columna_numero_recibo)
                self._ingresar_valor_en_input_xpath(self.xpath_input_busqueda_transacciones_tienda, boleta)
                self._hacer_clic_xpath(self.xpath_boton_buscar_transacciones_tienda)

                time.sleep(1)

                respusta_busqueda = self.driver.find_elements(By.XPATH, self.xpath_resultado_transacciones_tienda)

                if respusta_busqueda:
                    # print(f"Elemento {boleta} encontrado")
                    resultados_boletas[boleta] = {'estado': True}
                else:
                    # print(f"Elemento {boleta} no encontrado" )
                    resultados_boletas[boleta] = {'estado': False}
                    
                # Pausa entre búsquedas
                time.sleep(1)
                
            print(resultados_boletas)
            # Pausa al final de todas las búsquedas
            time.sleep(10)
            
        except (WebDriverException, NoSuchElementException) as e:
            print(f"Error al iniciar sesión: {str(e)}") 
      
      
      
    
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
# Crear instancia de AceptaFunctions
dynamic_bot = Dynamics_Bot()

lista_a_verificar = ["B040-00047319", "BE01-00131658", "BE01-00131493"]

# Ejecutar acciones
dynamic_bot.iniciar_sesion()
# dynamic_bot.seleccionar_ventas_marketing()
# dynamic_bot.seleccionar_todos_los_pedidos_de_devolucion()
time.sleep(1)
dynamic_bot.crear_nuevo_pedido()
# dynamic_bot.favoritos_diario_factura()
# dynamic_bot.busqueda_diario_factura(lista_a_verificar)
# dynamic_bot.favoritos_transacciones_tienda()
# dynamic_bot.busqueda_transacciones_tienda(lista_a_verificar)