# 🚀 Guía de Inicio Rápido

## Primeros Pasos

### 1. Ejecutar la Aplicación
```powershell
cd "c:\Users\ruben\Desktop\Importante\Github\password-manager-dnie\Scripts"
python Inicio_Gestor.py
```

### 2. Primera Vista - Pantalla de Bienvenida

Al iniciar verás:
- 🔒 Icono de candado con efecto brillante
- 🎨 Título "Gestor de Contraseñas"
- ⚙️ Icono de configuración (esquina superior derecha)
- 🟢 Botón "Acceder" (verde)
- 🔴 Botón "Salir" (rojo)

#### 💡 Tip: Cambia el Tema Inmediatamente
1. Click en ⚙️ (esquina superior derecha)
2. Panel se despliega con 5 temas
3. Selecciona tu favorito:
   - **Dark** - Oscuro elegante 🌙
   - **Light** - Claro minimalista ☀️
   - **Ocean Blue** - Azul profesional 🌊
   - **Purple Night** - Morado sofisticado 💜
   - **Forest Green** - Verde relajante 🌲

### 3. Detección del DNIe

Después de hacer click en "Acceder":
- Se detecta automáticamente tu DNIe
- Barra de progreso animada
- Mensaje de confirmación

### 4. Introducir PIN

Una vez detectado el DNIe:
- Campo para introducir PIN
- Asteriscos ocultan tu PIN por seguridad
- Botón "Verificar" para continuar
- Animación de carga durante verificación

### 5. Pantalla Principal - Gestor de Contraseñas

¡Bienvenido a tu gestor! Verás:

#### Barra Superior
- 🔍 **Barra de búsqueda** (izquierda)
- ⚙️ **Configuración** (derecha)
- 📊 **Estadísticas** (derecha)
- ➕ **Nueva Contraseña** (derecha, verde)

#### Área Central
- **Tarjetas de contraseñas** con diseño elegante
- Cada tarjeta muestra:
  - 📝 Nombre de la cuenta
  - 🔐 Contraseña (oculta por defecto)
  - 📊 Barra de fortaleza (débil/media/fuerte)
  - 5 botones de acción

#### Pie de Página
- 🚪 Botón "Salir" (rojo)

---

## 🎯 Acciones Principales

### Agregar Nueva Contraseña

1. Click en **"+ Nueva Contraseña"** (botón verde, arriba a la derecha)
2. Diálogo modal aparece
3. Completa:
   - **Nombre**: Ej. "Gmail", "Facebook", "Banco"
   - **Contraseña**: Mínimo 15 caracteres
4. Opciones:
   - 🔄 Click en botón circular para **generar** contraseña segura
   - ⌨️ O escribe tu propia contraseña
5. Observa la **barra de fortaleza** en tiempo real:
   - 🔴 Rojo = Débil
   - 🟡 Amarillo = Media
   - 🟢 Verde = Fuerte
6. Click en **"Añadir"**
7. ¡Listo! Notificación de confirmación

### Buscar Contraseñas

1. Click en la barra de búsqueda superior
2. Escribe el nombre de la cuenta
3. **Resultados en tiempo real** mientras escribes
4. Para limpiar: Click en ❌ o presiona ESC

### Gestionar Contraseñas Existentes

Cada tarjeta tiene 5 botones:

#### 👁️ Mostrar/Ocultar
- Click para revelar contraseña completa
- Click nuevamente para ocultar
- Por defecto aparece como `••••••••••••`

#### 📋 Copiar
- Copia contraseña al portapapeles
- Duración: 30 segundos (por defecto)
- Notificación confirma la acción
- **Seguridad**: Se borra automáticamente después

#### ✏️ Editar
- Modifica nombre o contraseña
- Diálogo similar a "Nueva Contraseña"
- Validaciones en tiempo real

#### 🔄 Generar
- Crea una nueva contraseña segura automática
- Confirmación antes de reemplazar
- Se guarda automáticamente

#### 🗑️ Borrar
- Elimina la entrada permanentemente
- **Confirmación requerida**
- No hay deshacer

---

## 📊 Ver Estadísticas

1. Click en botón 📊 (arriba a la derecha)
2. Panel lateral se despliega
3. Información mostrada:
   - **Total**: Número de contraseñas guardadas
   - **Fortaleza Promedio**: Porcentaje y barra visual
   - **Desglose**:
     - 🔴 Contraseñas débiles
     - 🟡 Contraseñas medias
     - 🟢 Contraseñas fuertes
4. Click nuevamente para ocultar

---

## ⚙️ Configuración Completa

Click en ⚙️ para acceder a:

### Temas de Color
- 5 temas profesionales
- Cambio instantáneo
- Se guarda automáticamente

### Tamaño de Fuente (Próximamente)
- Pequeño
- Mediano (predeterminado)
- Grande

### Otras Opciones
- Animaciones (On/Off)
- Tiempo de copiado (segundos)
- Notificaciones (On/Off)
- Vista compacta (On/Off)

---

## 💡 Tips y Trucos

### Seguridad
✅ Usa el generador para contraseñas fuertes
✅ Revisa regularmente las contraseñas débiles
✅ No compartas tu PIN del DNIe
✅ Cierra la aplicación al terminar

### Productividad
⚡ Usa la búsqueda para encontrar contraseñas rápido
⚡ Copia y pega con confianza (30s de vida)
⚡ Organiza con nombres descriptivos
⚡ Genera contraseñas nuevas regularmente

### Personalización
🎨 Cambia el tema según tu preferencia
🎨 Ajusta el tamaño de fuente si es necesario
🎨 Activa/desactiva animaciones según tu hardware

---

## 🔧 Solución de Problemas

### La aplicación no inicia
```powershell
# Verifica Python
python --version

# Reinstala dependencias
pip install pygame pyperclip cryptography python-pkcs11
```

### No se detecta el DNIe
- ✓ Verifica que el DNIe esté insertado
- ✓ Comprueba que los drivers estén instalados
- ✓ Reinicia la aplicación

### PIN incorrecto
- ✓ Tienes 3 intentos
- ✓ Después el DNIe se bloqueará
- ✓ Contacta con autoridades si lo olvidas

### Las animaciones van lentas
- ✓ Ve a Configuración
- ✓ Desactiva las animaciones
- ✓ Considera usar un tema más ligero (Light)

---

## 🎯 Casos de Uso Comunes

### Caso 1: Primera Vez
```
1. Abre la aplicación
2. Cambia al tema que prefieras
3. Click "Acceder"
4. Introduce PIN
5. Click "Nueva Contraseña"
6. Agrega tus primeras cuentas
```

### Caso 2: Uso Diario
```
1. Abre la aplicación
2. Introduce PIN
3. Busca la cuenta que necesitas
4. Click "Copiar"
5. Pega en el sitio web/app
6. Cierra cuando termines
```

### Caso 3: Auditoría de Seguridad
```
1. Abre la aplicación
2. Click en estadísticas 📊
3. Revisa contraseñas débiles
4. Para cada débil:
   - Click en la tarjeta
   - Click "Generar"
   - Confirma
5. Actualiza en los sitios web
```

### Caso 4: Organización
```
1. Usa nombres claros:
   - ✅ "Gmail - Personal"
   - ✅ "Banco Santander"
   - ❌ "Cuenta 1"
2. Busca por categorías
3. Mantén actualizado
```

---

## 🎓 Mejores Prácticas

### Contraseñas
- ✅ Mínimo 15 caracteres
- ✅ Usa el generador automático
- ✅ No reutilices contraseñas
- ✅ Cambia las débiles regularmente

### Organización
- ✅ Nombres descriptivos
- ✅ Coherencia en nombres similares
- ✅ Revisa periódicamente
- ✅ Elimina cuentas obsoletas

### Seguridad
- ✅ Nunca compartas tu PIN
- ✅ No dejes la app abierta sin supervisión
- ✅ Usa la función de copiado temporal
- ✅ Cierra al terminar

---

## 📞 Soporte

### Errores Conocidos
Ninguno actualmente ✅

### Reportar Problemas
Si encuentras un error:
1. Anota qué estabas haciendo
2. Captura de pantalla si es posible
3. Mensaje de error completo
4. Contacta con los desarrolladores

---

## 🎉 ¡Disfruta tu Gestor de Contraseñas!

Ya estás listo para usar tu gestor profesional de contraseñas con DNIe.

**Características que amarás:**
- 🎨 Interfaz hermosa y moderna
- 🚀 Rápida y fluida
- 🔒 Totalmente segura
- 🎯 Fácil de usar
- ⚙️ Personalizable

**¡Protege tu vida digital con estilo!** 💪🔐
