import segno
from PIL import Image
import os
import shutil
import tempfile

# URL para el código QR
google_review_url = "https://search.google.com/local/writereview?placeid=ChIJe2prou8uQg0RgZENtpxAgqY"

# Función para convertir JPEG a PNG con transparencia
def convert_jpeg_to_png(jpeg_path, output_png_path, dpi=300):
    """
    Convierte un archivo JPEG a PNG manteniendo la calidad para impresión.
    
    Args:
        jpeg_path: Ruta al archivo JPEG
        output_png_path: Ruta donde guardar el PNG
        dpi: Resolución para impresión (dots per inch)
    """
    try:
        # Abrir la imagen JPEG
        img = Image.open(jpeg_path)
        
        # Configurar la resolución para impresión
        img.info['dpi'] = (dpi, dpi)
        
        # Si queremos un fondo transparente, podemos crear una máscara
        # (Esto es opcional y depende de tu logo)
        """
        # Para hacer el fondo blanco transparente:
        img = img.convert("RGBA")
        datas = img.getdata()
        new_data = []
        for item in datas:
            # Si el pixel es casi blanco, hacerlo transparente
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((255, 255, 255, 0))  # Transparente
            else:
                new_data.append(item)  # Mantener el color original
        img.putdata(new_data)
        """
        
        # Guardar como PNG
        img.save(output_png_path, "PNG", dpi=(dpi, dpi))
        print(f"✅ Imagen convertida y guardada como {output_png_path}")
        return True
    except Exception as e:
        print(f"❌ Error al convertir la imagen: {e}")
        return False

# Función para crear un QR con logo
def create_qr_with_logo(url, logo_path, output_path, scale=10):
    """
    Crea un código QR con un logo en el centro.
    
    Args:
        url: URL para codificar en el QR
        logo_path: Ruta al archivo del logo (PNG)
        output_path: Ruta donde guardar el QR final
        scale: Escala del QR (mayor = mejor resolución)
    """
    try:
        # Crear el código QR con alta corrección de errores
        qr = segno.make(url, error='h')
        
        # Método alternativo compatible con todas las versiones de segno
        # Generar el QR básico primero
        qr.save(output_path, scale=scale, border=4, light="white")
        
        # Luego añadir el logo manualmente con PIL
        qr_img = Image.open(output_path)
        logo_img = Image.open(logo_path)
        
        # Calcular posición y tamaño para el logo
        qr_width, qr_height = qr_img.size
        logo_width, logo_height = logo_img.size
        
        # Redimensionar logo (20% del tamaño del QR)
        logo_size = int(qr_width * 0.2)
        # Usar método compatible con todas las versiones de PIL
        # En PIL moderno se usan valores enteros en lugar de constantes
        logo_img = logo_img.resize((logo_size, logo_size), resample=1)  # 1 = alta calidad
        
        # Calcular posición para centrar el logo
        position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        
        # Crear una nueva imagen con fondo blanco
        final_img = Image.new("RGBA", qr_img.size, "white")
        
        # Pegar el QR
        if qr_img.mode == "RGBA":
            final_img.paste(qr_img, (0, 0), qr_img)
        else:
            final_img.paste(qr_img, (0, 0))
        
        # Pegar el logo
        if logo_img.mode == "RGBA":
            final_img.paste(logo_img, position, logo_img)
        else:
            final_img.paste(logo_img, position)
        
        # Guardar imagen final
        final_img.save(output_path, "PNG")
        
        print(f"✅ QR generado como: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error al generar el QR: {e}")
        return False

# Ruta al logo JPEG
logo_jpeg_path = "logo.jpeg"
logo_png_path = "logo_for_qr.png"

# Convertir el logo de JPEG a PNG
if os.path.exists(logo_jpeg_path):
    convert_jpeg_to_png(logo_jpeg_path, logo_png_path)
else:
    print(f"❌ No se encontró el archivo {logo_jpeg_path}")
    exit()

# Crear QRs en diferentes formatos para diferentes usos
# QR para impresión (alta resolución)
create_qr_with_logo(
    url=google_review_url,
    logo_path=logo_png_path,
    output_path="qr_print_ready.png",
    scale=20  # Alta resolución para impresión
)

# QR para uso digital
create_qr_with_logo(
    url=google_review_url,
    logo_path=logo_png_path,
    output_path="qr_digital.png",
    scale=10  # Resolución estándar para web
)

# QR en formato SVG (para edición adicional)
svg_output = "qr_editable.svg"
qr = segno.make(google_review_url, error='h')
qr.save(svg_output, scale=10, border=4)
print(f"✅ QR básico en SVG generado como: {svg_output} (puedes añadir el logo manualmente)")

print("\n🖨️ El archivo qr_print_ready.png está optimizado para impresión")
print("🌐 El archivo qr_digital.png está optimizado para uso digital")
print("✏️ El archivo qr_editable.svg puede editarse con software como Illustrator o Inkscape")
