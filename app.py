from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    token = 'ANDERCODE'  # Reemplaza esto con tu token real
    auth_header = request.headers.get('Authorization')

    if auth_header != 'Bearer ' + token:
        return {'error': 'Unauthorized'}, 401

    print(request.json)
    return {'status': 'success'}, 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
