def vigenere_encrypt(text, key):
    steps = []
    key = key.upper()
    steps.append({
        'type': 'formula',
        'title': 'Rumus Enkripsi Vigenère',
        'formula': 'Cᵢ = (Pᵢ + Kᵢ) mod 26',
        'description': f'Kunci: {key} (diulang sesuai panjang plaintext)'
    })
    
    key_expanded = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            key_expanded.append(key[ki % len(key)])
            ki += 1
        else:
            key_expanded.append('-')
    
    steps.append({
        'type': 'key_expansion',
        'title': 'Ekspansi Kunci',
        'text': [c for c in text],
        'key_exp': key_expanded
    })
    
    char_steps = []
    encrypted = ''
    ki = 0
    
    for i, char in enumerate(text):
        if char.isalpha():
            is_upper = char.isupper()
            p = ord(char.upper()) - ord('A')
            k = ord(key[ki % len(key)]) - ord('A')
            c = (p + k) % 26
            enc_char = chr(c + ord('A'))
            if not is_upper:
                enc_char = enc_char.lower()
            encrypted += enc_char
            char_steps.append({
                'char': char,
                'key_char': key[ki % len(key)],
                'p_val': p,
                'k_val': k,
                'formula': f'({p} + {k}) mod 26 = {c}',
                'result': enc_char
            })
            ki += 1
        else:
            encrypted += char
            char_steps.append({
                'char': char,
                'key_char': '-',
                'p_val': '-',
                'k_val': '-',
                'formula': 'Bukan huruf',
                'result': char
            })
    
    steps.append({
        'type': 'table',
        'title': 'Proses Per Karakter',
        'headers': ['Plaintext', 'Kunci', 'Nilai P', 'Nilai K', 'Perhitungan', 'Ciphertext'],
        'rows': [[s['char'], s['key_char'], str(s['p_val']), str(s['k_val']), s['formula'], s['result']] for s in char_steps]
    })
    
    steps.append({
        'type': 'result',
        'title': 'Hasil Enkripsi',
        'plaintext': text,
        'ciphertext': encrypted
    })
    
    return encrypted, steps


def vigenere_decrypt(text, key):
    steps = []
    key = key.upper()
    steps.append({
        'type': 'formula',
        'title': 'Rumus Dekripsi Vigenère',
        'formula': 'Pᵢ = (Cᵢ - Kᵢ + 26) mod 26',
        'description': f'Kunci: {key} (diulang sesuai panjang ciphertext)'
    })
    
    char_steps = []
    decrypted = ''
    ki = 0
    
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            c = ord(char.upper()) - ord('A')
            k = ord(key[ki % len(key)]) - ord('A')
            p = (c - k + 26) % 26
            dec_char = chr(p + ord('A'))
            if not is_upper:
                dec_char = dec_char.lower()
            decrypted += dec_char
            char_steps.append({
                'char': char,
                'key_char': key[ki % len(key)],
                'c_val': c,
                'k_val': k,
                'formula': f'({c} - {k} + 26) mod 26 = {p}',
                'result': dec_char
            })
            ki += 1
        else:
            decrypted += char
            char_steps.append({
                'char': char,
                'key_char': '-',
                'c_val': '-',
                'k_val': '-',
                'formula': 'Bukan huruf',
                'result': char
            })
    
    steps.append({
        'type': 'table',
        'title': 'Proses Per Karakter',
        'headers': ['Ciphertext', 'Kunci', 'Nilai C', 'Nilai K', 'Perhitungan', 'Plaintext'],
        'rows': [[s['char'], s['key_char'], str(s['c_val']), str(s['k_val']), s['formula'], s['result']] for s in char_steps]
    })
    
    steps.append({
        'type': 'result',
        'title': 'Hasil Dekripsi',
        'ciphertext': text,
        'plaintext': decrypted
    })
    
    return decrypted, steps
