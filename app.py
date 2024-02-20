from flask import Flask, request, jsonify

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
        print(req)
        return jsonify({'message': 'EVENT_RECEIVED'})

    except Exception as e:
        print(e)
        return jsonify({'message': 'EVENT_RECEIVED'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
