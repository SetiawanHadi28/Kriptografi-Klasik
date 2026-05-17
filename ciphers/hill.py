import numpy as np
from math import gcd

def matrix_det_mod26(matrix):
    n = len(matrix)
    if n == 2:
        return int(round(matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0])) % 26
    elif n == 3:
        det = (matrix[0][0]*(matrix[1][1]*matrix[2][2] - matrix[1][2]*matrix[2][1])
              - matrix[0][1]*(matrix[1][0]*matrix[2][2] - matrix[1][2]*matrix[2][0])
              + matrix[0][2]*(matrix[1][0]*matrix[2][1] - matrix[1][1]*matrix[2][0]))
        return int(round(det)) % 26

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_inverse_mod26(matrix):
    n = len(matrix)
    det = matrix_det_mod26(matrix)
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        raise ValueError(f'Determinan matriks ({det}) tidak memiliki invers mod 26. Pilih matriks lain.')
    
    if n == 2:
        adj = [[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]]
    elif n == 3:
        adj = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                minor = [[matrix[r][c] for c in range(3) if c != j] for r in range(3) if r != i]
                cofactor = ((-1)**(i+j)) * (minor[0][0]*minor[1][1] - minor[0][1]*minor[1][0])
                adj[j][i] = cofactor
    
    inv = [[(det_inv * adj[i][j]) % 26 for j in range(n)] for i in range(n)]
    return inv

def hill_encrypt(text, matrix):
    steps = []
    n = len(matrix)
    
    text_upper = ''.join(c for c in text.upper() if c.isalpha())
    if len(text_upper) == 0:
        raise ValueError('Teks tidak mengandung huruf')
    
    while len(text_upper) % n != 0:
        text_upper += 'X'
    
    steps.append({
        'type': 'matrix_display',
        'title': f'Matriks Kunci ({n}×{n})',
        'matrix': matrix,
        'description': f'Teks diproses dalam blok {n} karakter'
    })
    
    steps.append({
        'type': 'formula',
        'title': 'Rumus Enkripsi Hill',
        'formula': 'C = K × P (mod 26)',
        'description': f'K = matriks kunci {n}×{n}, P = vektor plaintext {n}×1'
    })
    
    det = matrix_det_mod26(matrix)
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        raise ValueError(f'Determinan matriks kunci ({det}) tidak coprime dengan 26. Pilih matriks lain.')
    
    block_steps = []
    encrypted = ''
    
    for i in range(0, len(text_upper), n):
        block = text_upper[i:i+n]
        p_vec = [ord(c) - ord('A') for c in block]
        c_vec = []
        calc_rows = []
        
        for row in range(n):
            val = sum(matrix[row][col] * p_vec[col] for col in range(n)) % 26
            calc_str = ' + '.join([f'{matrix[row][col]}×{p_vec[col]}' for col in range(n)])
            calc_rows.append(f'({calc_str}) mod 26 = {val}')
            c_vec.append(val)
        
        enc_block = ''.join(chr(v + ord('A')) for v in c_vec)
        encrypted += enc_block
        
        block_steps.append({
            'block': block,
            'p_vec': p_vec,
            'c_vec': c_vec,
            'enc_block': enc_block,
            'calculations': calc_rows
        })
    
    steps.append({
        'type': 'block_steps',
        'title': 'Proses Per Blok',
        'n': n,
        'blocks': block_steps
    })
    
    steps.append({
        'type': 'result',
        'title': 'Hasil Enkripsi',
        'plaintext': text,
        'padded': text_upper,
        'ciphertext': encrypted
    })
    
    return encrypted, steps


def hill_decrypt(text, matrix):
    steps = []
    n = len(matrix)
    
    text_upper = ''.join(c for c in text.upper() if c.isalpha())
    if len(text_upper) == 0:
        raise ValueError('Teks tidak mengandung huruf')
    
    while len(text_upper) % n != 0:
        text_upper += 'X'
    
    try:
        inv_matrix = matrix_inverse_mod26(matrix)
    except ValueError as e:
        raise ValueError(str(e))
    
    steps.append({
        'type': 'matrix_display',
        'title': f'Matriks Kunci Asli ({n}×{n})',
        'matrix': matrix,
        'description': f'Matriks kunci yang digunakan untuk enkripsi'
    })
    
    det = matrix_det_mod26(matrix)
    det_inv = mod_inverse(det, 26)
    
    steps.append({
        'type': 'info',
        'title': 'Perhitungan Invers Matriks mod 26',
        'content': f'det(K) = {det}\ndet⁻¹ mod 26 = {det_inv}\nK⁻¹ = det⁻¹ × adj(K) mod 26'
    })
    
    steps.append({
        'type': 'matrix_display',
        'title': f'Matriks Invers K⁻¹ ({n}×{n})',
        'matrix': inv_matrix,
        'description': 'Matriks ini digunakan untuk dekripsi'
    })
    
    steps.append({
        'type': 'formula',
        'title': 'Rumus Dekripsi Hill',
        'formula': 'P = K⁻¹ × C (mod 26)',
        'description': f'K⁻¹ = invers matriks kunci mod 26'
    })
    
    block_steps = []
    decrypted = ''
    
    for i in range(0, len(text_upper), n):
        block = text_upper[i:i+n]
        c_vec = [ord(c) - ord('A') for c in block]
        p_vec = []
        calc_rows = []
        
        for row in range(n):
            val = sum(inv_matrix[row][col] * c_vec[col] for col in range(n)) % 26
            calc_str = ' + '.join([f'{inv_matrix[row][col]}×{c_vec[col]}' for col in range(n)])
            calc_rows.append(f'({calc_str}) mod 26 = {val}')
            p_vec.append(val)
        
        dec_block = ''.join(chr(v + ord('A')) for v in p_vec)
        decrypted += dec_block
        
        block_steps.append({
            'block': block,
            'c_vec': c_vec,
            'p_vec': p_vec,
            'dec_block': dec_block,
            'calculations': calc_rows
        })
    
    steps.append({
        'type': 'block_steps',
        'title': 'Proses Per Blok',
        'n': n,
        'blocks': block_steps
    })
    
    steps.append({
        'type': 'result',
        'title': 'Hasil Dekripsi',
        'ciphertext': text,
        'plaintext': decrypted
    })
    
    return decrypted, steps
