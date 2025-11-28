# 🔐 Gestor de Contraseñas DNIe - Professional Edition

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-production--ready-success.svg)

**Un gestor de contraseñas profesional y seguro que utiliza el DNI electrónico español (DNIe) para autenticación**

[🚀 Inicio Rápido](#-inicio-rápido) • [📖 Documentación](#-documentación) • [✨ Características](#-características) • [🎨 Capturas](#-capturas)

</div>

---

## 🌟 Novedades - Versión 2.0 Professional

La aplicación ha sido **completamente renovada** con un diseño profesional y características premium:

- 🎨 **5 Temas Profesionales** - Dark, Light, Ocean Blue, Purple Night, Forest Green
- 🔍 **Búsqueda en Tiempo Real** - Encuentra contraseñas al instante
- 📊 **Dashboard de Estadísticas** - Analiza la fortaleza de tus contraseñas
- ⚙️ **Panel de Configuración** - Personaliza completamente la aplicación
- 💫 **Animaciones Fluidas** - 60 FPS, transiciones suaves
- 🎯 **Componentes Modernos** - Interfaz de nivel comercial
- 📱 **Diseño Responsive** - Se adapta al tamaño de ventana

> 💡 **Ver todas las mejoras:** [MEJORAS_PROFESIONALES.md](MEJORAS_PROFESIONALES.md)

---

## 🎯 Descripción

Un gestor de contraseñas de escritorio seguro que utiliza las capacidades criptográficas del DNI electrónico español para el cifrado y acceso a los datos. Desarrollado en Python con una interfaz gráfica profesional creada con Pygame.

---

## ✨ Características

### 🔐 Seguridad de Nivel Gubernamental

- **Autenticación DNIe** - Utiliza el DNI electrónico español como factor de autenticación
- **Cifrado AES-256 GCM** - Base de datos completamente cifrada con el algoritmo más seguro
- **Firma Digital** - Cada operación firmada con la clave privada del DNIe
- **Base de Datos Anónima** - Archivos identificados por hash, sin datos personales
- **Sin Cloud** - Todo se almacena localmente, tú controlas tus datos

### 🎨 Interfaz Profesional

- **5 Temas Personalizables** - Desde claro minimalista hasta oscuro elegante
- **Animaciones Fluidas** - 60 FPS constantes, transiciones suaves
- **Diseño Moderno** - Tarjetas elegantes, botones con efectos, sombras dinámicas
- **Responsive** - Se adapta perfectamente a cualquier tamaño de pantalla
- **Intuitive UX** - Diseñada para ser amigable y fácil de usar

### 📊 Gestión Avanzada

- **Búsqueda Instantánea** - Encuentra cualquier contraseña en milisegundos
- **Indicador de Fortaleza** - Analiza la seguridad de cada contraseña en tiempo real
- **Dashboard de Estadísticas** - Métricas sobre tus contraseñas (débiles, medias, fuertes)
- **Generador Automático** - Crea contraseñas seguras de 15-25 caracteres
- **Copiado Temporal** - Portapapeles seguro con auto-limpieza (configurable)

### ⚙️ Personalización Total

- **Configuración Completa** - Ajusta cada aspecto de la aplicación
- **Temas Dinámicos** - Cambia el aspecto sin reiniciar
- **Tamaños de Fuente** - Pequeño, mediano o grande
- **Control de Animaciones** - Activa/desactiva según tu preferencia
- **Persistencia** - Todas tus preferencias se guardan automáticamente

---

## 🔒 Arquitectura de Seguridad

### Cómo Funciona

La seguridad se basa en un sistema de múltiples capas utilizando el DNIe como factor de autenticación:

```
1. Usuario inserta DNIe → 2. Introduce PIN → 3. DNIe firma desafío (C)
                                                          ↓
4. Genera S (firma digital) → 5. Deriva K (SHA-256) → 6. Descifra K_db
                                                          ↓
7. Accede a Base de Datos cifrada (AES-256 GCM)
```

### Flujo Detallado

1. **Desafío (C)** - Número aleatorio de 64 bits único por instalación
2. **Firma Digital (S)** - DNIe firma C con su clave privada
3. **Clave de Cifrado (K)** - SHA-256 de la firma S
4. **Clave Maestra (K_db)** - Descifrada usando K
5. **Base de Datos** - Cifrada con K_db usando AES-256 GCM

### Ventajas

- ✅ **Doble Factor**: DNIe físico + PIN
- ✅ **No Almacena Claves**: Se regeneran en cada sesión
- ✅ **Único por Usuario**: Cada DNIe genera claves diferentes
- ✅ **Imposible Replicar**: Sin el DNIe físico no hay acceso
- ✅ **Cumple GDPR**: Datos locales, control total del usuario

---

## 🚀 Inicio Rápido

### Requisitos Previos

- **Python 3.8+** - [Descargar](https://www.python.org/downloads/)
- **DNIe español** con lector o puerto USB
- **Drivers OpenSC** - [Descargar](https://github.com/OpenSC/OpenSC/releases)
- **Windows 10/11** (recomendado)

### Instalación

1. **Clona el repositorio**
```bash
git clone https://github.com/RubenSanzManovel/password-manager-dnie.git
cd password-manager-dnie
```

2. **Instala las dependencias**
```powershell
pip install pygame pyperclip cryptography python-pkcs11
```

3. **Verifica la instalación**
```powershell
cd Scripts
python test_instalacion.py
```

Deberías ver: `✅ ¡TODO LISTO PARA USAR!`

4. **Ejecuta la aplicación**
```powershell
python Inicio_Gestor.py
```

### Primera Configuración

1. La aplicación detectará tu DNIe automáticamente
2. Introduce tu PIN (tienes 3 intentos)
3. ¡Listo! Empieza a guardar contraseñas de forma segura

> 📖 **Guía completa:** [GUIA_INICIO_RAPIDO.md](GUIA_INICIO_RAPIDO.md)

---

## 📖 Documentación

### Para Usuarios

- 📘 **[Guía de Inicio Rápido](GUIA_INICIO_RAPIDO.md)** - Aprende a usar la aplicación
- ✨ **[Mejoras Profesionales](MEJORAS_PROFESIONALES.md)** - Todas las características nuevas
- 🔄 **[Instrucciones de Actualización](INSTRUCCIONES_ACTUALIZACION.md)** - Cómo actualizar
- 📊 **[Resumen Ejecutivo](RESUMEN_EJECUTIVO.md)** - Visión general del proyecto

### Para Desarrolladores

- 🛠️ **[Guía para Desarrolladores](GUIA_DESARROLLADORES.md)** - Arquitectura y componentes
- 🎨 **Sistema de Temas** - Cómo crear y personalizar temas
- 🧩 **Componentes UI** - Biblioteca de componentes reutilizables
- 📝 **API Documentation** - Documentación técnica completa

---

## 🎨 Capturas de Pantalla

### Pantalla de Inicio
<details>
<summary>Ver captura</summary>

- Animaciones de entrada suaves
- Icono de candado con efecto brillante
- Botones modernos con hover
- Acceso al panel de configuración

</details>

### Gestor Principal
<details>
<summary>Ver captura</summary>

- Diseño de tarjetas elegante
- Barra de búsqueda instantánea
- Panel de estadísticas lateral
- Indicadores de fortaleza
- Botones de acción rápida

</details>

### Panel de Configuración
<details>
<summary>Ver captura</summary>

- 5 temas profesionales
- Opciones de personalización
- Cambio en tiempo real
- Interfaz intuitiva

</details>

---

## 🎯 Casos de Uso

### 👤 Usuario Personal
- Gestiona contraseñas de redes sociales, email, bancos
- Genera contraseñas seguras automáticamente
- Organiza con nombres descriptivos
- Analiza seguridad de contraseñas existentes

### 💼 Profesional
- Múltiples cuentas corporativas
- Contraseñas de alta seguridad
- Auditorías periódicas
- Cumplimiento de políticas de seguridad

### 🏢 Pequeña Empresa
- Gestión de credenciales de equipo
- Almacenamiento local seguro
- Sin dependencias cloud
- Control total de datos

---

## 🔧 Requisitos Técnicos

### Dependencias de Python
```bash
pygame>=2.0.0          # Interfaz gráfica
pyperclip>=1.8.0       # Gestión del portapapeles
cryptography>=3.4.0    # Cifrado AES-256 GCM
python-pkcs11>=0.7.0   # Comunicación con DNIe
```

**Instalación:**
```bash
pip install pygame pyperclip cryptography python-pkcs11
```

### Software Adicional

**Drivers DNIe** (Obligatorio)
- Descarga: [Web oficial CNP](https://www.dnielectronico.es/portaldnie/)
- Incluye: OpenSC PKCS#11 library
- Ubicación Windows: `C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll`

**Lector de Tarjetas**
- Compatible con DNIe 3.0 y 4.0
- USB o integrado en portátil
- Drivers instalados y funcionando

---

## 📁 Estructura del Proyecto

```
password-manager-dnie/
├── Scripts/
│   ├── config_manager.py           # Sistema de configuración y temas
│   ├── ui_components.py            # Componentes UI reutilizables
│   ├── Inicio_Gestor.py            # Pantalla de inicio
│   ├── detectar_dnie_gui.py        # Detección del DNIe
│   ├── verificar_dnie_gui.py       # Verificación de PIN
│   ├── Interfaz_Contraseñas_Pro.py # Gestor principal (v2.0)
│   ├── Nombre_Contraseña_Pro.py    # Diálogo de nueva contraseña (v2.0)
│   ├── manejo_datos.py             # Lógica de cifrado y datos
│   ├── generador_contraseñas.py    # Generador de contraseñas
│   └── test_instalacion.py         # Script de verificación
├── MEJORAS_PROFESIONALES.md        # Documentación completa de mejoras
├── GUIA_INICIO_RAPIDO.md          # Guía para usuarios
├── GUIA_DESARROLLADORES.md        # Guía técnica
├── RESUMEN_EJECUTIVO.md           # Visión general del proyecto
└── README.md                       # Este archivo
```

### Archivos Principales

| Archivo | Descripción | Versión |
|---------|-------------|---------|
| `config_manager.py` | Gestión de temas y configuración | 2.0 |
| `ui_components.py` | Componentes UI modernos | 2.0 |
| `Interfaz_Contraseñas_Pro.py` | Gestor de contraseñas principal | 2.0 |
| `manejo_datos.py` | Lógica de seguridad y cifrado | 1.0 |
| `Inicio_Gestor.py` | Pantalla de inicio | 2.0 |

---

## 👥 Autores

**Desarrollo Original:**
- Enrique Landa
- Rubén Sanz Manovel

**Professional Edition (v2.0):**
- Diseño UI/UX moderno
- Sistema de temas
- Componentes reutilizables
- Documentación completa

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si quieres mejorar este proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Áreas de Contribución

- 🎨 Nuevos temas de color
- 🌐 Traducciones (internacionalización)
- 📱 Versión móvil
- ☁️ Sincronización cloud (opcional)
- 🔌 Extensión de navegador
- 🐛 Corrección de bugs
- 📚 Mejoras en documentación

---

## 🐛 Reportar Problemas

Si encuentras un bug o tienes una sugerencia:

1. Verifica que no exista ya en [Issues](https://github.com/RubenSanzManovel/password-manager-dnie/issues)
2. Crea un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs actual
   - Screenshots si aplica
   - Versión de Python y OS

---

## ⭐ Star History

Si este proyecto te ha sido útil, ¡considera darle una estrella! ⭐

---

## 📞 Contacto y Soporte

- 📧 Email: [rubensanzmanovel@gmail.com]
- 💬 GitHub Issues: [Reportar problema](https://github.com/RubenSanzManovel/password-manager-dnie/issues)
- 📖 Documentación: Ver archivos .md en el repositorio

---

## 🎉 Agradecimientos

- Al equipo de OpenSC por la librería PKCS#11
- A la comunidad de Python y Pygame
- A todos los contribuidores y usuarios

---

<div align="center">

**Desarrollado con ❤️ en España** 🇪🇸

**Seguridad • Privacidad • Control**

[⬆ Volver arriba](#-gestor-de-contraseñas-dnie---professional-edition)

</div>

