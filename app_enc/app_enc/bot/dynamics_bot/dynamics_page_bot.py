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
        self.wait_10 = WebDriverWait(self.driver , 10)
        self.driver.maximize_window() # Colocar dimensiones exactas

        # Credenciales
        self.url = "https://mistr-master.sandbox.operations.dynamics.com/?cmp=TRV&mi=ReturnTableListPage" # Ir defrente al devoluciones
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
        # self.xpath_todos_pedidos_de_devolucion='/html/body/div[2]/div/div[5]/div/div[2]/div/div[2]/div[67]/a[1]' # ?? Hace click en "Buscar Precios"

        self.xpath_boton_nuevo_pedido='//*[@id="returntablelistpage_6_SystemDefinedNewButton"]'

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
            # try:
            #     el = self.driver.find_element(By.XPATH,  self.xpath_todos_pedidos_de_devolucion)
            #     print('text_pedidos_de_dev: ', el.text)
            #     elemento = self.wait_10.until(EC.element_to_be_clickable((By.XPATH, self.xpath_todos_pedidos_de_devolucion)))
            #     elemento.click()
            # except TimeoutError:
            #     print("TimeoutError, primer intento no encontro xpath_todos_pedidos_de_devolucion")
            #     self._hacer_clic_xpath(self.xpath_devolucion_ventas)
            #     el = self.driver.find_element(By.XPATH,  self.xpath_todos_pedidos_de_devolucion)
            #     print('text_pedidos_de_dev2: ', el.text)
            #     elemento = self.wait_10.until(EC.element_to_be_clickable((By.XPATH, self.xpath_todos_pedidos_de_devolucion)))
            #     elemento.click()


        except Exception as e:
            print(f"Error al clickear en la opción todos los pedidos de devolución: {str(e)}")
    def crear_nuevo_pedido(self):
        try:
            self._hacer_clic_xpath(self.xpath_boton_nuevo_pedido)
            time.sleep(5)
        except Exception as e:
            print(f"Error al crear nuevo pedido: {str(e)}")
    # def favoritos_diario_factura(self):
    #     try:
    #         self._hacer_clic_xpath(self.xpath_favoritos)
    #         self._hacer_clic_xpath(self.xpath_favoritos_diario_facturas)
            
            
        
    #     except (WebDriverException, NoSuchElementException) as e:
    #         print(f"Error al iniciar sesión: {str(e)}")          
            
    # def busqueda_diario_factura(self, lista_boletas):
    #     try:
    #         # resuñtado de las boletas buscadas
    #         resultados_boletas = {}
            
    #         for boleta in lista_boletas:
    #             self._hacer_clic_xpath(self.xpath_columna_factura)
    #             self._ingresar_valor_en_input_xpath(self.xpath_input_busqueda_diario_factura, boleta)
    #             self._hacer_clic_xpath(self.xpath_boton_buscar_diario_factura)

    #             time.sleep(1)

    #             respusta_busqueda = self.driver.find_elements(By.XPATH, self.path_resultado_diario_factura)

    #             if respusta_busqueda:
    #                 # print(f"Elemento {boleta} encontrado")
    #                 resultados_boletas[boleta] = {'estado': True}
    #             else:
    #                 # print(f"Elemento {boleta} no encontrado")
    #                 resultados_boletas[boleta] = {'estado': False}

    #             # Pausa entre búsquedas
    #             time.sleep(1)

    #         print(resultados_boletas)
    #         # Pausa al final de todas las búsquedas

    #     except (WebDriverException, NoSuchElementException) as e:
    #         print(f"Error al iniciar sesión: {str(e)}")
            
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
dynamic_bot.seleccionar_ventas_marketing()
dynamic_bot.seleccionar_todos_los_pedidos_de_devolucion()
time.sleep(1)
dynamic_bot.crear_nuevo_pedido()
# dynamic_bot.favoritos_diario_factura()
# dynamic_bot.busqueda_diario_factura(lista_a_verificar)
# dynamic_bot.favoritos_transacciones_tienda()
# dynamic_bot.busqueda_transacciones_tienda(lista_a_verificar)