"""
Diálogo para agregar nuevas contraseñas - Versión Moderna
"""
import pygame
import password_generator as gc
from config_manager import ConfigManager
from ui_components import (ModernButton, ModernInputBox, ProgressBar, 
                           calculate_password_strength)

def Editar_Contraseña(ini, parent_screen, entry_nombre, config=None):
    """Diálogo modal para editar una contraseña existente"""
    
    if config is None:
        config = ConfigManager()
    
    # Obtener datos actuales
    entry_actual = None
    db = ini.cargar_bd()
    for entry in db.get("Contrasenas", []):
        if entry["nombre"] == entry_nombre:
            entry_actual = entry
            break
    
    if not entry_actual:
        return False
    
    WIDTH, HEIGHT = parent_screen.get_size()
    
    # Dimensiones del diálogo
    dialog_width = 600
    dialog_height = 450
    dialog_x = (WIDTH - dialog_width) // 2
    dialog_y = (HEIGHT - dialog_height) // 2
    dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
    
    # Fuentes
    font_sizes = config.get_font_sizes()
    fonts = {
        "title": pygame.font.SysFont('Segoe UI Bold', font_sizes["subtitle"]),
        "normal": pygame.font.SysFont('Segoe UI', font_sizes["normal"]),
        "small": pygame.font.SysFont('Segoe UI', font_sizes["small"])
    }
    
    # Componentes con datos actuales
    input_nombre = ModernInputBox(
        dialog_x + 30, dialog_y + 100, dialog_width - 60, 50,
        config, placeholder="Nombre de la cuenta"
    )
    input_nombre.text = entry_actual["nombre"]
    
    min_length = config.get_value("password_min_length") or 15
    input_pass = ModernInputBox(
        dialog_x + 30, dialog_y + 180, dialog_width - 150, 50,
        config, placeholder=f"Contraseña (mín. {min_length} caracteres)", password=True
    )
    input_pass.text = entry_actual["contrasena"]
    
    btn_generate = ModernButton(
        dialog_x + dialog_width - 110, dialog_y + 180, 80, 50,
        "Gen", config, "accent"
    )
    
    btn_save = ModernButton(
        dialog_x + dialog_width // 2 - 130, dialog_y + dialog_height - 70,
        120, 50, "Guardar", config, "success"
    )
    
    btn_cancel = ModernButton(
        dialog_x + dialog_width // 2 + 10, dialog_y + dialog_height - 70,
        120, 50, "Cancelar", config, "secondary"
    )
    
    progress_bar = ProgressBar(
        dialog_x + 30, dialog_y + 250, dialog_width - 60, 12, config
    )
    
    notification_text = ""
    notification_timer = 0
    notification_error = False
    original_nombre = entry_actual["nombre"]  # Guardar nombre original
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        dt = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            # Inputs
            result_nombre = input_nombre.handle_event(event)
            result_pass = input_pass.handle_event(event)
            
            if result_nombre == "submit" or result_pass == "submit":
                pass
            
            # Botón generar
            if btn_generate.handle_event(event):
                input_pass.text = gc.generar_contraseña()
                input_pass.error = False
            
            # Botón cancelar
            if btn_cancel.handle_event(event):
                return False
            
            # Botón guardar
            if btn_save.handle_event(event):
                nombre = input_nombre.text.strip()
                password = input_pass.text
                
                # Validaciones
                if not nombre:
                    input_nombre.error = True
                    input_nombre.error_message = "El nombre no puede estar vacío"
                    notification_text = "Error: Nombre vacío"
                    notification_timer = 2.0
                    notification_error = True
                else:
                    min_length = config.get_value("password_min_length") or 15
                    max_length = config.get_value("password_max_length") or 32
                    
                    if len(password) < min_length:
                        input_pass.error = True
                        input_pass.error_message = f"Mínimo {min_length} caracteres"
                        notification_text = f"Error: Contraseña muy corta (mín. {min_length})"
                        notification_timer = 2.0
                        notification_error = True
                    elif len(password) > max_length:
                        input_pass.error = True
                        input_pass.error_message = f"Máximo {max_length} caracteres"
                        notification_text = f"Error: Contraseña muy larga (máx. {max_length})"
                        notification_timer = 2.0
                        notification_error = True
                    else:
                        # Si cambió el nombre, verificar que no exista
                        if nombre != original_nombre:
                            # Verificar si el nuevo nombre ya existe
                            db_check = ini.cargar_bd()
                            existe = any(e["nombre"] == nombre for e in db_check.get("Contrasenas", []) 
                                       if e["nombre"] != original_nombre)
                            if existe:
                                input_nombre.error = True
                                input_nombre.error_message = "Ya existe una entrada con este nombre"
                                notification_text = f"Error: '{nombre}' ya existe"
                                notification_timer = 2.0
                                notification_error = True
                                continue
                        
                        # Eliminar la entrada antigua y agregar la nueva
                        if ini.eliminar_contraseña(original_nombre):
                            if ini.agregar_contraseña(nombre, password):
                                notification_text = "✓ Contraseña actualizada correctamente"
                                notification_timer = 1.5
                                notification_error = False
                                pygame.time.wait(1000)
                                return True
                            else:
                                # Si falla, restaurar la original
                                ini.agregar_contraseña(original_nombre, entry_actual["contrasena"])
                                notification_text = "Error al actualizar"
                                notification_timer = 2.0
                                notification_error = True
                        else:
                            notification_text = "Error al actualizar"
                            notification_timer = 2.0
                            notification_error = True
        
        # Actualizar componentes
        input_nombre.update(dt)
        input_pass.update(dt)
        btn_generate.check_hover(mouse_pos)
        btn_generate.update(dt)
        btn_save.check_hover(mouse_pos)
        btn_save.update(dt)
        btn_cancel.check_hover(mouse_pos)
        btn_cancel.update(dt)
        
        # Actualizar barra de fortaleza
        if input_pass.text:
            strength = calculate_password_strength(input_pass.text)
            progress_bar.set_progress(strength)
        else:
            progress_bar.set_progress(0.0)
        progress_bar.update(dt)
        
        # Actualizar timer de notificación
        if notification_timer > 0:
            notification_timer -= dt
        
        # Dibujar sobre la pantalla padre
        parent_screen.fill(config.get_color("bg_primary"))
        
        # Overlay oscuro
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((*config.get_color("overlay")[:3], 200))
        parent_screen.blit(overlay, (0, 0))
        
        # Diálogo principal
        # Sombra
        shadow_rect = dialog_rect.inflate(10, 10)
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, config.get_color("shadow"),
                        shadow_surf.get_rect(), border_radius=15)
        parent_screen.blit(shadow_surf, shadow_rect)
        
        # Fondo
        pygame.draw.rect(parent_screen, config.get_color("bg_secondary"),
                        dialog_rect, border_radius=15)
        pygame.draw.rect(parent_screen, config.get_color("border"),
                        dialog_rect, 2, border_radius=15)
        
        # Título
        title_surf = fonts["title"].render("Editar Contraseña", True,
                                          config.get_color("text_primary"))
        parent_screen.blit(title_surf, (dialog_x + 30, dialog_y + 30))
        
        # Labels
        label_nombre = fonts["small"].render("Nombre:", True,
                                            config.get_color("text_secondary"))
        parent_screen.blit(label_nombre, (dialog_x + 30, dialog_y + 75))
        
        label_pass = fonts["small"].render("Contraseña:", True,
                                          config.get_color("text_secondary"))
        parent_screen.blit(label_pass, (dialog_x + 30, dialog_y + 155))
        
        # Inputs
        input_nombre.draw(parent_screen, fonts["normal"])
        input_pass.draw(parent_screen, fonts["normal"])
        
        # Botón generar
        btn_generate.draw(parent_screen, fonts["normal"])
        
        # Barra de fortaleza
        progress_bar.draw(parent_screen)
        
        # Etiqueta de fortaleza
        if input_pass.text:
            strength = calculate_password_strength(input_pass.text)
            if strength < 0.4:
                strength_text = "Débil"
                strength_color = config.get_color("danger")
            elif strength < 0.7:
                strength_text = "Media"
                strength_color = config.get_color("warning")
            else:
                strength_text = "Fuerte"
                strength_color = config.get_color("success")
            
            strength_surf = fonts["small"].render(
                f"Fortaleza: {strength_text} ({int(strength * 100)}%)",
                True, strength_color
            )
            parent_screen.blit(strength_surf, (dialog_x + 30, dialog_y + 270))
        
        # Botones de acción
        btn_save.draw(parent_screen, fonts["normal"])
        btn_cancel.draw(parent_screen, fonts["normal"])
        
        # Notificación
        if notification_timer > 0:
            notif_color = config.get_color("danger") if notification_error else config.get_color("success")
            notif_surf = fonts["normal"].render(notification_text, True,
                                               config.get_color("text_primary"))
            notif_rect = notif_surf.get_rect(center=(dialog_x + dialog_width // 2,
                                                     dialog_y + dialog_height - 110))
            bg_rect = notif_rect.inflate(30, 15)
            
            bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(bg_surf, (*notif_color, 220),
                           bg_surf.get_rect(), border_radius=8)
            parent_screen.blit(bg_surf, bg_rect)
            parent_screen.blit(notif_surf, notif_rect)
        
        pygame.display.flip()
    
    return False


def Nombre_Contraseña(ini, parent_screen, config=None):
    """Diálogo modal para agregar nueva contraseña"""
    
    if config is None:
        config = ConfigManager()
    
    WIDTH, HEIGHT = parent_screen.get_size()
    
    # Dimensiones del diálogo
    dialog_width = 600
    dialog_height = 450
    dialog_x = (WIDTH - dialog_width) // 2
    dialog_y = (HEIGHT - dialog_height) // 2
    dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
    
    # Fuentes
    font_sizes = config.get_font_sizes()
    fonts = {
        "title": pygame.font.SysFont('Segoe UI Bold', font_sizes["subtitle"]),
        "normal": pygame.font.SysFont('Segoe UI', font_sizes["normal"]),
        "small": pygame.font.SysFont('Segoe UI', font_sizes["small"])
    }
    
    # Componentes
    input_nombre = ModernInputBox(
        dialog_x + 30, dialog_y + 100, dialog_width - 60, 50,
        config, placeholder="Nombre de la cuenta"
    )
    
    min_length = config.get_value("password_min_length") or 15
    input_pass = ModernInputBox(
        dialog_x + 30, dialog_y + 180, dialog_width - 150, 50,
        config, placeholder=f"Contraseña (mín. {min_length} caracteres)", password=True
    )
    
    btn_generate = ModernButton(
        dialog_x + dialog_width - 110, dialog_y + 180, 80, 50,
        "Gen", config, "accent"
    )
    
    btn_add = ModernButton(
        dialog_x + dialog_width // 2 - 130, dialog_y + dialog_height - 70,
        120, 50, "Añadir", config, "success"
    )
    
    btn_cancel = ModernButton(
        dialog_x + dialog_width // 2 + 10, dialog_y + dialog_height - 70,
        120, 50, "Cancelar", config, "secondary"
    )
    
    progress_bar = ProgressBar(
        dialog_x + 30, dialog_y + 250, dialog_width - 60, 12, config
    )
    
    notification_text = ""
    notification_timer = 0
    notification_error = False
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        dt = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            # Inputs
            result_nombre = input_nombre.handle_event(event)
            result_pass = input_pass.handle_event(event)
            
            if result_nombre == "submit" or result_pass == "submit":
                # Simular click en añadir
                pass
            
            # Botón generar
            if btn_generate.handle_event(event):
                input_pass.text = gc.generar_contraseña()
                input_pass.error = False
            
            # Botón cancelar
            if btn_cancel.handle_event(event):
                return False
            
            # Botón añadir
            if btn_add.handle_event(event):
                nombre = input_nombre.text.strip()
                password = input_pass.text
                
                # Validaciones
                if not nombre:
                    input_nombre.error = True
                    input_nombre.error_message = "El nombre no puede estar vacío"
                    notification_text = "Error: Nombre vacío"
                    notification_timer = 2.0
                    notification_error = True
                else:
                    min_length = config.get_value("password_min_length") or 15
                    max_length = config.get_value("password_max_length") or 32
                    
                    if len(password) < min_length:
                        input_pass.error = True
                        input_pass.error_message = f"Mínimo {min_length} caracteres"
                        notification_text = f"Error: Contraseña muy corta (mín. {min_length})"
                        notification_timer = 2.0
                        notification_error = True
                    elif len(password) > max_length:
                        input_pass.error = True
                        input_pass.error_message = f"Máximo {max_length} caracteres"
                        notification_text = f"Error: Contraseña muy larga (máx. {max_length})"
                        notification_timer = 2.0
                        notification_error = True
                    else:
                        # Intentar agregar
                        if ini.agregar_contraseña(nombre, password):
                            notification_text = "✓ Contraseña guardada correctamente"
                            notification_timer = 1.5
                            notification_error = False
                            # Esperar un poco y cerrar
                            pygame.time.wait(1000)
                            return True
                        else:
                            input_nombre.error = True
                            input_nombre.error_message = "Ya existe una entrada con este nombre"
                            notification_text = f"Error: '{nombre}' ya existe"
                            notification_timer = 2.0
                            notification_error = True
        
        # Actualizar componentes
        input_nombre.update(dt)
        input_pass.update(dt)
        btn_generate.check_hover(mouse_pos)
        btn_generate.update(dt)
        btn_add.check_hover(mouse_pos)
        btn_add.update(dt)
        btn_cancel.check_hover(mouse_pos)
        btn_cancel.update(dt)
        
        # Actualizar barra de fortaleza
        if input_pass.text:
            strength = calculate_password_strength(input_pass.text)
            progress_bar.set_progress(strength)
        else:
            progress_bar.set_progress(0.0)
        progress_bar.update(dt)
        
        # Actualizar timer de notificación
        if notification_timer > 0:
            notification_timer -= dt
        
        # Dibujar sobre la pantalla padre
        parent_screen.fill(config.get_color("bg_primary"))
        
        # Overlay oscuro
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((*config.get_color("overlay")[:3], 200))
        parent_screen.blit(overlay, (0, 0))
        
        # Diálogo principal
        # Sombra
        shadow_rect = dialog_rect.inflate(10, 10)
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, config.get_color("shadow"),
                        shadow_surf.get_rect(), border_radius=15)
        parent_screen.blit(shadow_surf, shadow_rect)
        
        # Fondo
        pygame.draw.rect(parent_screen, config.get_color("bg_secondary"),
                        dialog_rect, border_radius=15)
        pygame.draw.rect(parent_screen, config.get_color("border"),
                        dialog_rect, 2, border_radius=15)
        
        # Título
        title_surf = fonts["title"].render("Nueva Contraseña", True,
                                          config.get_color("text_primary"))
        parent_screen.blit(title_surf, (dialog_x + 30, dialog_y + 30))
        
        # Labels
        label_nombre = fonts["small"].render("Nombre:", True,
                                            config.get_color("text_secondary"))
        parent_screen.blit(label_nombre, (dialog_x + 30, dialog_y + 75))
        
        label_pass = fonts["small"].render("Contraseña:", True,
                                          config.get_color("text_secondary"))
        parent_screen.blit(label_pass, (dialog_x + 30, dialog_y + 155))
        
        # Inputs
        input_nombre.draw(parent_screen, fonts["normal"])
        input_pass.draw(parent_screen, fonts["normal"])
        
        # Botón generar
        btn_generate.draw(parent_screen, fonts["normal"])
        
        # Barra de fortaleza
        progress_bar.draw(parent_screen)
        
        # Etiqueta de fortaleza
        if input_pass.text:
            strength = calculate_password_strength(input_pass.text)
            if strength < 0.4:
                strength_text = "Débil"
                strength_color = config.get_color("danger")
            elif strength < 0.7:
                strength_text = "Media"
                strength_color = config.get_color("warning")
            else:
                strength_text = "Fuerte"
                strength_color = config.get_color("success")
            
            strength_surf = fonts["small"].render(
                f"Fortaleza: {strength_text} ({int(strength * 100)}%)",
                True, strength_color
            )
            parent_screen.blit(strength_surf, (dialog_x + 30, dialog_y + 270))
        
        # Botones de acción
        btn_add.draw(parent_screen, fonts["normal"])
        btn_cancel.draw(parent_screen, fonts["normal"])
        
        # Notificación
        if notification_timer > 0:
            notif_color = config.get_color("danger") if notification_error else config.get_color("success")
            notif_surf = fonts["normal"].render(notification_text, True,
                                               config.get_color("text_primary"))
            notif_rect = notif_surf.get_rect(center=(dialog_x + dialog_width // 2,
                                                     dialog_y + dialog_height - 110))
            bg_rect = notif_rect.inflate(30, 15)
            
            bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(bg_surf, (*notif_color, 220),
                           bg_surf.get_rect(), border_radius=8)
            parent_screen.blit(bg_surf, bg_rect)
            parent_screen.blit(notif_surf, notif_rect)
        
        pygame.display.flip()
    
    return False


# Mantener compatibilidad con versión anterior
class InputBox:
    """Clase legacy para compatibilidad"""
    def __init__(self, rect, font, text=''):
        config = ConfigManager()
        self.modern = ModernInputBox(rect[0], rect[1], rect[2], rect[3], config)
        self.modern.text = text
        self.text = text
        self.rect = pygame.Rect(rect)
        self.font = font
        self.active = False
    
    def handle_event(self, event):
        result = self.modern.handle_event(event)
        self.text = self.modern.text
        self.active = self.modern.active
        return result
    
    def draw(self, screen):
        self.modern.draw(screen, self.font)
        self.text = self.modern.text

class Button:
    """Clase legacy para compatibilidad"""
    def __init__(self, rect, text, color, hover_color=None, font=None):
        config = ConfigManager()
        color_map = {
            (25,135,84): "success",
            (108,117,125): "secondary",
            (0,123,255): "accent"
        }
        color_type = color_map.get(color, "accent")
        
        self.modern = ModernButton(rect[0], rect[1], rect[2], rect[3],
                                   text, config, color_type)
        self.rect = pygame.Rect(rect)
        self.text = text
        self.is_hovered = False
        self.font = font
    
    def draw(self, surface):
        if self.font:
            self.modern.draw(surface, self.font)
        else:
            font = pygame.font.Font(None, 24)
            self.modern.draw(surface, font)
    
    def check_hover(self, mouse_pos):
        self.modern.check_hover(mouse_pos)
        self.is_hovered = self.modern.is_hovered
    
    def is_clicked(self, event):
        return self.modern.handle_event(event)
