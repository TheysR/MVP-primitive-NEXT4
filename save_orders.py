1#creado por: Andres Marquez
#fecha de creacion: 13-09-22
#Ejecutado con Python -V == 3.9.5
#Fecha de ultima modificacion: 24-09-22
# version 1.1 (branch): limpieza y control (Theys Radmann)
# eliminado (comentado): sqlite3
#Librerias utilizadas
# import sqlite3 #SQLite3
# por hacer: pasar de Toga a formulario html (usando Quixote o pasar a Django) o bien usar Tkinter (es mas mainstream)
from asyncio.windows_events import NULL
import re
from tkinter import *
from tkinter import ttk
import psycopg2 #PostgreSQL
import requests #request a ecartapi
# import toga #front-end utilizado
from dbacess import LocalDatabase
from toga.style.pack import COLUMN, RIGHT, ROW, Pack


# from asyncio import timeout #front-end packages

global ldb
ver = "1.2"
#inserta los datos de tu PostGreSQL ACA abajo
# pg_host = "localhost" #por defecto
# pg_dbname = "postgres" #nombre de la base de datos de PostGreSQL
# pg_user = "postgres" #usuario de PostGreSQL
# pg_pass = "admin1234" #clave de PostGreSQL
ecart_url = "https://api.ecartapi.com/api/v2/orders"

# validador de numerico para port (4 digitos o menos)
def check_num(newval):
    return re.match('^[0-9]*$', newval) is not None and len(newval) <= 4

# crear tabla si no existe
def create_orders_table():
    global ldb

    #CODIGO PARA CREAR LA TABLA EN LA DB
    ldb.execute("""CREATE TABLE IF NOT EXISTS ORDERS (
            ID INTEGER,
            NUMBER INTEGER,
            NAME VARCHAR(255),
            EMAIL VARCHAR(255),
            STATUS VARCHAR(255),
            STATUS_ECARTAPI VARCHAR(255),
            SHIPPINGMETHOD VARCHAR(255),
            DESTINATARY VARCHAR(255),
            ADDRESS1 VARCHAR(255),
            ADDRESS2 VARCHAR(255),
            ADDRESS3 VARCHAR(255),
            COUNTRY_CODE VARCHAR(5),
            STATE_CODE VARCHAR(5),
            CITY VARCHAR(50),
            POSTALCODE INTEGER,
            PHONE VARCHAR(20),
            EMAIL_DESTINATARY VARCHAR(100),
            COMPANY VARCHAR(50),
            EXTRA VARCHAR(255)
            )""")

    result.set("Created Tables!")
    print(result.get())


def create_inventory_table():
    result.set("Aun no esta Desarrollado!")
    print(result)


def fetch_orders(token_auth):
    EcartApi_data = {
        "url" : ecart_url,
        "params" : {
            "status[status]" : "pending"
        },
        "headers" : {
            "Authorization" : token_auth
        }
    }
    #usar el endpoint para buscar los datos
    try:
        response = requests.get(url=EcartApi_data['url'], headers=EcartApi_data['headers'])
    except:
        print("Could not fetch from ecartapi")
        result.set("Error: could not fetch from Ecartapi")
        return None
    data_orders = response.json()
    return data_orders

def save_ecartapi_data():
    global ldb
    #datos de conexion a ecartapi
    #recorrer y almacenar la data_orders donde vienen todas las ordenes
    data_orders = fetch_orders(token)
    if data_orders is not None:
        for orders in data_orders["orders"]:
            order_id = orders["id"]
            order_number = orders["number"]
            order_name = orders["name"]
            order_email = orders["email"]
            order_status = orders["status"]["status"]
            order_status_ecartapi = orders["status"]["ecartapi"]
            #datos de direccion del destinatario
            order_shippingMethod = orders["shippingMethod"]
            order_destinatary_fullName = orders["shippingAddress"]["firstName"] + " " + orders["shippingAddress"]["lastName"]
            address_1 = orders["shippingAddress"]["address1"]
            address_2 = orders["shippingAddress"]["address2"]
            address_3 = orders["shippingAddress"]["address3"]
            code_country = orders["shippingAddress"]["country"]["code"]
            code_state  = orders["shippingAddress"]["state"]["code"]
            order_shippingAddress_city = orders["shippingAddress"]["city"]
            order_shippingAddress_postalCode = orders["shippingAddress"]["postalCode"]
            order_shippingAddress_phone = orders["shippingAddress"]["phone"]
            order_shippingAddress_email = orders["shippingAddress"]["email"]
            order_shippingAddress_company = orders["shippingAddress"]["company"]
            order_shippingAddress_references = orders["shippingAddress"]["references"]
            #insertar los datos a la DB de sqlite3
            #insertar los datos a la DB de PostGreSQL
            if ldb.execute("""INSERT INTO ORDERS(
                ID,
                NUMBER,
                NAME,
                EMAIL,
                STATUS,
                STATUS_ECARTAPI,
                SHIPPINGMETHOD,
                DESTINATARY,
                ADDRESS1,
                ADDRESS2,
                ADDRESS3,
                COUNTRY_CODE,
                STATE_CODE,
                CITY,
                POSTALCODE,
                PHONE,
                EMAIL_DESTINATARY,
                COMPANY,
                EXTRA
                ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(
                    order_id,
                    order_number,
                    order_name,
                    order_email,
                    order_status,
                    order_status_ecartapi,
                    order_shippingMethod,
                    order_destinatary_fullName,
                    address_1,
                    address_2,
                    address_3,
                    code_country,
                    code_state,
                    order_shippingAddress_city,
                    order_shippingAddress_postalCode,
                    order_shippingAddress_phone,
                    order_shippingAddress_email,
                    order_shippingAddress_company,
                    order_shippingAddress_references
                    )):

                # aqui, poner codigo para guardar en Invas WMS
                # primero, crear json
                # armar string
                # ejecutar post
                # si fue exitoso,guardar y cerrar la conexion a la DB
                        ldb.commit()
                        ldb.close()
                        result.set("Saved Orders!")
            # end_if
            else:
                # si no fue exitoso, dar error y rollback
                ldb.rollback()
                result.set("Error while inseerting orders into local db")


    # end_if

# funcion que guarda ordenes, llamada por botón en formulario Toga
def save_orders():
        global ldb
        host_name = host.get()
        db_name= dbname.get()
        pass_word=passw.get()
        db_user = user.get()
        ldb = LocalDatabase("postgres")
        print(ldb.db_type)
        try:
            ldb.connect(dbname=db_name, user=db_user, hostname=host_name, password=pass_word)
        except:
            result.set("Error: coud not connect to local db " + ldb.sql_result)
            print(result.get())
    #       return
        try:
            create_orders_table()
            save_ecartapi_data(token.get())
            result.set("Succesful!")
        except:
            pass

def save_inventory():
    pass
'''
def reset_inputs():
    global result, result_label

    host_input.value = ""
    host_input.value = "localhost"
    port_input.value = ""
    port_input.value = "5432"
    dbname_input.value = ""
    dbname_input.value = "postgres"
    user_input.value = ""
    user_input.value = "postgres"
    pass_input.value = ""
    token_input.value = ""
    result = "inicializado..."
    result_label.text = result
'''

root = Tk()
check_num_wrapper = (root.register(check_num), '%P')

root.title = ("Procesar Ordenes Nuevas")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe = ttk.Frame(root, padding="2 9 80 80")
mainframe.grid(column=0, row=0, sticky=(N, W, S, E))

host = StringVar()
host_input = ttk.Entry(mainframe, width=10, textvariable=host)
host_input.grid(column=2, row=1, sticky=(W, E))

port = StringVar()
port_input = ttk.Entry(mainframe, width=4, textvariable=port, validatecommand=check_num_wrapper)
port_input.grid(column=2, row=2, sticky=(W, E))

dbname = StringVar()
dbname_input = ttk.Entry(mainframe, width=10, textvariable=dbname)
dbname_input.grid(column=2, row=3, sticky=(W, E))

user = StringVar()
user_input = ttk.Entry(mainframe, width=10,textvariable=user)
user_input.grid(column=2, row=4, sticky=(W, E))

passw = StringVar()
passw_input = ttk.Entry(mainframe, width=15, textvariable=passw)
passw_input.grid(column=2, row=5, sticky=(W, E))

token = StringVar()
token_input = ttk.Entry(mainframe, width=40, textvariable=token)
token_input.grid(column=2, row=6, sticky=(W, E))

result = StringVar()
ttk.Label(mainframe, textvariable=result).grid(column=2, row=9, sticky=(W, E))

ttk.Label(mainframe, text="Host:").grid(column=1, row=1, sticky=(E))
ttk.Label(mainframe, text="Port:").grid(column=1, row=2, sticky=(E))
ttk.Label(mainframe, text="DB Name:").grid(column=1, row=3, sticky=(E))
ttk.Label(mainframe, text="User:").grid(column=1, row=4, sticky=(E))
ttk.Label(mainframe, text="Password:").grid(column=1, row=5, sticky=(E))
ttk.Label(mainframe, text="Ecartapi Token:").grid(column=1, row=6, sticky=(E))
ttk.Button(mainframe, text="Guardar ordenes en tabla orders", command=save_orders).grid(column=2, row=8, sticky=(W))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# set defaults
host.set("localhost")
dbname.set("postgres")
user.set("postgres")
port.set("5432")
token.set("eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ3UFRSVUx4andpOXp4aWZrVWZhMVlySWltYVk1RDI3SCIsImlhdCI6MTY2MzA5MTc4NTgxNn0.CNipxaKcOJ-2bpHz38yAT9Y-J65Hvk9znVDfgdjKpabQyNOlYjsVBOjbtq5zObpee0NwsEJM7phHyZMLCjTLDQ")

host_input.focus()
result.set("Inicializado")
root.mainloop()
