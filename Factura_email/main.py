#!/usr/bin/env python3



from tkinter import *
from tkinter import messagebox
import smtplib, getpass, os
import openpyxl as pxl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64


import tkinter.filedialog
from datetime import date



root = Tk()
root.title("Send Mail")

def SearchFile():
    file_path = tkinter.filedialog.askopenfile(parent=root,title='Escoge la base de datos') #abre el explorador de archivos y guarda la seleccion en la variable!
    abs_path = file_path.name
    database_textBox.config(state=NORMAL)
    database_textBox.insert(0, abs_path)
    database_textBox.config(state=DISABLED)
    return None



def SendMail():
    meses = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    path = direction_textBox.get()
    header = header_textBox.get()
    if header == '':
        header = f"Facturacion {meses[(date.today().month ) - 1]} del {date.today().year}"
    body = body_textBox.get()
    if body == '':
        body = "Descargue su factura."
    else:
        body = body
    database = database_textBox.get()
    sheet = sheet_textBox.get()
    
    aptos = get_emailFromDatabase(database,sheet)
    print(aptos)
    send_email(path,header,body,aptos)
    pass

def SearchPath():
    file_path = tkinter.filedialog.askdirectory(parent=root,title='Escoge la carpeta raiz') #abre el explorador de archivos y guarda la seleccion en la variable!
    abs_path = os.path.abspath(file_path)
    direction_textBox.config(state=NORMAL)
    direction_textBox.insert(0, abs_path)
    direction_textBox.config(state=DISABLED)
    return None

#Frames
frame_1 = Frame(root, width=500, height=400)
frame_1.pack()

#Text
title = Label(frame_1, text="FactuPH Send Mail", padx=200)
title.grid(row=0,column=0)

direction = Label(frame_1, text="Ingresa la direccion local de las facturas").grid(row=1,column=0)
header = Label(frame_1, text="Escribe el encabezado de la factura").grid(row=2,column=0)
body = Label(frame_1, text="Escribe aqui el cuerpo de la factura").grid(row=3,column=0)

database = Label(frame_1, text="Selecciona la base de datos").grid(row=4, column=0)
database = Label(frame_1, text="Selecciona la hoja dentro de la base de datos").grid(row=5, column=0)

#Entry boxes
direction_textBox = Entry(frame_1, state=DISABLED)
direction_textBox.grid(row= 1,column=1)
header_textBox = Entry(frame_1)
header_textBox.grid(row=2,column=1)
body_textBox = Entry(frame_1)
body_textBox.grid(row=3,column=1)
database_textBox = Entry(frame_1, state=DISABLED)
database_textBox.grid(row=4,column=1)
sheet_textBox = Entry(frame_1)
sheet_textBox.grid(row=5,column=1)

#Buttons
search_file = Button(frame_1, text="Buscar archivo", command=SearchFile).grid(row=4, column=2)
search_path = Button(frame_1, text="Buscar directorio",command=SearchPath).grid(row=1,column=2)
send = Button(frame_1,text="Enviar", command=SendMail).grid(row=6,column=1)

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
        while iterator < len(aptos):

                destinatario = aptos[iterator]
                archivo = (dir +'/'+str(archivos[iterator]))
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
        messagebox.showinfo(message="Facturacion enviada exitosamente", title="Felicidades")


if __name__ == '__main__':
    root.mainloop()