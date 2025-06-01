from datetime import datetime

import pymysql.cursors
from .conexion import ConexionMySQL
import pymysql

class LoginMySQL:
    
    @staticmethod
    def GetAdmin(data):
        try: 
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM `administrador` 
                    WHERE AdminUserName = %s 
                    AND AdminContraseña = %s
                """, (data['AdminUserName'],data['AdminContraseña'],))
                return cursor.fetchone()
        except pymysql.Error as error:
            print(f"Error al encontrar el administrador: {error}")
            return None
        finally:
            cone.close()