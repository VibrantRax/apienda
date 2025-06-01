from datetime import datetime
from .conexion import ConexionMySQL
import pymysql

class GendersMySQL:

    @staticmethod
    def ViewGenders():
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT * 
                    FROM genero 
                    WHERE GeneroStatus = 'A'
                """)
                return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Error al mostrar los generos: {error}")
            return []
        finally:
            cone.close()
            
    @staticmethod
    def ViewGendersByID(id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM `genero` WHERE GeneroID = %s
                """, (id,))
                return cursor.fetchone()
        except pymysql.Error as error:
            print(f"Error al mostrar el genero: {error}")
            return None
        finally:
            cone.close()
            
    @staticmethod
    def UpdateGenders(data, id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                sql = """
                    UPDATE genero SET
                        GeneroDescripcion = %s, 
                        GeneroFechMod = %s 
                    WHERE genero.GeneroID = %s
                """ 
                values = (
                    data['GeneroDescripcion'],
                    datetime.now(),
                    id
                ) 
                rows = cursor.execute(sql, values)
                cone.commit()
                return rows > 0     

        except pymysql.Error as error:
            print(f"Error al actualizar el genero: {error}")
            return False
        finally:
            cone.close()
            
    @staticmethod
    def CreateGenders(data):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(GeneroID) AS max_id FROM genero")        
                result = cursor.fetchone()
                max_id = result['max_id'] or 4000
                
                new_id = max_id + 1
                fechmod = datetime.now()
                status = 'A'

                sql = """
                    INSERT INTO genero (
                        GeneroID, GeneroDescripcion, 
                        GeneroFechMod, GeneroStatus
                    ) VALUES (%s, %s, %s, %s);
                """
                values = (
                    new_id,
                    data['GeneroDescripcion'],
                    fechmod,
                    status
                )
                
                cursor.execute(sql, values)
                cone.commit()
                return new_id

        except pymysql.Error as error:
            print(f"Error al crear el genero: {error}")
            return None
        finally:
            cone.close()
            
    @staticmethod
    def DeleteGenders(id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                
                fechmod = datetime.now()
                status = 'N'
                
                sql = "UPDATE genero SET GeneroFechMod = %s, GeneroStatus = %s WHERE GeneroID = %s"
                values = (fechmod,status,id) 
                rows = cursor.execute(sql, values)
                cone.commit()
                return rows > 0
        except pymysql.Error as error:
            print(f"Error al eliminar el genero: {error}")
            return False
        finally:
            cone.close()