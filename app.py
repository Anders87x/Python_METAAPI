from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN_ANDERCODE = "ANDERCODEPYTHONAPIMETA"

def verificar_token(req):
    try:
        token = req.args.get('hub.verify_token')
        challenge = req.args.get('hub.challenge')

        if challenge and token and token == TOKEN_ANDERCODE:
            return jsonify({'hub.challenge': challenge})
        else:
            return jsonify({'error': 'Invalid token'})

    except Exception as e:
        return jsonify({'error': f'Error during token verification: {str(e)}'})

def recibir_mensajes(req):
    try:
        entry = req.json['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']

        # Procesar el mensaje según tus necesidades

        return jsonify({'message': 'EVENT_RECEIVED'})

    except Exception as e:
        return jsonify({'error': f'Error processing message: {str(e)}'})

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return verificar_token(request)
    elif request.method == 'POST':
        return recibir_mensajes(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)