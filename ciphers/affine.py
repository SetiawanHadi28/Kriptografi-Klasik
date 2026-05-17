from math import gcd

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt(text, a, b):
    steps = []
    steps.append({
        'type': 'formula',
        'title': 'Rumus Enkripsi Affine',
        'formula': 'C = (a × P + b) mod 26',
        'description': f'a = {a}, b = {b}, gcd(a, 26) = {gcd(a, 26)}'
    })
    
    char_steps = []
    encrypted = ''
    
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            p = ord(char.upper()) - ord('A')
            c = (a * p + b) % 26
            enc_char = chr(c + ord('A'))
            if not is_upper:
                enc_char = enc_char.lower()
            encrypted += enc_char
            char_steps.append({
                'char': char,
                'p_val': p,
                'formula': f'({a} × {p} + {b}) mod 26 = ({a*p + b}) mod 26 = {c}',
                'result': enc_char
            })
        else:
            encrypted += char
            char_steps.append({
                'char': char,
                'p_val': '-',
                'formula': 'Bukan huruf',
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


def affine_decrypt(text, a, b):
    steps = []
    a_inv = mod_inverse(a, 26)
    
    if a_inv is None:
        raise ValueError(f'Invers dari {a} mod 26 tidak ada. Pilih nilai a yang coprime dengan 26.')
    
    steps.append({
        'type': 'formula',
        'title': 'Rumus Dekripsi Affine',
        'formula': 'P = a⁻¹ × (C - b) mod 26',
        'description': f'a = {a}, b = {b}, a⁻¹ mod 26 = {a_inv}'
    })
    
    steps.append({
        'type': 'info',
        'title': 'Perhitungan Invers Modular',
        'content': f'Mencari a⁻¹ sehingga ({a} × a⁻¹) mod 26 = 1\n→ ({a} × {a_inv}) mod 26 = {(a * a_inv) % 26} ✓'
    })
    
    char_steps = []
    decrypted = ''
    
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            c = ord(char.upper()) - ord('A')
            p = (a_inv * (c - b)) % 26
            dec_char = chr(p + ord('A'))
            if not is_upper:
                dec_char = dec_char.lower()
            decrypted += dec_char
            char_steps.append({
                'char': char,
                'c_val': c,
                'formula': f'{a_inv} × ({c} - {b}) mod 26 = {a_inv * (c - b)} mod 26 = {p}',
                'result': dec_char
            })
        else:
            decrypted += char
            char_steps.append({
                'char': char,
                'c_val': '-',
                'formula': 'Bukan huruf',
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
