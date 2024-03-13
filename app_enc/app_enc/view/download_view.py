from django.http import HttpResponse, FileResponse
from django.views import View
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


class DownloadView:
    def getTxt(self, nro_nota_credito):
        try:
            download_dir = os.path.join(os.getcwd(),  'static\\downloads')
            file_name = nro_nota_credito
            print('download_dir', download_dir)
            # Encuentra el archivo descargado
            downloaded_file_path = os.path.join(download_dir, file_name)

            # Devuelve el archivo descargado como una respuesta de archivo de Django
            response = HttpResponse(open(downloaded_file_path, 'rb'))
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
            print('response_file:', response)
            return response
        except Exception as e:
            print("An error occurred:", str(e))
            # Si el archivo no existe, devuelve una respuesta indicando que no se encontró el archivo
            return HttpResponse('El archivo solicitado no se encontró', status=404)
