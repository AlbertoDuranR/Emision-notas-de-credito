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

    url = os.environ.get("url_api_dynamics")

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

        # def process_data_method_2(self,x):
        #     return self.process_data(path=path_final,method=2,i=x)

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
                #print(result)
                result = result.to_dict(orient='records')
                return result
            else:
                result = self.process_data(path=path_final)
                ###
                products = pd.read_json(json.dumps(result["value"]))
                products["Product"] = products["ProductNumber"].apply(str) +' - ' + products["ProductDescription"].apply(str)
                result = products[["ProductNumber","ProductDescription","Product"]]
                result = result.to_dict(orient='records')
                ##
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
    