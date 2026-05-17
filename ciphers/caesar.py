def caesar_encrypt(text, shift):
    result = []
    steps = []
    steps.append({
        'type': 'formula',
        'title': 'Rumus Enkripsi Caesar',
        'formula': 'C = (P + K) mod 26',
        'description': f'C = ciphertext, P = plaintext (nilai numerik), K = shift ({shift})'
    })
    
    char_steps = []
    encrypted = ''
    
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            p = ord(char.upper()) - ord('A')
            c = (p + shift) % 26
            enc_char = chr(c + ord('A'))
            if not is_upper:
                enc_char = enc_char.lower()
            encrypted += enc_char
            char_steps.append({
                'char': char,
                'p_val': p,
                'formula': f'({p} + {shift}) mod 26 = {c}',
                'result': enc_char
            })
        else:
            encrypted += char
            char_steps.append({
                'char': char,
                'p_val': '-',
                'formula': 'Bukan huruf, tidak diubah',
                'result': char
            })
    
    steps.append({
        'type': 'table',
        'title': 'Proses Per Karakter',
        'headers': ['Plaintext', 'Nilai P', 'Perhitungan', 'Ciphertext'],
        'rows': [[s['char'], str(s['p_val']), s['formula'], s['result']] for s in char_steps]
    })
    
    steps.append({
        'type': 'result',
        'title': 'Hasil Enkripsi',
        'plaintext': text,
        'ciphertext': encrypted
    })
    
    return encrypted, steps


def caesar_decrypt(text, shift):
    result = []
    steps = []
    steps.append({
        'type': 'formula',
        'title': 'Rumus Dekripsi Caesar',
        'formula': 'P = (C - K + 26) mod 26',
        'description': f'P = plaintext, C = ciphertext (nilai numerik), K = shift ({shift})'
    })
    
    char_steps = []
    decrypted = ''
    
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            c = ord(char.upper()) - ord('A')
            p = (c - shift + 26) % 26
            dec_char = chr(p + ord('A'))
            if not is_upper:
                dec_char = dec_char.lower()
            decrypted += dec_char
            char_steps.append({
                'char': char,
                'c_val': c,
                'formula': f'({c} - {shift} + 26) mod 26 = {p}',
                'result': dec_char
            })
        else:
            decrypted += char
            char_steps.append({
                'char': char,
                'c_val': '-',
                'formula': 'Bukan huruf, tidak diubah',
                'result': char
            })
    
    steps.append({
        'type': 'table',
        'title': 'Proses Per Karakter',
        'headers': ['Ciphertext', 'Nilai C', 'Perhitungan', 'Plaintext'],
        'rows': [[s['char'], str(s['c_val']), s['formula'], s['result']] for s in char_steps]
    })
    
    steps.append({
        'type': 'result',
        'title': 'Hasil Dekripsi',
        'ciphertext': text,
        'plaintext': decrypted
    })
    
    return decrypted, steps
