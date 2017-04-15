### Create key pairs

from cryptography.hazmat.primitives.asymmetric import rsa, ec, dsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.ec import SECP256K1

private_key_rsa = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
private_ke_ec = ec.generate_private_key(curve=SECP256K1, backend=default_backend())
private_key_dsa = dsa.generate_private_key(key_size=2048, backend=default_backend())

public_key_rsa = private_key_rsa.public_key()
public_key_ec = private_key_ec.public_key()
public_key_dsa = private_key_dsa.public_key()

pem_pub_rsa = public_key_rsa.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
pem_pub_ec = public_key_ec.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
pem_pub_dsa = public_key_dsa.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

for line in pem_pub_rsa.splitlines():
	print(line)

for line in pem_pub_ec.splitlines():
	print(line)

for line in pem_pub_dsa.splitlines():
	print(line)