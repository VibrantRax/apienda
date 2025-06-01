from datetime import datetime
from .conexion import ConexionMySQL
import pymysql

class PlatfomsMySQL:

    @staticmethod
    def ViewPlatfoms():
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM `plataforma` WHERE PlataformaStatus = 'A'
                """)
                return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Error al mostrar las plataformas: {error}")
            return []
        finally:
            cone.close()
            
    @staticmethod
    def ViewPlatfomsByID(id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM `plataforma` WHERE PlataformaID = %s
                """, (id,))
                return cursor.fetchone()
        except pymysql.Error as error:
            print(f"Error al mostrar la plataforma: {error}")
            return None
        finally:
            cone.close()
            
    @staticmethod
    def UpdatePlatfoms(data, id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                sql = """
                    UPDATE plataforma SET 
                        PlataformaDescripcion = %s, 
                        PlataformaFechMod = %s 
                    WHERE plataforma.PlataformaID = %s
                """
                values = (
                    data['PlataformaDescripcion'],
                    datetime.now(),
                    id
                )
                rows = cursor.execute(sql, values)
                cone.commit()
                return rows > 0     

        except pymysql.Error as error:
            print(f"Error al actualizar la plataforma: {error}")
            return False
        finally:
            cone.close()
            
    @staticmethod
    def CreatePlatforms(data):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(PlataformaID) AS max_id FROM plataforma")
                result = cursor.fetchone()
                max_id = result['max_id'] or 4000
                
                new_id = max_id + 1
                fechmod = datetime.now()
                status = 'A'
                
                sql = """
                    INSERT INTO plataforma (
                        PlataformaID, PlataformaDescripcion,
                        PlataformaFechMod, PlataformaStatus
                    ) VALUES (%s, %s, %s, %s);
                """
                values = (
                    new_id,
                    data['PlataformaDescripcion'],
                    fechmod,
                    status
                )
                cursor.execute(sql, values)
                cone.commit()
                return new_id

        except pymysql.Error as error:
            print(f"Error al crear la plataforma: {error}")
            return None
        finally:
            cone.close()
            
    @staticmethod
    def DeletePlatforms(id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                
                fechmod = datetime.now() 
                status = 'N'   
                
                sql = "UPDATE plataforma SET PlataformaFechMod = %s, PlataformaStatus = %s WHERE PlataformaID = %s"        
                values = (fechmod,status,id) 
                rows = cursor.execute(sql, values)
                cone.commit()
                return rows > 0
        except pymysql.Error as error:
            print(f"Error al eliminar la plataforma: {error}")
            return False
        finally:
            cone.close()