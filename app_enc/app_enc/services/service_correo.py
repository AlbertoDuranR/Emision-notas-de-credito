from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Importando Variables de Entornos
from dotenv import load_dotenv
import os

class ServiceCorreo:
    ###
    data = []
    ###

    def __init__(self) -> None:
        pass

    def enviarCorreo(self):
        # Cargamos las variables de entorno
        load_dotenv()

        # Creando Instancia de correo
        msg = MIMEMultipart()

        # Configurando parametros de envio
        password = os.environ.get("PASSWORD")
        msg['From'] = os.environ.get("EMAIL_USER")
        # msg['To'] = os.environ.get("EMAIL_USER")
        msg['To'] = os.environ.get("EMAILS_TO")
        msg['Subject'] = "Reporte de Verificación de Productos"
        msg['CC'] = os.environ.get("EMAILS_CC")

        # Agregando contenido de mensaje
        # msg.attach(MIMEText(message, 'plain'))
        msg_contenido = ""
        #####

        #####
        for d in self.data:
            msg_contenido=msg_contenido+'''
<table style="margin: auto;">
                <thead>
                    <tr>
                    <th colspan="2" style="background-color: rgb(251 191 36); padding: 10px;">Solicitud de Emisión de Notas de Crédito</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="background-color: rgb(251 191 36)">
                        <td style="font-weight: bold; text-align: center;">Detalle</td>
                        <td style="font-weight: bold; text-align: center;">Datos</td>
                    </tr>
                    <tr>
                        <td colspan="2" style="font-weight: bold;">I. Documento de Origen</td>
                    </tr>
                    <tr>
                        <td>Fecha de Emisión</td>
                        <td style="text-align: center;">xxxxxx</td>
                    </tr>
                    <tr>
                        <td>Nro de Comprobante</td>
                        <td style="text-align: center;">xxxxxx</td>
                    </tr>
                    <tr>
                        <td>Importe Total</td>
                        <td style="text-align: center;">xxxxxx</td>
                    </tr>
                    <tr>
                        <td colspan="2" style="font-weight: bold;">II. Detalle de la Solicitud</td>
                    </tr>
                    <tr>
                        <td>Fecha</td>
                        <td style="text-align: center;">xxxxxx</td>
                    </tr>
                    <tr>
                        <td>Motivo</td>
                        <td style="text-align: center;">xxxxxx</td>
                    </tr>
                    <tr>
                        <td>Justificación</td>
                        <td style="text-align: center;">xxxxxx</td>
                    </tr>
                    <tr>
                        <td>Método</td>
                        <td style="text-align: center;">xxxxxx</td>
                    </tr>

                    
                </tbody>
            </table>
            <br>
'''
        #####
        msg.attach(MIMEText('''<!DOCTYPE html>
<html>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;font-size: 14px;">
    <div style="padding:20px 0px;width: 100%; height: 100%;">
        <img src="https://trujillodatalake.blob.core.windows.net/public/img/logo.png" style="height: 100px;">
        <div style="background-color:black;padding-top: 1px;padding-bottom: 1px;margin-top: 10px; margin-bottom: 20px;">
            <h2 style="color:white; font-size: 15px; margin-left: 14px;">Reporte de Emisión de Notas de Crédito</h2>
        </div>
        <div style="height: 100%; display: block; margin-bottom: 20px; padding-left: 15px;">
            <div style="height:100%;">
                <span style="font-weight: bold;">Tipo de Nota de Crédito: </span><span> Puntos de Venta</span>
            </div>
            <div style="height:100%;">
                <span style="font-weight: bold;">Market: </span><span>Market Bolivar</span>
            </div>
            <div style="height:100%;">
                <span style="font-weight: bold;">Solicitante: </span><span>José Licas Ludeña</span>
            </div>
        </div>
        <div style="justify-content: center; align-items: center; width: 100%; height: 100%; display: block;">
        '''+msg_contenido+'''
    </div>
    </div>
    <div style="margin-left: 14px; margin-top: 5px; font-size: 14px;">
            <span>El presente correo electrónico fue generado por un proceso automático, para más información o inconveniente por favor comuníquese con el área TI.
                <br><br><span style="background-color: black; color: white; font-weight: bold; padding-left: 5px; padding-right: 5px;">Saludos</span>
            </span>
        </div>
</body>
</html>''', 'html'))
        #####
        self.attach_file_to_email(msg, self.path_file)
        #####
        try:
            # Creando servidor
            server = smtplib.SMTP('smtp.outlook.com: 587')
            server.starttls()

            # Direccion de envio "DE"
            server.login(msg['From'], password)
            # Agregando CC
            emails = f"{msg['To']}, {msg['CC']}".split(",")
            # emails = f"{msg['To']}".split(",")

            # Direccion de envio "PARA"
            server.sendmail(msg['From'], emails, msg.as_string())
            server.quit()
        except Exception as e:
            print(e)
        else:
            print("Correo enviado correctamente a", (msg['To']))

    def attach_file_to_email(self, email_message, filename):
        # Abriendo archivo
        with open(filename, "rb") as f:
            file_attachment = MIMEApplication(f.read())
        # Agregamos archivo en cabecera
        file_name = filename.split("/")[-1]
        file_attachment.add_header(
            "Content-Disposition",
            f"attachment; filename= {file_name}",
        )
        # Agregamos el archivo en el mensaje
        email_message.attach(file_attachment)
    