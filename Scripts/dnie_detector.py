import pygame
import sys
import time
from smartcard.System import readers
import dnie_authenticator as vdnie
from config_manager import ConfigManager

def detectar_dnie_hardware():
    """Detecta si un lector de tarjetas y un DNIe están conectados"""
    try:
        lista_lectores = readers()
        if not lista_lectores:
            return False
        
        lector = lista_lectores[0]
        conexion = lector.createConnection()
        
        try:
            conexion.connect()
            return True
        except Exception:
            return False
    except Exception:
        return False

def detectar_dnie():
    # Inicialización de Pygame
    pygame.init()
    
    # Cargar configuración
    config = ConfigManager()
    font_sizes = config.get_font_sizes()

    # Configuración de la Ventana 
    WIDTH, HEIGHT = 600, 250
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Detectando DNIe")

    # Configuración de las Fuentes dinámicas
    title_font = pygame.font.Font(None, font_sizes["title"])
    subtitle_font = pygame.font.Font(None, font_sizes["normal"])

    # Configuración de la Barra de Carga
    BAR_WIDTH, BAR_HEIGHT = 300, 15
    bar_x = (WIDTH - BAR_WIDTH) // 2
    bar_y = HEIGHT // 2 + 40
    bar_bg_rect = pygame.Rect(bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT)

    # Constante para el tiempo de espera
    WAIT_SECONDS = 1.0 

    # Variables de estado
    start_time = time.time()
    detection_result = None
    status_message = "Detectando DNIe..."
    status_color = config.get_color("text_primary")
    transition_time = None

    # Bucle Principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = time.time()

        if detection_result is None and (current_time - start_time) > WAIT_SECONDS:
            if detectar_dnie_hardware():
                detection_result = True
                status_message = "DNIe detectado correctamente."
                status_color = config.get_color("success")
                transition_time = current_time
            else:
                detection_result = False
                status_message = "No se ha detectado el DNIe."
                status_color = config.get_color("danger")

        if transition_time and (current_time - transition_time) > WAIT_SECONDS:
            running = False

        screen.fill(config.get_color("bg_primary"))
        text_surf = title_font.render(status_message, True, status_color)
        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(text_surf, text_rect)

        pygame.draw.rect(screen, config.get_color("border"), bar_bg_rect, 2, border_radius=5)

        if detection_result is None:
            
            elapsed = current_time - start_time
            progress = min(elapsed / WAIT_SECONDS, 1.0)
            
            current_bar_width = int(BAR_WIDTH * progress)
            bar_fill_rect = pygame.Rect(bar_x, bar_y, current_bar_width, BAR_HEIGHT)
            pygame.draw.rect(screen, config.get_color("accent_primary"), bar_fill_rect, border_radius=5)
        else:
            final_bar_color = config.get_color("success") if detection_result else config.get_color("danger")
            pygame.draw.rect(screen, final_bar_color, bar_bg_rect, border_radius=5)
        
        pygame.display.flip()

    pygame.quit()

    if detection_result:
        vdnie.iniciar_verificacion() 
    
    sys.exit()

if __name__ == "__main__":
    detectar_dnie()

