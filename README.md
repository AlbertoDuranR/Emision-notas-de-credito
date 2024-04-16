# APLICATIVO EMISION NOTAS DE CREDITO

## Iniciar el aplicativo

instalamos y habilitamos el entorno virtual

entramos a la carpeta app_enc

pip install -r requirements.txt

pip install pandas

pip install dill

python manage.py runserver

abrimos otro terminal 

entramos a app_enc

npm install

actualizamos las librerias

pip freeze > requirements.txt

Activamos el entorno virtual

.\venv\Scripts\activate

cd app_enc

python manage.py runserver

cd app_enc

npm install

npm run dev

## Iniciar Aplicativo en producción
### 1. Levantar .venv
En la carpeta de Emision-notas-de-credito
''' .\.venv\Scripts\activate '''

### 2. Backend - django
Ingresar a "..\Emision-notas-de-credito\app_enc" y ejecutar
''' python manage.py runserver 10.5.0.11:8000 '''

## 3. Frontend - VueJS
Ingresar a "..\Emision-notas-de-credito\app_enc" y ejecutar:
''' npm run dev '''