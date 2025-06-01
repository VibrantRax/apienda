from datetime import datetime
from .conexion import ConexionMySQL
import pymysql

class VideogamesMySQL:

    @staticmethod
    def ViewGames():
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT videojuego.*, 
                            plataforma.PlataformaDescripcion, 
                            genero.GeneroDescripcion 
                    FROM videojuego 
                    INNER JOIN plataforma ON plataforma.PlataformaID = videojuego.PlataformaID 
                    INNER JOIN genero ON genero.GeneroID = videojuego.GeneroID
                """)
                return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Error al mostrar los juegos: {error}")
            return []
        finally:
            cone.close()

    @staticmethod
    def ViewGamesByID(id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT videojuego.*, 
                            plataforma.PlataformaDescripcion, 
                            genero.GeneroDescripcion 
                    FROM videojuego 
                    INNER JOIN plataforma ON plataforma.PlataformaID = videojuego.PlataformaID 
                    INNER JOIN genero ON genero.GeneroID = videojuego.GeneroID
                    WHERE videojuego.VideojuegoID = %s
                """, (id,))
                return cursor.fetchone()
        except pymysql.Error as error:
            print(f"Error al mostrar el juego: {error}")
            return None
        finally:
            cone.close()
            
    @staticmethod
    def ViewGameCard():
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT * 
                    FROM `videojuego`
                    WHERE VideojuegoStatus = 'A' 
                    ORDER BY `VideojuegoID` 
                    DESC 
                    LIMIT 3
                """)
                return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Error al mostrar los juegos: {error}")
            return []
        finally:
            cone.close()
            
    @staticmethod
    def UpdateGame(nombre, descripcion, plataforma_id, genero_id, precio, lanzamiento, stock, id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                sql = """
                    UPDATE videojuego SET 
                        VideojuegoNombre = %s,
                        VideojuegoDescripcion = %s,
                        PlataformaID = %s,
                        GeneroID = %s,
                        VideojuegoPrecio = %s,
                        VideojuegoLanzamiento = %s,
                        VideojuegoStock = %s,
                        VideojuegoFechMod = %s
                    WHERE VideojuegoID = %s
                """
                values = (
                    nombre,
                    descripcion,
                    plataforma_id,
                    genero_id,
                    precio,
                    lanzamiento,
                    stock,
                    datetime.now(),
                    id
                )
                rows = cursor.execute(sql, values)
                cone.commit()
                return rows > 0
        except pymysql.Error as error:
            print(f"Error al actualizar el juego: {error}")
            return False
        finally:
            cone.close()
            

    @staticmethod
    def CreateGames(nombre, descripcion, plataforma_id, genero_id, precio, lanzamiento, stock):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(VideojuegoID) AS max_id FROM videojuego")
                result = cursor.fetchone()
                max_id = result['max_id'] or 4000
                
                
                new_id = max_id + 1
                fechmod = datetime.now()
                status = 'A'
                
                sql = """
                    INSERT INTO videojuego (
                        VideojuegoID, VideojuegoNombre, VideojuegoDescripcion, 
                        PlataformaID, GeneroID, VideojuegoPrecio, 
                        VideojuegoLanzamiento, VideojuegoStock, VideojuegoFechMod, VideojuegoStatus
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                values = (
                    new_id,
                    nombre,
                    descripcion,
                    plataforma_id,
                    genero_id,
                    precio,
                    lanzamiento,
                    stock,
                    fechmod,
                    status
                )
                cursor.execute(sql, values)
                cone.commit()
                return new_id

        except pymysql.Error as error:
            print(f"Error al crear el videojuego: {error}")
            return None
        finally:
            cone.close()    

    @staticmethod
    def DeleteGame(id):
        try:
            cone = ConexionMySQL.conexion()
            with cone.cursor() as cursor:
                sql = "UPDATE videojuego SET VideojuegoStatus = 'N', VideojuegoFechMod = %s WHERE VideojuegoID = %s "
                values = (datetime.now(), id)
                rows = cursor.execute(sql, values)
                cone.commit()
                return rows > 0
        except pymysql.Error as error:
            print(f"Error al eliminar el juego: {error}")
            return False
        finally:
            cone.close()
