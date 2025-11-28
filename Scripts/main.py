import pygame
import sys
import time 
import math
import dnie_detector as detdniegui
from config_manager import ConfigManager
from ui_components import ModernButton, draw_lock_icon, draw_settings_icon

# Inicialización de Pygame, para la interfaz del programa
pygame.init()

# Configuración de la Ventana
WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gestor de Contraseñas DNIe")

# Cargar configuración y tema
config = ConfigManager()
font_sizes = config.get_font_sizes()

# Fuentes dinámicas según configuración
try:
    title_font = pygame.font.SysFont('Segoe UI Bold', font_sizes["title"])
    button_font = pygame.font.SysFont('Segoe UI Bold', font_sizes["subtitle"])  # Más grande y bold
    subtitle_font = pygame.font.SysFont('Segoe UI Light', font_sizes["small"]) 
except pygame.error:
    # En el caso en el que las fuentes no esten instaladas en el sistema utiliza fuentes por defecto
    title_font = pygame.font.Font(None, font_sizes["title"] + 10)
    button_font = pygame.font.Font(None, font_sizes["subtitle"] + 8)  # Más grande
    subtitle_font = pygame.font.Font(None, font_sizes["small"] + 4)

# Panel de configuración (botón en la esquina)
settings_button_rect = pygame.Rect(WIDTH - 50, 10, 40, 40)
show_settings = False
settings_panel_alpha = 0

def draw_settings_panel(surface):
    """Dibuja el panel de configuración"""
    panel_width = 350
    panel_height = 450
    panel_x = WIDTH - panel_width - 20
    panel_y = 60
    
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
    title_surf = button_font.render("Configuración", True, config.get_color("text_primary"))
    surface.blit(title_surf, (panel_x + 20, panel_y + 20))
    
    y_offset = 70
    
    # Sección de temas
    section_font = pygame.font.Font(None, font_sizes["small"])
    section_surf = section_font.render("Tema de Color", True, config.get_color("text_secondary"))
    surface.blit(section_surf, (panel_x + 20, panel_y + y_offset))
    y_offset += 30
    
    # Botones de temas
    themes = config.get_theme_names()
    current_theme = config.config["theme"]
    
    for theme_name in themes:
        theme_rect = pygame.Rect(panel_x + 20, panel_y + y_offset, panel_width - 40, 35)
        
        # Resaltar tema actual
        if theme_name == current_theme:
            pygame.draw.rect(surface, config.get_color("accent_primary"), 
                           theme_rect, border_radius=6)
            text_color = config.get_color("text_primary")
        else:
            pygame.draw.rect(surface, config.get_color("bg_tertiary"), 
                           theme_rect, border_radius=6)
            text_color = config.get_color("text_secondary")
        
        theme_text = section_font.render(theme_name, True, text_color)
        text_rect = theme_text.get_rect(center=theme_rect.center)
        surface.blit(theme_text, text_rect)
        
        y_offset += 45
    
    return panel_rect

def handle_settings_click(mouse_pos):
    """Maneja clicks en el panel de configuración"""
    if not show_settings:
        return
    
    panel_width = 350
    panel_x = WIDTH - panel_width - 20
    panel_y = 60
    y_offset = 100
    
    themes = config.get_theme_names()
    
    for theme_name in themes:
        theme_rect = pygame.Rect(panel_x + 20, panel_y + y_offset, panel_width - 40, 35)
        if theme_rect.collidepoint(mouse_pos):
            config.set_theme(theme_name)
            return True
        y_offset += 45
    
    return False

# Creación de elementos de la GUI modernos
icon_y = 70
title_surf = title_font.render("Gestor de Contraseñas", True, config.get_color("text_primary"))
title_rect = title_surf.get_rect(center=(WIDTH // 2, 140))

subtitle_surf = subtitle_font.render("Seguridad certificada con DNIe", True, 
                                     config.get_color("text_secondary"))
subtitle_rect = subtitle_surf.get_rect(center=(WIDTH // 2, 180))

author_surf = subtitle_font.render("by Enrique Landa & Rubén Sanz", True, 
                                   config.get_color("text_disabled"))
author_rect = author_surf.get_rect(center=(WIDTH // 2, HEIGHT - 20))

# Botones modernos - más arriba y más grandes
button_width, button_height = 160, 60
button_y = 240
spacing = 40

exit_button = ModernButton(
    WIDTH // 2 - button_width - spacing // 2, button_y, 
    button_width, button_height, 'SALIR', config, color_type="danger"
)

access_button = ModernButton(
    WIDTH // 2 + spacing // 2, button_y, 
    button_width, button_height, 'ACCEDER', config, color_type="success"
)

buttons = [exit_button, access_button]

# Variables para animaciones
start_time = time.time()
fade_duration = 0.8
icon_float_offset = 0
last_frame_time = time.time()

# Bucle principal que genera la ventana
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000.0  # Delta time en segundos
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Settings button
            if settings_button_rect.collidepoint(event.pos):
                show_settings = not show_settings
            elif show_settings:
                if handle_settings_click(event.pos):
                    # Recargar fuentes si cambió el tema
                    try:
                        font_sizes = config.get_font_sizes()
                        title_font = pygame.font.SysFont('Segoe UI Bold', font_sizes["title"])
                        button_font = pygame.font.SysFont('Segoe UI', font_sizes["normal"])
                        subtitle_font = pygame.font.SysFont('Segoe UI Light', font_sizes["small"])
                    except:
                        pass
                    
                    # Actualizar superficies de texto
                    title_surf = title_font.render("Gestor de Contraseñas", True, 
                                                  config.get_color("text_primary"))
                    subtitle_surf = subtitle_font.render("Seguridad certificada con DNIe", True, 
                                                        config.get_color("text_secondary"))
                    author_surf = subtitle_font.render("by Enrique Landa & Rubén Sanz", True, 
                                                      config.get_color("text_disabled"))
        
        # Manejo de botones
        for button in buttons:
            if button.handle_event(event):
                if button == exit_button:
                    running = False
                elif button == access_button:
                    pygame.quit() 
                    detdniegui.detectar_dnie() 
                    sys.exit()

    mouse_pos = pygame.mouse.get_pos()
    
    # Actualizar animaciones de botones
    for button in buttons:
        button.check_hover(mouse_pos)
        button.update(dt)
    
    # Animación del panel de settings
    if show_settings:
        settings_panel_alpha = min(255, settings_panel_alpha + dt * 500)
    else:
        settings_panel_alpha = max(0, settings_panel_alpha - dt * 500)
    
    # Relleno de la pantalla con el color del tema
    screen.fill(config.get_color("bg_primary"))
    
    # Gradiente sutil en el fondo
    for i in range(HEIGHT):
        alpha = int(30 * (i / HEIGHT))
        gradient_color = (*config.get_color("bg_secondary")[:3], alpha)
        pygame.draw.line(screen, gradient_color, (0, i), (WIDTH, i))
    
    # Código que genera la animacion de aparición
    elapsed_time = time.time() - start_time
    alpha = min(255, int(255 * (elapsed_time / fade_duration)))
    
    # Animación flotante del icono
    icon_float_offset = math.sin(current_time * 2) * 5
    
    # Crea una superficie temporal para aplicar la transparencia
    ui_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ui_surface.fill((0, 0, 0, 0)) 
    
    # Dibuja el icono del candado con efecto brillante
    icon_x = WIDTH // 2
    icon_y_pos = icon_y + icon_float_offset
    
    # Efecto de brillo detrás del icono
    if config.get_value("animations_enabled"):
        glow_size = 80 + math.sin(current_time * 3) * 10
        glow_surf = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*config.get_color("accent_primary"), 30), 
                         (int(glow_size), int(glow_size)), int(glow_size))
        ui_surface.blit(glow_surf, (icon_x - glow_size, icon_y_pos - glow_size))
    
    draw_lock_icon(ui_surface, icon_x, int(icon_y_pos), 
                  config.get_color("accent_primary"), size=40)
    
    # Textos
    ui_surface.blit(title_surf, title_rect)
    ui_surface.blit(subtitle_surf, subtitle_rect)
    ui_surface.blit(author_surf, author_rect)
    
    # Dibuja botones modernos
    for button in buttons:
        button.draw(ui_surface, button_font)
    
    # Aplica la transparencia y dibuja en la pantalla principal
    ui_surface.set_alpha(alpha)
    screen.blit(ui_surface, (0, 0))
    
    # Botón de configuración (siempre visible)
    pygame.draw.circle(screen, config.get_color("bg_secondary"), 
                      settings_button_rect.center, 20)
    pygame.draw.circle(screen, config.get_color("border"), 
                      settings_button_rect.center, 20, 2)
    
    if settings_button_rect.collidepoint(mouse_pos):
        pygame.draw.circle(screen, config.get_color("accent_primary"), 
                          settings_button_rect.center, 20, 2)
    
    draw_settings_icon(screen, *settings_button_rect.center, 
                      config.get_color("text_primary"), size=20)
    
    # Panel de configuración
    if settings_panel_alpha > 0:
        settings_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        draw_settings_panel(settings_surf)
        settings_surf.set_alpha(int(settings_panel_alpha))
        screen.blit(settings_surf, (0, 0))
    
    pygame.display.flip()

# Finalizar
pygame.quit()
sys.exit()

