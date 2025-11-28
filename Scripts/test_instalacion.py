"""
Script de prueba para verificar la instalación de componentes
"""
import sys
import os

print("=" * 60)
print("🔍 VERIFICACIÓN DEL GESTOR DE CONTRASEÑAS DNIe")
print("=" * 60)
print()

# Verificar Python
print("1. Verificando Python...")
print(f"   ✓ Versión: {sys.version}")
print()

# Verificar dependencias
print("2. Verificando dependencias...")

required_modules = {
    "pygame": "Interfaz gráfica",
    "pyperclip": "Portapapeles",
    "cryptography": "Cifrado",
    "pkcs11": "DNIe",
    "json": "Base de datos",
    "threading": "Hilos",
    "hashlib": "Hash"
}

missing = []
for module, desc in required_modules.items():
    try:
        __import__(module)
        print(f"   ✓ {module:15} - {desc}")
    except ImportError:
        print(f"   ✗ {module:15} - {desc} (FALTA)")
        missing.append(module)

print()

if missing:
    print("❌ FALTAN DEPENDENCIAS")
    print("   Ejecuta: pip install " + " ".join(missing))
    print()
else:
    print("✅ Todas las dependencias instaladas correctamente")
    print()

# Verificar archivos
print("3. Verificando archivos del proyecto...")

required_files = [
    "main.py",
    "dnie_detector.py",
    "dnie_authenticator.py",
    "password_manager_ui.py",
    "password_dialog.py",
    "data_manager.py",
    "password_generator.py",
    "config_manager.py",
    "ui_components.py",
    "certificate_reader.py"
]

script_dir = os.path.dirname(os.path.abspath(__file__))
missing_files = []

for filename in required_files:
    filepath = os.path.join(script_dir, filename)
    if os.path.exists(filepath):
        print(f"   ✓ {filename}")
    else:
        print(f"   ✗ {filename} (FALTA)")
        missing_files.append(filename)

print()

if missing_files:
    print("❌ FALTAN ARCHIVOS DEL PROYECTO")
    print()
else:
    print("✅ Todos los archivos del proyecto encontrados")
    print()

# Verificar importaciones locales
print("4. Verificando componentes nuevos...")

try:
    from config_manager import ConfigManager
    print("   ✓ ConfigManager importado")
    
    config = ConfigManager()
    print(f"   ✓ Tema actual: {config.config['theme']}")
    print(f"   ✓ Temas disponibles: {len(config.get_theme_names())}")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    missing_files.append("config_manager.py")

try:
    from ui_components import ModernButton, ModernInputBox, SearchBar
    print("   ✓ Componentes UI importados")
except Exception as e:
    print(f"   ✗ Error: {e}")
    missing_files.append("ui_components.py")

print()

# Resumen final
print("=" * 60)
print("📊 RESUMEN")
print("=" * 60)

if not missing and not missing_files:
    print()
    print("✅ ¡TODO LISTO PARA USAR!")
    print()
    print("🚀 Para iniciar la aplicación ejecuta:")
    print("   python Inicio_Gestor.py")
    print()
    print("📚 Consulta la documentación:")
    print("   - MEJORAS_PROFESIONALES.md")
    print("   - GUIA_INICIO_RAPIDO.md")
    print()
else:
    print()
    print("❌ HAY PROBLEMAS QUE RESOLVER")
    print()
    if missing:
        print("Dependencias faltantes:")
        for m in missing:
            print(f"  - {m}")
        print()
        print("Comando para instalar:")
        print(f"  pip install {' '.join(missing)}")
        print()
    
    if missing_files:
        print("Archivos faltantes:")
        for f in missing_files:
            print(f"  - {f}")
        print()

print("=" * 60)
