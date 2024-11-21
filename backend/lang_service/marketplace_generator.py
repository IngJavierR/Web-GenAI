import os
import gc
import pandas as pd
import base64

# Configuración
EXCEL_PATH = "files/Tecnoloite/Master Descripciones en tecnolite.mx.xlsx"
IMAGES_DIR = "files/Tecnoloite/"

def _convertir_imagenes_a_base64(imagenes: list[str]) -> list[str]:
    """Convierte una lista de rutas de imágenes a un arreglo de Base64."""
    imagenes_base64 = []
    for imagen in imagenes:
        try:
            with open(imagen, "rb") as img_file:
                encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
                imagenes_base64.append(encoded_image)
        except Exception as e:
            print(f"Error al convertir la imagen {imagen} a Base64: {e}")
    return imagenes_base64

def _obtener_caracteristicas_producto(producto, imagenes):
    """Genera un diccionario con las características del producto y sus imágenes en Base64."""
    return {
        "codigo": producto.get("Código", "N/A"),
        "nombre": producto.get("Nombre", "N/A"),
        "marca": producto.get("Marca", "N/A"),
        "descripcion_corta": producto.get("Descripción Corta", "N/A"),
        "descripcion_larga": producto.get("Descripción Larga", "N/A"),
        "promocion": producto.get("Promocion", "N/A"),
        "precio": producto.get("Precio", "N/A"),
        "caracteristicas": {
            "tipo_acabado": producto.get("Tipo de acabado", "N/A"),
            "base_bombilla": producto.get("Base de la bombilla", "N/A"),
            "tipo_lampara": producto.get("Tipo de lámpara", "N/A"),
        },
        "imagenes": _convertir_imagenes_a_base64(imagenes),
    }

# Leer el Excel
def _leer_excel(file_path) -> pd.DataFrame:
    try:
        return pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return None

# Obtener las imágenes asociadas a un producto
def _obtener_imagenes(codigo) -> list[str]:
    return [os.path.join(IMAGES_DIR, img) 
            for img in os.listdir(IMAGES_DIR)
            if img.startswith(str(codigo))]

# Programa principal
def marketplace_generator():
    data = _leer_excel(EXCEL_PATH)
    if data is None:
        return
    
    product_with_images = None

    for index, row in data.iterrows():
        producto = row.to_dict()
        codigo = producto["Código"]
        imagenes = _obtener_imagenes(codigo)
        
        if not imagenes:
            print(f"No se encontraron imágenes para el producto: {codigo}")
            continue
        
        # Generar estructura
        product_with_images = _obtener_caracteristicas_producto(producto, imagenes)
        break

    # Liberar memoria del DataFrame
    del data
    gc.collect()  # Llama al recolector de basura

    return product_with_images
