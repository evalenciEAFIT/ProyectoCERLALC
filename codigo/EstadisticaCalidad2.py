import pandas as pd
import sys
import os
import gc
import re
from tqdm import tqdm

# Expresiones regulares para validar ISBN-10 e ISBN-13
isbn_10_regex = re.compile(r'^\d{9}[\dX]$')
isbn_13_regex = re.compile(r'^(978|979)-\d{1,5}-\d{1,7}-\d{1,6}-\d$')

def validar_isbn(valor):
    if isinstance(valor, str):
        valor = valor.replace("-", "").strip()
        if len(valor) == 13 and valor.isdigit():
            # Validar ISBN-13
            suma = sum((int(d) if i % 2 == 0 else int(d) * 3) for i, d in enumerate(valor[:-1]))
            digito_control = (10 - (suma % 10)) % 10
            if digito_control == int(valor[-1]):
                return "ISBN-13"
        elif len(valor) == 10 and (valor[:-1].isdigit() and (valor[-1].isdigit() or valor[-1] == 'X')):
            # Validar ISBN-10
            suma = sum((i + 1) * (10 if x == 'X' else int(x)) for i, x in enumerate(valor[:-1]))
            digito_control = (11 - (suma % 11)) % 11
            if digito_control == 10:
                digito_control = 'X'
            if str(digito_control) == valor[-1]:
                return "ISBN-10"
    return "No es ISBN"

def detectar_tipo(valor):
    if pd.isna(valor):
        return "Nulo"
    elif isinstance(valor, str):
        valor = valor.strip()
        if validar_isbn(valor) in ["ISBN-10", "ISBN-13"]:
            return validar_isbn(valor)
        try:
            pd.to_datetime(valor, format="%Y-%m-%d", errors="raise")
            return "Fecha"
        except Exception:
            return "Texto"
    elif isinstance(valor, (int, float)):
        return "Número"
    else:
        return "Otro"

def generar_estadisticas_csv(archivo_entrada, archivo_salida, chunksize=10000):
    total_registros = 0
    total_columnas = None
    tipos_datos = {}
    valores_nulos = {}
    tipo_valores = {}
    distribucion_tipos = {}

    try:
        with tqdm(total=os.path.getsize(archivo_entrada), desc="Procesando archivo", unit="B", unit_scale=True) as progreso:
            for chunk in pd.read_csv(
                archivo_entrada,
                sep=None,
                engine="python",
                on_bad_lines="skip",
                encoding="utf-8",
                quotechar='"',
                skip_blank_lines=True,
                chunksize=chunksize
            ):
                if total_columnas is None:
                    total_columnas = len(chunk.columns)
                    for col in chunk.columns:
                        valores_nulos[col] = 0
                        tipo_valores[col] = {
                            "Texto": 0,
                            "Número": 0,
                            "Fecha": 0,
                            "ISBN-10": 0,
                            "ISBN-13": 0,
                            "No es ISBN": 0,
                            "Otro": 0,
                            "Nulo": 0
                        }

                total_registros += len(chunk)

                # Tipos de datos y valores nulos
                for col in chunk.columns:
                    valores_nulos[col] += chunk[col].isnull().sum()

                    # Detectar tipo de valor
                    for valor in chunk[col]:
                        tipo = detectar_tipo(valor)
                        tipo_valores[col][tipo] += 1

                progreso.update(len(chunk) * 1024)
                del chunk
                gc.collect()

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no existe.")
        return
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return

    # ---- Escribir resultados en el archivo de salida ----
    with open(archivo_salida, 'w') as f:
        f.write(f"Archivo de entrada: {archivo_entrada}\n")
        f.write(f"Archivo de salida: {archivo_salida}\n\n")
        f.write(f"Número total de registros: {total_registros}\n")
        f.write(f"Número total de columnas: {total_columnas}\n\n")

        # Diagnóstico por columna
        for col in tipo_valores:
            f.write(f"**Diagnóstico de columna: {col}**\n")
            total = sum(tipo_valores[col].values())
            for tipo, cantidad in tipo_valores[col].items():
                porcentaje = (cantidad / total) * 100 if total > 0 else 0
                if cantidad > 0:
                    f.write(f"- {tipo}: {cantidad} registros ({porcentaje:.2f}%)\n")
                else:
                    f.write(f"- {tipo}: - \n")
                #f.write(f"- {tipo}: {cantidad} registros ({porcentaje:.2f}%)\n")
            f.write("\n")

        f.write("\n**VALORES NULOS POR COLUMNA:**\n")
        for col, nulos in valores_nulos.items():
            f.write(f"{col}: {nulos}\n")

    print(f"Informe de calidad generado en: {archivo_salida}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py <archivo_entrada.csv> <archivo_salida.txt>")
        sys.exit(1)

    archivo_entrada = sys.argv[1]
    archivo_salida = sys.argv[2]

    if not os.path.exists(archivo_entrada):
        print(f"Error: El archivo '{archivo_entrada}' no existe.")
        sys.exit(1)

    generar_estadisticas_csv(archivo_entrada, archivo_salida)
