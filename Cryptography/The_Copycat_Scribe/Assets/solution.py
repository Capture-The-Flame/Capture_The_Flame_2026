import subprocess
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption

# ------------------------
# 1️⃣ Paste values here
# ------------------------
r_hex  = "26BA72A86B95D957E6149B908186D96740D85CEE39E8291CA09122A36CC1A29F"
s1_hex = "876C08651C0197337297774256803B58ECE1273FE995C584C798A93A8E85C779"
s2_hex = "7D8C43B123EB9ED8E41C9BAED026CE75CA604C149E1C1FA2C80A3B14296348A6"

z1_hex = "7a0afa9a9dbbc8079281541863a940791eabfa6a2375cc6f01d4be619bc33329"
z2_hex = "be27469739c72167aea976ff0193a53b269f3878e706e83b6b372195d7f13653"

# Curve order (secp256k1)
n_hex = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141"

# ------------------------
# 2️⃣ Convert to integers
# ------------------------
r  = int(r_hex, 16)
s1 = int(s1_hex, 16)
s2 = int(s2_hex, 16)
z1 = int(z1_hex, 16)
z2 = int(z2_hex, 16)
n  = int(n_hex, 16)

# ------------------------
# 3️⃣ Recover nonce k
# ------------------------
k = ((z1 - z2) * pow(s1 - s2, -1, n)) % n
print("Recovered nonce k:", hex(k))

# ------------------------
# 4️⃣ Recover private key d
# ------------------------
d = ((s1 * k - z1) * pow(r, -1, n)) % n
print("Recovered private key d:", hex(d))

# ------------------------
# 5️⃣ Build private key object
# ------------------------
private_key = ec.derive_private_key(d, ec.SECP256K1(), default_backend())

pem = private_key.private_bytes(
    Encoding.PEM,
    PrivateFormat.TraditionalOpenSSL,
    NoEncryption()
)

with open("recovered_key.pem", "wb") as f:
    f.write(pem)

print("Private key saved as recovered_key.pem")

# ------------------------
# 6️⃣ Decrypt flag.enc using OpenSSL
# ------------------------
subprocess.run([
    "openssl", "pkeyutl",
    "-decrypt",
    "-inkey", "recovered_key.pem",
    "-in", "flag.enc",
    "-out", "flag.txt"
])

# ------------------------
# 7️⃣ Print decrypted flag
# ------------------------
with open("flag.txt", "r") as f:
    flag = f.read()

print("\nDecrypted Flag:\n", flag)