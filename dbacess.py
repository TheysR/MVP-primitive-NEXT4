# local_db.py
# biblioteca de clases y funciones para extraer datos de ecartapi y guardar a base de datos local
'''
clases:
    LocalDatabase: clase para la conexion a base de datos local
functions:

'''
# conectar a la base de datos local de Next4
import sys
import sqlite3
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
from psycopg2 import __version__ as psycopg2_version
#
class LocalDatabase:
    '''
    Methods:
        connect()   conecta a db local
        execute()   ejecuta sql
        commit()    commmit
        close()     cierre conexion a db
    '''
    def __init__(self, db_type):
    #inicializa la clase con valores por defecto
        # asigna valores por defecto
        self.db_type = db_type
        self.host = "localhost"
        self.dbname = "postgres"
        self.db_user = "postgres"
        self.db_pass = ""
        self.sql_result = ""
        self.connection_sql = None
        self.cursor_sql = None
        if db_type == "":
            self.db_type = "postgres"

        match db_type:
            case "sqllite3":
                self.dbname = "DATA" # por defecto
            case "postgres":   #postgres es por defecto en caso de no asignar
                self.host = "localhost"
                self.dbname = "postgres"
                self.db_user = "postgres"
                self.db_pass = ""

# method: connect() : conecta a base de datos local
    def connect(self, **kwargs):
        # loop thru arguments
        for key, value in kwargs.items():
            match key:
                case "dbname":
                    self.dbname = value
                case "hostname":
                    self.host = value
                case "user":
                    self.db_user = value
                case "password":
                    self.db_pass = value
                case "dbtype":
                    self.db_type = value
            # end_match
        # end_for

        match self.db_type:
            case "postgres":
                print("Try connecting")
                try:
                    print("Connecting to db")
                    self.connection_sql= psycopg2.connect(
                    host = self.host,
                    database = self.dbname,
                    user = self.db_user,
                    password = self.db_pass,
                    connect_timeout = 3
                    )
                    print("Connected")
                except OperationalError as e:
                    print_psycopg2_exception(e)
                    self.connection_sql = None
                    return False
            case "sqlite3":
                self.connection_sql = sqlite3.connect(self.dbname)
                # falta chequear por exception
        # end_match
        # se supone que se conectó
        self.cursor_sql = self.connection_sql.cursor()
        return True
    # end connect()

    # method: close(): cierra conexion a db
    def close(self):
    # cierra conexion
        if self.connection_sql:
            self.connection_sql.close()
            # return status?
        else:
            print("no connection to close")
            return False

    # end method close()

    # method: commit(): commit transaction
    def commit(self):
        if self.connection_sql:
            self.connection_sql.commit()
            # return status?
    # end method commit()

    def rollback(self):
        if self.connection_sql:
            self.connection_sql.rollback()
            # return status?
    # end method rollback()
    # method: execute(): exexute sql statement
    def execute(self, sql_string, *var_list):
        if self.cursor_sql:
            try:
                self.cursor_sql.execute(sql_string, var_list)
            except Exception as e:
                print_psycopg2_exception(e)
                return False

# end class LocalDatabase
def print_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno
    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
