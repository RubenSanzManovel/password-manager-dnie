"""
Interfaz Principal del Gestor de Contraseñas - Versión Profesional
Incluye búsqueda, filtros, estadísticas y diseño moderno
"""
import pygame
import sys
import pyperclip
import threading
import time
import math
from datetime import datetime
import password_dialog as Nombre_Contraseña
import password_generator as gc
from config_manager import ConfigManager
from ui_components import (ModernButton, ModernInputBox, SearchBar, 
                           ToggleSwitch, ProgressBar, Slider, Dropdown,
                           draw_stats_icon, draw_settings_icon, draw_lock_icon,
                           calculate_password_strength)

def copy_password_temporal(password, duration=30):
    """Copia la contraseña temporalmente en el portapapeles"""
    pyperclip.copy(password)
    def clear_clipboard():
        time.sleep(duration)
        if pyperclip.paste() == password:
            pyperclip.copy("")
    threading.Thread(target=clear_clipboard, daemon=True).start()

class PasswordCard:
    """Tarjeta de contraseña con diseño moderno"""
    
    def __init__(self, entry, y_pos, width, config, is_shown=False, show_timer=0):
        self.entry = entry
        self.rect = pygame.Rect(20, y_pos, width - 40, 100)
        self.config = config
        self.is_hovered = False
        self.is_shown = is_shown
        self.show_timer = show_timer  # Tiempo restante para ocultar automáticamente
        self.hover_progress = 0.0
        self.expand_progress = 0.0
        self.buttons = {}
        self.create_buttons()
        
    def create_buttons(self):
        """Crea los botones de acción"""
        btn_width = 80
        btn_height = 32
        btn_y = self.rect.y + self.rect.height - btn_height - 15
        btn_x = self.rect.right - 450
        
        self.buttons = {
            "show": ModernButton(btn_x, btn_y, btn_width, btn_height, 
                               "Mostrar", self.config, "accent"),
            "copy": ModernButton(btn_x + 90, btn_y, btn_width, btn_height, 
                               "Copiar", self.config, "secondary"),
            "edit": ModernButton(btn_x + 180, btn_y, btn_width, btn_height, 
                               "Editar", self.config, "secondary"),
            "gen": ModernButton(btn_x + 270, btn_y, btn_width, btn_height, 
                              "Generar", self.config, "accent"),
            "del": ModernButton(btn_x + 360, btn_y, btn_width, btn_height, 
                              "Borrar", self.config, "danger")
        }
    
    def update(self, dt, mouse_pos, scroll_offset):
        """Actualiza animaciones y temporizador"""
        # Hover
        adjusted_mouse = (mouse_pos[0], mouse_pos[1] + scroll_offset)
        self.is_hovered = self.rect.collidepoint(adjusted_mouse)
        
        target = 1.0 if self.is_hovered else 0.0
        self.hover_progress += (target - self.hover_progress) * min(dt * 8, 1.0)
        
        # Auto-ocultar contraseña después del tiempo configurado
        if self.is_shown and self.show_timer > 0:
            self.show_timer -= dt
            if self.show_timer <= 0:
                self.is_shown = False
                self.show_timer = 0
        
        # Actualizar texto del botón mostrar
        if self.is_shown:
            remaining = int(self.show_timer) if self.show_timer > 0 else 0
            self.buttons["show"].text = f"Ocultar ({remaining}s)" if remaining > 0 else "Ocultar"
        else:
            self.buttons["show"].text = "Mostrar"
        
        # Actualizar botones
        for button in self.buttons.values():
            button.update(dt)
            # Ajustar posición del mouse para los botones
            button_mouse = (mouse_pos[0], adjusted_mouse[1])
            button.check_hover(button_mouse)
    
    def draw(self, surface, fonts):
        """Dibuja la tarjeta"""
        # Sombra con efecto hover
        shadow_offset = 3 + int(self.hover_progress * 3)
        shadow_rect = self.rect.inflate(6, 6)
        shadow_rect.y += shadow_offset
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_alpha = 80 + int(self.hover_progress * 40)
        pygame.draw.rect(shadow_surf, (*self.config.get_color("shadow")[:3], shadow_alpha),
                        shadow_surf.get_rect(), border_radius=12)
        surface.blit(shadow_surf, shadow_rect)
        
        # Fondo de la tarjeta
        bg_color = self.config.get_color("bg_secondary")
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=12)
        
        # Borde con efecto hover
        border_color = self.config.get_color("accent_primary") if self.is_hovered else self.config.get_color("border")
        border_width = 2 if self.is_hovered else 1
        pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=12)
        
        # Nombre de la entrada
        name_surf = fonts["normal"].render(self.entry["nombre"], True, 
                                          self.config.get_color("text_primary"))
        surface.blit(name_surf, (self.rect.x + 20, self.rect.y + 15))
        
        # Contraseña
        pass_text = self.entry["contrasena"] if self.is_shown else "•" * 12
        pass_surf = fonts["small"].render(pass_text, True, 
                                         self.config.get_color("text_secondary"))
        surface.blit(pass_surf, (self.rect.x + 20, self.rect.y + 45))
        
        # Barra de fortaleza
        if self.config.get_value("show_password_strength"):
            strength = calculate_password_strength(self.entry["contrasena"])
            progress_bar = ProgressBar(self.rect.x + 20, self.rect.y + 75, 200, 8, self.config)
            progress_bar.set_progress(strength)
            progress_bar.progress = strength  # Set directo para no animar
            progress_bar.draw(surface)
            
            # Etiqueta de fortaleza
            if strength < 0.4:
                strength_text = "Débil"
                strength_color = self.config.get_color("danger")
            elif strength < 0.7:
                strength_text = "Media"
                strength_color = self.config.get_color("warning")
            else:
                strength_text = "Fuerte"
                strength_color = self.config.get_color("success")
            
            strength_surf = fonts["small"].render(strength_text, True, strength_color)
            surface.blit(strength_surf, (self.rect.x + 230, self.rect.y + 72))
        
        # Botones
        for button in self.buttons.values():
            button.draw(surface, fonts["small"])
    
    def handle_event(self, event, scroll_offset):
        """Maneja eventos de la tarjeta"""
        # Ajustar posición del evento para el scroll
        if event.type == pygame.MOUSEBUTTONDOWN:
            adjusted_event_pos = (event.pos[0], event.pos[1] + scroll_offset)
            
            for key, button in self.buttons.items():
                # Crear evento temporal con posición ajustada
                temp_event = type('Event', (), {
                    'type': event.type,
                    'button': event.button,
                    'pos': adjusted_event_pos
                })()
                
                if button.handle_event(temp_event):
                    return key
        return None

class ModernConfirmDialog:
    """Diálogo de confirmación moderno"""
    
    def __init__(self, text, config, screen, action_type=None, entry_name=None):
        self.text = text
        self.config = config
        self.screen = screen
        self.result = None
        self.active = True
        self.alpha = 0
        self.action_type = action_type  # "delete" o "generate"
        self.entry_name = entry_name
        
        self.box_rect = pygame.Rect(0, 0, 500, 200)
        self.box_rect.center = screen.get_rect().center
        
        btn_width = 120
        btn_y = self.box_rect.bottom - 60
        spacing = 20
        
        self.yes_button = ModernButton(
            self.box_rect.centerx - btn_width - spacing // 2, btn_y,
            btn_width, 45, "Sí", config, "success"
        )
        self.no_button = ModernButton(
            self.box_rect.centerx + spacing // 2, btn_y,
            btn_width, 45, "No", config, "danger"
        )
    
    def update(self, dt):
        """Actualiza animaciones"""
        if self.active:
            self.alpha = min(255, self.alpha + dt * 800)
        else:
            self.alpha = max(0, self.alpha - dt * 800)
        
        self.yes_button.update(dt)
        self.no_button.update(dt)
    
    def handle_event(self, event, mouse_pos):
        """Maneja eventos"""
        if not self.active:
            return
        
        self.yes_button.check_hover(mouse_pos)
        self.no_button.check_hover(mouse_pos)
        
        if self.yes_button.handle_event(event):
            self.result = True
            self.active = False
        elif self.no_button.handle_event(event):
            self.result = False
            self.active = False
    
    def draw(self, font):
        """Dibuja el diálogo"""
        if self.alpha <= 0:
            return
        
        # Overlay oscuro
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((*self.config.get_color("overlay")[:3], int(self.alpha * 0.7)))
        self.screen.blit(overlay, (0, 0))
        
        # Caja del diálogo
        dialog_surf = pygame.Surface((self.box_rect.width, self.box_rect.height), pygame.SRCALPHA)
        
        # Fondo
        pygame.draw.rect(dialog_surf, self.config.get_color("bg_secondary"),
                        dialog_surf.get_rect(), border_radius=15)
        pygame.draw.rect(dialog_surf, self.config.get_color("accent_primary"),
                        dialog_surf.get_rect(), 3, border_radius=15)
        
        # Texto
        text_surf = font.render(self.text, True, self.config.get_color("text_primary"))
        text_rect = text_surf.get_rect(center=(dialog_surf.get_width() // 2, 60))
        dialog_surf.blit(text_surf, text_rect)
        
        # Botones (posición relativa al diálogo)
        temp_yes = ModernButton(
            self.box_rect.width // 2 - 120 - 10, self.box_rect.height - 60,
            120, 45, "Sí", self.config, "success"
        )
        temp_yes.is_hovered = self.yes_button.is_hovered
        temp_yes.hover_progress = self.yes_button.hover_progress
        temp_yes.draw(dialog_surf, font)
        
        temp_no = ModernButton(
            self.box_rect.width // 2 + 10, self.box_rect.height - 60,
            120, 45, "No", self.config, "danger"
        )
        temp_no.is_hovered = self.no_button.is_hovered
        temp_no.hover_progress = self.no_button.hover_progress
        temp_no.draw(dialog_surf, font)
        
        dialog_surf.set_alpha(int(self.alpha))
        self.screen.blit(dialog_surf, self.box_rect)

class SettingsPanel:
    """Panel de ajustes modular y extensible"""
    
    def __init__(self, config, screen, fonts):
        self.config = config
        self.screen = screen
        self.fonts = fonts
        self.active = False
        self.alpha = 0
        self.theme_changed = False  # Bandera para indicar cambio de tema
        
        WIDTH, HEIGHT = screen.get_size()
        panel_width = 500
        panel_height = 600
        panel_x = WIDTH - panel_width - 20
        panel_y = 80
        
        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        # Crear controles de ajustes
        self.controls = {}
        self.setup_controls()
    
    def setup_controls(self):
        """Configura todos los controles del panel (modular para añadir más fácilmente)"""
        panel_x = self.panel_rect.x
        panel_y = self.panel_rect.y
        y_offset = 70
        
        # 1. TEMA
        themes = [
            ("Dark", "Oscuro"),
            ("Light", "Claro"),
            ("Ocean Blue", "Azul Océano"),
            ("Purple Night", "Noche Púrpura"),
            ("Forest Green", "Verde Bosque")
        ]
        self.controls["theme"] = {
            "type": "dropdown",
            "label": "Tema:",
            "y": panel_y + y_offset,
            "widget": Dropdown(panel_x + 20, panel_y + y_offset + 25, 
                             self.panel_rect.width - 40, 45,
                             themes, self.config.get_value("theme"), self.config)
        }
        y_offset += 90
        
        # 2. TIEMPO AUTO-OCULTAR CONTRASEÑA
        self.controls["password_auto_hide"] = {
            "type": "slider",
            "label": "Tiempo mostrar contraseña (segundos):",
            "y": panel_y + y_offset,
            "widget": Slider(panel_x + 20, panel_y + y_offset + 25,
                           self.panel_rect.width - 40, 5, 60,
                           self.config.get_value("password_auto_hide_seconds"),
                           self.config, step=1),
            "suffix": "s"
        }
        y_offset += 80
        
        # 3. TIEMPO PORTAPAPELES
        self.controls["auto_copy_timeout"] = {
            "type": "slider",
            "label": "Tiempo en portapapeles (segundos):",
            "y": panel_y + y_offset,
            "widget": Slider(panel_x + 20, panel_y + y_offset + 25,
                           self.panel_rect.width - 40, 10, 120,
                           self.config.get_value("auto_copy_timeout"),
                           self.config, step=5),
            "suffix": "s"
        }
        y_offset += 80
        
        # 4. LONGITUD MÍNIMA DE CONTRASEÑA
        self.controls["password_min_length"] = {
            "type": "slider",
            "label": "Longitud mínima de contraseña:",
            "y": panel_y + y_offset,
            "widget": Slider(panel_x + 20, panel_y + y_offset + 25,
                           self.panel_rect.width - 40, 8, 20,
                           self.config.get_value("password_min_length"),
                           self.config, step=1),
            "suffix": " caracteres"
        }
        y_offset += 80
        
        # 5. LONGITUD MÁXIMA DE CONTRASEÑA
        self.controls["password_max_length"] = {
            "type": "slider",
            "label": "Longitud máxima de contraseña:",
            "y": panel_y + y_offset,
            "widget": Slider(panel_x + 20, panel_y + y_offset + 25,
                           self.panel_rect.width - 40, 20, 64,
                           self.config.get_value("password_max_length"),
                           self.config, step=2),
            "suffix": " caracteres"
        }
        y_offset += 80
        
        # Botón Guardar
        self.save_button = ModernButton(
            panel_x + self.panel_rect.width // 2 - 75,
            panel_y + self.panel_rect.height - 60,
            150, 45, "Guardar", self.config, "success"
        )
    
    def handle_event(self, event, mouse_pos):
        """Maneja eventos del panel"""
        if not self.active:
            return False
        
        # BLOQUEAR ABSOLUTAMENTE TODOS los eventos de mouse cuando el panel está activo
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, 
                          pygame.MOUSEWHEEL):
            # Procesar eventos de controles
            for key, control_data in self.controls.items():
                widget = control_data["widget"]
                if widget.handle_event(event):
                    return True
            
            # Botón guardar
            if self.save_button.handle_event(event):
                self.apply_settings()
                return True
            
            # CONSUMIR el evento aunque no se haya manejado - así no pasa a elementos de abajo
            return True
        
        return False
    
    def apply_settings(self):
        """Aplica los ajustes y los guarda"""
        # GUARDAR tema original ANTES de procesar controles
        old_theme = self.config.config["theme"]
        
        # Recopilar valores de todos los controles
        for key, control_data in self.controls.items():
            widget = control_data["widget"]
            
            if control_data["type"] == "slider":
                value = int(widget.value)
            elif control_data["type"] == "dropdown":
                value = widget.selected_value
            else:
                continue
            
            # Mapear keys a nombres de configuración
            config_key_map = {
                "theme": "theme",
                "password_auto_hide": "password_auto_hide_seconds",
                "auto_copy_timeout": "auto_copy_timeout",
                "password_min_length": "password_min_length",
                "password_max_length": "password_max_length"
            }
            
            if key in config_key_map:
                self.config.set_value(config_key_map[key], value)
        
        # Verificar si cambió el tema
        new_theme = self.config.config["theme"]
        print(f"[DEBUG] Tema anterior: {old_theme}, Tema nuevo: {new_theme}")
        if new_theme != old_theme:
            print(f"[DEBUG] ¡Tema cambiado! Estableciendo theme_changed=True")
            self.config.set_theme(new_theme)
            self.theme_changed = True
        else:
            print(f"[DEBUG] Tema NO cambió")
        
        # Guardar configuración
        self.config.save_config()
        
        # Cerrar el panel
        self.active = False
        print(f"[DEBUG] apply_settings completado, theme_changed={self.theme_changed}")
        
        return True
    
    def update(self, dt, mouse_pos):
        """Actualiza animaciones y controles"""
        if self.active:
            self.alpha = min(255, self.alpha + dt * 800)
        else:
            self.alpha = max(0, self.alpha - dt * 800)
        
        # Actualizar controles
        for control_data in self.controls.values():
            widget = control_data["widget"]
            widget.check_hover(mouse_pos)
            widget.update(dt)
        
        self.save_button.check_hover(mouse_pos)
        self.save_button.update(dt)
    
    def draw(self):
        """Dibuja el panel de ajustes"""
        if self.alpha <= 0:
            return
        
        # Overlay oscuro sobre toda la pantalla
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(150 * (self.alpha / 255))))
        self.screen.blit(overlay, (0, 0))
        
        # Panel principal
        panel_surf = pygame.Surface((self.panel_rect.width, self.panel_rect.height), pygame.SRCALPHA)
        
        # Sombra
        shadow_rect = self.panel_rect.inflate(10, 10)
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (*self.config.get_color("shadow")[:3], 120),
                        shadow_surf.get_rect(), border_radius=15)
        self.screen.blit(shadow_surf, shadow_rect)
        
        # Fondo del panel
        pygame.draw.rect(panel_surf, self.config.get_color("bg_secondary"),
                        panel_surf.get_rect(), border_radius=12)
        pygame.draw.rect(panel_surf, self.config.get_color("border"),
                        panel_surf.get_rect(), 2, border_radius=12)
        
        # Título
        title_surf = self.fonts["subtitle"].render("Ajustes", True,
                                                   self.config.get_color("text_primary"))
        panel_surf.blit(title_surf, (20, 20))
        
        # Aplicar alpha al panel
        panel_surf.set_alpha(int(self.alpha))
        self.screen.blit(panel_surf, self.panel_rect)
        
        # Dibujar controles (sobre la pantalla principal para que no se vean afectados por el alpha)
        if self.alpha > 200:  # Solo dibujar cuando esté casi visible
            # Primero dibujar todos los controles excepto dropdowns
            for control_data in self.controls.values():
                # Label
                label_surf = self.fonts["normal"].render(control_data["label"], True,
                                                         self.config.get_color("text_secondary"))
                self.screen.blit(label_surf, (self.panel_rect.x + 20, control_data["y"]))
                
                # Widget (excepto dropdowns que se dibujan después)
                widget = control_data["widget"]
                if control_data["type"] != "dropdown":
                    widget.draw(self.screen, self.fonts["small"])
                
                # Mostrar valor actual del slider a la derecha
                if control_data["type"] == "slider":
                    suffix = control_data.get("suffix", "")
                    value_text = f"{int(widget.value)}{suffix}"
                    value_surf = self.fonts["normal"].render(value_text, True,
                                                             self.config.get_color("accent_primary"))
                    value_x = self.panel_rect.right - 20 - value_surf.get_width()
                    value_y = control_data["y"] + 30
                    self.screen.blit(value_surf, (value_x, value_y))
            
            # Botón guardar
            self.save_button.draw(self.screen, self.fonts["normal"])
            
            # Dibujar dropdowns AL FINAL para que aparezcan encima de todo
            for control_data in self.controls.values():
                if control_data["type"] == "dropdown":
                    widget = control_data["widget"]
                    widget.draw(self.screen, self.fonts["small"])

def interfaz_contrasenas(ini):
    """Interfaz principal del gestor de contraseñas"""
    # Bucle externo para reiniciar cuando cambie el tema
    while True:
        print("[DEBUG] Iniciando interfaz...")
        theme_changed = _run_interface(ini)
        if not theme_changed:
            print("[DEBUG] Saliendo normalmente")
            break  # Salir normalmente
        print("[DEBUG] Reiniciando interfaz con nuevo tema...")
        # Pequeña pausa para asegurar que pygame se limpia
        time.sleep(0.1)

def _run_interface(ini):
    """Ejecuta la interfaz y retorna True si cambió el tema"""
    pygame.init()
    
    # Cargar configuración
    config = ConfigManager()
    
    WIDTH, HEIGHT = 1500, 850
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Gestor de Contraseñas DNIe - Professional Edition")
    
    # Fuentes dinámicas
    font_sizes = config.get_font_sizes()
    fonts = {
        "title": pygame.font.SysFont('Segoe UI Bold', font_sizes["title"]),
        "subtitle": pygame.font.SysFont('Segoe UI', font_sizes["subtitle"]),
        "normal": pygame.font.SysFont('Segoe UI', font_sizes["normal"]),
        "small": pygame.font.SysFont('Segoe UI', font_sizes["small"])
    }
    
    # Estado de la aplicación
    lista_entries = []
    scroll_y = 0
    max_scroll = 0
    notification_text = ""
    notification_end_time = 0
    notification_color = config.get_color("success")
    dialogs = []
    show_stats = False
    show_settings = False
    search_text = ""
    password_visibility = {}  # {nombre: {"is_shown": bool, "timer": float}}
    editing_entry = None  # Nombre de la entrada siendo editada
    pending_generate = None  # Nombre de la entrada para generar nueva contraseña
    needs_reload = False  # Bandera para indicar que se debe recargar la interfaz
    
    # Componentes UI
    search_bar = SearchBar(20, 20, 400, 45, config)
    settings_panel = SettingsPanel(config, screen, fonts)
    
    def notify(text, duration=2500, error=False):
        """Muestra una notificación"""
        nonlocal notification_text, notification_end_time, notification_color
        notification_text = text
        notification_end_time = pygame.time.get_ticks() + duration
        notification_color = config.get_color("danger") if error else config.get_color("success")
    
    def reload_data():
        """Recarga las contraseñas desde la base de datos"""
        nonlocal lista_entries, max_scroll
        lista_entries = []
        raw_list = ini.cargar_bd().get("Contrasenas", [])
        
        for item in raw_list:
            lista_entries.append({
                "nombre": item["nombre"],
                "contrasena": item["contrasena"],
                "fecha_creacion": item.get("fecha_creacion", datetime.now().isoformat()),
                "fecha_modificacion": item.get("fecha_modificacion", datetime.now().isoformat())
            })
        
        # Calcular scroll máximo
        card_height = 110
        total_height = len(lista_entries) * card_height
        max_scroll = max(0, total_height - (HEIGHT - 200))
    
    def get_filtered_entries():
        """Retorna las entradas filtradas por búsqueda"""
        if not search_text:
            return lista_entries
        
        search_lower = search_text.lower()
        return [e for e in lista_entries if search_lower in e["nombre"].lower()]
    
    def draw_stats_panel(surface):
        """Dibuja el panel de estadísticas"""
        panel_width = 350
        panel_height = 400
        panel_x = WIDTH - panel_width - 20
        panel_y = 80
        
        # Fondo con sombra
        shadow_surf = pygame.Surface((panel_width + 10, panel_height + 10), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, config.get_color("shadow"),
                        shadow_surf.get_rect(), border_radius=15)
        surface.blit(shadow_surf, (panel_x - 5, panel_y - 5))
        
        # Panel principal
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(surface, config.get_color("bg_secondary"),
                        panel_rect, border_radius=12)
        pygame.draw.rect(surface, config.get_color("border"),
                        panel_rect, 2, border_radius=12)
        
        # Título
        title_surf = fonts["subtitle"].render("Estadísticas", True, 
                                             config.get_color("text_primary"))
        surface.blit(title_surf, (panel_x + 20, panel_y + 20))
        
        y_offset = 70
        
        # Total de contraseñas
        total = len(lista_entries)
        stat_surf = fonts["normal"].render(f"Total: {total}", True,
                                          config.get_color("text_secondary"))
        surface.blit(stat_surf, (panel_x + 20, panel_y + y_offset))
        y_offset += 40
        
        # Fortaleza promedio
        if lista_entries:
            avg_strength = sum(calculate_password_strength(e["contrasena"]) 
                             for e in lista_entries) / len(lista_entries)
            
            strength_text = f"Fortaleza Promedio: {int(avg_strength * 100)}%"
            stat_surf = fonts["normal"].render(strength_text, True,
                                              config.get_color("text_secondary"))
            surface.blit(stat_surf, (panel_x + 20, panel_y + y_offset))
            
            # Barra de progreso
            progress_bar = ProgressBar(panel_x + 20, panel_y + y_offset + 35,
                                     panel_width - 40, 12, config)
            progress_bar.set_progress(avg_strength)
            progress_bar.progress = avg_strength
            progress_bar.draw(surface)
            
            y_offset += 80
            
            # Desglose de fortaleza
            weak = sum(1 for e in lista_entries 
                      if calculate_password_strength(e["contrasena"]) < 0.4)
            medium = sum(1 for e in lista_entries 
                        if 0.4 <= calculate_password_strength(e["contrasena"]) < 0.7)
            strong = sum(1 for e in lista_entries 
                        if calculate_password_strength(e["contrasena"]) >= 0.7)
            
            breakdown_font = fonts["small"]
            
            # Débiles
            weak_surf = breakdown_font.render(f"Débiles: {weak}", True,
                                            config.get_color("danger"))
            surface.blit(weak_surf, (panel_x + 20, panel_y + y_offset))
            
            # Medias
            medium_surf = breakdown_font.render(f"Medias: {medium}", True,
                                              config.get_color("warning"))
            surface.blit(medium_surf, (panel_x + 20, panel_y + y_offset + 30))
            
            # Fuertes
            strong_surf = breakdown_font.render(f"Fuertes: {strong}", True,
                                              config.get_color("success"))
            surface.blit(strong_surf, (panel_x + 20, panel_y + y_offset + 60))
    
    reload_data()
    
    # Botones de acción principales
    btn_new = ModernButton(WIDTH - 220, 20, 190, 45, "+ Nueva Contraseña", 
                          config, "success")
    btn_stats = ModernButton(WIDTH - 480, 20, 110, 45, "Estadísticas", config, "secondary")
    btn_settings = ModernButton(WIDTH - 600, 20, 110, 45, "Ajustes", config, "secondary")
    btn_exit = ModernButton(20, HEIGHT - 70, 150, 45, "Salir", config, "danger")
    
    running = True
    clock = pygame.time.Clock()
    last_time = time.time()
    theme_changed = False
    
    while running:
        dt = clock.tick(60) / 1000.0
        current_time = time.time()
        mouse_pos = pygame.mouse.get_pos()
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                # Reposicionar elementos
                btn_new.rect.x = WIDTH - 220
                btn_stats.rect.x = WIDTH - 430
                btn_settings.rect.x = WIDTH - 480
                btn_exit.rect.y = HEIGHT - 70
            
            # Panel de ajustes tiene PRIORIDAD máxima para capturar todos los eventos
            if show_settings and settings_panel.active:
                if settings_panel.handle_event(event, mouse_pos):
                    # Si el panel se cerró (guardó cambios), actualizar show_settings
                    if not settings_panel.active:
                        show_settings = False
                        # Si cambió el tema, salir del bucle para recargar
                        if settings_panel.theme_changed:
                            print("=" * 60)
                            print("[DEBUG] ¡¡¡TEMA CAMBIADO DETECTADO!!!")
                            print("[DEBUG] Cerrando interfaz actual y reiniciando...")
                            print("=" * 60)
                            theme_changed = True
                            running = False
                    # Evento consumido por el panel, no procesar nada más
                    continue
            
            if event.type == pygame.MOUSEWHEEL:
                scroll_y = max(0, min(scroll_y - event.y * 30, max_scroll))
            
            # Búsqueda
            search_result = search_bar.handle_event(event)
            if search_result:
                search_text = search_bar.text
            
            # Botones principales
            if btn_new.handle_event(event):
                import password_dialog as NCP
                NCP.Nombre_Contraseña(ini, screen, config)
                reload_data()
            
            if btn_stats.handle_event(event):
                show_stats = not show_stats
            
            if btn_settings.handle_event(event):
                show_settings = not show_settings
                settings_panel.active = show_settings
            
            if btn_exit.handle_event(event):
                running = False
            
            # Diálogos
            for dialog in dialogs:
                dialog.handle_event(event, mouse_pos)
        
        # Actualizar componentes
        btn_new.check_hover(mouse_pos)
        btn_new.update(dt)
        btn_stats.check_hover(mouse_pos)
        btn_stats.update(dt)
        btn_settings.check_hover(mouse_pos)
        btn_settings.update(dt)
        btn_exit.check_hover(mouse_pos)
        btn_exit.update(dt)
        
        for dialog in dialogs:
            dialog.update(dt)
        
        # Actualizar panel de ajustes
        settings_panel.update(dt, mouse_pos)
        
        # Renderizado
        screen.fill(config.get_color("bg_primary"))
        
        # Gradiente sutil
        for i in range(HEIGHT):
            alpha = int(20 * (i / HEIGHT))
            gradient_color = (*config.get_color("bg_secondary")[:3], alpha)
            pygame.draw.line(screen, gradient_color, (0, i), (WIDTH, i))
        
        # Header
        header_height = 80
        pygame.draw.rect(screen, config.get_color("bg_secondary"),
                        (0, 0, WIDTH, header_height))
        
        # Título
        title_surf = fonts["title"].render("Gestor de Contraseñas", True,
                                          config.get_color("text_primary"))
        screen.blit(title_surf, (20, 85))
        
        # Barra de búsqueda
        search_bar.draw(screen, fonts["normal"])
        
        # Botones del header
        btn_new.draw(screen, fonts["normal"])
        btn_stats.draw(screen, fonts["normal"])
        btn_settings.draw(screen, fonts["normal"])
        
        # Área de contraseñas
        filtered = get_filtered_entries()
        
        if not filtered:
            # Mensaje cuando no hay contraseñas
            no_data_surf = fonts["subtitle"].render(
                "No hay contraseñas" if not search_text else "No se encontraron resultados",
                True, config.get_color("text_disabled")
            )
            no_data_rect = no_data_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(no_data_surf, no_data_rect)
        else:
            # Dibujar tarjetas
            card_height = 110
            visible_area = pygame.Rect(0, header_height + 70, WIDTH, HEIGHT - header_height - 140)
            
            for i, entry in enumerate(filtered):
                card_y = header_height + 80 + i * card_height - scroll_y
                
                # Solo dibujar si está visible
                if card_y + card_height < header_height or card_y > HEIGHT:
                    continue
                
                # Obtener estado de visibilidad persistente
                entry_name = entry["nombre"]
                if entry_name not in password_visibility:
                    password_visibility[entry_name] = {"is_shown": False, "timer": 0}
                
                vis_state = password_visibility[entry_name]
                card = PasswordCard(entry, card_y, WIDTH, config, 
                                  vis_state["is_shown"], vis_state["timer"])
                card.update(dt, mouse_pos, scroll_y)
                
                # Actualizar estado persistente
                vis_state["is_shown"] = card.is_shown
                vis_state["timer"] = card.show_timer
                
                # Clip para no salir del área
                screen.set_clip(visible_area)
                card.draw(screen, fonts)
                screen.set_clip(None)
                
                # Manejar eventos de la tarjeta SOLO si el panel de ajustes NO está activo
                if not (show_settings and settings_panel.active):
                    for event in events:
                        action = card.handle_event(event, scroll_y)
                        if action == "show":
                            # Toggle visibilidad
                            if vis_state["is_shown"]:
                                vis_state["is_shown"] = False
                                vis_state["timer"] = 0
                            else:
                                vis_state["is_shown"] = True
                                # TODO: Hacer configurable desde ajustes
                                auto_hide_time = config.get_value("password_auto_hide_seconds") or 15
                                vis_state["timer"] = float(auto_hide_time)
                        elif action == "copy":
                            timeout = config.get_value("auto_copy_timeout") or 30
                            copy_password_temporal(entry["contrasena"], int(timeout))
                            notify(f"Contraseña copiada ({timeout}s)")
                        elif action == "edit":
                            editing_entry = entry["nombre"]
                        elif action == "gen":
                            dialog = ModernConfirmDialog(
                                f"¿Generar nueva contraseña para '{entry['nombre']}'?",
                                config, screen, "generate", entry['nombre']
                            )
                            dialogs.append(dialog)
                        elif action == "del":
                            dialog = ModernConfirmDialog(
                                f"¿Eliminar '{entry['nombre']}'?",
                                config, screen, "delete", entry['nombre']
                            )
                            dialogs.append(dialog)
        
        # Botón salir
        btn_exit.draw(screen, fonts["normal"])
        
        # Panel de estadísticas
        if show_stats:
            draw_stats_panel(screen)
        
        # Panel de ajustes
        if show_settings or settings_panel.alpha > 0:
            settings_panel.draw()
        
        # Notificaciones
        if pygame.time.get_ticks() < notification_end_time:
            notif_surf = fonts["normal"].render(notification_text, True,
                                               config.get_color("text_primary"))
            notif_rect = notif_surf.get_rect(center=(WIDTH // 2, HEIGHT - 40))
            bg_rect = notif_rect.inflate(40, 20)
            
            bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(bg_surf, (*notification_color, 220),
                           bg_surf.get_rect(), border_radius=10)
            screen.blit(bg_surf, bg_rect)
            screen.blit(notif_surf, notif_rect)
        
        # Manejar diálogo de edición
        if editing_entry:
            if Nombre_Contraseña.Editar_Contraseña(ini, screen, editing_entry, config):
                reload_data()
                notify(f"'{editing_entry}' actualizado correctamente")
            editing_entry = None
        
        # Diálogos
        for dialog in dialogs[:]:
            dialog.draw(fonts["normal"])
            
            if dialog.result is not None and not dialog.active and dialog.alpha <= 0:
                if dialog.result:
                    # Procesar acción confirmada
                    if dialog.action_type == "delete":
                        if ini.eliminar_contraseña(dialog.entry_name):
                            # Limpiar estado de visibilidad
                            if dialog.entry_name in password_visibility:
                                del password_visibility[dialog.entry_name]
                            reload_data()
                            notify(f"'{dialog.entry_name}' eliminado correctamente")
                        else:
                            notify(f"Error al eliminar '{dialog.entry_name}'", error=True)
                    elif dialog.action_type == "generate":
                        # Generar nueva contraseña
                        nueva_pass = gc.generar_contraseña()
                        # Eliminar y agregar con nueva contraseña
                        if ini.eliminar_contraseña(dialog.entry_name):
                            if ini.agregar_contraseña(dialog.entry_name, nueva_pass):
                                reload_data()
                                notify(f"Nueva contraseña generada para '{dialog.entry_name}'")
                            else:
                                notify(f"Error al generar contraseña", error=True)
                        else:
                            notify(f"Error al generar contraseña", error=True)
                    elif "Generar" in dialog.text:
                        nombre = dialog.text.split("'")[1]
                        nueva = gc.generar_contraseña()
                        if ini.editar_contraseña(nombre, nueva):
                            reload_data()
                            notify(f"Nueva contraseña generada para '{nombre}'")
                
                dialogs.remove(dialog)
        
        pygame.display.flip()
    
    # Limpiar pygame antes de salir o reiniciar
    print(f"[DEBUG] Limpiando pygame, theme_changed={theme_changed}")
    pygame.quit()
    
    # Retornar si cambió el tema para reiniciar
    return theme_changed
