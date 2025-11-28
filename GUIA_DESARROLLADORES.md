# 🛠️ Guía para Desarrolladores

## Arquitectura del Sistema

### Estructura Modular

```
Scripts/
├── config_manager.py        # Sistema de configuración y temas
├── ui_components.py         # Componentes UI reutilizables
├── Inicio_Gestor.py         # Pantalla principal de inicio
├── detectar_dnie_gui.py     # Detección del DNIe
├── verificar_dnie_gui.py    # Verificación del PIN
├── Interfaz_Contraseñas_Pro.py  # Gestor principal
├── Nombre_Contraseña_Pro.py     # Diálogo nueva contraseña
├── manejo_datos.py          # Lógica de datos y cifrado
└── generador_contraseñas.py # Generador de contraseñas
```

---

## 🎨 Sistema de Temas

### Cómo Funciona

El sistema de temas se basa en tres componentes:

1. **ConfigManager** - Gestiona la configuración
2. **ThemeColors** - Define paletas de colores
3. **Archivos UI** - Consumen los colores dinámicamente

### Agregar un Nuevo Tema

**Paso 1:** Edita `config_manager.py`

```python
class ThemeColors:
    # ... temas existentes ...
    
    MI_NUEVO_TEMA = {
        "name": "Mi Tema Custom",
        "bg_primary": (R, G, B),      # Fondo principal
        "bg_secondary": (R, G, B),    # Fondo secundario
        "bg_tertiary": (R, G, B),     # Fondo terciario
        "bg_hover": (R, G, B),        # Hover
        "text_primary": (R, G, B),    # Texto principal
        "text_secondary": (R, G, B),  # Texto secundario
        "text_disabled": (R, G, B),   # Texto deshabilitado
        "accent_primary": (R, G, B),  # Acento principal
        "accent_secondary": (R, G, B),# Acento hover
        "success": (R, G, B),         # Verde éxito
        "success_hover": (R, G, B),   # Verde hover
        "danger": (R, G, B),          # Rojo peligro
        "danger_hover": (R, G, B),    # Rojo hover
        "warning": (R, G, B),         # Amarillo advertencia
        "info": (R, G, B),            # Azul información
        "border": (R, G, B),          # Borde normal
        "border_light": (R, G, B),    # Borde claro
        "shadow": (R, G, B, A),       # Sombra (con alpha)
        "overlay": (R, G, B, A)       # Overlay (con alpha)
    }
```

**Paso 2:** Registra el tema

```python
class ConfigManager:
    THEMES = {
        "Dark": ThemeColors.DARK_THEME,
        "Light": ThemeColors.LIGHT_THEME,
        # ... otros temas ...
        "Mi Tema Custom": ThemeColors.MI_NUEVO_TEMA  # <- AGREGAR AQUÍ
    }
```

**Paso 3:** ¡Listo! El tema aparecerá automáticamente en la configuración.

### Guía de Colores

#### Fondos
- `bg_primary`: Fondo principal de la aplicación
- `bg_secondary`: Paneles, tarjetas, diálogos
- `bg_tertiary`: Elementos dentro de tarjetas
- `bg_hover`: Estado hover de elementos

#### Textos
- `text_primary`: Títulos, texto importante
- `text_secondary`: Subtítulos, texto secundario
- `text_disabled`: Placeholders, texto deshabilitado

#### Acentos
- `accent_primary`: Color principal de marca
- `accent_secondary`: Hover del color de marca

#### Semánticos
- `success`: Acciones positivas (guardar, confirmar)
- `danger`: Acciones destructivas (borrar, cancelar)
- `warning`: Advertencias
- `info`: Información

#### Estructura
- `border`: Bordes normales
- `border_light`: Bordes sutiles
- `shadow`: Sombras (incluir alpha channel)
- `overlay`: Overlay de diálogos (incluir alpha)

---

## 🧩 Componentes UI

### ModernButton

Botón con animaciones y efectos.

```python
from ui_components import ModernButton
from config_manager import ConfigManager

config = ConfigManager()

button = ModernButton(
    x=100,              # Posición X
    y=100,              # Posición Y
    width=120,          # Ancho
    height=45,          # Alto
    text="Mi Botón",    # Texto
    config=config,      # Configuración
    color_type="accent" # Tipo: accent, success, danger, secondary
)

# En el loop de eventos
button.check_hover(mouse_pos)
button.update(dt)

if button.handle_event(event):
    print("¡Click!")

# Dibujar
button.draw(surface, font)
```

**Tipos de color:**
- `"accent"` - Azul (acción primaria)
- `"success"` - Verde (éxito)
- `"danger"` - Rojo (peligro)
- `"secondary"` - Gris (acción secundaria)

### ModernInputBox

Campo de entrada con validación.

```python
from ui_components import ModernInputBox

input_box = ModernInputBox(
    x=100,
    y=100,
    width=300,
    height=50,
    config=config,
    placeholder="Escribe aquí...",
    password=False  # True para campos de contraseña
)

# En el loop de eventos
result = input_box.handle_event(event)
if result == "submit":
    print(f"Enter presionado: {input_box.text}")

# Actualizar y dibujar
input_box.update(dt)
input_box.draw(surface, font)

# Validación con error
if not input_box.text:
    input_box.error = True
    input_box.error_message = "Este campo es obligatorio"
```

### SearchBar

Barra de búsqueda con iconos.

```python
from ui_components import SearchBar

search = SearchBar(
    x=20,
    y=20,
    width=400,
    height=45,
    config=config
)

# En el loop de eventos
result = search.handle_event(event)
if result == "change":
    print(f"Búsqueda: {search.text}")
elif result == "clear":
    print("Búsqueda limpiada")

# Dibujar
search.draw(surface, font)
```

### ToggleSwitch

Switch On/Off animado.

```python
from ui_components import ToggleSwitch

toggle = ToggleSwitch(
    x=100,
    y=100,
    config=config,
    enabled=True  # Estado inicial
)

# En el loop de eventos
if toggle.handle_event(event, mouse_pos):
    print(f"Nuevo estado: {toggle.enabled}")

# Actualizar y dibujar
toggle.update(dt)
toggle.draw(surface)
```

### ProgressBar

Barra de progreso animada.

```python
from ui_components import ProgressBar

progress = ProgressBar(
    x=100,
    y=100,
    width=300,
    height=12,
    config=config
)

# Establecer progreso (0.0 a 1.0)
progress.set_progress(0.75)  # 75%

# Actualizar y dibujar
progress.update(dt)
progress.draw(surface)
```

---

## 🎯 Crear una Nueva Pantalla

### Template Básico

```python
import pygame
from config_manager import ConfigManager
from ui_components import ModernButton

def mi_nueva_pantalla():
    pygame.init()
    
    # Configuración
    config = ConfigManager()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mi Nueva Pantalla")
    
    # Fuentes
    font_sizes = config.get_font_sizes()
    font = pygame.font.Font(None, font_sizes["normal"])
    
    # Componentes
    btn_volver = ModernButton(
        20, HEIGHT - 70, 150, 45,
        "Volver", config, "secondary"
    )
    
    # Loop principal
    running = True
    clock = pygame.time.Clock()
    
    while running:
        dt = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if btn_volver.handle_event(event):
                running = False
        
        # Actualizar
        btn_volver.check_hover(mouse_pos)
        btn_volver.update(dt)
        
        # Dibujar
        screen.fill(config.get_color("bg_primary"))
        
        # Tu contenido aquí...
        
        btn_volver.draw(screen, font)
        
        pygame.display.flip()
    
    pygame.quit()
```

---

## 🔧 Mejores Prácticas

### 1. Siempre Usa ConfigManager

❌ **Mal:**
```python
COLOR_BG = (34, 38, 41)
screen.fill(COLOR_BG)
```

✅ **Bien:**
```python
config = ConfigManager()
screen.fill(config.get_color("bg_primary"))
```

### 2. Delta Time para Animaciones

❌ **Mal:**
```python
self.x += 5  # Depende del framerate
```

✅ **Bien:**
```python
self.x += 5 * dt * 60  # Independiente del framerate
```

### 3. Actualizar Antes de Dibujar

✅ **Correcto:**
```python
# 1. Eventos
for event in events:
    button.handle_event(event)

# 2. Actualizar
button.check_hover(mouse_pos)
button.update(dt)

# 3. Dibujar
button.draw(screen, font)
```

### 4. Usar Componentes Existentes

❌ **No reinventes la rueda:**
```python
# Crear tu propio botón desde cero
```

✅ **Usa los componentes:**
```python
from ui_components import ModernButton
```

---

## 📊 Añadir Nueva Configuración

### Paso 1: Definir en DEFAULT_CONFIG

```python
# En config_manager.py
class ConfigManager:
    DEFAULT_CONFIG = {
        # ... configs existentes ...
        "mi_nueva_opcion": True,  # <- AGREGAR AQUÍ
    }
```

### Paso 2: Usar en la Aplicación

```python
config = ConfigManager()

if config.get_value("mi_nueva_opcion"):
    # Hacer algo...
    pass

# Cambiar valor
config.set_value("mi_nueva_opcion", False)
```

### Paso 3: (Opcional) Agregar a UI de Configuración

En `Inicio_Gestor.py` o donde quieras:

```python
toggle_opcion = ToggleSwitch(
    x, y, config,
    enabled=config.get_value("mi_nueva_opcion")
)

if toggle_opcion.handle_event(event, mouse_pos):
    config.set_value("mi_nueva_opcion", toggle_opcion.enabled)
```

---

## 🐛 Debug y Testing

### Activar Modo Debug

```python
# Al inicio del archivo
DEBUG = True

if DEBUG:
    print(f"Valor: {variable}")
    # Dibujar rectángulos de debug
    pygame.draw.rect(screen, (255, 0, 0), rect, 1)
```

### Imprimir FPS

```python
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000.0
    
    if DEBUG:
        fps = clock.get_fps()
        fps_surf = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
        screen.blit(fps_surf, (10, 10))
```

### Test de Componentes Individuales

Crea archivos `test_*.py` para cada componente:

```python
# test_button.py
from ui_components import ModernButton
from config_manager import ConfigManager
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
config = ConfigManager()

button = ModernButton(150, 125, 100, 50, "Test", config)
font = pygame.font.Font(None, 24)

running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if button.handle_event(event):
            print("Click!")
    
    button.check_hover(pygame.mouse.get_pos())
    button.update(dt)
    
    screen.fill((30, 30, 30))
    button.draw(screen, font)
    pygame.display.flip()

pygame.quit()
```

---

## 📚 Recursos Adicionales

### Documentación de Pygame
https://www.pygame.org/docs/

### Paletas de Colores
- https://colorhunt.co/
- https://coolors.co/
- https://flatuicolors.com/

### Iconos y Assets
- https://fontawesome.com/
- https://icons8.com/
- https://www.flaticon.com/

---

## 🚀 Roadmap de Mejoras Futuras

### Corto Plazo
- [ ] Implementar edición completa de contraseñas
- [ ] Añadir más opciones de configuración
- [ ] Soporte para categorías de contraseñas
- [ ] Importar/Exportar contraseñas

### Medio Plazo
- [ ] Historial de contraseñas
- [ ] Generador de contraseñas con opciones
- [ ] Comprobación de contraseñas comprometidas
- [ ] Sincronización en la nube (opcional)

### Largo Plazo
- [ ] Aplicación móvil
- [ ] Extensión de navegador
- [ ] Auto-relleno de formularios
- [ ] Autenticación biométrica adicional

---

## 💡 Tips de Desarrollo

### Mantén el Código Limpio
- Usa nombres descriptivos
- Comenta código complejo
- Divide funciones largas
- Sigue PEP 8

### Testea Constantemente
- Prueba cada cambio inmediatamente
- Usa diferentes temas
- Prueba con diferentes tamaños de ventana
- Verifica en diferentes sistemas

### Mantén la Consistencia
- Usa los mismos patrones en toda la app
- Respeta la guía de estilos
- Documenta cambios importantes
- Actualiza la documentación

---

## 📞 Contacto y Soporte

Para consultas de desarrollo:
- 📧 Email: [Tu email]
- 💬 Issues: GitHub Issues
- 📖 Docs: Este archivo y MEJORAS_PROFESIONALES.md

---

**¡Feliz desarrollo! 🎉**

Recuerda: El código limpio es el mejor código.
