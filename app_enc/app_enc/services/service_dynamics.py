import requests
import os
import json
import jwt
import pandas as pd

from dotenv import load_dotenv
from datetime import datetime
from io import StringIO
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

load_dotenv()
is_development_mode = os.environ.get("ENVIRONMENT") == 'development'
is_production_mode = os.environ.get("ENVIRONMENT") == 'production'


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ServiceDynamics(metaclass=SingletonMeta):
    def __init__(self) -> None:
        print('INIT SERVICE DYNAMCIS')
        if is_development_mode:
            self.url = os.environ.get("url_api_dynamics_master")
        elif is_production_mode:
            self.url = os.environ.get("url_api_dynamics")
        self.token_dynamics = TokenDynamics(self.url)

    def fetch_data(self, full_path_url):
        """
        Fetches data from the given url using a token for authorization.

        Args:
            url (str): The URL url from which to fetch the data.

        Returns:
            dict or list: The JSON data returned from the request, or an empty list if the request fails.
        """
        print('fetch_data: ', full_path_url);
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            token = self.token_dynamics.get_token()
            headers = {
                "Authorization": token,
                "Content-Type": "application/json"
            }

            try:
                response = requests.get(full_path_url, headers=headers)
                response.raise_for_status()  # Raise an error for non-200 status codes
                return response.json()  # Return the JSON response
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 401:
                    print(f"Attempt {attempt + 1}: Unauthorized (401) - Refreshing token and retrying...")
                    self.token_dynamics.set_token_in_json()  # Method to refresh the token
                else:
                    print(f"HTTP error occurred: {http_err}")
                    return []
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data: {e}")
                return []  # Return an empty list if there's another type of error

            attempt += 1

        print(f"Failed to fetch data after {max_attempts} attempts")
        return []  # Return an empty list if all attempts fail


    def getUnitsConversion(self):
        #Definir url
        path = f"{self.url}/data/UnitsOfMeasure"
        query = f"?$count=true&$select=UnitSymbol"
        path = path+query

        try:
            temp1 = self.fetch_data(path)
            count = int(int(temp1["@odata.count"])/10000)
            if count > 0 :
                result= temp1["value"]
                for i in range(count):
                    path_query_update = f"{path}&$top=10000&$skip={int(i)+1}0000"
                    response = self.fetch_data(path_query_update)
                    result.extend(response.json()["value"])
                products = pd.read_json(StringIO(json.dumps(result)))
                result = products[["UnitSymbol"]]
                result = result.to_dict(orient='records')
                return result
            else:
                products = pd.read_json(StringIO(json.dumps(temp1["value"])))
                result = products[["UnitSymbol"]]
                result = result.to_dict(orient='records')
                return result
        except:
            return None

    def get_return_order_headers_by_return_order_number(self, return_order_number: str):
        """
            :param return_order_number: The ReturnOrderNumber to query.
                Ex. 'TRV-03299965'
            :return: A list of dictionaries containing return order details.
                Ex.
                    [{
                        'ReturnOrderNumber': 'TRV-03299965',
                        'ReturnAddressName': 'CLIENTE DESCRIPTIVO',
                        'RMANumber': 'TRV-009248',
                        'ReturnOrderStatus': 'Invoiced' | 'Backorder' | 'canceled'
                    }]
        """
        # Definir url
        path = f"{self.url}/data/ReturnOrderHeaders"
        query = f"?$count=true&$filter=ReturnOrderNumber eq '{return_order_number}'"
        full_path_url=f"{path}{query}"
        try:
            data = self.fetch_data(full_path_url)
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            return_order_data = pd.read_json(StringIO(json.dumps(data["value"])))
            result = return_order_data[
                ["ReturnOrderNumber", "ReturnAddressName", "RMANumber", "ReturnOrderStatus"]
            ]
            return result.to_dict(orient='records')
        except Exception as e:
            print(f"An exception occurred in get_sales_invoice_headers_by_invoice_number: {e}")
            return None

    def get_sales_order_headers_by_sales_order_number(self, sales_order_number: str):
        """
            :param invoice_number: The invoice number to query.
                Ex. 'TRV-02755697'
            :return: A list of dictionaries containing invoice details.
                Ex.
                    [{
                        "SalesOrderOriginCode": "PV",
                        "DefaultShippingWarehouseId": "MD04_SUC",
                        "RequestedShippingDate": "2024-02-22T12:00:00Z",
                        "SalesOrderProcessingStatus": "Invoiced",
                        "PaymentTermsName": "CONT",
                        "CustomerPaymentMethodName": "FP015"
                    }]
        """
        # Definir url
        path = f"{self.url}/data/SalesOrderHeaders"
        query = f"?$count=true&$select=SalesOrderOriginCode,DefaultShippingWarehouseId,RequestedShippingDate,SalesOrderProcessingStatus,PaymentTermsName,CustomerPaymentMethodName&$filter=SalesOrderNumber eq '{sales_order_number}'"
        full_path_url=f"{path}{query}"
        try:
            data = self.fetch_data(full_path_url)
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            invoice_data = pd.read_json(StringIO(json.dumps(data["value"])))
            result = invoice_data[
                [
                 "SalesOrderOriginCode",
                 "DefaultShippingWarehouseId",
                 "RequestedShippingDate",
                 "SalesOrderProcessingStatus",
                 "PaymentTermsName",
                 "CustomerPaymentMethodName"
                ]
            ]
            return result.to_dict(orient='records')
        except Exception as e:
            print(f"An exception occurred in get_sales_invoice_headers_by_invoice_number: {e}")
            return None

    def get_sales_invoice_headers_by_invoice_number(self, invoice_number: str):
        """
            :param invoice_number: The invoice number to query.
                Ex. 'BG02-00052743'
            :return: A list of dictionaries containing invoice details.
                Ex.
                    [{
                        "SalesOrderNumber": "TRV-02931050",
                        "InvoiceDate": "2024-02-22T12:00:00Z",
                        "TotalTaxAmount": 1.06,
                        "TotalInvoiceAmount": 6.9,
                        "PaymentTermsName": "CONT"
                    }]
        """
        # Definir url
        path = f"{self.url}/data/SalesInvoiceHeadersV2"
        query = f"?$count=true&$select=SalesOrderNumber,InvoiceDate,TotalTaxAmount,SalesOrderNumber,TotalInvoiceAmount,PaymentTermsName&$filter=InvoiceNumber eq '{invoice_number}'"
        full_path_url=f"{path}{query}"

        try:
            data = self.fetch_data(full_path_url)
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            # Envuelve la cadena JSON en un objeto StringIO.
            json_buffer = StringIO(json.dumps(data["value"]))
            invoice_data = pd.read_json(json_buffer)
            result = invoice_data[
                ["InvoiceDate", "TotalTaxAmount", "SalesOrderNumber", "TotalInvoiceAmount", "PaymentTermsName"]
            ]
            return result.to_dict(orient='records')
        except Exception as e:
            print(f"An exception occurred in get_sales_invoice_headers_by_invoice_number: {e}")
            return None

    def get_sales_oder_number_by_invoice_number(self, invoice_number: str):
        """
            :param invoice_number: The invoice number to query.
                Ex. 'BG02-00052743'
            :return: A list of dictionaries containing invoice details.
                Ex.
                    [{ 'InvoiceNumber': 'BG02-00052743' }]
        """
        # Definir url
        path = f"{self.url}/data/SalesInvoiceHeadersV2"
        query = f"?$count=true&$select=SalesOrderNumber&$filter=InvoiceNumber eq '{invoice_number}'"
        full_path_url=f"{path}{query}"

        try:
            data = self.fetch_data(full_path_url)
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            invoice_data = pd.read_json(StringIO(json.dumps(data["value"])))
            result = invoice_data[["InvoiceNumber"]]
            return result.to_dict(orient='records')
        except Exception as e:
            print(f"An exception occurred in get_sales_invoice_headers_by_invoice_number: {e}")
            return None

    def get_sales_invoice_headers_by_sales_order_number(self, sales_order_number: str):
        """
            :param invoice_number: The invoice number to query.
                Ex. 'TRV-02756528'
            :return: A list of dictionaries containing invoice details.
                Ex.
                    [{
                        'InvoiceNumber': 'BG02-00052743',
                        'InvoiceDate': '2024-01-10T12:00:00Z',
                        'TotalTaxAmount': 29.07,
                        'SalesOrderNumber': 'TRV-02697594',
                        'TotalInvoiceAmount': 190.6,
                        'PaymentTermsName' : 'CONT'
                    }]
        """
        # Definir url
        path = f"{self.url}/data/SalesInvoiceHeadersV2"
        query = f"?$count=true&$filter=SalesOrderNumber eq '{sales_order_number}'"
        full_path_url=f"{path}{query}"

        try:
            data = self.fetch_data(full_path_url)
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            invoice_data = pd.read_json(StringIO(json.dumps(data["value"])))
            result = invoice_data[
                ["InvoiceNumber", "InvoiceDate", "TotalTaxAmount", "SalesOrderNumber", "TotalInvoiceAmount", "PaymentTermsName"]
            ]
            return result.to_dict(orient='records')
        except Exception as e:
            print(f"An exception occurred in get_sales_invoice_headers_by_sales_order_number: {e}")
            return None

    def get_sales_invoice_lines(self, invoice_number: str):
        """
            :param invoice_number: The invoice number to query.
            :return: A list of dictionaries containing invoice lines details.
        """
        # https://mistr.operations.dynamics.com/data/SalesInvoiceLines?$count=true&$filter=InvoiceNumber eq 'BA01-00249590'
        # Definir url
        path = f"{self.url}/data/SalesInvoiceLines"
        query = f"?$count=true&$filter=InvoiceNumber eq '{invoice_number}'"
        full_path_url=f"{path}{query}"
        try:
            data = self.fetch_data(full_path_url)
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            products = pd.read_json(StringIO(json.dumps(data["value"])))
            products["Product"] = products["ProductNumber"].apply(str) +' - ' + products["ProductDescription"].apply(str)
            result = products[["ProductNumber", "ProductDescription", "Product", "InvoicedQuantity", "SalesPrice", "SalesUnitSymbol", "LineAmount"]]
            return result.to_dict(orient='records')
        except Exception as e:
            print(f"An exception occurred in get_sales_invoice_lines_by_invoice_number: {e}")
            return None

    def get_employeesv2_by_personnel_number(self, personnel_number: str):
        '''
            :param personnel_number: DNI
            :return: [{"PersonnelNumber": "" , "Name": ""}]
        '''
        # https://mistr.operations.dynamics.com/data/EmployeesV2?$count=true&$select=PersonnelNumber, Name&$filter=PersonnelNumber eq '47518569'
        # Definir url
        path = f"{self.url}/data/EmployeesV2"
        query = f"?$count=true&$select=PersonnelNumber, Name&$filter=PersonnelNumber eq '{personnel_number}'"
        full_path_url=f"{path}{query}"
        try:
            data = self.fetch_data(full_path_url)
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            data = pd.read_json(StringIO(json.dumps(data["value"])))
            result = data[
                ["PersonnelNumber", "Name"]
            ]
            return result.to_dict(orient='records')
        except Exception as e:
            print(f"An exception occurred in get_employeesv2_by_personnel_number: {e}")
            return None

    def get_positionsv2_by_personnel_number(self, worker_personnel_number: str):
        '''
            :param personnel_number: DNI
            :return: [{
                "PositionId": "P0070",
                "Description": "Auxiliar de Almacén",
                "WorkerName": "ELVIS CRISTHIAN CHAUCA CORAL",
                "DepartmentNumber": "D012",
                "WorkerPersonnelNumber": "75650740"
                }]
        '''
        # https://mistr.operations.dynamics.com/data/PositionsV2?$count=true&$select=PositionId, Description, WorkerName, DepartmentNumber, WorkerPersonnelNumber&$filter=WorkerPersonnelNumber eq '75650740'
        # Definir url
        path = f"{self.url}/data/PositionsV2"
        query = f"?$count=true&$select=PositionId, Description, WorkerName, DepartmentNumber, WorkerPersonnelNumber&$filter=WorkerPersonnelNumber eq '{worker_personnel_number}'"
        full_path_url=f"{path}{query}"
        try:
            data = self.fetch_data(full_path_url)
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            data = pd.read_json(StringIO(json.dumps(data["value"])))
            result = data[
                ["PositionId", "Description", "WorkerName", "DepartmentNumber", "WorkerPersonnelNumber"]
            ]
            return result.to_dict(orient='records')
        except Exception as e:
            print(f"An exception occurred in get_positionsv2_by_personnel_number: {e}")
            return None

    def get_retail_transaction_payment_lines_v2_by_receip_id(self, receip_id: str):
        '''
            :param receip_id: Nro_comprobante
            :return: [{
                "TransactionNumber": "000022-000089-73574",
                "ReceiptId": "BB06-00068688",
                "TenderType": "1",
                }]
        '''
        # https://mistr.operations.dynamics.com/data/RetailTransactionPaymentLinesV2?$count=true&$select=TransactionNumber, ReceiptId, TenderType&$filter=ReceiptId eq 'BB06-00068688'
        # Definir url
        path = f"{self.url}/data/RetailTransactionPaymentLinesV2"
        query = f"?$count=true&$select=TransactionNumber, ReceiptId, TenderType&$filter=ReceiptId eq '{receip_id}'"
        full_path_url=f"{path}{query}"
        try:
            data = self.fetch_data(full_path_url)
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            data = pd.read_json(StringIO(json.dumps(data["value"])))
            print('data retail transaction: ')
            print(data)
            result = data[
                ["TransactionNumber", "ReceiptId", "TenderType"]
            ]
            return result.to_dict(orient='records')
        except Exception as e:
            print(f"An exception occurred in get_retail_transaction_payment_lines_v2_by_receip_id: {e}")
            return None


class TokenDynamics():
    def __init__(self, url) -> None:
        print('INIT TOKEN DYNAMICS', url)
        self.url = url

    def _decode_token(self, token):
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except ExpiredSignatureError:
            print("El token ha expirado.")
            return None
        except InvalidTokenError:
            print("El token es inválido.")
            return None

    def _expired_token(self, payload):
        if payload:
            expiracion = payload.get("exp", 0)
            if expiracion > 0:
                exp_timestamp = datetime.utcfromtimestamp(expiracion)
                curr_date = datetime.utcnow()
                expired_token = exp_timestamp < curr_date
                # print('entro expired_token', expired_token, exp_timestamp, curr_date)
                if expired_token:
                    print("El token ha expirado.")
                else:
                    print("El token es válido hasta:", exp_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                return expired_token
            else:
                print("El token no incluye información de expiración.")
        else:
            print('Sin payload', payload)

    def set_token_in_json(self):
        env = {
                "client_id": os.environ.get("CLIENT_ID_DYNAMICS"),
                "client_secret": os.environ.get("CLIENT_SECRET_DYNAMICS"),
                "resource":f"{self.url}",
                "grant_type":"client_credentials"
            }
        endp = 'https://login.microsoftonline.com/ceb88b8e-4e6a-4561-a112-5cf771712517/oauth2/token'

        try:
            req = requests.post(endp,env)
            if req.status_code == 200:
                token = req.json()['access_token']
                # print('token' * 20, token)
                # Guardar el token en un archivo JSON
                data = {"dynamics_token": token}
                print('set_token_in_json', data)
                # Ruta al directorio static de tu aplicación Django
                directorio_static = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'services')
                ruta_json = os.path.join(directorio_static, 'data_token.json')
                with open(ruta_json, 'w') as json_file:
                    json.dump(data, json_file)
            else:
                return None
        except:
            return None

    def is_active_token(self, token):
        payload = self._decode_token(token)
        if payload is None:
            return False
        return not self._expired_token(payload)

    def get_token_from_json(self):
        # Cargar el token desde el archivo JSON
        try:
            # Ruta al directorio static de tu aplicación Django
            directorio_static = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'services')
            ruta_json = os.path.join(directorio_static, 'data_token.json')
            with open(ruta_json, 'r') as json_file:
                data = json.load(json_file)
                return data["dynamics_token"]
        except FileNotFoundError as e:
            print(e)
            return None

    def get_token(self):
        # Cargar el token desde el archivo JSON
        token = self.get_token_from_json()
        try:
            if token == '' or not self.is_active_token(token):
                self.set_token_in_json()
                token = self.get_token_from_json()
                print('Token: ', token)
            return 'Bearer {0}'.format(token)
        except FileNotFoundError as e:
            print(e)
            return None