import os

def cifrar_texto(texto, desplazamiento):
    texto_cifrado = ""

    for caracter in texto:
        if caracter.isalpha():
            if caracter.islower():
                codigo = ord('a')
            else:
                codigo = ord('A')

            codigo_cifrado = (ord(caracter) - codigo + desplazamiento) % 26 + codigo
            texto_cifrado += chr(codigo_cifrado)
        else:
            texto_cifrado += caracter

    return texto_cifrado


def descifrar_texto(texto_cifrado, desplazamiento):
    texto_descifrado = ""

    for caracter in texto_cifrado:
        if caracter.isalpha():
            mayuscula = caracter.isupper()
            codigo = ord(caracter.upper())
            codigo_descifrado = (codigo - 65 - desplazamiento + 26) % 26 + 65
            caracter_descifrado = chr(codigo_descifrado)
            if mayuscula:
                texto_descifrado += caracter_descifrado
            else:
                texto_descifrado += caracter_descifrado.lower()
        else:
            texto_descifrado += caracter

    return texto_descifrado


def cifrar_archivo(nombre_archivo, desplazamiento):
    try:
        with open(nombre_archivo, 'r') as archivo:
            texto_original = archivo.read()
            texto_cifrado = cifrar_texto(texto_original, desplazamiento)
            nombre_archivo_cifrado = input("Ingrese el nombre para el archivo cifrado (incluya la extensión .txt): ")
            escritorio = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            ruta_archivo_cifrado = os.path.join(escritorio, nombre_archivo_cifrado)
            with open(ruta_archivo_cifrado, 'w') as archivo_cifrado:
                archivo_cifrado.write(texto_cifrado)
            print("Archivo cifrado creado en el escritorio:", nombre_archivo_cifrado)
    except FileNotFoundError:
        print("El archivo", nombre_archivo, "no se encontró.")


def descifrar_archivo(nombre_archivo, desplazamiento):
    try:
        with open(nombre_archivo, 'r') as archivo:
            texto_cifrado = archivo.read()
            texto_descifrado = descifrar_texto(texto_cifrado, desplazamiento)
            nombre_archivo_descifrado = input("Ingrese el nombre para el archivo descifrado (incluya la extensión .txt): ")
            escritorio = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            ruta_archivo_descifrado = os.path.join(escritorio, nombre_archivo_descifrado)
            with open(ruta_archivo_descifrado, 'w') as archivo_descifrado:
                archivo_descifrado.write(texto_descifrado)
            print("Archivo descifrado creado en el escritorio:", nombre_archivo_descifrado)
    except FileNotFoundError:
        print("El archivo", nombre_archivo, "no se encontró.")


def menu():
    while True:
        print("1. Cifrar archivo")
        print("2. Descifrar archivo")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre_archivo = input("Ingrese el nombre del archivo a cifrar (incluya la extensión .txt): ")
            desplazamiento = int(input("Ingrese la clave: "))
            cifrar_archivo(nombre_archivo, desplazamiento)
        elif opcion == "2":
            nombre_archivo = input("Ingrese el nombre del archivo cifrado a descifrar (incluya la extensión .txt): ")
            desplazamiento = int(input("Ingrese la clave para descifrar: "))
            descifrar_archivo(nombre_archivo, desplazamiento)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    menu()
