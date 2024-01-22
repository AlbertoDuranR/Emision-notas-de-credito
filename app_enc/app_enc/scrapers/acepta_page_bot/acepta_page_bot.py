# acepta_functions.py
from dotenv import load_dotenv
import os
import pandas as pd
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .acepta_functions import AuxiliaryFunctions

load_dotenv()

class AceptaScraper:
    def __init__(self):
        # Credenciales
        self.url = "https://escritorio.acepta.pe/"
        self.usuario = "wilfredo.caceres@terranovatrading.com.pe"
        self.contrasena = "118499544"

        # XPaths
        self.xpath_opcion_emitido = "/html/body/div[8]/div[1]/aside/ul/li[2]/a"
        self.xpath_desde = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[3]/input"
        self.xpath_hasta = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[5]/input"
        self.xpath_serie = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[11]/input"
        self.xpath_correlativo_desde = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[13]/input"
        self.xpath_buscar = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[9]/input"
        self.xpath_busqueda_avanzada = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[1]/form/div[5]/a"
        self.xpath_buscar_avanzado = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[25]/input"
        self.xpath_tabla_opciones = '/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[3]/table'
        self.xpath_tabla_resultados = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[4]/div/div[2]/div[2]/div/table"
        self.xpath_nota_credito = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[3]/table/tbody/tr[4]/td[10]/a"
        self.xpath_paginacion = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[4]/div/center[1]/nav/ul[@class='pagination pagination-lg']/li"

    def config_navigator(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.wait_10 = WebDriverWait(self.driver , 10)
        self.wait_20 = WebDriverWait(self.driver , 20)
        self.driver.maximize_window()

    def iniciar_sesion(self):
        try:
            self.driver.get(self.url)
            self._ingresar_valor_en_input_id("loginrut", self.usuario)
            self._ingresar_valor_en_input_name("LoginForm[password]", self.contrasena)
            self._hacer_clic_class_name("btn-acepta")
        except (WebDriverException, NoSuchElementException) as e:
            print(f"Error al iniciar sesión: {str(e)}")

    def seleccionar_opcion_emitidos(self):
        try:
            elemento = self.wait_10.until(EC.element_to_be_clickable((By.XPATH, self.xpath_opcion_emitido)))
            elemento.click()
        except Exception as e:
            print(f"Error al clickear en la opción emitidos: {str(e)}")

    def seleccionar_busqueda_avanzada(self):
        try:
            elemento = self.wait_10.until(EC.element_to_be_clickable((By.XPATH, self.xpath_busqueda_avanzada)))
            elemento.click()
        except Exception as e:
            print(f"Error al clickear en en opciones avanzadas: {str(e)}")

    def buscar_comprobante(self, serie, correlativo_desde):
        try:
            # Reemplazar time.sleep(3) con una espera explícita si es necesario después de hacer clic en nota_credito
            # espera.until(...)  # Agregar espera explícita si es necesario
            self._ingresar_valor_en_input_xpath(self.xpath_serie, serie)
            self._ingresar_valor_en_input_xpath(self.xpath_correlativo_desde, correlativo_desde)
            self._hacer_clic_xpath(self.xpath_buscar_avanzado)
        except Exception as e:
            print(f"Error al seleccionar opciones: {str(e)}")

    def extraer_estado_por_comprobante(self, nro_comprobante):
        serie, correlativo_desde = nro_comprobante.split('-')
        # Vista de Documentos Emitidos - Opciones avanzadas
        self.buscar_comprobante(serie, correlativo_desde)
        try:
            # Esperar a que la tabla esté presente
            self.wait_10.until(EC.presence_of_element_located((By.XPATH, self.xpath_tabla_resultados)))
            # Extraer datos de la tabla
            tabla_resultado = self.driver.find_element(By.XPATH, self.xpath_tabla_resultados)
        except TimeoutException:
            print("No se encontro la tabla de estados")
            return None

        try:
            datos_totales = []
            # Recorrer filas y columnas
            for fila in tabla_resultado.find_elements(By.TAG_NAME, 'tr'):
                # print('fila:', fila)
                columnas = fila.find_elements(By.TAG_NAME, 'td')
                if len(columnas) > 7:
                    datos_totales.append((columnas[3].text, columnas[7].text))
            # Convertir la lista de datos en un DataFrame
            df = pd.DataFrame(datos_totales, columns=['Estado', 'NRO CPE'])
            # Crear la lista de diccionarios
            lista_diccionarios = df.set_index('NRO CPE')['Estado'].to_dict()
            # Imprimir el DataFrame
            print(df)
            return lista_diccionarios[nro_comprobante]
        except Exception as e:
            print(f"Error al imprimir datos de la tabla: {str(e)}")

    def get_estado_por_comprobante(self, nro_comprobante: str):
        self.config_navigator()
        # Ejecutar acciones
        self.iniciar_sesion()
        self.seleccionar_opcion_emitidos()
        self.seleccionar_busqueda_avanzada()
        estado_comprobante = self.extraer_estado_por_comprobante(nro_comprobante)
        self.cerrar_sesion()
        return estado_comprobante

    def cerrar_sesion(self):
        time.sleep(10)
        self.driver.quit()
        print("Sesión cerrada")

    # Funciones auxiliares
    def _ingresar_valor_en_input_id(self, xpath, valor):
        AuxiliaryFunctions.ingresar_valor_en_input_id(self.driver, self.wait_10, xpath, valor)

    def _ingresar_valor_en_input_name(self, xpath, valor):
        AuxiliaryFunctions.ingresar_valor_en_input_name(self.driver, self.wait_10, xpath, valor)

    def _ingresar_valor_en_input_xpath(self, xpath, valor):
        AuxiliaryFunctions.ingresar_valor_en_input_xpath(self.driver, self.wait_10, xpath, valor)

    def _hacer_clic_class_name(self, class_name):
        AuxiliaryFunctions.hacer_clic_class_name(self.driver, self.wait_10, class_name)

    def _hacer_clic_xpath(self, xpath):
        AuxiliaryFunctions.hacer_clic_xpath(self.driver, self.wait_10, xpath)

"""
    Para Obtener el rango de tiempo de busqueda
    Buscara desde hoy a un día antes
"""
import datetime
# Obtener la fecha actual
curr_date = datetime.datetime.now()
# Crear un objeto timedelta con un día de duración
dias = datetime.timedelta(days=1)
# Restar un día a la fecha actual
yesterday = curr_date - dias
# Formatear la fecha en formato "DDMMAAAA"
fecha_hoy = curr_date.strftime("%d%m%Y")
fecha_ayer = yesterday.strftime("%d%m%Y")
# Imprimir la fecha formateada
print(fecha_hoy, fecha_ayer)

desde = "01122023"
hasta = "15122023"

nro_comprobantes = ['BC11-00000329', 'BC11-00000329X', 'BA01-00249590', 'BA01-00249590']

"""
    INIT BOT
"""
# # Crear instancia de AceptaScraper
# acepta_bot = AceptaScraper()

# # Ejecutar acciones
# acepta_bot.iniciar_sesion()
# acepta_bot.seleccionar_opcion_emitidos()
# acepta_bot.seleccionar_busqueda_avanzada()
# # acepta_bot.seleccionar_opciones(fecha_ayer, fecha_hoy)
# # acepta_bot.buscar_comprobante(serie, correlativo_desde)
# # estado_comprobante = acepta_bot.extraer_estado_por_comprobante('BA01-00249590')
# for nro_comprobante in nro_comprobantes:
#     estado_comprobante = acepta_bot.extraer_estado_por_comprobante(nro_comprobante)
#     print(f'Estado Comprobante: {nro_comprobante} : {estado_comprobante if estado_comprobante else 'No Existe'}')
#     time.sleep(1)
# # acepta_bot.extraer_estados()
# acepta_bot.cerrar_sesion()
