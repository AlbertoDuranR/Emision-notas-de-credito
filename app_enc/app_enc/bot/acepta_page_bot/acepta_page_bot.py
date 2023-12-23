from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import pandas as pd


class Acepta_Bot_Selenium:
    def __init__(self) -> None:
        self.url = "https://escritorio.acepta.pe/"
        self.usuario = "wilfredo.caceres@terranovatrading.com.pe"
        self.contrasena = "118499544"
        self.driver = webdriver.Chrome()
        self.wait =  WebDriverWait(self.driver, 10)
        self.driver.maximize_window()

    def iniciar_sesion(self):
        try:
            self.driver.get(self.url)

            # Introducir el nombre de usuario y contraseña
            self.wait.until(EC.element_to_be_clickable((By.ID, "loginrut"))).send_keys(
                self.usuario
            )
            self.driver.find_element(By.NAME, "LoginForm[password]").send_keys(
                self.contrasena
            )

            # Hacer clic en el botón de ingresar
            self.driver.find_element(By.CLASS_NAME, "btn-acepta").click()

        except (WebDriverException, NoSuchElementException) as e:
            print(f"Error al iniciar sesión: {str(e)}")

    def seleccionar_opcion_emitido(self):
        try:
            xpath = "/html/body/div[8]/div[1]/aside/ul/li[2]/a"
            elemento = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elemento.click()
        except Exception as e:
            print(f"Error al clickear en la opción: {str(e)}")

    def seleccionar_opciones(self):
        try:
            # Seleccionar periodo desde
            xpath_desde = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[3]/input"
            elemento_desde = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_desde)))
            elemento_desde.send_keys("01122023")

            # Seleccionar periodo hasta
            xpath_hasta = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[5]/input"
            elemento_hasta = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_hasta)))
            elemento_hasta.send_keys("20122023")

            # Click en el botón de búsqueda
            xpath_buscar = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[2]/form/div[9]/input"
            elemento_buscar = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_buscar)))
            elemento_buscar.click()
           
            time.sleep(5)
           
            tabla_xpath = '/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[3]/table'
            self.wait.until(EC.presence_of_element_located((By.XPATH, tabla_xpath)))

            # Extraer datos de la tabla
            tabla = self.driver.find_element(By.XPATH, tabla_xpath)

            # Recorrer filas y columnas
            indice_fila_objetivo = 3  # Tercera fila (indexación basada en cero)
            indice_columna_objetivo = 9  # Décima columna (indexación basada en cero)
            elemento_objetivo  = None

            for i, fila in enumerate(tabla.find_elements(By.TAG_NAME, 'tr')):
                # Verificar si es la fila objetivo
                if i == indice_fila_objetivo:
                    columnas = fila.find_elements(By.TAG_NAME, 'td')

                    # Verificar si la columna objetivo existe
                    if len(columnas) > indice_columna_objetivo:
                        elemento_objetivo = columnas[indice_columna_objetivo].find_element(By.TAG_NAME, 'a')
                        break

            # Imprimir el valor si se encuentra
            if elemento_objetivo is not None:
                elemento_objetivo.click()
                print("Valor en la tercera fila, décima columna:")
            else:
                print("No se encontró el valor en la tercera fila, décima columna")
                    
            time.sleep(5)

        except Exception as e:
            print(f"Error al realizar la operación: {str(e)}")

                
        def cerrar_sesion(self):
            time.sleep(10)
            self.driver.quit()
            print("Sesión cerrada")

    def imprimir_datos_tabla(self):  # Agrega 'self' como primer parámetro
        try:
            
            
            # Encontrar todos los elementos <li> dentro de la estructura
            elementos_li = self.driver.find_elements(By.XPATH, "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[4]/div/center[1]/nav/ul[@class='pagination pagination-lg']/li")


            # Imprimir la cantidad de elementos <li>
            print(f"La cantidad de elementos <li> es: {len(elementos_li)}")
            
            # Imprimir cada elemento <li>
            for elemento in elementos_li:
                print(elemento.text)

            
            xpath_tabla = "/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div[4]/div/div[2]/div[2]/div/table"
            # Esperar a que la tabla esté presente
            espera = WebDriverWait(self.driver, 10)
            espera.until(EC.presence_of_element_located((By.XPATH, xpath_tabla)))

            # Extraer datos de la tabla
            tabla = self.driver.find_element(By.XPATH, xpath_tabla)
            
            # Lista para almacenar los datos
            datos = []

            # Recorrer filas y columnas
            for fila in tabla.find_elements(By.TAG_NAME, 'tr'):
                columnas = fila.find_elements(By.TAG_NAME, 'td')

                # Imprimir las columnas 1, 3 y 7
                if len(columnas) > 7:  # Asegurarse de que hay suficientes columnas
                    # print(columnas[0].text, columnas[3].text, columnas[7].text)
                    datos.append((columnas[3].text, columnas[7].text))
            
            # Convertir la lista de datos en un DataFrame
            df = pd.DataFrame(datos, columns=['Estado', 'NRO CPE'])

            # Imprimir el DataFrame
            print(df)

        except Exception as e:
            print(f"Error al imprimir datos de la tabla: {str(e)}")


bot = Acepta_Bot_Selenium()
bot.iniciar_sesion()
bot.seleccionar_opcion_emitido()
bot.seleccionar_opciones()
bot.imprimir_datos_tabla()  
