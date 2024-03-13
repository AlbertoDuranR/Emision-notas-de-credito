from dotenv import load_dotenv
import requests,json
import os
import pandas as pd
import multiprocessing
import dill
#
load_dotenv()
#
class ServiceDynamics:

    url = os.environ.get("url_api_dynamics_master")

    def get_Token(self):
        env = {
                "client_id":"53f3c906-9bfc-4a5d-89d8-30ce9a672481",
                "client_secret":"zNA3~9-5wuywwiflFbAP52cgJ_5wQ__Y48",
                "resource":f"{self.url}",
                "grant_type":"client_credentials"
            }
        endp = 'https://login.microsoftonline.com/ceb88b8e-4e6a-4561-a112-5cf771712517/oauth2/token'

        try:
            req = requests.post(endp,env)
            if req.status_code == 200:
                token = req.json()['access_token']
                # print('token' * 20, token)
                return 'Bearer {0}'.format(token)
            else:
                return None
        except:
            return None

    def fetch_data(self,query_update):
        token = self.get_Token()
        #Headers
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        response = requests.get(query_update, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def process_data(self,path,method=1,i=0):
        if method == 1:
            query_update = f"{path}"
            return self.fetch_data(query_update)
        elif method == 2:
            query_update = f"{path}&$top=1000&$skip={int(i)}"
            return self.fetch_data(query_update)["value"]

    def getProductsIssued(self):
        #Definir url
        path = f"{self.url}/data/AllProducts"
        # token = self.get_Token()
        #Queries
        query_temp = f"?$count=true&$top=1"
        path_temp=path+query_temp

        query = f"?$count=true&$select=ProductNumber,ProductDescription"
        path_final=path+query

        try:
            count_temp = self.process_data(path=path_temp)
            count = int((int(count_temp["@odata.count"]))/1000)
            if count >0:
                list_count = list(range(0,int(count_temp["@odata.count"])+1000,1000))
                result = []
                pool = multiprocessing.Pool()
                # results = pool.map(self.process_data,path_final,2,list_count)
                #results = pool.map(lambda x: self.process_data(path=path_final,method=2,i=x),list_count)
                # results = pool.map(process_data_method_2,list_count)
                # pool.close()
                # pool.join()
                # Apply the process_data_method_2 function asynchronously to each element in list_count
                results = [pool.apply_async(self.process_data,args=(path_final, 2, x)) for x in list_count]
                for item in results:
                    temp= list(item.get())
                    result.extend(temp)
                pool.close()
                pool.join()
                ##
                print(len(result))
                products = pd.read_json(json.dumps(result))
                products["Product"] = products["ProductNumber"].apply(str) +' - ' + products["ProductDescription"].apply(str)
                result = products[["ProductNumber","ProductDescription","Product"]]
                result = result.to_dict(orient='records')
                return result
            else:
                result = self.process_data(path=path_final)
                products = pd.read_json(json.dumps(result["value"]))
                products["Product"] = products["ProductNumber"].apply(str) +' - ' + products["ProductDescription"].apply(str)
                result = products[["ProductNumber","ProductDescription","Product"]]
                result = result.to_dict(orient='records')
                return result
        except Exception as e:
            print(e)
            return []

    def getUnitsConversion(self):
        #Definir url
        path = f"{self.url}/data/UnitsOfMeasure"
        token = self.get_Token()
        #Queries
        query = f"?$count=true&$select=UnitSymbol"
        #Headers
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        path=path+query

        try:
            response = requests.get(path,headers=headers)
            if response.status_code == 200:
                temp1= response.json()
                #
                count = int(int(temp1["@odata.count"])/10000)
                if count > 0 :
                    result= temp1["value"]
                    for i in range(count):
                        query_update = f"{path}&$top=10000&$skip={int(i)+1}0000"
                        response = requests.get(query_update,headers=headers)
                        if response.status_code == 200:
                            result.extend(response.json()["value"])
                    ##
                    products = pd.read_json(json.dumps(result))
                    result = products[["UnitSymbol"]]
                    result = result.to_dict(orient='records')
                    ##
                    return result
                else:
                    ##
                    products = pd.read_json(json.dumps(temp1["value"]))
                    result = products[["UnitSymbol"]]
                    result = result.to_dict(orient='records')
                    ##
                    return result
        except:
            return None

    def get_return_order_headers_by_return_order_number(self, return_order_number: str):
        """
            :param invoice_number: The invoice number to query.
                Ex. 'BG02-00052743'
            :return: A list of dictionaries containing invoice details.
                Ex.
                    [{
                        'SalesOrderNumber': 'TRV-02755697',
                        'SalesOrderOriginCode': 'PV',
                        'DefaultShippingWarehouseId': 'MD04_SUC',
                        'RequestedShippingDate': '2024-01-21T12:00:00Z',
                        'SalesOrderProcessingStatus': 'Invoiced',
                        'CustomerPaymentMethodName': 'FP015'
                    }]
        """
        # Definir url
        path = f"{self.url}/data/ReturnOrderHeaders"
        token = self.get_Token()
        query = f"?$count=true&$filter=ReturnOrderNumber eq '{return_order_number}'"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        full_path_url=f"{path}{query}"
        try:
            response = requests.get(full_path_url, headers=headers)
            response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            return_order_data = pd.read_json(json.dumps(data["value"]))
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
        token = self.get_Token()
        query = f"?$count=true&$select=SalesOrderOriginCode,DefaultShippingWarehouseId,RequestedShippingDate,SalesOrderProcessingStatus,PaymentTermsName,CustomerPaymentMethodName&$filter=SalesOrderNumber eq '{sales_order_number}'"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        full_path_url=f"{path}{query}"
        try:
            response = requests.get(full_path_url, headers=headers)
            response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            invoice_data = pd.read_json(json.dumps(data["value"]))
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
        path = f"{self.url}/data/SalesInvoiceHeaders"
        token = self.get_Token()
        query = f"?$count=true&$select=SalesOrderNumber,InvoiceDate,TotalTaxAmount,SalesOrderNumber,TotalInvoiceAmount,PaymentTermsName&$filter=InvoiceNumber eq '{invoice_number}'"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        full_path_url=f"{path}{query}"

        try:
            response = requests.get(full_path_url, headers=headers)
            response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            invoice_data = pd.read_json(json.dumps(data["value"]))
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
        path = f"{self.url}/data/SalesInvoiceHeaders"
        token = self.get_Token()
        query = f"?$count=true&$select=SalesOrderNumber&$filter=InvoiceNumber eq '{invoice_number}'"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        full_path_url=f"{path}{query}"

        try:
            response = requests.get(full_path_url, headers=headers)
            response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            invoice_data = pd.read_json(json.dumps(data["value"]))
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
        path = f"{self.url}/data/SalesInvoiceHeaders"
        token = self.get_Token()
        query = f"?$count=true&$filter=SalesOrderNumber eq '{sales_order_number}'"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        full_path_url=f"{path}{query}"

        try:
            response = requests.get(full_path_url, headers=headers)
            response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            invoice_data = pd.read_json(json.dumps(data["value"]))
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
        token = self.get_Token()
        query = f"?$count=true&$filter=InvoiceNumber eq '{invoice_number}'"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        full_path_url=f"{path}{query}"
        try:
            response = requests.get(full_path_url, headers=headers)
            response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            products = pd.read_json(json.dumps(data["value"]))
            products["Product"] = products["ProductNumber"].apply(str) +' - ' + products["ProductDescription"].apply(str)
            result = products[["ProductNumber", "ProductDescription", "Product", "InvoicedQuantity", "SalesPrice", "SalesUnitSymbol"]]
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
        token = self.get_Token()
        query = f"?$count=true&$select=PersonnelNumber, Name&$filter=PersonnelNumber eq '{personnel_number}'"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        full_path_url=f"{path}{query}"
        try:
            response = requests.get(full_path_url, headers=headers)
            response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            data = pd.read_json(json.dumps(data["value"]))
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
        token = self.get_Token()
        query = f"?$count=true&$select=PositionId, Description, WorkerName, DepartmentNumber, WorkerPersonnelNumber&$filter=WorkerPersonnelNumber eq '{worker_personnel_number}'"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        full_path_url=f"{path}{query}"
        try:
            response = requests.get(full_path_url, headers=headers)
            response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            data = pd.read_json(json.dumps(data["value"]))
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
        token = self.get_Token()
        query = f"?$count=true&$select=TransactionNumber, ReceiptId, TenderType&$filter=ReceiptId eq '{receip_id}'"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        full_path_url=f"{path}{query}"
        try:
            response = requests.get(full_path_url, headers=headers)
            response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            count_data = int(data["@odata.count"])
            if count_data == 0:
                return None
            data = pd.read_json(json.dumps(data["value"]))
            print('data retail transaction: ')
            print(data)
            result = data[
                ["TransactionNumber", "ReceiptId", "TenderType"]
            ]
            return result.to_dict(orient='records')
        except Exception as e:
            print(f"An exception occurred in get_retail_transaction_payment_lines_v2_by_receip_id: {e}")
            return None