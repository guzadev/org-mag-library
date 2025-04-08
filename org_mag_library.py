import os
import shutil
import pandas as pd
from datetime import datetime

def find_max_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for d in dirs:
            if "max" in d.lower():
                return os.path.join(root, d)
    return None

def find_maps_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for d in dirs:
            if "map" in d.lower():  # Acepta 'MAP' o 'MAPS'
                return os.path.join(root, d)
    return None

def save_to_excel(data, error_data, excel_file="org-mag-library.xlsx"):
    try:
        if not os.path.exists(excel_file):
            with pd.ExcelWriter(excel_file, mode='w', engine='openpyxl') as writer:
                pd.DataFrame(columns=["principal", "carpeta del modelo", "nuevo nombre .max", "nuevo nombre carpeta 'maps'", "fecha y hora"]).to_excel(writer, sheet_name="Modificaciones", index=False)
                pd.DataFrame(columns=["principal", "carpeta del modelo", "evento", "fecha y hora"]).to_excel(writer, sheet_name="Eventos", index=False)
        
        existing_modifications = pd.read_excel(excel_file, sheet_name="Modificaciones")
        existing_errors = pd.read_excel(excel_file, sheet_name="Eventos")
        
        new_modifications = pd.DataFrame(data, columns=["principal", "carpeta del modelo", "nuevo nombre .max", "nuevo nombre carpeta 'maps'", "fecha y hora"])
        new_errors = pd.DataFrame(error_data, columns=["principal", "carpeta del modelo", "evento", "fecha y hora"])
        
        df_modifications = pd.concat([existing_modifications, new_modifications]).drop_duplicates()
        df_errors = pd.concat([existing_errors, new_errors]).drop_duplicates()
        
        with pd.ExcelWriter(excel_file, mode='w', engine='openpyxl') as writer:
            df_modifications.to_excel(writer, sheet_name="Modificaciones", index=False)
            df_errors.to_excel(writer, sheet_name="Eventos", index=False)
    except Exception as e:
        print(f"Error guardando en Excel: {e}")

def find_existing_numbers(folder_path):
    """Encuentra los números de archivos .max en la carpeta base."""
    existing_numbers = []
    for file in os.listdir(folder_path):
        if file.endswith(".max") and file[:-4].isdigit():
            existing_numbers.append(int(file[:-4]))
    return sorted(existing_numbers)

def get_next_number(folder_path):
    """Determina la siguiente numeración disponible basado en los archivos .max existentes."""
    existing_numbers = find_existing_numbers(folder_path)
    if not existing_numbers:
        return int(input("No se encontraron archivos .max. Ingrese la numeración inicial: "))
    
    last_number = existing_numbers[-1]
    missing_numbers = sorted(set(range(existing_numbers[0], last_number)) - set(existing_numbers))
    
    if missing_numbers:
        return missing_numbers[0]  # Rellena el primer hueco encontrado
    else:
        return last_number + 1  # Si no hay huecos, continúa con el siguiente número

def rename_and_move_files(base_path):
    try:
        base_path = base_path.strip().strip('"')
        if not os.path.exists(base_path):
            print(f"Error: La ruta {base_path} no existe. Verifica la ruta ingresada.")
            return

        folders = sorted([f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))])
        number = get_next_number(base_path)
        renamed_files = 0
        renamed_folders = 0
        log_data = []
        error_log = []
        fecha_actual = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        
        existing_modifications = pd.read_excel("org-mag-library.xlsx", sheet_name="Modificaciones") if os.path.exists("org-mag-library.xlsx") else pd.DataFrame()
        processed_folders = set(existing_modifications["carpeta del modelo"].tolist()) if "carpeta del modelo" in existing_modifications.columns else set()
        
        for folder in folders:
            if folder.isdigit():
                continue
            
            if folder in processed_folders:
                event = [base_path, folder, "Carpeta ya procesada previamente", fecha_actual]
                error_log.append(event)
                print(event)
                continue

            folder_path = os.path.join(base_path, folder)
            max_folder = find_max_folder(folder_path)
            maps_folder = find_maps_folder(folder_path)
            
            if not max_folder:
                event = [base_path, folder, "Falta carpeta MAX o 3Ds Max", fecha_actual]
                error_log.append(event)
                print(event)
                continue
            
            found = False
            for file in os.listdir(max_folder):
                if 'corona' in file.lower() and file.endswith('.max'):
                    old_file_path = os.path.join(max_folder, file)
                    new_file_name = f"{number}.max"
                    new_file_path = os.path.join(base_path, new_file_name)
                    
                    shutil.move(old_file_path, new_file_path)
                    renamed_files += 1
                    found = True
                    
                    if maps_folder and os.path.exists(maps_folder):
                        new_maps_path = os.path.join(base_path, str(number))
                        shutil.move(maps_folder, new_maps_path)
                        renamed_folders += 1
                        log_data.append([base_path, folder, new_file_name, str(number), fecha_actual])
                    else:
                        log_data.append([base_path, folder, new_file_name, "Sin carpeta maps", fecha_actual])
                        event = [base_path, folder, "Falta carpeta MAP o MAPS", fecha_actual]
                        error_log.append(event)
                        print(event)
                    
                    number = get_next_number(base_path)  # Busca el siguiente número disponible
                    break
            
            if not found:
                event = [base_path, folder, "Falta archivo .max con 'corona'", fecha_actual]
                error_log.append(event)
                print(event)

        if renamed_files == renamed_folders:
            print(f"Proceso completado correctamente. {renamed_files} archivos y carpetas renombradas.")
        else:
            error_message = "Error: la cantidad de archivos renombrados no coincide con la cantidad de carpetas renombradas."
            print(error_message)
            error_log.append([base_path, "GENERAL", "Desajuste entre archivos y carpetas renombradas", fecha_actual])
        
        save_to_excel(log_data, error_log)
    except Exception as e:
        print(f"Error: {e}")

while True:
    base_directory = input("Ingrese la ruta de la carpeta (ej. 'Z:\\Library\\Models\\Accessories\\Book - Libro'): ").strip().strip('"')
    
    if not base_directory:
        print("No ingresaste una ruta. Intenta de nuevo.")
        continue
    
    rename_and_move_files(base_directory)
    
    repetir = input("¿Quieres procesar otra carpeta? (s/n): ").strip().lower()
    if repetir != 's':
        break
