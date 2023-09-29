from flask import Flask, render_template, request, jsonify
from config import Config
from .database import DatabaseConnection
from werkzeug.exceptions import BadRequest

def init_app():
    """Crea y configura la app Flask"""

    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
    app.config.from_object(Config)

    @app.route('/')
    def inicio():
        return render_template('login.html')
    
    @app.route('/register.html')
    def register():
        return render_template('register.html')
    
    @app.route('/chat')
    def chat():
        return render_template('chat.html')

    @app.route('/crearUsuario', methods=['POST'])
    def procesar_registro():
        """Toma los datos del formulario html register.html y los procesa"""
        if request.method == 'POST':
            usuario = request.form['username']
            contrasenia = request.form['password']
            email = request.form['mail']
            nombre = request.form['nombre']
            apellido = request.form['apellido']

        query = "INSERT INTO appd.usuario (USUARIO, CONTRASEN, NOMBRE, APELLIDO, EMAIL) VALUES (%s, %s, %s, %s, %s);"
        params = (usuario, contrasenia, nombre, apellido, email)
            
        try:
            # Ejecutar la construccion de insercion
            DatabaseConnection.execute_query(query, params=params) 
            # Construir el objeto JSON con los datos del cleinte  
            usuario_insertado = {
                "Usuario": usuario,
                "Contrasenia": contrasenia,
                "Email": email,
                "Nombre": nombre,
                "Apellido": apellido
            }
 
            return render_template('login.html')
        
        except Exception as e:
            return {"msg": "Error al registrar el cliente"}

    def exists(usuario, contrasenia):
        """Verifica si una pelicula con el ID dado existe
        en la base de datos. """ 
        query = "SELECT 1 FROM appd.usuario WHERE usuario = %s and CONTRASEN = %s LIMIT 1"
        params = (usuario, contrasenia)

        result = DatabaseConnection.fetch_one(query, params=params)  

        # Si result no es None, significa que se encontró una película con el ID dado
        return result is not None

    @app.route('/loginComprobar', methods=['POST'])
    def login():
        if request.method == 'POST':
            usuario = request.form['username']
            contrasenia= request.form['password']
            
            if not exists(usuario, contrasenia):
               raise BadRequest("Usuario o contraseña incorrecta")
   
        return render_template("chat.html")

    @app.route('/crearServidor', methods=['POST'])
    def crearServidor():
        if request.method == 'POST':
            nombre=request.form['nombreServidor']
            serverid=request.form['descripcion']

        query = "INSERT INTO appd.servidor (NOMBRESV) VALUES (%s);"
        params = (nombre,)

        try:
            DatabaseConnection.execute_query(query, params=params)
            return render_template('chat.html')
        except Exception as e:
            return jsonify({"msg": "Error al registrar el servidor"})

    @app.route('/obtenerCanales')
    def obtenerCanales():
        try:
            query ="SELECT SERVERID, NOMBRESV from appd.servidor"
            datos = DatabaseConnection.fetch_all(query)
            lista_canales = [{"serverid": serverid, "nombre": nombre} for serverid, nombre in datos]

            #devuelve la lista de los canales como JSON 
            return jsonify({"canales": lista_canales})
        
        except Exception as e:
            return jsonify({"error": "Error al obtener los canales"})

       
    @app.route('/crearCanal', methods=['POST'])
    def crearCanal():
        if request.method == 'POST':
            nombre=request.form['nombreServidor']
            serverid=request.form['descripcion']

        query = "INSERT INTO appd.canal (NOMBRECANAL) VALUES (%s);"
        params = (nombre,)

        try:
            DatabaseConnection.execute_query(query, params=params)
            return render_template('chat.html')
        except Exception as e:
            return jsonify({"msg": "Error al registrar un nuevo canal"})



    return app

app = init_app()