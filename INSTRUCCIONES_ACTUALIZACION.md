# 🔄 Instrucciones de Actualización

## ⚠️ IMPORTANTE: Lee Antes de Actualizar

Tu aplicación ha sido **completamente mejorada** con nuevos archivos y funcionalidades. Esta guía te ayudará a actualizar correctamente.

---

## 📋 Checklist Pre-Actualización

Antes de comenzar, verifica:

- [ ] Tienes una copia de seguridad de tu proyecto
- [ ] Has cerrado la aplicación si está en ejecución
- [ ] Tienes Python 3.8+ instalado
- [ ] Tienes todas las dependencias (`pip install pygame pyperclip cryptography python-pkcs11`)

---

## 🔄 Proceso de Actualización

### Opción A: Actualización Limpia (Recomendado)

Los nuevos archivos ya están en tu proyecto y **NO sobrescriben** los antiguos. Los archivos originales siguen funcionando.

**Archivos NUEVOS (no reemplazan nada):**
- ✅ `config_manager.py` - Sistema de configuración
- ✅ `ui_components.py` - Componentes UI modernos
- ✅ `Interfaz_Contraseñas_Pro.py` - Nueva interfaz principal
- ✅ `Nombre_Contraseña_Pro.py` - Nuevo diálogo
- ✅ `test_instalacion.py` - Script de verificación

**Archivos ACTUALIZADOS (mejoras compatibles):**
- ✅ `Inicio_Gestor.py` - Ahora soporta temas
- ✅ `detectar_dnie_gui.py` - Colores dinámicos
- ✅ `verificar_dnie_gui.py` - Usa sistema de temas

**Archivos SIN CAMBIOS:**
- ✅ `manejo_datos.py` - Seguridad intacta
- ✅ `generador_contraseñas.py` - Funcionalidad original
- ✅ `detectar_dnie.py` - Lógica de detección
- ✅ Resto de archivos auxiliares

---

## 🚀 Activar la Nueva Versión

### Paso 1: Verificar Instalación

```powershell
cd "c:\Users\ruben\Desktop\Importante\Github\password-manager-dnie\Scripts"
python test_instalacion.py
```

Deberías ver: `✅ ¡TODO LISTO PARA USAR!`

### Paso 2: Probar la Nueva Interfaz

```powershell
python Inicio_Gestor.py
```

La aplicación debería:
1. ✅ Iniciar con animaciones suaves
2. ✅ Mostrar botón de configuración (⚙️)
3. ✅ Permitir cambiar de tema
4. ✅ Funcionar perfectamente

### Paso 3: Revisar Características

Prueba todas las nuevas funciones:
- [ ] Cambiar tema (Dark, Light, Ocean Blue, Purple Night, Forest Green)
- [ ] Buscar contraseñas
- [ ] Ver estadísticas (botón 📊)
- [ ] Crear nueva contraseña con indicador de fortaleza
- [ ] Verificar animaciones suaves

---

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'config_manager'"

**Solución:**
```powershell
# Verifica que estés en el directorio correcto
cd "c:\Users\ruben\Desktop\Importante\Github\password-manager-dnie\Scripts"
dir config_manager.py
```

Si no aparece el archivo, descárgalo nuevamente.

### Error: "ImportError: cannot import name 'ConfigManager'"

**Causa:** Error de sintaxis en `config_manager.py`

**Solución:**
```powershell
# Verifica el archivo
python -c "from config_manager import ConfigManager; print('OK')"
```

### La aplicación se ve igual que antes

**Causa posible:** Usando archivos antiguos

**Solución:**
1. Verifica que `Inicio_Gestor.py` tenga la línea:
   ```python
   from config_manager import ConfigManager
   ```
2. Si no está, los archivos no se actualizaron correctamente

### Los temas no cambian

**Solución:**
1. Verifica que existe `app_config.json` en la carpeta Scripts
2. Si no existe, se creará automáticamente al cambiar el tema
3. Cierra y reabre la aplicación

### Las animaciones van lentas

**Soluciones:**
1. Ve a Configuración → Desactiva animaciones
2. Usa el tema "Light" (es más ligero)
3. Cierra otros programas para liberar recursos

---

## 📦 Archivos de Configuración

### app_config.json

Este archivo se crea automáticamente y contiene tus preferencias:

```json
{
    "theme": "Dark",
    "font_size": "medium",
    "animations_enabled": true,
    "auto_copy_timeout": 30,
    "show_password_strength": true,
    "compact_view": false,
    "show_notifications": true
}
```

**Ubicación:** `Scripts/app_config.json`

**¿Puedo editarlo manualmente?** 
Sí, pero es más fácil usar el panel de configuración.

**¿Se puede borrar?**
Sí, se recreará con valores por defecto.

---

## 🔙 Rollback (Volver a Versión Anterior)

Si por alguna razón necesitas volver a la versión anterior:

### Opción 1: Usar archivos originales

Los archivos originales siguen intactos. No se han borrado ni reemplazado.

**Archivo original:** `Interfaz_Contraseñas.py`
**Nueva versión:** `Interfaz_Contraseñas_Pro.py`

Para usar la versión antigua, simplemente:

1. Abre `verificar_dnie_gui.py`
2. Cambia la línea:
   ```python
   import Interfaz_Contraseñas_Pro as ic
   ```
   Por:
   ```python
   import Interfaz_Contraseñas as ic
   ```

### Opción 2: Usar Git

Si usas Git:
```bash
git checkout HEAD -- Scripts/
```

---

## 🆕 Migración de Datos

### ¿Se pierden mis contraseñas?

**NO.** Las contraseñas se guardan en archivos cifrados que **no han cambiado**.

Archivos de datos (intactos):
- `Database_*.json.enc` - Tu base de datos cifrada
- `kdb_enc_*.bin` - Clave de cifrado
- `C_value.bin` - Valor C

Estos archivos siguen siendo **100% compatibles**.

### ¿Tengo que reconfigurar algo?

No. Al primer inicio:
1. Se detecta que no existe `app_config.json`
2. Se crea automáticamente con valores por defecto
3. Tema "Dark" se activa por defecto
4. Puedes cambiarlo cuando quieras

---

## 📊 Comparación de Versiones

| Característica | Versión Anterior | Nueva Versión |
|----------------|------------------|---------------|
| Temas | 1 fijo | 5 dinámicos |
| Configuración | No | Sí |
| Búsqueda | No | Sí |
| Estadísticas | No | Sí |
| Animaciones | Básicas | Profesionales |
| Indicador fortaleza | No | Sí |
| Diseño tarjetas | No | Sí |
| Panel lateral | No | Sí |
| Notificaciones | Básicas | Elegantes |
| Componentes UI | Básicos | Modernos |

---

## 🎯 Siguiente Paso: Usar la Nueva Versión

Una vez verificado que todo funciona:

1. ✅ Lee `GUIA_INICIO_RAPIDO.md`
2. ✅ Explora todas las nuevas características
3. ✅ Personaliza con tu tema favorito
4. ✅ Disfruta de la nueva interfaz

---

## 🐛 Reportar Problemas

Si encuentras algún problema durante la actualización:

### Información a Incluir

1. **Error exacto** (copia el mensaje completo)
2. **Paso donde ocurre** (al iniciar, al cambiar tema, etc.)
3. **Versión de Python** (`python --version`)
4. **Sistema operativo** (Windows 10/11)
5. **Captura de pantalla** (si es posible)

### Ejemplo de Reporte

```
Error: ModuleNotFoundError: No module named 'config_manager'

Pasos:
1. Ejecuté python Inicio_Gestor.py
2. Apareció el error inmediatamente
3. No se abrió ninguna ventana

Sistema:
- Python 3.10.5
- Windows 11
- PowerShell 5.1

Verificación:
- config_manager.py SÍ existe en la carpeta Scripts
- Las otras dependencias están instaladas
```

---

## ✅ Verificación Post-Actualización

Después de actualizar, verifica:

### Funcionalidad Básica
- [ ] La aplicación inicia correctamente
- [ ] Se detecta el DNIe
- [ ] El PIN funciona
- [ ] Las contraseñas se cargan
- [ ] Puedo crear nuevas contraseñas
- [ ] Puedo copiar contraseñas

### Nuevas Características
- [ ] Puedo abrir configuración (⚙️)
- [ ] Puedo cambiar de tema
- [ ] El tema se guarda al reiniciar
- [ ] La búsqueda funciona
- [ ] Las estadísticas se muestran
- [ ] Las animaciones son fluidas
- [ ] Los botones responden al hover

### Rendimiento
- [ ] La app inicia en <2 segundos
- [ ] Las animaciones son suaves (60 FPS)
- [ ] No hay lag al hacer scroll
- [ ] La búsqueda es instantánea

---

## 📞 Soporte

### Auto-Diagnóstico

```powershell
# Script de diagnóstico rápido
cd "c:\Users\ruben\Desktop\Importante\Github\password-manager-dnie\Scripts"

# 1. Verificar archivos
dir config_manager.py
dir ui_components.py
dir Interfaz_Contraseñas_Pro.py

# 2. Verificar importaciones
python -c "from config_manager import ConfigManager; print('✓ config_manager OK')"
python -c "from ui_components import ModernButton; print('✓ ui_components OK')"

# 3. Ejecutar test completo
python test_instalacion.py
```

---

## 🎉 ¡Actualización Completada!

Si todos los checks están ✅:

**¡Felicitaciones!** Tu aplicación ahora está actualizada a la versión profesional.

**Siguiente paso:** 
```powershell
python Inicio_Gestor.py
```

**¡Disfruta de tu nuevo gestor de contraseñas profesional!** 🚀🔐

---

**Última actualización:** 28 de Noviembre de 2025
**Versión:** 2.0 Professional Edition
