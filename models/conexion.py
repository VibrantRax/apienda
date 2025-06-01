import pymysql

class ConexionMySQL:
    
    @staticmethod
    def conexion():
        """Establece la conexión con la base de datos MySQL"""
        
        try:
            conexion = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                db="apienda",
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Conexión correcta")
            return conexion
        
        except pymysql.Error as error:
            print(f"Error al conectar con la base de datos: {error}")
            return None