from flask import Flask, jsonify
import bcrypt
import time
import requests
import base64

app = Flask(__name__)

@app.route('/token', methods=['POST'])
def get_token():
    from flask import request
    data = request.json
    client_id = data['client_id']
    client_secret = data['client_secret']
    
    timestamp = str(int(time.time() * 1000) - 3000)
    password = (client_id + '_' + timestamp).encode('utf-8')
    hashed = bcrypt.hashpw(password, client_secret.encode('utf-8'))
    signature = base64.b64encode(hashed).decode('utf-8')
    
    response = requests.post(
        'https://api.commerce.naver.com/external/v1/oauth2/token',
        data={
            'client_id': client_id,
            'timestamp': timestamp,
            'client_secret_sign': signature,
            'grant_type': 'client_credentials',
            'type': 'SELF'
        }
    )
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
