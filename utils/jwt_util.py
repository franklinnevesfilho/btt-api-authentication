from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import jwt

def encode(data: dict, algorithm: str = "HS256"):
    return jwt.encode(data, _get_private_key(), algorithm)

def decode(token: str, algorithms: [] =None):
    if algorithms is None:
        algorithms = ["HS256"]

    return jwt.decode(token, _get_private_key(), algorithms=algorithms)


def _get_private_key(strip_markers: bool = True) -> str:
    with open("utils/private_key.pem", "r") as f:
        lines = f.readlines()
    
    if strip_markers:
        # Remove first and last lines (BEGIN and END markers)
        key_content = ''.join(lines[1:-1]).replace('\n', '')
        return key_content
    else:
        # Return full key content
        return ''.join(lines)


def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
        )
    # Serialize private key to PEM format
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Optionally, save the private key to a file
    with open("utils/private_key.pem", "wb") as f:
        f.write(pem)

    print("Private key generated and saved to private_key.pem")