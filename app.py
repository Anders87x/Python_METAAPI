from flask import Flask, request, jsonify, render_template
import http.client
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la tabla Log
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=datetime.utcnow)
    texto = db.Column(db.TEXT)

# Crear la tabla si no existe
with app.app_context():
    db.create_all()

# Función para ordenar los registros por fecha y hora
def ordenar_por_fecha_y_hora(registros):
    return sorted(registros, key=lambda x: x.fecha_y_hora, reverse=True)

@app.route('/')
def index():
    # Obtener todos los registros de la base de datos
    registros = Log.query.all()
    registros_ordenados = ordenar_por_fecha_y_hora(registros)
    return render_template('index.html', registros=registros_ordenados)

mensajes_log = []

# Función para agregar mensajes y guardar en la base de datos
def agregar_mensaje_log(texto):
    mensajes_log.append(texto)

    # Guardar el mensaje en la base de datos
    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()

# Token de verificación para la configuración inicial
TOKEN_ANDERCODE = "ANDERCODE"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Manejar solicitud GET durante la configuración inicial
        challenge = verificar_token(request)
        return challenge
    elif request.method == 'POST':
        # Manejar mensajes POST (mensajes de usuario)
        response = recibir_mensajes(request)
        return response

def verificar_token(req):
    # Función para verificar el token durante la configuración inicial
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKEN_ANDERCODE:
        return challenge
    else:
        return jsonify({'error': 'Invalid token'}), 401

def recibir_mensajes(req):

    agregar_mensaje_log(json.dumps(request))

    try:
        # Manejar mensajes entrantes
        req = request.get_json()
        entry = req['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        objeto_mensaje = value['messages']

        if objeto_mensaje:
            messages = objeto_mensaje[0]

            if "type" in messages:
                tipo = messages["type"]

                if tipo == "interactive":
                    # Manejar mensajes interactivos
                    tipo_interactivo = messages["interactive"]["type"]

                    if tipo_interactivo == "button_reply":
                        texto = messages["interactive"]["button_reply"]["id"]
                        numero = messages["from"]
                        enviar_mensaje_whatsapp(texto, numero)

                    elif tipo_interactivo == "list_reply":
                        texto = messages["interactive"]["list_reply"]["id"]
                        numero = messages["from"]
                        enviar_mensaje_whatsapp(texto, numero)

                if "text" in messages:
                    # Manejar mensajes de texto
                    texto = messages["text"]["body"]
                    numero = messages["from"]
                    enviar_mensaje_whatsapp(texto, numero)

        return jsonify({'message': 'EVENT_RECEIVED'})

    except Exception as e:
        print(e)
        return jsonify({'message': 'EVENT_RECEIVED'})

def enviar_mensaje_whatsapp(texto, number):
    # Función para enviar mensajes de WhatsApp
    texto = texto.lower()

    if "hola" in texto:
        # Enviar mensaje de bienvenida
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "🚀 Hola, ¿Cómo estás? Bienvenido."
            }
        }
    elif "1" in texto:
        # Enviar información detallada
        data={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
            }
        }
    elif "boton" in texto:
        data={
            "messaging_product": "whatsapp",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": "¿Confirmas tu registro?"
                },
                "footer": {
                    "text": "Selecciona una de las opciones"
                },
                "action" :{
                    "buttons": [
                        {
                            "type": "reply",
                            "reply":{
                                "id":"btnsi",
                                "title":"Si"
                            }
                        },
                        {
                            "type": "reply",
                            "reply":{
                                "id":"btnno",
                                "title":"No"
                            }
                        },
                        {
                            "type": "reply",
                            "reply":{
                                "id":"btntalvez",
                                "title":"Tal vez"
                            }
                        }
                    ]
                }
            }
        }
    elif "lista" in texto:
        data={
            "messaging_product": "whatsapp",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type":"list",
                "body":{
                    "text":"Selecciona alguna opcion"
                },
                "footer":{
                    "text":"Selecciona una de las opciones para poder ayudarte"
                },
                "action":{
                    "button":"Ver opciones",
                    "sections":[
                        {
                            "title":"Compra y Venta",
                            "rows":[
                                {
                                    "id":"btncomprar",
                                    "title":"Comprar",
                                    "description":"Compra los mejores articulos de tecnologia"
                                },
                                {
                                    "id":"btnvender",
                                    "title":"Vender",
                                    "description":"Vende lo que ya no estes usando"
                                }
                            ]
                        },
                        {
                            "title":"Distribución y Recojo",
                            "rows":[
                                {
                                    "id":"btndireccion",
                                    "title":"Local",
                                    "description":"Puedes visitar nuestro local."
                                },
                                {
                                    "id":"btndistribucion",
                                    "title":"Distribución",
                                    "description":"La distribución se realiza todos los dias."
                                }
                            ]
                        }
                    ]
                }
            }
        }
    elif "btnsi" in texto:
        data={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Excelente muchas gracias por registrarse. 🤩"
            }
        }
    elif "btnno" in texto:
        data={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Entiendo, muchas gracias. "
            }
        }
    elif "btntalvez" in texto:
        data={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Espero se anime. "
            }
        }
    elif "adios" in texto or "bye" in texto or "nos vemos" in texto or "adiós" in texto:
        data={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Hasta luego. 🌟"
            }
        }
    else:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "🚀 Hola, visita mi web anderson-bastidas.com para más información.\n \n📌Por favor, ingresa un número #️⃣ para recibir información.\n \n1️⃣. Información del Curso. ❔\n2️⃣. Ubicación del local. 📍\n3️⃣. Enviar temario en PDF. 📄\n4️⃣. Audio explicando curso. 🎧\n5️⃣. Video de Introducción. ⏯️\n6️⃣. Hablar con AnderCode. 🙋‍♂️\n7️⃣. Horario de Atención. 🕜\n8️⃣. Consultar a Chatgtp usar 'gchatgpt: <Ingrese Consulta>'. \n0️⃣. Regresar al Menú. 🕜"
            }
        }

    # Convertir el diccionario a formato JSON
    data = json.dumps(data)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer EAAK2skfVxy4BO8udon6ZAnAyg7QoJww2ZCjGDXCWCWrlQrurOBSFJowy2TU4sSBswynxyx5WiqzKgvcCtsaSKESPIZAdCctKO8VbJcWygcpU1aivcuGbUm5729cACe6PU5L0ao7jcUaUal1m2NE9MJJKWfFfEfgdkVzrpsD5O58O61kPkWOKAE0Vldlp7L9ZCtIdN0Rgf4X2LHSHNZBbo5zHZAuZAh9"
    }

    connection = http.client.HTTPSConnection("graph.facebook.com")

    try:
        # Enviar la solicitud HTTP
        connection.request("POST", "/v18.0/229523723581696/messages", data, headers)
        response = connection.getresponse()

        # Puedes imprimir la respuesta en la consola de Render
        print(response.status, response.reason)
        print(response.read().decode("utf-8"))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()

if __name__ == '__main__':
    # Ejecutar la aplicación Flask
    app.run(host='0.0.0.0', port=80, debug=True)
