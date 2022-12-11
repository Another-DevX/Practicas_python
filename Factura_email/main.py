import smtplib, getpass, os
import openpyxl as pxl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64



def get_emailFromDatabase(database, sheet_name):

        excel_document = pxl.load_workbook(database)    
        sheet = excel_document.get_sheet_by_name(sheet_name)
        mail_cells = sheet['C2' : 'C243'] #Realmente para facilidad del uso actual, es preferible dejar esto como un rango estatico, aunque lo ideal seria integrar una variable
        aptos=[]
        for row in mail_cells:
                for cell in row:
                        aptos.append(cell.value)
        return aptos


def send_email(dir,subject, bodyText, aptos):
        archivos = os.listdir(dir) 

        print("**** Enviar email con Gmail ****")
        user = ('factuphonline@gmail.com')
        password = ('txqldgjhfxxuhxpq')

        #Para las cabeceras del email
        remitente = ('Administracion Sol del rodeo')
        asunto = (subject)
        body = (bodyText)
        iterator = 0
        while iterator < 245:

                destinatario = aptos[iterator]
                archivo = (dir + str(archivos[iterator]))
                print(f'La celda actual es: {iterator + 2}')
        
                #Host y puerto SMTP de Gmail
                gmail = smtplib.SMTP('smtp.gmail.com', 587)

                #protocolo de cifrado de datos utilizado por gmail
                gmail.starttls()

                #Credenciales
                gmail.login(user, password)

                #muestra la depuraci�n de la operacion de env�o 1=true

                gmail.set_debuglevel(1)

                header = MIMEMultipart()
                header['Subject'] = asunto
                header['From'] = remitente
                header['To'] = destinatario
                header.attach(MIMEText(body, 'plain'))


                #Adjuntamos archivo

                adjunto = MIMEBase('application', 'octet-stream')
                adjunto.set_payload(open(archivo, "rb").read())
                encode_base64(adjunto)
                adjunto.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(archivo))
                header.attach(adjunto)

                #Enviar email
                
                gmail.sendmail(remitente, destinatario,header.as_string())
                iterator += 1

        #Cerrar la conexi�n SMTP
        gmail.quit()



if __name__ == '__main__':
        #Aca va el nombre de el archivo de la base de datos, y la pagina en que se encuentra
        aptos = get_emailFromDatabase('BASE DE DATOS sol del rodeo.xlsx','Hoja1')
        #Direccion en donde se encuentran las facturas en formato pdf, Asunto email, mensaje email
        send_email('C://Users/Luis/Desktop/SolDelRodeoDic/','Facturacion diciembre 2022','Descargue su factura',aptos)



