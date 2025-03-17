import pandas as pd
import sys
import os
import gc
from tqdm import tqdm

def generar_estadisticas_csv(archivo_entrada, archivo_salida, chunksize=10000):
    total_registros = 0
    total_columnas = None
    tipos_datos = {}
    valores_nulos = {}
    valores_unicos = {}
    valores_duplicados = {}
    muestra_valores = {}
    distribucion_valores = {}
    estadisticas_numericas = None
    registros_duplicados = 0
    
    try:
        # Primera pasada para obtener el número total de registros y columnas
        with tqdm(total=os.path.getsize(archivo_entrada), desc="Procesando archivo", unit="B", unit_scale=True) as progreso:
            for chunk in pd.read_csv(
                archivo_entrada,
                sep=None,  # Detección automática de separador
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
                        valores_unicos[col] = set()
                        valores_duplicados[col] = 0
                        muestra_valores[col] = set()
                        distribucion_valores[col] = {}

                total_registros += len(chunk)

                # Tipos de datos
                for col in chunk.columns:
                    if col not in tipos_datos:
                        tipos_datos[col] = chunk[col].dtype

                # Nulos
                for col in chunk.columns:
                    valores_nulos[col] += chunk[col].isnull().sum()

                # Únicos
                for col in chunk.columns:
                    valores_unicos[col].update(chunk[col].dropna().unique())

                # Duplicados por columna
                for col in chunk.columns:
                    valores_duplicados[col] += chunk[col].duplicated().sum()

                # Muestra de valores (máximo 5 valores únicos)
                for col in chunk.columns:
                    if len(muestra_valores[col]) < 5:
                        muestra_valores[col].update(chunk[col].dropna().unique())
                        muestra_valores[col] = set(list(muestra_valores[col])[:5])

                # Distribución de valores categóricos
                for col in chunk.select_dtypes(include='object').columns:
                    distribucion_valores[col] = chunk[col].value_counts().to_dict()

                # Duplicados totales
                registros_duplicados += chunk.duplicated().sum()

                # Estadísticas numéricas
                if estadisticas_numericas is None:
                    estadisticas_numericas = chunk.describe()
                else:
                    estadisticas_numericas = pd.concat([estadisticas_numericas, chunk.describe()]).groupby(level=0).mean()

                # Liberar memoria
                del chunk
                gc.collect()

                # Progreso por tamaño leído
                progreso.update(chunksize * 1024)
            
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{archivo_entrada}' no existe.")
        return
    except Exception as e:
        print(f"❌ Error al leer el archivo CSV: {e}")
        return

    # ---- Escribir resultados en el archivo de salida ----
    with open(archivo_salida, 'w') as f:
        f.write(f"📂 Archivo de entrada: {archivo_entrada}\n")
        f.write(f"📂 Archivo de salida: {archivo_salida}\n\n")
        f.write(f"📌 Número total de registros: {total_registros}\n")
        f.write(f"📌 Número total de columnas: {total_columnas}\n\n")

        f.write("📊 **TIPOS DE DATOS POR COLUMNA:**\n")
        for col, tipo in tipos_datos.items():
            f.write(f"{col}: {tipo}\n")
        f.write("\n")

        f.write("📌 **VALORES NULOS POR COLUMNA:**\n")
        for col, nulos in valores_nulos.items():
            f.write(f"{col}: {nulos}\n")
        f.write("\n")

        f.write("📌 **VALORES ÚNICOS POR COLUMNA:**\n")
        for col, unicos in valores_unicos.items():
            f.write(f"{col}: {len(unicos)}\n")
        f.write("\n")

        f.write("📌 **VALORES DUPLICADOS POR COLUMNA:**\n")
        for col, duplicados in valores_duplicados.items():
            f.write(f"{col}: {duplicados}\n")
        f.write("\n")

        f.write("📌 **MUESTRA DE VALORES POR COLUMNA:**\n")
        for col, muestra in muestra_valores.items():
            f.write(f"{col}: {', '.join(map(str, muestra))}\n")
        f.write("\n")

        f.write("📊 **DISTRIBUCIÓN DE VALORES EN COLUMNAS CATEGÓRICAS:**\n")
        for col, dist in distribucion_valores.items():
            f.write(f"\n- {col}:\n")
            for valor, cantidad in dist.items():
                f.write(f"  {valor}: {cantidad}\n")

        f.write("\n📈 **ESTADÍSTICAS DESCRIPTIVAS DE COLUMNAS NUMÉRICAS:**\n")
        f.write(estadisticas_numericas.to_string())
        f.write("\n")

    print(f"✅ Informe de calidad generado en: {archivo_salida}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❌ Uso: python script.py <archivo_entrada.csv> <archivo_salida.txt>")
        sys.exit(1)

    archivo_entrada = sys.argv[1]
    archivo_salida = sys.argv[2]

    if not os.path.exists(archivo_entrada):
        print(f"❌ Error: El archivo '{archivo_entrada}' no existe.")
        sys.exit(1)

    generar_estadisticas_csv(archivo_entrada, archivo_salida)
