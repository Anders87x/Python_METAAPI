from flask import Flask, request, jsonify
import http.client
import json

app = Flask(__name__)

TOKEN_ANDERCODE = "ANDERCODE"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        challenge = verificar_token(request)
        print("GET")
        return challenge
    elif request.method == 'POST':
        response = recibir_mensajes(request)
        print("POST")
        return response

def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKEN_ANDERCODE:
        return challenge
    else:
        return jsonify({'error': 'Invalid token'}), 401

def recibir_mensajes(req):
    try:
        req = request.get_json()
        entry = req['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        objeto_mensaje = value['messages']

        if objeto_mensaje:
            messages = objeto_mensaje[0]
            texto = messages['text']['body']
            numero = messages['from']

            enviar_mensaje_whatsapp(texto, numero)

        return jsonify({'message': 'EVENT_RECEIVED'})

    except Exception as e:
        print(e)
        return jsonify({'message': 'EVENT_RECEIVED'})

def enviar_mensaje_whatsapp(texto, number):
    texto = texto.lower()

    if "hola" in texto:
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

    data = json.dumps(data)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer EAAK2skfVxy4BOwO3AfguPDN7kNnGV9OUiMIEzj2JOMrH8Rr8zajjxQ9XOtiVBAplcrpREB2QmIMZCVYrjKWzwDu7se9B9vQ9R655Schdib2bwK6zZCGF3Woi7CZBZBPZC2nXbHwOIKafChfiPyoqcgSTgtQAzczIOmBUT9cbZAVatm3N9IoCZCNmPQtuIxMSLGLL7ZBSU5CriGXqL2WZCCUcCVzHZAk2oZD"
    }

    connection = http.client.HTTPSConnection("graph.facebook.com")

    try:
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
    app.run(host='0.0.0.0', port=80, debug=True)
