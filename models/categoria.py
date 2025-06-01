from datetime import datetime

import pymysql.cursors
from .conexion import ConexionMySQL
import pymysql

class CategoriesMySQL:

    @staticmethod
    def ViewCategories():
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT * 
                    FROM categoria
                    WHERE CategoriaStatus = 'A'
                """)
                return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Error al mostrar las categorias: {error}")
            return []
        finally:
            cone.close()
            
    @staticmethod
    def ViewCategoriesByID(id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM categoria WHERE CategoriaID = %s 
                """, (id,))
                return cursor.fetchone()
        except pymysql.Error as error:
            print(f"Error al mostrar la categoria: {error}")
            return None
        finally:
            cone.close()
            
    @staticmethod
    def UpdateCategories(data, id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                sql = """
                    UPDATE categoria SET 
                        CategoriaDescripcion = %s,
                        CategoriaFechMod = %s
                    WHERE categoria.CategoriaID = %s
                """
                values = (
                    data['CategoriaDescripcion'],
                    datetime.now(),
                    id
                )
                rows = cursor.execute(sql, values)
                cone.commit()
                return rows > 0
        except pymysql.Error as error:
            print(f"Error al actualizar la categoria: {error}")
            return False
        finally:
            cone.close()
            
    @staticmethod
    def CreateCategory(data):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(CategoriaID) AS max_id FROM categoria")
                result = cursor.fetchone()
                max_id = result['max_id'] or 4000

                new_id = max_id + 1
                
                fechmod = datetime.now()
                status = 'A'
                
                sql = """
                    INSERT INTO categoria (
                        CategoriaID, CategoriaDescripcion, 
                        CategoriaFechMod, CategoriaStatus
                    ) VALUES (%s, %s, %s, %s);
                """

                values = (
                    new_id,
                    data['CategoriaDescripcion'],
                    fechmod,
                    status
                )
                
                cursor.execute(sql, values)
                cone.commit()
                return new_id

        except pymysql.Error as error:
            print(f"Error al crear la categoria: {error}")
            return None
        finally:
            cone.close()
            
    @staticmethod
    def DeleteCategory(id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                
                fechmod = datetime.now()
                status = 'N'
                
                sql = "UPDATE categoria SET CategoriaFechMod = %s, CategoriaStatus = %s WHERE CategoriaID = %s" 
                values = (fechmod,status,id) 
                rows = cursor.execute(sql, values)
                cone.commit()
                return rows > 0
        except pymysql.Error as error:
            print(f"Error al eliminar la categoria: {error}")
            return False
        finally:
            cone.close()