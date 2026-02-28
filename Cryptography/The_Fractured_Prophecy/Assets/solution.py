import math

# ======================
# Step 0: Set your values
# ======================

# Paste your modulus N (from oracle_public.pem) here as a single hex string
N_hex = "ACBE9A93B00EC0ED731CA85B12FD61D169418940407B6B6D50BA6E92DEC9A7756F82BB1CB25B6F4EDAB6D59857DAAC385416367BA3582EBA85AC8D0C9CA9CF4FD6BCE35EB1FA08C57F594D2251F383C4BF533039D682D0595B8221390CD1740E03BBF1E48DEDD66C58876CD21EAE7338C57AB7C0E67A8DC2789C3E1D8B2D48757A65D616DA8F71E804570F72C386CAABED0E1AAB1FD480590F8BE9E79C55D16D87A51198A6C5A498DA57710D57D37D39C34FA6D927B409AE7B0CDACDCF5B06BFE391887D9120A40814B3799F2D26B66BE987F3D0A3FDC9005E7EC5BC01974DB5A467DAE835CE42A7960628363ED25AB60574B38520B6BA4AC1B98B618406AA97"
N = int(N_hex, 16)

# Usually RSA public exponent
e = 65537

# Load S1 and S2 from your .bin files
def load_signature(path):
    with open(path, "rb") as f:
        return int.from_bytes(f.read(), "big")

S1 = load_signature("prophecy_valid.bin")       # valid signature
S2 = load_signature("prophecy_fractured.bin")   # faulty signature

# ======================
# Step 1: Compute p
# ======================
# Since your CTF gives CRT outputs, we just use:
p = math.gcd(abs(S1 - S2), N)
q = N // p

print(f"Recovered p: {p} ({p.bit_length()} bits)")
print(f"Recovered q: {q} ({q.bit_length()} bits)")

# ======================
# Step 2: Compute private exponent
# ======================
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
print(f"Private exponent d computed successfully.")

# ======================
# Step 3: Decrypt ciphertext
# ======================
with open("Secret_Scroll.enc", "rb") as f:
    C = int.from_bytes(f.read(), "big")

M = pow(C, d, N)
plaintext = M.to_bytes((M.bit_length() + 7) // 8, "big")

print("Decrypted message:")
print(plaintext.decode(errors="ignore"))