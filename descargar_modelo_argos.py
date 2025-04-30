import argostranslate.package
import argostranslate.translate

# Define los códigos de idioma (ISO 639-1)
from_code = "es"  # Idioma de origen (por ejemplo, 'es' para español)
to_code = "en"    # Idioma de destino (por ejemplo, 'en' para inglés)

# Actualiza el índice de paquetes disponibles
argostranslate.package.update_package_index()

# Obtiene la lista de paquetes disponibles
available_packages = argostranslate.package.get_available_packages()

# Filtra el paquete que coincide con los idiomas especificados
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code,
        available_packages
    ),
    None
)

# Verifica si se encontró el paquete y procede a descargar e instalar
if package_to_install:
    download_path = package_to_install.download()
    argostranslate.package.install_from_path(download_path)
    print(f"✅ Modelo de traducción de '{from_code}' a '{to_code}' instalado correctamente.")
else:
    print(f"❌ No se encontró un modelo de traducción de '{from_code}' a '{to_code}'.")
