# 🎮 Proyecto: API de Tienda en Línea de Videojuegos

Esta es una API RESTful desarrollada en Flask para gestionar una tienda en línea de videojuegos. Permite el manejo de administradores, categorías, productos, usuarios y resultados de actividades. El objetivo es ofrecer una base funcional para un sistema de comercio electrónico enfocado en videojuegos.

🔗 Repositorio GitHub: [https://github.com/VibrantRax/apienda/tree/main](https://github.com/VibrantRax/apienda/tree/main)

---

## 🚀 Funcionalidades principales

- Registro y autenticación de administradores.
- Gestión de categorías de videojuegos.
- Alta, consulta y administración de productos.
- Control de usuarios y almacenamiento de resultados.
- API estructurada y lista para consumo desde aplicaciones frontend o móviles.

---

## ⚙ Tecnologías y dependencias

### Backend

- *Python 3.11+*
- *Flask*
- *Flask-Session*
- *MySQL*
- *mysql-connector-python*

Instalación de dependencias:
```bash
pip install Flask Flask-Session mysql-connector-python
🧑‍💻 Instrucciones de uso
Clona este repositorio:

bash
Copiar
Editar
git clone https://github.com/VibrantRax/apienda.git
cd apienda
Asegúrate de tener MySQL corriendo y crea la base de datos utilizando el script SQL proporcionado (estructura.sql).

Configura tu archivo de conexión en el backend (LoginMySQL.py o similar), con tus credenciales de MySQL:

python
Copiar
Editar
host = "localhost"
user = "tu_usuario"
password = "tu_contraseña"
database = "nombre_de_tu_base"
Ejecuta la aplicación Flask:

bash
Copiar
Editar
python app.py
Abre tu navegador en:

arduino
Copiar
Editar
http://localhost:5000
📂 Estructura del proyecto
bash
Copiar
Editar
/apienda
│
├── app.py                # Servidor principal Flask
├── LoginMySQL.py         # Funciones de acceso a la base de datos
├── estructura.sql        # Script SQL para crear todas las tablas
├── templates/            # Archivos HTML (si aplica)
├── static/               # Archivos estáticos (CSS, JS, imágenes)
└── README.md             # Este archivo
🔐 Seguridad
El login de administradores requiere usuario y contraseña válidos.

Las sesiones se manejan con Flask-Session.

Para entornos de producción se recomienda cifrar las contraseñas y usar HTTPS.
