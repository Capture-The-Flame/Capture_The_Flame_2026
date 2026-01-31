import base64
from cryptography.fernet import Fernet

# ---------------------------------------------
# - THIS CODE GENERATES THE ENCRYPTED PAYLOAD -
# ---------------------------------------------

SOURCE_CODE = """
passw = input("What\'s the password?")

if passw == 'i_l0v3_y0u':
  print('flame{h4ppy_v4lent1n3s_d4y!}')
else:
  print('That password is incorrect.')
"""


key_str = "valentinevalentinevalentinevalen"
key_base64 = base64.b64encode(key_str.encode())
f = Fernet(key_base64)
payload = f.encrypt(SOURCE_CODE.encode())
print(payload)


# ---------------------------------------------
# --------- THIS CODE IS THE SOLUTION ---------
# ---------------------------------------------


# encrypted payload
payload = b'gAAAAABpfPOKqvM_8c9Oqu4QXZ1_h-10bXEMl9cMvgALNZuxkgYEG8rSljtenMFBJoFAxogYGghuJ1ClfgL8UndIB4Y5n_uJGofEBMd2cuilK8GDuwoZHNzsXqGJT7vpqxRjRTcWjIkwB1O1Vlr2mLlYQwHGwlaEPLVRiIAY4fPqclI9PJ9F8uht8gQL0cTGisyBqpMhpMHXsQXINj9-L_KlBVWFcjN-mhqlleb785HVENJPhlmzNNJrsUYbrobYCcWI4RbqfGGS7p_LUEMUh2m9GB61UwnkRA=='

# key string
key_str = 'valentinevalentinevalentinevalen'

key_base64 = base64.b64encode(key_str.encode())
f = Fernet(key_base64)

plain = f.decrypt(payload)

print("Source code:")
print(plain.decode())