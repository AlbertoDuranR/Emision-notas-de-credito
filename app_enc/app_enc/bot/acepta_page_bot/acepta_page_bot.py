# acepta_functions.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import pandas as pd
from acepta_functions import AuxiliaryFunctions


class AceptaFunctions:
    def __init__(self):
        
        # Configuración del navegador
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver , 10)
        self.driver.maximize_window()

        # Credenciales
        self.usuario = "wilfredo.caceres@terranovatrading.com.pe"
        self.contrasena = "118499544"

        # XPaths
        self.xpath_opcion_emitido = "/html/body/div[8]/div[1]/aside/ul/li[2]/a"
        self.xpath_desde = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[3]/input"
        self.xpath_hasta = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[5]/input"
        self.xpath_buscar = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[9]/input"
        self.xpath_tabla_opciones = '/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[3]/table'
        self.xpath_tabla_resultados = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[4]/div/div[2]/div[2]/div/table"
        self.xpath_nota_credito = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[3]/table/tbody/tr[4]/td[10]/a"
        self.xpath_paginacion = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[4]/div/center[1]/nav/ul[@class='pagination pagination-lg']/li"
        
    def iniciar_sesion(self):
        try:
            self.driver.get("https://escritorio.acepta.pe/")
            self._ingresar_valor_en_input_id("loginrut", self.usuario)
            self._ingresar_valor_en_input_name("LoginForm[password]", self.contrasena)
            self._hacer_clic_class_name("btn-acepta")
        except (WebDriverException, NoSuchElementException) as e:
            print(f"Error al iniciar sesión: {str(e)}")

    def seleccionar_opcion(self):
        try:
            elemento = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.xpath_opcion_emitido)))
            elemento.click()
        except Exception as e:
            print(f"Error al clickear en la opción: {str(e)}")

    def seleccionar_opciones(self, desde, hasta):
        try:
            self._ingresar_valor_en_input_xpath(self.xpath_desde, desde)
            self._ingresar_valor_en_input_xpath(self.xpath_hasta, hasta)

            self._hacer_clic_xpath(self.xpath_buscar)

            # Reemplazar time.sleep(5) con una espera explícita para que el elemento esté presente y sea clickeable
            espera = WebDriverWait(self.driver, 10)
            espera.until(EC.element_to_be_clickable((By.XPATH, self.xpath_nota_credito))).click()

            # Reemplazar time.sleep(3) con una espera explícita si es necesario después de hacer clic en nota_credito
            # espera.until(...)  # Agregar espera explícita si es necesario
        except Exception as e:
            print(f"Error al seleccionar opciones: {str(e)}")

    def extraer_estados(self):
        try:
            # Utilizar WebDriverWait en lugar de time.sleep
            espera = WebDriverWait(self.driver, 10)

            # Esperar a que la paginación esté presente
            paginacion_li = espera.until(EC.presence_of_all_elements_located((By.XPATH, self.xpath_paginacion)))
            # Lista para almacenar los datos
            datos_totales = []
            
            if not paginacion_li or len(paginacion_li) == 1:
                espera = WebDriverWait(self.driver, 10)
                espera.until(EC.presence_of_element_located((By.XPATH, self.xpath_tabla_resultados)))
                
                # Extraer datos de la tabla
                tabla_resultado = self.driver.find_element(By.XPATH, self.xpath_tabla_resultados)

                # Recorrer filas y columnas
                for fila in tabla_resultado.find_elements(By.TAG_NAME, 'tr'):
                    columnas = fila.find_elements(By.TAG_NAME, 'td')

                    if len(columnas) > 7:  
                        datos_totales.append((columnas[3].text, columnas[7].text))
            else:
                
                 for numero_pestaña in range(1, len(paginacion_li) - 1):
                    # Cambiar a la pestaña correspondiente
                    self.cambiar_pestaña(numero_pestaña)
                    
                    # Esperar a que la tabla esté presente
                    espera = WebDriverWait(self.driver, 10)
                    espera.until(EC.presence_of_element_located((By.XPATH, self.xpath_tabla_resultados)))
                    
                    # Extraer datos de la tabla
                    tabla_resultado = self.driver.find_element(By.XPATH, self.xpath_tabla_resultados)
                    
                    # Lista para almacenar los datos de la pestaña actual
                    datos_pestaña = []
                    
                     # Recorrer filas y columnas
                    for fila in tabla_resultado.find_elements(By.TAG_NAME, 'tr'):
                        columnas = fila.find_elements(By.TAG_NAME, 'td')

                        # Imprimir las columnas 1, 3 y 7
                        if len(columnas) > 7:  # Asegurarse de que hay suficientes columnas
                            # print(columnas[0].text, columnas[3].text, columnas[7].text)
                            datos_pestaña.append((columnas[3].text, columnas[7].text))

                    # Agregar los datos de la pestaña actual a la lista total
                    datos_totales.extend(datos_pestaña)

            # Convertir la lista de datos en un DataFrame
            df = pd.DataFrame(datos_totales, columns=['Estado', 'NRO CPE'])

            # Imprimir el DataFrame
            print(df)       
                
        except Exception as e:
            print(f"Error al imprimir datos de la tabla: {str(e)}")    
               
    def cambiar_pestaña(self, numero_pestaña):
        # Cambiar a la pestaña especificada
        self.driver.find_element(By.XPATH, f"//nav/ul[@class='pagination pagination-lg']/li/a[text()='{numero_pestaña}']").click()
    
    def cerrar_sesion(self):
        time.sleep(10)
        self.driver.quit()
        print("Sesión cerrada")

    # Funciones auxiliares
 # Funciones auxiliares
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



desde = "01122023"
hasta = "15122023"


# Crear instancia de AceptaFunctions
acepta_bot = AceptaFunctions()

# Ejecutar acciones
acepta_bot.iniciar_sesion()
acepta_bot.seleccionar_opcion()
acepta_bot.seleccionar_opciones(desde, hasta)
acepta_bot.extraer_estados()