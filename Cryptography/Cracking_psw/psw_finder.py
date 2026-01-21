import hashlib

FILE_NAME = "psw.txt"
given_hash = "ccd6716608569d2df2ec83a9e7fc69909717cfff8f74528e8d13a9b9f32885cc"

with open(FILE_NAME, "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        hashed_psw = hashlib.sha256(line.encode()).hexdigest()
        if hashed_psw == given_hash:
            print(f"Password found: {line}")
            break
