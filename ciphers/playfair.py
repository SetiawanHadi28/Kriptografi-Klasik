def generate_playfair_matrix(key):
    key = key.upper().replace('J', 'I')
    seen = []
    for c in key:
        if c.isalpha() and c not in seen:
            seen.append(c)
    
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    for c in alphabet:
        if c not in seen:
            seen.append(c)
    
    matrix = [seen[i*5:(i+1)*5] for i in range(5)]
    return matrix

def find_pos(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return None

def prepare_text(text):
    text = text.upper().replace('J', 'I')
    text = ''.join(c for c in text if c.isalpha())
    
    prepared = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                prepared.append((a, 'X'))
                i += 1
            else:
                prepared.append((a, b))
                i += 2
        else:
            prepared.append((a, 'X'))
            i += 1
    
    return prepared

def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    steps = []
    
    steps.append({
        'type': 'playfair_matrix',
        'title': f'Tabel Playfair 5×5 (Kunci: {key.upper()})',
        'matrix': matrix
    })
    
    pairs = prepare_text(text)
    
    steps.append({
        'type': 'pairs',
        'title': 'Persiapan Teks (Digraph Pairs)',
        'original': text,
        'pairs': [f'{a}{b}' for a, b in pairs],
        'note': 'J diganti I, huruf kembar dalam pasangan diselipkan X, panjang ganjil ditambah X'
    })
    
    steps.append({
        'type': 'formula',
        'title': 'Aturan Enkripsi Playfair',
        'rules': [
            'Baris Sama: Geser kanan 1 kolom (wrapping)',
            'Kolom Sama: Geser bawah 1 baris (wrapping)',
            'Persegi Panjang: Tukar kolom (ambil pojok persegi panjang)'
        ]
    })
    
    pair_steps = []
    encrypted = ''
    
    for a, b in pairs:
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)
        
        if r1 == r2:
            ec1 = matrix[r1][(c1 + 1) % 5]
            ec2 = matrix[r2][(c2 + 1) % 5]
            rule = f'Baris sama (baris {r1+1}): geser kanan'
            detail = f'{a}[{r1+1},{c1+1}] → [{r1+1},{(c1+1)%5+1}]={ec1}, {b}[{r2+1},{c2+1}] → [{r2+1},{(c2+1)%5+1}]={ec2}'
        elif c1 == c2:
            ec1 = matrix[(r1 + 1) % 5][c1]
            ec2 = matrix[(r2 + 1) % 5][c2]
            rule = f'Kolom sama (kolom {c1+1}): geser bawah'
            detail = f'{a}[{r1+1},{c1+1}] → [{(r1+1)%5+1},{c1+1}]={ec1}, {b}[{r2+1},{c2+1}] → [{(r2+1)%5+1},{c2+1}]={ec2}'
        else:
            ec1 = matrix[r1][c2]
            ec2 = matrix[r2][c1]
            rule = f'Persegi panjang: tukar kolom'
            detail = f'{a}[{r1+1},{c1+1}] → [{r1+1},{c2+1}]={ec1}, {b}[{r2+1},{c2+1}] → [{r2+1},{c1+1}]={ec2}'
        
        encrypted += ec1 + ec2
        pair_steps.append({
            'pair': f'{a}{b}',
            'rule': rule,
            'detail': detail,
            'result': f'{ec1}{ec2}'
        })
    
    steps.append({
        'type': 'table',
        'title': 'Proses Enkripsi Per Pasangan',
        'headers': ['Pasangan', 'Aturan', 'Detail Posisi', 'Hasil'],
        'rows': [[s['pair'], s['rule'], s['detail'], s['result']] for s in pair_steps]
    })
    
    steps.append({
        'type': 'result',
        'title': 'Hasil Enkripsi',
        'plaintext': text,
        'ciphertext': encrypted
    })
    
    return encrypted, steps


def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    steps = []
    
    steps.append({
        'type': 'playfair_matrix',
        'title': f'Tabel Playfair 5×5 (Kunci: {key.upper()})',
        'matrix': matrix
    })
    
    text_clean = text.upper().replace('J', 'I')
    text_clean = ''.join(c for c in text_clean if c.isalpha())
    
    pairs = [(text_clean[i], text_clean[i+1]) for i in range(0, len(text_clean), 2)]
    
    steps.append({
        'type': 'pairs',
        'title': 'Pasangan Ciphertext',
        'original': text,
        'pairs': [f'{a}{b}' for a, b in pairs],
        'note': 'Teks dibagi menjadi pasangan 2 karakter'
    })
    
    steps.append({
        'type': 'formula',
        'title': 'Aturan Dekripsi Playfair',
        'rules': [
            'Baris Sama: Geser kiri 1 kolom (wrapping)',
            'Kolom Sama: Geser atas 1 baris (wrapping)',
            'Persegi Panjang: Tukar kolom (sama dengan enkripsi)'
        ]
    })
    
    pair_steps = []
    decrypted = ''
    
    for a, b in pairs:
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)
        
        if r1 == r2:
            dc1 = matrix[r1][(c1 - 1) % 5]
            dc2 = matrix[r2][(c2 - 1) % 5]
            rule = f'Baris sama (baris {r1+1}): geser kiri'
            detail = f'{a}[{r1+1},{c1+1}] → [{r1+1},{(c1-1)%5+1}]={dc1}, {b}[{r2+1},{c2+1}] → [{r2+1},{(c2-1)%5+1}]={dc2}'
        elif c1 == c2:
            dc1 = matrix[(r1 - 1) % 5][c1]
            dc2 = matrix[(r2 - 1) % 5][c2]
            rule = f'Kolom sama (kolom {c1+1}): geser atas'
            detail = f'{a}[{r1+1},{c1+1}] → [{(r1-1)%5+1},{c1+1}]={dc1}, {b}[{r2+1},{c2+1}] → [{(r2-1)%5+1},{c2+1}]={dc2}'
        else:
            dc1 = matrix[r1][c2]
            dc2 = matrix[r2][c1]
            rule = 'Persegi panjang: tukar kolom'
            detail = f'{a}[{r1+1},{c1+1}] → [{r1+1},{c2+1}]={dc1}, {b}[{r2+1},{c2+1}] → [{r2+1},{c1+1}]={dc2}'
        
        decrypted += dc1 + dc2
        pair_steps.append({
            'pair': f'{a}{b}',
            'rule': rule,
            'detail': detail,
            'result': f'{dc1}{dc2}'
        })
    
    steps.append({
        'type': 'table',
        'title': 'Proses Dekripsi Per Pasangan',
        'headers': ['Pasangan', 'Aturan', 'Detail Posisi', 'Hasil'],
        'rows': [[s['pair'], s['rule'], s['detail'], s['result']] for s in pair_steps]
    })
    
    steps.append({
        'type': 'result',
        'title': 'Hasil Dekripsi',
        'ciphertext': text,
        'plaintext': decrypted
    })
    
    return decrypted, steps
