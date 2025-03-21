
# Índice de Calidad de Datos para una Base de Datos Editorial

El índice de calidad de datos (IQD) es una métrica que mide la **completitud**, **consistencia**, **validez**, **precisión** y **unicidad** de los datos almacenados en una base de datos editorial.


# Guía para el uso de parámetros de calidad de datos

## a. Abrir el archivo
Accede a la hoja de cálculo desde el siguiente enlace:  
 [**Parametrización de calidad**](https://docs.google.com/spreadsheets/d/1pPO_obkfmVQWzPJz8hAdkly9GrDG-SgA_NEvTtR2jlY/edit?usp=sharing)  

---

## b. Seleccionar columna
Identifica la columna que deseas evaluar para asegurar que cumpla con los estándares de calidad de datos.

---

## c. Asignar parámetros
Usa las listas desplegables en las columnas correspondientes para establecer los siguientes parámetros:

- **Importancia** → Clasifica si la columna es obligatoria o secundaria.  
- **Consistencia** → Evalúa si los datos están en el formato correcto y siguen las reglas establecidas.  
- **Valoración de duplicados** → Determina si los duplicados son válidos o deben eliminarse para mantener la integridad de los datos.  

---

## d. Guardar cambios
Verifica que los parámetros de calidad estén correctamente configurados y guarda los ajustes para mantener la consistencia de los datos.  

---

**Esta guía te permitirá evaluar y mejorar la calidad de los datos de manera estructurada y eficiente.**



---
## 1. Componentes clave del índice de calidad de datos (IQD)

### 1.1. Completitud
Evalúa el porcentaje de valores no nulos en cada columna.

$$ 
\text{Completitud} = \frac{\text{Número de valores NO nulos}}{\text{Número total de registros}} \times 100
$$ 

---

### 1.2. Consistencia
Evalúa si los valores de una columna son consistentes con un formato o estándar definido.

$$ 
\text{Consistencia} = \frac{\text{Número de valores consistentes}}{\text{Número total de registros}} \times 100
$$

---

### 1.3. Validez
Evalúa si los valores en una columna cumplen con las reglas de negocio o estándares específicos.

$$ 
\text{Validez} = \frac{\text{Número de valores válidos}}{\text{Número total de registros}} \times 100
$$

---

### 1.4. Precisión
Evalúa la exactitud de los valores.

$$ 
\text{Precisión} = \frac{\text{Número de valores precisos}}{\text{Número total de registros}} \times 100
$$

---

### 1.5. Unicidad
Evalúa si la columna ISBN tiene valores únicos y no repetidos.

$$ 
\text{Unicidad} = \frac{\text{Número de valores únicos en ISBN}}{\text{Número total de registros}} \times 100
$$ 

---

## 2. Fórmula para el índice de calidad de datos (IQD)
Una vez calculadas las cinco dimensiones anteriores, el índice de calidad de datos puede expresarse como el promedio ponderado de estas dimensiones:

$$
\text{IQD} = \frac{\text{Completitud} + \text{Consistencia} + \text{Validez} + \text{Precisión} + \text{Unicidad}}{5}
$$ 

---

## 3. Ejemplo de cálculo del índice de calidad
**Base de datos:** 1,000 registros

- Completitud → 950 valores completos → $$ \frac{950}{1000} \times 100 = 95\% \) $$  
- Consistencia → 900 valores con formato correcto → $$\( \frac{900}{1000} \times 100 = 90\% \) $$  
- Validez → 800 valores válidos → $$ \frac{800}{1000} \times 100 = 80\% \) $$  
- Precisión → 850 valores precisos → $$ \frac{850}{1000} \times 100 = 85\% \) $$    
- Unicidad → 990 valores únicos → $$ \frac{990}{1000} \times 100 = 99\% \) $$    

**IQD Total:**  
$$ 
IQD = \frac{95 + 90 + 80 + 85 + 99}{5} = 89.8\%
$$ 

---

## 4. Interpretación del Índice de Calidad de Datos

| Rango (%) | Interpretación |
|-----------|----------------|
| 90% - 100% | Datos de alta calidad |
| 75% - 90% | Datos de calidad aceptable (con algunos problemas menores) |
| 50% - 75% | Datos de baja calidad (requerirán limpieza y corrección) |
| 0% - 50% | Datos de muy baja calidad (inviables para análisis o reportes) |

---

## 5. Estrategia de mejora de calidad de datos
### **Completitud**
- Implementar restricciones en las columnas clave para evitar valores nulos.  
- Establecer un proceso automatizado para rellenar datos faltantes mediante imputación de datos.  

### **Consistencia**
- Estandarizar formatos en columnas específicas (como ISBN).  
- Usar restricciones.  

### **Validez**
- Definir reglas de validación para datos numéricos, fechas y textos.  
- Implementar validaciones para verificar el dígito de control en ISBN.  

### **Precisión**
- Limpiar valores duplicados o incorrectos.  
- Verificar errores de tipografía o formato en títulos y fechas.  

### **Unicidad**
- Implementar restricciones `UNIQUE` en la columna ISBN.  
- Crear procesos de detección y eliminación de duplicados.  

---

## **Conclusión**
El índice de calidad de datos (IQD) proporciona una visión clara de la calidad de los datos almacenados en la base de datos. Al medir y mejorar continuamente cada dimensión, se puede garantizar que la base de datos tenga datos de alta calidad, fiables y consistentes para apoyar decisiones comerciales y análisis estratégicos.
