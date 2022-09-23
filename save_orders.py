#creado por: Andres Marquez
#fecha de creacion: 13-09-22
#Ejecutado con Python -V == 3.9.5
#Fecha de ultima modificacion: 20-09-22
#Librerias utilizadas
import sqlite3 #SQLite3
import psycopg2 #PostgreSQL
import requests #request a ecartapi
import toga #front-end utilizado
from toga.style.pack import COLUMN, RIGHT, ROW, Pack #front-end packages

global result
result = "inicializado..."
#inserta los datos de tu PostGreSQL ACA abajo
# pg_host = "localhost" #por defecto
# pg_dbname = "postgres" #nombre de la base de datos de PostGreSQL
# pg_user = "postgres" #usuario de PostGreSQL
# pg_pass = "admin1234" #clave de PostGreSQL

def db_connection(pg_host, pg_dbname, pg_user, pg_pass):
    #crea la DB DATA si no existe en postgres y en sqlite3
    global connection_sql3 , connection_pgsql, result, result_label
    connection_sql3 = sqlite3.connect("DATA")
    connection_pgsql = psycopg2.connect(
        host = pg_host,
        database = pg_dbname,
        user = pg_user,
        password = pg_pass
        )
    #cursores de las bases de datos
    global cursor_sql3 , cursor_pgsql
    cursor_sql3 = connection_sql3.cursor()
    cursor_pgsql = connection_pgsql.cursor()

    result = "Connection successfully!"
    print(result)
    result_label.text = result

def create_orders_table():
    global result, result_label
    #CODIGO PARA CREAR LA TABLA EN LA DB DATA de sqlite3
    cursor_sql3.execute("""CREATE TABLE IF NOT EXISTS ORDERS (
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
    #CODIGO PARA CREAR LA TABLA EN LA DB DATA de PostGreSQL
    cursor_pgsql.execute("""CREATE TABLE IF NOT EXISTS ORDERS (
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

    result = "Created Tables!"
    print(result)
    result_label.text = result

def create_inventory_table():
    result = "Aun no esta Desarrollado!"
    print(result)
    result_label.text = result

def save_ecartapi_data(token_auth):
    global result, result_label
    #datos de conexion a ecartapi
    EcartApi_data = {
        "url" : "https://api.ecartapi.com/api/v2/orders",
        "params" : {
            "status[status]" : "cancelled"
        },
        "headers" : {
            "Authorization" : token_auth
        }
    }
    #usar el endpoint para buscar los datos
    response = requests.get(url=EcartApi_data['url'], headers=EcartApi_data['headers'])
    data_orders = response.json()
    #recorrer y almacenar la data_orders donde vienen todas las ordenes
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
        cursor_sql3.execute("""INSERT INTO ORDERS(
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
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
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
                ))
        #insertar los datos a la DB de PostGreSQL
        cursor_pgsql.execute("""INSERT INTO ORDERS(
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
                ))
    #guardar y cerrar la conexion a la DB de sqlite3
    connection_sql3.commit()
    connection_sql3.close()
    #guardar y cerrar la conexion a la DB de PostGreSQL
    connection_pgsql.commit()
    connection_pgsql.close()

    result = "Saved Orders!"
    print(result)
    result_label.text = result

def save_orders(widget):
        global result, result_label
        try:
            db_connection(host_input.value, dbname_input.value, user_input.value, pass_input.value)
            create_orders_table()
            save_ecartapi_data(token_input.value)
        except:
            result = "Error!"
            result_label.text = result

def save_inventory(widget):
    pass

def reset_inputs(widget):
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

def build(app):

    box = toga.Box()

    result_box = toga.Box()

    host_box = toga.Box()
    port_box = toga.Box()
    dbname_box = toga.Box()
    user_box = toga.Box()
    pass_box = toga.Box()
    ecartapi_box = toga.Box()

    global result_label
    result_label = toga.Label(text=result, style=Pack(text_align=RIGHT))

    global host_input, port_input, dbname_input, user_input, pass_input, token_input
    host_input = toga.TextInput(value="localhost")
    port_input = toga.TextInput(value="5432")
    dbname_input = toga.TextInput(value="postgres")
    user_input = toga.TextInput(value="postgres")
    pass_input = toga.TextInput()
    token_input = toga.TextInput()

    host_label = toga.Label('HOST', style=Pack(text_align=RIGHT))
    port_label = toga.Label('PORT', style=Pack(text_align=RIGHT))
    dbname_label = toga.Label('DB NAME', style=Pack(text_align=RIGHT))
    user_label = toga.Label('USER', style=Pack(text_align=RIGHT))
    pass_label = toga.Label('PASSWORD', style=Pack(text_align=RIGHT))
    token_label = toga.Label('ECARTAPI TOKEN', style=Pack(text_align=RIGHT))

    save_button = toga.Button('Guardar ordenes en tabla orders', on_press=save_orders)
    reset_button = toga.Button('Reiniar y limpiar campos', on_press=reset_inputs)

    host_box.add(host_label)
    host_box.add(host_input)

    port_box.add(port_label)
    port_box.add(port_input)

    dbname_box.add(dbname_label)
    dbname_box.add(dbname_input)

    user_box.add(user_label)
    user_box.add(user_input)

    pass_box.add(pass_label)
    pass_box.add(pass_input)

    ecartapi_box.add(token_label)
    ecartapi_box.add(token_input)

    result_box.add(result_label)

    box.add(host_box)
    box.add(port_box)
    box.add(dbname_box)
    box.add(user_box)
    box.add(pass_box)
    box.add(ecartapi_box)
    box.add(save_button)
    box.add(result_box)
    box.add(reset_button)

    box.style.update(direction=COLUMN, padding_top=10)

    host_box.style.update(direction=ROW, padding=5)
    port_box.style.update(direction=ROW, padding=5)
    dbname_box.style.update(direction=ROW, padding=5)
    user_box.style.update(direction=ROW, padding=5)
    pass_box.style.update(direction=ROW, padding=5)
    ecartapi_box.style.update(direction=ROW, padding=5)
    result_box.style.update(direction=ROW, padding=5)

    host_input.style.update(flex=1, width=100, padding_left=10)
    port_input.style.update(flex=1, width=100, padding_left=10)
    dbname_input.style.update(flex=1, width=100, padding_left=10)
    user_input.style.update(flex=1, width=100, padding_left=10)
    pass_input.style.update(flex=1, width=100, padding_left=10)
    token_input.style.update(flex=1, width=100, padding_left=10)

    host_label.style.update(width=100, padding_left=10)
    port_label.style.update(width=100, padding_left=10)
    dbname_label.style.update(width=100, padding_left=10)
    user_label.style.update(width=100, padding_left=10)
    pass_label.style.update(width=100, padding_left=10)
    token_label.style.update(width=100, padding_left=10)

    result_label.style.update(width=100, padding_left=10, padding=5, flex=1)

    save_button.style.update(width=200, flex=1, padding=15)
    reset_button.style.update(width=200, flex=1, padding=15)

    return box

def main():
    return toga.App(
        'MVP primitivo - next4',
        'Andres.Marquez',
        startup=build,
        author="Andres Marquez",
        version="1.1.3",
        home_page="https://linkedin.com/in/andreslool",
        description="MVP muy primitivo del Middleware final (MVP del MVP)"
        )

if __name__ == '__main__':
    main().main_loop()