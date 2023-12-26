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
        self.driver.maximize_window()

        # Credenciales
        self.url = "https://mistr.operations.dynamics.com/"
        self.usuario = "teogenes.duran@terranovatrading.com.pe"
        self.contrasena = "pepito123"

        # XPaths
        self.xpath_siguiente = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[4]/div/div/div/div/input"
        
        self.xpath_input_login = '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]'
        self.xpath_input_contrasena = '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input'
        
        self.xpath_contrasena = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input"
        self.xpath_iniciar_sesion = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[4]/div[2]/div/div/div/div/input"
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
# dynamic_bot.favoritos_diario_factura()
# dynamic_bot.busqueda_diario_factura(lista_a_verificar)
dynamic_bot.favoritos_transacciones_tienda()
dynamic_bot.busqueda_transacciones_tienda(lista_a_verificar)