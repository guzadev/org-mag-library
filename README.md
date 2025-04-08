
# 🧠 org-mag-library

Este script permite organizar y renombrar automáticamente archivos `.max` y sus carpetas `maps` asociadas dentro de una biblioteca de modelos 3D.

## 🚀 ¿Qué hace?

- Busca carpetas con archivos `.max` que contengan "corona" en su nombre.
- Renombra estos archivos secuencialmente (ej: `001.max`, `002.max`, ...).
- Mueve la carpeta `maps` (si existe) y la renombra con el mismo número (`001/`, `002/`...).
- Registra todas las modificaciones y errores en un archivo Excel (`org-mag-library.xlsx`).

## 🛠️ Requisitos

- Python 3.x
- Librerías:
  - `pandas`
  - `openpyxl`

Instalación rápida de dependencias:

```bash
pip install pandas openpyxl
```

## 📂 Estructura esperada

> ⚠️ **Nota importante**:  
> Esta estructura de carpetas es **la más común** en los modelos descargados desde la página **[Zeel Project](https://zeelproject.com/)**.  
> De hecho, **la mayoría (por no decir todos) de los modelos que usamos en el estudio han sido descargados desde Zeel Project**, y cerca del **90% de ellos siguen esta estructura**.  
> Como teníamos una enorme cantidad de modelos descargados con esa misma organización, decidí crear este script para **ordenarlos de manera rápida y precisa**, manteniendo la relación entre los archivos `.max` y sus carpetas `maps`.

```
Library/
├── ModeloX/
│   ├── MAX/ o 3Ds Max/
│   │   └── archivo_corona.max
│   └── maps/ o MAPS/
```

## 💻 Uso

1. Ejecuta el script:
```bash
python script.py
```

2. Ingresa la ruta completa de la carpeta base (ejemplo):
```
Z:\Library\Models\Accessories\Book - Libro
```

3. El script procesará las subcarpetas y renombrará los archivos y carpetas si encuentra los elementos necesarios.

4. Puedes procesar múltiples carpetas en una sola sesión.

## 🧾 Registro

Se genera un archivo `org-mag-library.xlsx` con dos hojas:

- `Modificaciones`: Registro de archivos y carpetas renombradas.
- `Eventos`: Errores detectados (por ejemplo, carpetas faltantes).

## 🐞 Notas

- Si ya procesaste una carpeta antes, será ignorada para evitar duplicados.
- Si no existen archivos `.max` en la base, se solicitará una numeración inicial.

---

## 🧪 Convertir el Script en un Ejecutable (.exe)

Si querés ejecutar este script en cualquier computadora sin tener Python instalado, podés convertirlo en un archivo `.exe` con **PyInstaller**.

### Paso a paso:

1. Instalá PyInstaller:

```bash
pip install pyinstaller
```

2. Generá el `.exe`:

```bash
pyinstaller --onefile script.py
```

Esto creará una carpeta `dist/` donde estará el ejecutable:  
```
dist/
└── script.exe
```

3. Podés copiar ese `.exe` a cualquier otra PC con Windows, y funcionará sin necesidad de instalar Python.

> 📦 Consejo: Para mejor portabilidad, ejecutá PyInstaller desde una máquina limpia (por ejemplo, una VM) para evitar dependencias innecesarias.

---

## ✨ Contexto y motivación

Este proyecto nace como solución a una necesidad real dentro de nuestro emprendimiento **MAG Studio**, del cual soy cofundador. En **MAG** nos especializamos en **visualización arquitectónica**, y como parte de nuestro flujo de trabajo diario manejamos una gran cantidad de modelos 3D descargados de distintas fuentes, especialmente **Zeel Project**.

La mayoría (por no decir todos) de nuestros modelos provienen de Zeel Project, y cerca del 90% siguen una estructura de carpetas muy similar. Como teníamos muchísimos modelos descargados con esa misma organización, decidí crear este script para **ordenarlos de manera rápida y precisa**, manteniendo la integridad entre modelos y sus texturas.

Gracias a esta solución, **ahorramos muchísimo tiempo** en tareas de gestión de archivos, lo cual nos permitió **centrarnos más en la parte creativa y menos en tareas repetitivas**, optimizando así el flujo de trabajo del estudio.

---
