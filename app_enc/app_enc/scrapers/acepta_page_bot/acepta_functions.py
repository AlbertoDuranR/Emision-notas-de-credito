# auxiliary_functions.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException

class AuxiliaryFunctions:
    @staticmethod
    def ingresar_valor_en_input_id(driver, wait, xpath, valor):
        elemento = wait.until(EC.element_to_be_clickable((By.ID, xpath)))
        elemento.clear()
        elemento.send_keys(valor)

    @staticmethod
    def ingresar_valor_en_input_name(driver, wait, xpath, valor):
        elemento = wait.until(EC.element_to_be_clickable((By.NAME, xpath)))
        elemento.clear()
        elemento.send_keys(valor)

    @staticmethod
    def ingresar_valor_en_input_xpath(driver, wait, xpath, valor):
        elemento = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elemento.clear()
        elemento.send_keys(valor)

    @staticmethod
    def hacer_clic_class_name(driver, wait, class_name):
        elemento = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
        elemento.click()

    @staticmethod
    def hacer_clic_xpath(driver, wait, xpath):
        elemento = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elemento.click()

