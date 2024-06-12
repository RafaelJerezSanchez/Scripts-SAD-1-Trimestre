from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os

def generate_keys():
    name = input("Ingrese un nombre para identificar el par de claves: ")

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    with open(f"{name}_private_key.pem", "wb") as private_file:
        private_file.write(private_pem)
    
    with open(f"{name}_public_key.pem", "wb") as public_file:
        public_file.write(public_pem)
    
    print(f"Claves generadas y guardadas en {name}_private_key.pem y {name}_public_key.pem")

def list_keys():
    files = os.listdir()
    private_keys = [file for file in files if file.endswith("_private_key.pem")]
    public_keys = [file for file in files if file.endswith("_public_key.pem")]
    
    print("\nClaves privadas disponibles:")
    for key in private_keys:
        print(key)
    
    print("\nClaves públicas disponibles:")
    for key in public_keys:
        print(key)

def load_private_key(file_path):
    with open(file_path, "rb") as private_file:
        private_key = serialization.load_pem_private_key(
            private_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def load_public_key(file_path):
    with open(file_path, "rb") as public_file:
        public_key = serialization.load_pem_public_key(
            public_file.read(),
            backend=default_backend()
        )
    return public_key

def encrypt_message(public_key, message):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_message(private_key, encrypted_message):
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()

def menu():
    while True:
        print("\nMenú:")
        print("1. Generar claves")
        print("2. Listar claves")
        print("3. Cifrar archivo de texto")
        print("4. Descifrar archivo de texto")
        print("5. Salir")
        
        choice = input("Seleccione una opción: ")
        
        if choice == '1':
            generate_keys()
        elif choice == '2':
            list_keys()
        elif choice == '3':
            public_key_file = input("Ingrese el nombre del archivo de clave pública: ")
            public_key = load_public_key(public_key_file)
            input_file = input("Ingrese el nombre del archivo de texto a cifrar: ")
            output_file = input("Ingrese el nombre del archivo donde guardar el texto cifrado: ")
            with open(input_file, "r", encoding="utf-8") as file:
                message = file.read()
            encrypted_message = encrypt_message(public_key, message)
            with open(output_file, "wb") as enc_file:
                enc_file.write(encrypted_message)
            print(f"Mensaje cifrado y guardado en {output_file}")
        elif choice == '4':
            private_key_file = input("Ingrese el nombre del archivo de clave privada: ")
            private_key = load_private_key(private_key_file)
            input_file = input("Ingrese el nombre del archivo de texto cifrado: ")
            output_file = input("Ingrese el nombre del archivo donde guardar el texto descifrado: ")
            with open(input_file, "rb") as enc_file:
                encrypted_message = enc_file.read()
            decrypted_message = decrypt_message(private_key, encrypted_message)
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(decrypted_message)
            print(f"Mensaje descifrado y guardado en {output_file}")
        elif choice == '5':
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

if __name__ == "__main__":
    menu()
