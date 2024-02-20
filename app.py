from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN_ANDERCODE = "ANDERCODEPYTHONAPIMETA"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return verificar_token(request)
    elif request.method == 'POST':
        return recibir_mensajes(request)

def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKEN_ANDERCODE:
        return jsonify({'hub.challenge': challenge})
    else:
        return jsonify({'error': 'Invalid token'}), 401

def recibir_mensajes(req):
    data = req.get_json()

    if 'entry' in data:
        for entry in data['entry']:
            if 'changes' in entry:
                for change in entry['changes']:
                    if 'value' in change:
                        # Procesar el mensaje según tus necesidades
                        print(change['value'])

    return jsonify({'message': 'EVENT_RECEIVED'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
