import requests, json
 
class ApiDynamics:
    url = "https://mistr.operations.dynamics.com/"
    # url = "https://mistr-master.sandbox.operations.dynamics.com/"
   
    def get_Token(self):
        env = {
                "client_id":"53f3c906-9bfc-4a5d-89d8-30ce9a672481",
                "client_secret":"zNA3~9-5wuywwiflFbAP52cgJ_5wQ__Y48",
                "resource":f"{self.url}",
                "grant_type":"client_credentials"
            }
       
        endp = 'https://login.microsoftonline.com/ceb88b8e-4e6a-4561-a112-5cf771712517/oauth2/token'
       
        req = requests.post(endp,env)
       
        if req.status_code == 200:
            token = req.json()['access_token']
            print('token', token)
            return 'Bearer {0}'.format(token)
        else:
            return None

api=ApiDynamics()
api.get_Token()