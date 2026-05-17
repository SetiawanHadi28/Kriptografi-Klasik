import numpy as np
import math
from typing import List, Tuple, Dict, Any

# ─────────────────────────────────────────────
# CAESAR CIPHER
# ─────────────────────────────────────────────

def caesar_encrypt(text: str, shift: int) -> Dict[str, Any]:
    steps = []
    result = []
    shift = shift % 26

    steps.append({
        "title": "Rumus",
        "content": f"E(x) = (x + k) mod 26  →  k = {shift}"
    })

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char) - base
            encrypted = (x + shift) % 26
            enc_char = chr(encrypted + base)
            steps.append({
                "char": char,
                "x": x,
                "formula": f"({x} + {shift}) mod 26 = {encrypted}",
                "result": enc_char
            })
            result.append(enc_char)
        else:
            steps.append({"char": char, "x": "-", "formula": "non-alpha, skip", "result": char})
            result.append(char)

    return {"ciphertext": "".join(result), "steps": steps}


def caesar_decrypt(text: str, shift: int) -> Dict[str, Any]:
    steps = []
    result = []
    shift = shift % 26

    steps.append({
        "title": "Rumus",
        "content": f"D(x) = (x - k) mod 26  →  k = {shift}"
    })

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char) - base
            decrypted = (x - shift) % 26
            dec_char = chr(decrypted + base)
            steps.append({
                "char": char,
                "x": x,
                "formula": f"({x} - {shift}) mod 26 = {decrypted}",
                "result": dec_char
            })
            result.append(dec_char)
        else:
            steps.append({"char": char, "x": "-", "formula": "non-alpha, skip", "result": char})
            result.append(char)

    return {"plaintext": "".join(result), "steps": steps}


# ─────────────────────────────────────────────
# VIGENÈRE CIPHER
# ─────────────────────────────────────────────

def vigenere_encrypt(text: str, key: str) -> Dict[str, Any]:
    key = key.upper()
    steps = []
    result = []
    key_idx = 0

    steps.append({
        "title": "Rumus",
        "content": "E(x) = (x + k_i) mod 26"
    })

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char.upper()) - ord('A')
            k = ord(key[key_idx % len(key)]) - ord('A')
            encrypted = (x + k) % 26
            enc_char = chr(encrypted + (ord('A') if char.isupper() else ord('a')))
            steps.append({
                "char": char,
                "key_char": key[key_idx % len(key)],
                "x": x,
                "k": k,
                "formula": f"({x} + {k}) mod 26 = {encrypted}",
                "result": enc_char
            })
            result.append(enc_char)
            key_idx += 1
        else:
            steps.append({"char": char, "key_char": "-", "x": "-", "k": "-", "formula": "non-alpha, skip", "result": char})
            result.append(char)

    return {"ciphertext": "".join(result), "steps": steps}


def vigenere_decrypt(text: str, key: str) -> Dict[str, Any]:
    key = key.upper()
    steps = []
    result = []
    key_idx = 0

    steps.append({
        "title": "Rumus",
        "content": "D(x) = (x - k_i) mod 26"
    })

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char.upper()) - ord('A')
            k = ord(key[key_idx % len(key)]) - ord('A')
            decrypted = (x - k) % 26
            dec_char = chr(decrypted + (ord('A') if char.isupper() else ord('a')))
            steps.append({
                "char": char,
                "key_char": key[key_idx % len(key)],
                "x": x,
                "k": k,
                "formula": f"({x} - {k}) mod 26 = {decrypted}",
                "result": dec_char
            })
            result.append(dec_char)
            key_idx += 1
        else:
            steps.append({"char": char, "key_char": "-", "x": "-", "k": "-", "formula": "non-alpha, skip", "result": char})
            result.append(char)

    return {"plaintext": "".join(result), "steps": steps}


# ─────────────────────────────────────────────
# AFFINE CIPHER
# ─────────────────────────────────────────────

def mod_inverse(a: int, m: int) -> int:
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return -1


def affine_encrypt(text: str, a: int, b: int) -> Dict[str, Any]:
    if math.gcd(a, 26) != 1:
        raise ValueError(f"Nilai 'a' = {a} harus relatif prima dengan 26. gcd({a}, 26) = {math.gcd(a, 26)} ≠ 1")

    steps = []
    result = []

    steps.append({
        "title": "Rumus",
        "content": f"E(x) = (a·x + b) mod 26  →  a={a}, b={b}"
    })

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char.upper()) - ord('A')
            encrypted = (a * x + b) % 26
            enc_char = chr(encrypted + (ord('A') if char.isupper() else ord('a')))
            steps.append({
                "char": char,
                "x": x,
                "formula": f"({a}×{x} + {b}) mod 26 = {(a*x+b)} mod 26 = {encrypted}",
                "result": enc_char
            })
            result.append(enc_char)
        else:
            steps.append({"char": char, "x": "-", "formula": "non-alpha, skip", "result": char})
            result.append(char)

    return {"ciphertext": "".join(result), "steps": steps}


def affine_decrypt(text: str, a: int, b: int) -> Dict[str, Any]:
    if math.gcd(a, 26) != 1:
        raise ValueError(f"Nilai 'a' = {a} harus relatif prima dengan 26.")

    a_inv = mod_inverse(a, 26)
    steps = []
    result = []

    steps.append({
        "title": "Rumus",
        "content": f"D(x) = a⁻¹·(x - b) mod 26  →  a={a}, a⁻¹={a_inv}, b={b}"
    })

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char.upper()) - ord('A')
            decrypted = (a_inv * (x - b)) % 26
            dec_char = chr(decrypted + (ord('A') if char.isupper() else ord('a')))
            steps.append({
                "char": char,
                "x": x,
                "formula": f"{a_inv}×({x} - {b}) mod 26 = {a_inv*(x-b)} mod 26 = {decrypted}",
                "result": dec_char
            })
            result.append(dec_char)
        else:
            steps.append({"char": char, "x": "-", "formula": "non-alpha, skip", "result": char})
            result.append(char)

    return {"plaintext": "".join(result), "steps": steps, "a_inv": a_inv}


# ─────────────────────────────────────────────
# HILL CIPHER
# ─────────────────────────────────────────────

def matrix_mod_inverse(matrix: List[List[int]], mod: int) -> List[List[int]]:
    n = len(matrix)
    mat = np.array(matrix, dtype=float)
    det = round(np.linalg.det(mat))
    det = int(det) % mod
    det_inv = mod_inverse(det, mod)
    if det_inv == -1:
        raise ValueError(f"Matriks tidak memiliki invers mod {mod}. det={det}, gcd({det},{mod})≠1")

    adjugate = np.round(np.linalg.det(mat) * np.linalg.inv(mat)).astype(int)
    inv_matrix = (det_inv * adjugate % mod).tolist()
    return [[int(v % mod) for v in row] for row in inv_matrix]


def hill_encrypt(text: str, key_matrix: List[List[int]]) -> Dict[str, Any]:
    n = len(key_matrix)
    text_clean = ''.join(c.upper() for c in text if c.isalpha())

    while len(text_clean) % n != 0:
        text_clean += 'X'

    steps = []
    result = []

    steps.append({
        "title": "Persiapan",
        "content": f"Teks dibersihkan: '{text_clean}', dibagi dalam blok {n} huruf"
    })

    for i in range(0, len(text_clean), n):
        block = text_clean[i:i+n]
        vec = [ord(c) - ord('A') for c in block]
        mat = np.array(key_matrix)
        product = (mat @ vec) % 26
        enc_block = ''.join(chr(int(v) + ord('A')) for v in product)

        calc_rows = []
        for row_idx, row in enumerate(key_matrix):
            terms = " + ".join(f"{row[j]}×{vec[j]}" for j in range(n))
            raw = sum(row[j] * vec[j] for j in range(n))
            calc_rows.append(f"[{', '.join(str(r) for r in row)}] · [{', '.join(str(v) for v in vec)}] = {terms} = {raw} ≡ {int(product[row_idx])} (mod 26) → {enc_block[row_idx]}")

        steps.append({
            "block": block,
            "vec": vec,
            "calc_rows": calc_rows,
            "result": enc_block
        })
        result.append(enc_block)

    return {
        "ciphertext": "".join(result),
        "steps": steps,
        "key_matrix": key_matrix,
        "padded_text": text_clean
    }


def hill_decrypt(text: str, key_matrix: List[List[int]]) -> Dict[str, Any]:
    n = len(key_matrix)
    text_clean = ''.join(c.upper() for c in text if c.isalpha())

    while len(text_clean) % n != 0:
        text_clean += 'X'

    inv_matrix = matrix_mod_inverse(key_matrix, 26)
    steps = []
    result = []

    steps.append({
        "title": "Persiapan",
        "content": f"Menghitung matriks invers K⁻¹ (mod 26)"
    })

    for i in range(0, len(text_clean), n):
        block = text_clean[i:i+n]
        vec = [ord(c) - ord('A') for c in block]
        mat = np.array(inv_matrix)
        product = (mat @ vec) % 26
        dec_block = ''.join(chr(int(v) + ord('A')) for v in product)

        calc_rows = []
        for row_idx, row in enumerate(inv_matrix):
            terms = " + ".join(f"{row[j]}×{vec[j]}" for j in range(n))
            raw = sum(row[j] * vec[j] for j in range(n))
            calc_rows.append(f"[{', '.join(str(r) for r in row)}] · [{', '.join(str(v) for v in vec)}] = {terms} = {raw} ≡ {int(product[row_idx])} (mod 26) → {dec_block[row_idx]}")

        steps.append({
            "block": block,
            "vec": vec,
            "calc_rows": calc_rows,
            "result": dec_block
        })
        result.append(dec_block)

    return {
        "plaintext": "".join(result),
        "steps": steps,
        "key_matrix": key_matrix,
        "inv_matrix": inv_matrix
    }


# ─────────────────────────────────────────────
# PLAYFAIR CIPHER
# ─────────────────────────────────────────────

def generate_playfair_matrix(key: str) -> List[List[str]]:
    key = key.upper().replace('J', 'I')
    seen = set()
    sequence = []
    for c in key:
        if c.isalpha() and c not in seen:
            seen.add(c)
            sequence.append(c)
    for c in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if c not in seen:
            seen.add(c)
            sequence.append(c)
    return [sequence[i*5:(i+1)*5] for i in range(5)]


def find_position(matrix: List[List[str]], char: str) -> Tuple[int, int]:
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return -1, -1


def playfair_prepare_text(text: str) -> str:
    text = text.upper().replace('J', 'I')
    text = ''.join(c for c in text if c.isalpha())
    result = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 == len(text):
            result.extend([a, 'X'])
            i += 1
        elif text[i] == text[i+1]:
            result.extend([a, 'X'])
            i += 1
        else:
            result.extend([text[i], text[i+1]])
            i += 2
    return ''.join(result)


def playfair_encrypt(text: str, key: str) -> Dict[str, Any]:
    matrix = generate_playfair_matrix(key)
    prepared = playfair_prepare_text(text)
    steps = []
    result = []

    steps.append({
        "title": "Teks Dipersiapkan",
        "content": f"'{prepared}' → pasangan: {[prepared[i:i+2] for i in range(0, len(prepared), 2)]}"
    })

    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            ea = matrix[r1][(c1+1) % 5]
            eb = matrix[r2][(c2+1) % 5]
            rule = f"Baris sama → geser kolom kanan: ({r1},{c1})→({r1},{(c1+1)%5}), ({r2},{c2})→({r2},{(c2+1)%5})"
        elif c1 == c2:
            ea = matrix[(r1+1) % 5][c1]
            eb = matrix[(r2+1) % 5][c2]
            rule = f"Kolom sama → geser baris bawah: ({r1},{c1})→({(r1+1)%5},{c1}), ({r2},{c2})→({(r2+1)%5},{c2})"
        else:
            ea = matrix[r1][c2]
            eb = matrix[r2][c1]
            rule = f"Persegi panjang → tukar kolom: ({r1},{c1})→({r1},{c2}), ({r2},{c2})→({r2},{c1})"

        steps.append({
            "pair": f"{a}{b}",
            "pos_a": (r1, c1),
            "pos_b": (r2, c2),
            "rule": rule,
            "result": f"{ea}{eb}"
        })
        result.append(ea + eb)

    return {
        "ciphertext": "".join(result),
        "steps": steps,
        "matrix": matrix,
        "prepared": prepared
    }


def playfair_decrypt(text: str, key: str) -> Dict[str, Any]:
    matrix = generate_playfair_matrix(key)
    prepared = playfair_prepare_text(text)
    steps = []
    result = []

    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            da = matrix[r1][(c1-1) % 5]
            db = matrix[r2][(c2-1) % 5]
            rule = f"Baris sama → geser kolom kiri: ({r1},{c1})→({r1},{(c1-1)%5}), ({r2},{c2})→({r2},{(c2-1)%5})"
        elif c1 == c2:
            da = matrix[(r1-1) % 5][c1]
            db = matrix[(r2-1) % 5][c2]
            rule = f"Kolom sama → geser baris atas: ({r1},{c1})→({(r1-1)%5},{c1}), ({r2},{c2})→({(r2-1)%5},{c2})"
        else:
            da = matrix[r1][c2]
            db = matrix[r2][c1]
            rule = f"Persegi panjang → tukar kolom: ({r1},{c1})→({r1},{c2}), ({r2},{c2})→({r2},{c1})"

        steps.append({
            "pair": f"{a}{b}",
            "pos_a": (r1, c1),
            "pos_b": (r2, c2),
            "rule": rule,
            "result": f"{da}{db}"
        })
        result.append(da + db)

    return {
        "plaintext": "".join(result),
        "steps": steps,
        "matrix": matrix
    }
