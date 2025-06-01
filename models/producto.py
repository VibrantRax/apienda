from datetime import datetime
from .conexion import ConexionMySQL
import pymysql

class ProductsMySQL:

    @staticmethod
    def ViewProducts():
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT producto.*, 
                            categoria.CategoriaDescripcion 
                    FROM producto
                    INNER JOIN categoria ON categoria.CategoriaID = producto.CategoriaID
                    WHERE ProductoStatus = 'A'
                """)
                return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Error al mostrar los productos: {error}")
            return []
        finally:
            cone.close()

    @staticmethod
    def ViewProductsByID(id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT producto.*, 
                            categoria.CategoriaDescripcion 
                    FROM producto
                    INNER JOIN categoria ON categoria.CategoriaID = producto.CategoriaID 
                    WHERE ProductoID = %s
                """, (id,))
                return cursor.fetchone()
        except pymysql.Error as error:
            print(f"Error al mostrar el produto: {error}")
            return None
        finally:
            cone.close()
            
    @staticmethod
    def UpdateProducts(nombre,descripcion,categoria_id,precio,stock, id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                sql = """
                    UPDATE producto SET 
                        ProductoNombre = %s, ProductoDescripcion = %s, 
                        CategoriaID = %s, ProductoPrecio = %s, 
                        ProductoStock = %s, ProductoFechMod = %s 
                    WHERE ProductoID = %s
                """
                values = (
                    nombre,
                    descripcion,
                    categoria_id,
                    precio,
                    stock,
                    datetime.now(),
                    id
                )
                rows = cursor.execute(sql, values)
                cone.commit()
                return rows > 0     

        except pymysql.Error as error:
            print(f"Error al actualizar el producto: {error}")
            return False
        finally:
            cone.close()
            
    
    @staticmethod
    def CreateProducts(nombre,descripcion,categoria_id,precio,stock):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(ProductoID) AS max_id FROM producto")
                result = cursor.fetchone()
                max_id = result['max_id'] or 4000
                
                new_id = max_id + 1
                fechmod = datetime.now()
                status = 'A'
                
                sql = """
                    INSERT INTO producto (
                        ProductoID, ProductoNombre, ProductoDescripcion, 
                        CategoriaID, ProductoPrecio, ProductoStock, 
                        ProductoFechMod, ProductoStatus
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                values = (
                    new_id,
                    nombre,
                    descripcion,
                    categoria_id,
                    precio,
                    stock,
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
    def DeleteProduct(id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                
                fechmod = datetime.now() 
                status = 'N'   
                
                sql = "UPDATE producto SET ProductoFechMod = %s, ProductoStatus = %s WHERE ProductoID = %s"
                values = (fechmod,status,id) 
                rows = cursor.execute(sql, values)
                cone.commit()
                return rows > 0
        except pymysql.Error as error:
            print(f"Error al eliminar el producto: {error}")
            return False
        finally:
            cone.close()