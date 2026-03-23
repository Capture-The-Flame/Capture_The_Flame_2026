import random

# List of animal names
animals = [
    "Lion", "Tiger", "Bear", "Wolf", "Fox", "Eagle", "Shark", "Whale", "Dolphin", "Panda",
    "Rabbit", "Snake", "Hawk", "Falcon", "Owl", "Panther", "Leopard", "Cheetah", "Elephant", "Giraffe",
    "Zebra", "Hippo", "Rhino", "Gorilla", "Monkey", "Koala", "Kangaroo", "Penguin", "Seal", "Otter"
]

def generate_passwords(filename="psw.txt", count=10000):
    passwords = set()
    
    while len(passwords) < count:
        animal = random.choice(animals)
        # Generate 8 random digits
        digits = random.randint(0, 99999999)
        # Format as animal name + 8 digits (zero-padded if necessary)
        password = f"{animal}{digits:08d}"
        passwords.add(password)
    
    with open(filename, "w") as f:
        for psw in passwords:
            f.write(psw + "\n")
            
    print(f"Generated {len(passwords)} unique passwords in {filename}")

if __name__ == "__main__":
    generate_passwords()
