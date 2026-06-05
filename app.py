from flask import Flask, jsonify, request
import bcrypt
import time
import base64
import traceback

app = Flask(__name__)

@app.route('/sign', methods=['POST'])
def get_signature():
    try:
        data = request.json
        client_id = data['client_id']
        client_secret = data['client_secret']
        
        timestamp = str(int(time.time() * 1000) - 3000)
        password = (client_id + '_' + timestamp).encode('utf-8')
        hashed = bcrypt.hashpw(password, client_secret.encode('utf-8'))
        signature = base64.b64encode(hashed).decode('utf-8')
        
        return jsonify({
            'timestamp': timestamp,
            'signature': signature
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500

@app.route('/ip')
def get_ip():
    try:
        import urllib.request
        ip = urllib.request.urlopen('https://api.ipify.org').read().decode()
        return jsonify({'ip': ip})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
