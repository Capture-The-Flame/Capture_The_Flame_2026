import hashlib

FILE_NAME = "psw.txt"
given_hash = "b4d50069458f02d73deb8cf4eb3de340031b230f026d4f1feca5879fe1fe06be"

print("GENERATING HASH FOR THE PASSWORD:")
psw = "Elephant16369131"
hashed_psw = hashlib.sha256(psw.encode()).hexdigest()
print(f"Hash of '{psw}': {hashed_psw}")


# SOLUTION:
with open(FILE_NAME, "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        hashed_psw = hashlib.sha256(line.encode()).hexdigest()
        if hashed_psw == given_hash:
            print(f"Password found: {line}")
            break
