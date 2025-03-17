import pandas as pd
import re
import os

# Archivos de entrada y salida
archivo_entrada = 'datos/DATA2010-2024.csv'
archivo_ok = 'DataBase_ok.csv'
archivo_error = 'DataBase_error.csv'

# Expresiones regulares para ISBN-10 y ISBN-13
isbn_10_regex = re.compile(r'^\d{9}[\dX]$')
isbn_13_regex = re.compile(r'^(978|979)-\d{1,5}-\d{1,7}-\d{1,6}-\d$')

def validar_isbn(isbn):
    """Valida si el ISBN es válido (tanto ISBN-10 como ISBN-13)"""
    if isinstance(isbn, float) or not isbn:
        return False
    
    isbn = str(isbn).strip().replace('-', '')

    # Verifica ISBN-13
    if len(isbn) == 13 and isbn.isdigit():
        suma = sum((int(d) if i % 2 == 0 else int(d) * 3) for i, d in enumerate(isbn[:-1]))
        digito_control = (10 - (suma % 10)) % 10
        return digito_control == int(isbn[-1])

    # Verifica ISBN-10
    if len(isbn) == 10 and isbn[:-1].isdigit() and (isbn[-1].isdigit() or isbn[-1] == 'X'):
        suma = sum((i + 1) * (10 if x == 'X' else int(x)) for i, x in enumerate(isbn[:-1]))
        digito_control = (11 - (suma % 11)) % 11
        digito_control = 'X' if digito_control == 10 else str(digito_control)
        return digito_control == isbn[-1]
    
    return False

def procesar_csv(archivo_entrada):
    try:
        # Cargar el archivo CSV separado por ';'
        df = pd.read_csv(archivo_entrada, sep=';', dtype=str)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
    
    # Validar los ISBN y dividir en válidos e inválidos
    registros_validos = df[df['ISBN'].apply(validar_isbn)]
    registros_invalidos = df[~df['ISBN'].apply(validar_isbn)]

    # Guardar los datos válidos en el archivo acumulativo
    if not registros_validos.empty:
        if os.path.exists(archivo_ok):
            registros_validos.to_csv(archivo_ok, mode='a', index=False, header=False, sep=';')
        else:
            registros_validos.to_csv(archivo_ok, mode='w', index=False, header=True, sep=';')

    # Guardar los datos inválidos en el archivo acumulativo
    if not registros_invalidos.empty:
        if os.path.exists(archivo_error):
            registros_invalidos.to_csv(archivo_error, mode='a', index=False, header=False, sep=';')
        else:
            registros_invalidos.to_csv(archivo_error, mode='w', index=False, header=True, sep=';')

    # Mostrar resumen del proceso
    print(f"Se han procesado {len(df)} registros:")
    print(f"{len(registros_validos)} registros válidos añadidos a '{archivo_ok}'.")
    print(f"{len(registros_invalidos)} registros inválidos añadidos a '{archivo_error}'.")

if __name__ == "__main__":
    procesar_csv(archivo_entrada)
