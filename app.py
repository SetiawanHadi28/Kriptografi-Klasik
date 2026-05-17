from flask import Flask, render_template, request, jsonify, session
import json
import datetime
from crypto_algorithms import (
    caesar_encrypt, caesar_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    affine_encrypt, affine_decrypt,
    hill_encrypt, hill_decrypt,
    playfair_encrypt, playfair_decrypt,
    generate_playfair_matrix
)

app = Flask(__name__)
app.secret_key = 'crypto_sim_secret_2024'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/caesar', methods=['POST'])
def api_caesar():
    data = request.get_json()
    text = data.get('text', '')
    shift = data.get('shift', 3)
    mode = data.get('mode', 'encrypt')
    if not text:
        return jsonify({'error': 'Teks tidak boleh kosong'}), 400
    try:
        shift = int(shift)
        if not (1 <= shift <= 25):
            return jsonify({'error': 'Shift harus antara 1-25'}), 400
    except ValueError:
        return jsonify({'error': 'Shift harus berupa angka'}), 400
    try:
        if mode == 'encrypt':
            result = caesar_encrypt(text, shift)
            result['mode'] = 'encrypt'
        else:
            result = caesar_decrypt(text, shift)
            result['mode'] = 'decrypt'
        result['algorithm'] = 'Caesar Cipher'
        result['timestamp'] = datetime.datetime.now().strftime('%H:%M:%S')
        _add_to_history(result, 'caesar', mode, text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vigenere', methods=['POST'])
def api_vigenere():
    data = request.get_json()
    text = data.get('text', '')
    key = data.get('key', '')
    mode = data.get('mode', 'encrypt')
    if not text:
        return jsonify({'error': 'Teks tidak boleh kosong'}), 400
    if not key or not key.isalpha():
        return jsonify({'error': 'Kunci harus berupa huruf saja'}), 400
    try:
        if mode == 'encrypt':
            result = vigenere_encrypt(text, key)
            result['mode'] = 'encrypt'
        else:
            result = vigenere_decrypt(text, key)
            result['mode'] = 'decrypt'
        result['algorithm'] = 'Vigenère Cipher'
        result['timestamp'] = datetime.datetime.now().strftime('%H:%M:%S')
        _add_to_history(result, 'vigenere', mode, text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/affine', methods=['POST'])
def api_affine():
    data = request.get_json()
    text = data.get('text', '')
    a = data.get('a', 5)
    b = data.get('b', 8)
    mode = data.get('mode', 'encrypt')
    if not text:
        return jsonify({'error': 'Teks tidak boleh kosong'}), 400
    try:
        a, b = int(a), int(b)
    except ValueError:
        return jsonify({'error': 'Nilai a dan b harus berupa angka'}), 400
    try:
        if mode == 'encrypt':
            result = affine_encrypt(text, a, b)
            result['mode'] = 'encrypt'
        else:
            result = affine_decrypt(text, a, b)
            result['mode'] = 'decrypt'
        result['algorithm'] = 'Affine Cipher'
        result['timestamp'] = datetime.datetime.now().strftime('%H:%M:%S')
        _add_to_history(result, 'affine', mode, text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/hill', methods=['POST'])
def api_hill():
    data = request.get_json()
    text = data.get('text', '')
    matrix = data.get('matrix', [[3, 3], [2, 5]])
    mode = data.get('mode', 'encrypt')
    if not text:
        return jsonify({'error': 'Teks tidak boleh kosong'}), 400
    if not isinstance(matrix, list) or len(matrix) not in [2, 3]:
        return jsonify({'error': 'Matriks harus 2x2 atau 3x3'}), 400
    try:
        if mode == 'encrypt':
            result = hill_encrypt(text, matrix)
            result['mode'] = 'encrypt'
        else:
            result = hill_decrypt(text, matrix)
            result['mode'] = 'decrypt'
        result['algorithm'] = 'Hill Cipher'
        result['timestamp'] = datetime.datetime.now().strftime('%H:%M:%S')
        _add_to_history(result, 'hill', mode, text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playfair', methods=['POST'])
def api_playfair():
    data = request.get_json()
    text = data.get('text', '')
    key = data.get('key', '')
    mode = data.get('mode', 'encrypt')
    if not text:
        return jsonify({'error': 'Teks tidak boleh kosong'}), 400
    if not key or not key.replace(' ', '').isalpha():
        return jsonify({'error': 'Kunci harus berupa huruf saja'}), 400
    try:
        if mode == 'encrypt':
            result = playfair_encrypt(text, key)
            result['mode'] = 'encrypt'
        else:
            result = playfair_decrypt(text, key)
            result['mode'] = 'decrypt'
        result['algorithm'] = 'Playfair Cipher'
        result['timestamp'] = datetime.datetime.now().strftime('%H:%M:%S')
        _add_to_history(result, 'playfair', mode, text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playfair_matrix', methods=['POST'])
def api_playfair_matrix():
    data = request.get_json()
    key = data.get('key', '')
    matrix = generate_playfair_matrix(key)
    return jsonify({'matrix': matrix})

@app.route('/api/history', methods=['GET'])
def api_history():
    history = session.get('history', [])
    return jsonify({'history': history[-20:]})

@app.route('/api/history/clear', methods=['POST'])
def api_clear_history():
    session['history'] = []
    return jsonify({'success': True})

def _add_to_history(result, algo, mode, original_text):
    if 'history' not in session:
        session['history'] = []
    history = session['history']
    output = result.get('ciphertext') or result.get('plaintext') or ''
    entry = {
        'algorithm': result.get('algorithm', algo),
        'mode': mode,
        'input': original_text[:40] + ('...' if len(original_text) > 40 else ''),
        'output': output[:40] + ('...' if len(output) > 40 else ''),
        'timestamp': result.get('timestamp', '')
    }
    history.append(entry)
    session['history'] = history[-50:]
    session.modified = True

if __name__ == '__main__':
    app.run(debug=True, port=5000)
