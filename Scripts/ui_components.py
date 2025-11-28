"""
Componentes UI Modernos y Reutilizables
Biblioteca de componentes profesionales con animaciones y efectos
"""
import pygame
import math
from typing import Tuple, Callable, Optional

def calculate_password_strength(password):
    """Calcula la fortaleza de una contraseña (0.0 a 1.0)"""
    strength = 0.0
    
    # Longitud
    if len(password) >= 15:
        strength += 0.3
    elif len(password) >= 10:
        strength += 0.2
    else:
        strength += 0.1
    
    # Complejidad
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    complexity = sum([has_lower, has_upper, has_digit, has_special])
    strength += complexity * 0.15
    
    # Variedad de caracteres
    unique_chars = len(set(password))
    if unique_chars > 10:
        strength += 0.1
    
    return min(1.0, strength)

class ModernButton:
    """Botón moderno con animaciones y efectos hover"""
    
    def __init__(self, x, y, width, height, text, config, 
                 color_type="accent", icon=None, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.config = config
        self.color_type = color_type
        self.icon = icon
        self.callback = callback
        self.is_hovered = False
        self.is_pressed = False
        self.hover_progress = 0.0
        self.ripple_effects = []
        self.enabled = True
        
    def get_colors(self):
        """Obtiene los colores según el tipo y estado"""
        if not self.enabled:
            return {
                "base": self.config.get_color("text_disabled"),
                "hover": self.config.get_color("text_disabled"),
                "text": self.config.get_color("bg_primary")
            }
        
        color_map = {
            "accent": {
                "base": self.config.get_color("accent_primary"),
                "hover": self.config.get_color("accent_secondary"),
                "text": self.config.get_color("text_primary")
            },
            "success": {
                "base": self.config.get_color("success"),
                "hover": self.config.get_color("success_hover"),
                "text": self.config.get_color("text_primary")
            },
            "danger": {
                "base": self.config.get_color("danger"),
                "hover": self.config.get_color("danger_hover"),
                "text": self.config.get_color("text_primary")
            },
            "secondary": {
                "base": self.config.get_color("bg_tertiary"),
                "hover": self.config.get_color("bg_hover"),
                "text": self.config.get_color("text_primary")
            }
        }
        return color_map.get(self.color_type, color_map["accent"])
    
    def update(self, dt):
        """Actualiza animaciones"""
        # Animación hover suave
        target = 1.0 if self.is_hovered else 0.0
        self.hover_progress += (target - self.hover_progress) * min(dt * 8, 1.0)
        
        # Actualizar ripple effects
        self.ripple_effects = [
            (x, y, radius + dt * 500, alpha - dt * 255)
            for x, y, radius, alpha in self.ripple_effects
            if alpha > 0
        ]
    
    def draw(self, surface, font):
        """Dibuja el botón con efectos"""
        colors = self.get_colors()
        
        # Interpolar color entre base y hover
        base = colors["base"]
        hover = colors["hover"]
        current_color = (
            int(base[0] + (hover[0] - base[0]) * self.hover_progress),
            int(base[1] + (hover[1] - base[1]) * self.hover_progress),
            int(base[2] + (hover[2] - base[2]) * self.hover_progress)
        )
        
        # Sombra
        if self.config.get_value("animations_enabled"):
            shadow_offset = 2 + int(self.hover_progress * 4)
            shadow_rect = self.rect.inflate(4, 4)
            shadow_rect.y += shadow_offset
            shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, self.config.get_color("shadow"), 
                           shadow_surf.get_rect(), border_radius=8)
            surface.blit(shadow_surf, shadow_rect)
        
        # Fondo del botón
        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        
        # Ripple effects
        for rx, ry, radius, alpha in self.ripple_effects:
            if alpha > 0:
                ripple_surf = pygame.Surface((int(radius * 2), int(radius * 2)), pygame.SRCALPHA)
                pygame.draw.circle(ripple_surf, (*colors["hover"], int(alpha)), 
                                 (int(radius), int(radius)), int(radius))
                surface.blit(ripple_surf, (rx - radius, ry - radius), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Texto centrado
        text_surf = font.render(self.text, True, colors["text"])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def check_hover(self, mouse_pos):
        """Verifica si el mouse está sobre el botón"""
        if self.enabled:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_event(self, event):
        """Maneja eventos del mouse"""
        if not self.enabled:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_pressed = True
                # Agregar efecto ripple
                self.ripple_effects.append((*event.pos, 0, 200))
                if self.callback:
                    self.callback()
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False
        return False

class ModernInputBox:
    """Campo de entrada moderno con animaciones"""
    
    def __init__(self, x, y, width, height, config, placeholder="", password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.config = config
        self.text = ""
        self.placeholder = placeholder
        self.password = password
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.focus_progress = 0.0
        self.error = False
        self.error_message = ""
        
    def update(self, dt):
        """Actualiza animaciones"""
        # Cursor parpadeante
        self.cursor_timer += dt
        if self.cursor_timer >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
        
        # Animación de foco
        target = 1.0 if self.active else 0.0
        self.focus_progress += (target - self.focus_progress) * min(dt * 8, 1.0)
    
    def draw(self, surface, font):
        """Dibuja el input con efectos"""
        # Color del borde según estado
        if self.error:
            border_color = self.config.get_color("danger")
        elif self.active:
            border_color = self.config.get_color("accent_primary")
        else:
            border_color = self.config.get_color("border")
        
        # Interpolar grosor del borde
        border_width = int(2 + self.focus_progress * 2)
        
        # Fondo
        pygame.draw.rect(surface, self.config.get_color("bg_secondary"), 
                        self.rect, border_radius=6)
        
        # Borde
        pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=6)
        
        # Texto o placeholder
        display_text = self.text if not self.password else "•" * len(self.text)
        if not display_text and not self.active:
            text_surf = font.render(self.placeholder, True, 
                                   self.config.get_color("text_disabled"))
        else:
            text_surf = font.render(display_text, True, 
                                   self.config.get_color("text_primary"))
        
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 15, self.rect.centery))
        
        # Clip para no salir del rectángulo
        clip_rect = self.rect.inflate(-20, -10)
        surface.set_clip(clip_rect)
        surface.blit(text_surf, text_rect)
        
        # Cursor
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            cursor_y = self.rect.centery - 10
            pygame.draw.line(surface, self.config.get_color("text_primary"),
                           (cursor_x, cursor_y), (cursor_x, cursor_y + 20), 2)
        
        surface.set_clip(None)
        
        # Mensaje de error
        if self.error and self.error_message:
            error_font = pygame.font.Font(None, self.config.get_font_sizes()["small"])
            error_surf = error_font.render(self.error_message, True, 
                                          self.config.get_color("danger"))
            surface.blit(error_surf, (self.rect.x, self.rect.bottom + 5))
    
    def handle_event(self, event):
        """Maneja eventos de teclado y mouse"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.cursor_visible = True
            self.cursor_timer = 0
            
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.error = False
            elif event.key == pygame.K_RETURN:
                return "submit"
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Pegar desde portapapeles
                try:
                    import pyperclip
                    self.text += pyperclip.paste()
                except:
                    pass
            else:
                # Limitar longitud
                if len(self.text) < 100:
                    self.text += event.unicode
                    self.error = False
        return None

class SearchBar:
    """Barra de búsqueda moderna con iconos"""
    
    def __init__(self, x, y, width, height, config):
        self.rect = pygame.Rect(x, y, width, height)
        self.config = config
        self.text = ""
        self.active = False
        self.placeholder = "Buscar contraseñas..."
        
    def draw(self, surface, font):
        """Dibuja la barra de búsqueda"""
        # Fondo
        bg_color = self.config.get_color("bg_tertiary")
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=20)
        
        # Borde si está activo
        if self.active:
            pygame.draw.rect(surface, self.config.get_color("accent_primary"), 
                           self.rect, 2, border_radius=20)
        
        # Icono de búsqueda
        icon_x = self.rect.x + 15
        icon_y = self.rect.centery
        draw_search_icon(surface, icon_x, icon_y, 
                        self.config.get_color("text_secondary"))
        
        # Texto o placeholder
        text_x = self.rect.x + 45
        if self.text:
            text_surf = font.render(self.text, True, 
                                   self.config.get_color("text_primary"))
        else:
            text_surf = font.render(self.placeholder, True, 
                                   self.config.get_color("text_disabled"))
        
        text_rect = text_surf.get_rect(midleft=(text_x, self.rect.centery))
        surface.blit(text_surf, text_rect)
        
        # Botón limpiar si hay texto
        if self.text:
            clear_x = self.rect.right - 30
            clear_y = self.rect.centery
            pygame.draw.circle(surface, self.config.get_color("text_disabled"),
                             (clear_x, clear_y), 8)
            pygame.draw.line(surface, self.config.get_color("bg_tertiary"),
                           (clear_x - 4, clear_y - 4), (clear_x + 4, clear_y + 4), 2)
            pygame.draw.line(surface, self.config.get_color("bg_tertiary"),
                           (clear_x - 4, clear_y + 4), (clear_x + 4, clear_y - 4), 2)
    
    def handle_event(self, event):
        """Maneja eventos"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            # Click en el botón limpiar
            if self.text and self.active:
                clear_rect = pygame.Rect(self.rect.right - 40, 
                                        self.rect.y, 40, self.rect.height)
                if clear_rect.collidepoint(event.pos):
                    self.text = ""
                    return "clear"
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return "change"
            elif event.key == pygame.K_ESCAPE:
                self.text = ""
                self.active = False
                return "clear"
            elif len(event.unicode) > 0 and event.unicode.isprintable():
                self.text += event.unicode
                return "change"
        return None

class ToggleSwitch:
    """Switch toggle animado"""
    
    def __init__(self, x, y, config, enabled=True):
        self.rect = pygame.Rect(x, y, 50, 26)
        self.config = config
        self.enabled = enabled
        self.progress = 1.0 if enabled else 0.0
        self.is_hovered = False
        
    def update(self, dt):
        """Actualiza animación"""
        target = 1.0 if self.enabled else 0.0
        self.progress += (target - self.progress) * min(dt * 10, 1.0)
    
    def draw(self, surface):
        """Dibuja el switch"""
        # Fondo
        bg_color = self.config.get_color("success") if self.enabled else self.config.get_color("bg_hover")
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=13)
        
        # Circle animado
        circle_x = int(self.rect.x + 13 + (self.rect.width - 26) * self.progress)
        circle_y = self.rect.centery
        circle_color = self.config.get_color("text_primary")
        
        # Efecto hover
        radius = 11 if self.is_hovered else 10
        pygame.draw.circle(surface, circle_color, (circle_x, circle_y), radius)
    
    def handle_event(self, event, mouse_pos):
        """Maneja eventos"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.enabled = not self.enabled
                return True
        return False

class ProgressBar:
    """Barra de progreso animada"""
    
    def __init__(self, x, y, width, height, config):
        self.rect = pygame.Rect(x, y, width, height)
        self.config = config
        self.progress = 0.0
        self.target_progress = 0.0
        
    def set_progress(self, value):
        """Establece el progreso objetivo (0.0 a 1.0)"""
        self.target_progress = max(0.0, min(1.0, value))
    
    def update(self, dt):
        """Actualiza animación"""
        self.progress += (self.target_progress - self.progress) * min(dt * 5, 1.0)
    
    def draw(self, surface):
        """Dibuja la barra de progreso"""
        # Fondo
        pygame.draw.rect(surface, self.config.get_color("bg_tertiary"), 
                        self.rect, border_radius=self.rect.height // 2)
        
        # Progreso
        if self.progress > 0:
            progress_rect = pygame.Rect(
                self.rect.x, self.rect.y,
                int(self.rect.width * self.progress), self.rect.height
            )
            
            # Color según el progreso
            if self.progress < 0.33:
                color = self.config.get_color("danger")
            elif self.progress < 0.66:
                color = self.config.get_color("warning")
            else:
                color = self.config.get_color("success")
            
            pygame.draw.rect(surface, color, progress_rect, 
                           border_radius=self.rect.height // 2)

# Funciones auxiliares para dibujar iconos
def draw_search_icon(surface, x, y, color):
    """Dibuja icono de búsqueda"""
    pygame.draw.circle(surface, color, (x, y), 7, 2)
    pygame.draw.line(surface, color, (x + 5, y + 5), (x + 10, y + 10), 2)

def draw_settings_icon(surface, x, y, color, size=20):
    """Dibuja icono de configuración (engranaje)"""
    center = (x, y)
    outer_radius = size // 2
    inner_radius = size // 4
    teeth = 8
    
    for i in range(teeth):
        angle1 = (i / teeth) * 2 * math.pi
        angle2 = ((i + 0.5) / teeth) * 2 * math.pi
        
        x1 = center[0] + math.cos(angle1) * outer_radius
        y1 = center[1] + math.sin(angle1) * outer_radius
        x2 = center[0] + math.cos(angle2) * outer_radius
        y2 = center[1] + math.sin(angle2) * outer_radius
        
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), 2)
    
    pygame.draw.circle(surface, color, center, inner_radius, 2)

def draw_stats_icon(surface, x, y, color, size=20):
    """Dibuja icono de estadísticas (gráfico de barras)"""
    bar_width = size // 5
    heights = [size * 0.4, size * 0.7, size * 0.5, size * 0.9]
    
    for i, height in enumerate(heights):
        bar_x = x - size//2 + i * (bar_width + 2)
        bar_y = y + size//2 - height
        pygame.draw.rect(surface, color, (bar_x, bar_y, bar_width, height), border_radius=2)

def draw_lock_icon(surface, x, y, color, size=20):
    """Dibuja icono de candado"""
    # Cuerpo
    body_rect = pygame.Rect(x - size//3, y, size*2//3, size//2)
    pygame.draw.rect(surface, color, body_rect, 2, border_radius=3)
    
    # Arco
    arc_rect = pygame.Rect(x - size//4, y - size//3, size//2, size//2)
    pygame.draw.arc(surface, color, arc_rect, 0, math.pi, 2)

class Slider:
    """Control deslizante para valores numéricos con animaciones"""
    
    def __init__(self, x, y, width, min_val, max_val, initial_val, config, step=1):
        self.rect = pygame.Rect(x, y, width, 30)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.step = step
        self.config = config
        self.is_dragging = False
        self.is_hovered = False
        self.hover_progress = 0.0
        
        # Calcular posición inicial del handle
        self.handle_radius = 12
        self.track_height = 6
        self.track_y = self.rect.y + self.rect.height // 2
        self.update_handle_position()
    
    def update_handle_position(self):
        """Actualiza la posición del handle basado en el valor"""
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = self.rect.x + ratio * self.rect.width
    
    def get_value_from_position(self, mouse_x):
        """Calcula el valor basado en la posición del mouse"""
        ratio = (mouse_x - self.rect.x) / self.rect.width
        ratio = max(0.0, min(1.0, ratio))
        raw_value = self.min_val + ratio * (self.max_val - self.min_val)
        # Redondear al step más cercano
        stepped_value = round(raw_value / self.step) * self.step
        return max(self.min_val, min(self.max_val, stepped_value))
    
    def handle_event(self, event):
        """Maneja eventos del mouse"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_rect = pygame.Rect(
                self.handle_x - self.handle_radius,
                self.track_y - self.handle_radius,
                self.handle_radius * 2,
                self.handle_radius * 2
            )
            if handle_rect.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self.value = self.get_value_from_position(event.pos[0])
                self.update_handle_position()
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                return True
        
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.value = self.get_value_from_position(event.pos[0])
                self.update_handle_position()
                return True
        
        return False
    
    def check_hover(self, mouse_pos):
        """Verifica si el mouse está sobre el control"""
        handle_rect = pygame.Rect(
            self.handle_x - self.handle_radius,
            self.track_y - self.handle_radius,
            self.handle_radius * 2,
            self.handle_radius * 2
        )
        self.is_hovered = handle_rect.collidepoint(mouse_pos) or self.rect.collidepoint(mouse_pos)
    
    def update(self, dt):
        """Actualiza animaciones"""
        target = 1.0 if (self.is_hovered or self.is_dragging) else 0.0
        self.hover_progress += (target - self.hover_progress) * min(dt * 10, 1.0)
    
    def draw(self, surface, font):
        """Dibuja el slider"""
        # Track (línea de fondo)
        track_rect = pygame.Rect(
            self.rect.x, 
            self.track_y - self.track_height // 2,
            self.rect.width,
            self.track_height
        )
        pygame.draw.rect(surface, self.config.get_color("border"),
                        track_rect, border_radius=3)
        
        # Track relleno (parte activa)
        if self.handle_x > self.rect.x:
            filled_width = self.handle_x - self.rect.x
            filled_rect = pygame.Rect(
                self.rect.x,
                self.track_y - self.track_height // 2,
                filled_width,
                self.track_height
            )
            pygame.draw.rect(surface, self.config.get_color("accent_primary"),
                           filled_rect, border_radius=3)
        
        # Handle (círculo)
        handle_radius = self.handle_radius + int(self.hover_progress * 3)
        
        # Sombra del handle
        shadow_offset = 2
        pygame.draw.circle(surface, (*self.config.get_color("shadow")[:3], 100),
                         (int(self.handle_x) + shadow_offset, 
                          int(self.track_y) + shadow_offset),
                         handle_radius)
        
        # Handle principal
        pygame.draw.circle(surface, self.config.get_color("bg_secondary"),
                         (int(self.handle_x), int(self.track_y)),
                         handle_radius)
        
        # Borde del handle
        border_color = self.config.get_color("accent_primary") if self.is_hovered or self.is_dragging else self.config.get_color("border")
        pygame.draw.circle(surface, border_color,
                         (int(self.handle_x), int(self.track_y)),
                         handle_radius, 3)

class Dropdown:
    """Menú desplegable moderno"""
    
    def __init__(self, x, y, width, height, options, initial_value, config):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options  # Lista de tuplas (valor, etiqueta)
        self.selected_value = initial_value
        self.config = config
        self.is_open = False
        self.is_hovered = False
        self.hover_progress = 0.0
        self.hovered_option = None
        
    def get_selected_label(self):
        """Obtiene la etiqueta del valor seleccionado"""
        for value, label in self.options:
            if value == self.selected_value:
                return label
        return str(self.selected_value)
    
    def handle_event(self, event):
        """Maneja eventos"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
                return True
            elif self.is_open:
                # Verificar si se hizo clic en una opción
                for i, (value, label) in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.bottom + i * 40,
                        self.rect.width,
                        40
                    )
                    if option_rect.collidepoint(event.pos):
                        self.selected_value = value
                        self.is_open = False
                        return True
                # Clic fuera del menú
                self.is_open = False
        
        return False
    
    def check_hover(self, mouse_pos):
        """Verifica hover"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_open:
            self.hovered_option = None
            for i, (value, label) in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.bottom + i * 40,
                    self.rect.width,
                    40
                )
                if option_rect.collidepoint(mouse_pos):
                    self.hovered_option = i
                    break
    
    def update(self, dt):
        """Actualiza animaciones"""
        target = 1.0 if self.is_hovered else 0.0
        self.hover_progress += (target - self.hover_progress) * min(dt * 8, 1.0)
    
    def draw(self, surface, font):
        """Dibuja el dropdown"""
        # Botón principal
        bg_color = self.config.get_color("bg_tertiary") if self.is_hovered else self.config.get_color("bg_secondary")
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, self.config.get_color("border"), self.rect, 2, border_radius=8)
        
        # Texto seleccionado
        label = self.get_selected_label()
        text_surf = font.render(label, True, self.config.get_color("text_primary"))
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 15, self.rect.centery))
        surface.blit(text_surf, text_rect)
        
        # Flecha
        arrow_x = self.rect.right - 20
        arrow_y = self.rect.centery
        arrow_size = 6
        arrow_points = [
            (arrow_x, arrow_y - arrow_size // 2),
            (arrow_x + arrow_size, arrow_y - arrow_size // 2),
            (arrow_x + arrow_size // 2, arrow_y + arrow_size // 2)
        ]
        pygame.draw.polygon(surface, self.config.get_color("text_secondary"), arrow_points)
        
        # Menú desplegable
        if self.is_open:
            menu_height = len(self.options) * 40
            menu_rect = pygame.Rect(self.rect.x, self.rect.bottom + 5, self.rect.width, menu_height)
            
            # Sombra
            shadow_rect = menu_rect.inflate(6, 6)
            shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, self.config.get_color("shadow"),
                           shadow_surf.get_rect(), border_radius=8)
            surface.blit(shadow_surf, shadow_rect)
            
            # Fondo del menú
            pygame.draw.rect(surface, self.config.get_color("bg_secondary"),
                           menu_rect, border_radius=8)
            pygame.draw.rect(surface, self.config.get_color("border"),
                           menu_rect, 2, border_radius=8)
            
            # Opciones
            for i, (value, label) in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.bottom + 5 + i * 40,
                    self.rect.width,
                    40
                )
                
                # Highlight si está hovered
                if self.hovered_option == i:
                    pygame.draw.rect(surface, self.config.get_color("bg_hover"),
                                   option_rect, border_radius=6)
                
                # Marca de selección
                if value == self.selected_value:
                    check_x = option_rect.x + 10
                    check_y = option_rect.centery
                    pygame.draw.circle(surface, self.config.get_color("accent_primary"),
                                     (check_x, check_y), 4)
                
                # Texto
                option_surf = font.render(label, True, self.config.get_color("text_primary"))
                option_text_rect = option_surf.get_rect(midleft=(option_rect.x + 25, option_rect.centery))
                surface.blit(option_surf, option_text_rect)
