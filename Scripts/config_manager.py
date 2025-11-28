"""
Sistema de Configuración y Gestión de Temas
Maneja las preferencias del usuario y persistencia de configuración
"""
import json
import os
from typing import Dict, Any

class ThemeColors:
    """Define los esquemas de color para diferentes temas"""
    
    DARK_THEME = {
        "name": "Dark",
        "bg_primary": (25, 28, 33),
        "bg_secondary": (34, 38, 43),
        "bg_tertiary": (43, 48, 53),
        "bg_hover": (52, 58, 64),
        "text_primary": (239, 239, 239),
        "text_secondary": (173, 181, 189),
        "text_disabled": (108, 117, 125),
        "accent_primary": (0, 123, 255),
        "accent_secondary": (102, 178, 255),
        "success": (25, 135, 84),
        "success_hover": (21, 115, 71),
        "danger": (220, 53, 69),
        "danger_hover": (187, 45, 59),
        "warning": (255, 193, 7),
        "info": (23, 162, 184),
        "border": (52, 58, 64),
        "border_light": (73, 80, 87),
        "shadow": (0, 0, 0, 100),
        "overlay": (0, 0, 0, 180)
    }
    
    LIGHT_THEME = {
        "name": "Light",
        "bg_primary": (248, 249, 250),
        "bg_secondary": (255, 255, 255),
        "bg_tertiary": (241, 243, 245),
        "bg_hover": (233, 236, 239),
        "text_primary": (33, 37, 41),
        "text_secondary": (73, 80, 87),
        "text_disabled": (173, 181, 189),
        "accent_primary": (0, 123, 255),
        "accent_secondary": (0, 86, 179),
        "success": (40, 167, 69),
        "success_hover": (33, 136, 56),
        "danger": (220, 53, 69),
        "danger_hover": (200, 35, 51),
        "warning": (255, 193, 7),
        "info": (23, 162, 184),
        "border": (222, 226, 230),
        "border_light": (206, 212, 218),
        "shadow": (0, 0, 0, 50),
        "overlay": (0, 0, 0, 120)
    }
    
    BLUE_THEME = {
        "name": "Ocean Blue",
        "bg_primary": (15, 23, 42),
        "bg_secondary": (30, 41, 59),
        "bg_tertiary": (51, 65, 85),
        "bg_hover": (71, 85, 105),
        "text_primary": (248, 250, 252),
        "text_secondary": (203, 213, 225),
        "text_disabled": (148, 163, 184),
        "accent_primary": (56, 189, 248),
        "accent_secondary": (14, 165, 233),
        "success": (34, 197, 94),
        "success_hover": (22, 163, 74),
        "danger": (239, 68, 68),
        "danger_hover": (220, 38, 38),
        "warning": (251, 191, 36),
        "info": (96, 165, 250),
        "border": (51, 65, 85),
        "border_light": (71, 85, 105),
        "shadow": (0, 0, 0, 120),
        "overlay": (15, 23, 42, 200)
    }
    
    PURPLE_THEME = {
        "name": "Purple Night",
        "bg_primary": (24, 24, 37),
        "bg_secondary": (40, 37, 53),
        "bg_tertiary": (58, 53, 74),
        "bg_hover": (76, 70, 95),
        "text_primary": (241, 234, 255),
        "text_secondary": (196, 181, 253),
        "text_disabled": (139, 124, 175),
        "accent_primary": (168, 85, 247),
        "accent_secondary": (147, 51, 234),
        "success": (34, 197, 94),
        "success_hover": (22, 163, 74),
        "danger": (244, 63, 94),
        "danger_hover": (225, 29, 72),
        "warning": (251, 191, 36),
        "info": (168, 85, 247),
        "border": (58, 53, 74),
        "border_light": (76, 70, 95),
        "shadow": (0, 0, 0, 130),
        "overlay": (24, 24, 37, 210)
    }
    
    GREEN_THEME = {
        "name": "Forest Green",
        "bg_primary": (17, 24, 28),
        "bg_secondary": (26, 46, 42),
        "bg_tertiary": (39, 68, 61),
        "bg_hover": (52, 89, 79),
        "text_primary": (236, 253, 245),
        "text_secondary": (167, 243, 208),
        "text_disabled": (110, 168, 140),
        "accent_primary": (52, 211, 153),
        "accent_secondary": (16, 185, 129),
        "success": (34, 197, 94),
        "success_hover": (22, 163, 74),
        "danger": (248, 113, 113),
        "danger_hover": (239, 68, 68),
        "warning": (251, 191, 36),
        "info": (52, 211, 153),
        "border": (39, 68, 61),
        "border_light": (52, 89, 79),
        "shadow": (0, 0, 0, 140),
        "overlay": (17, 24, 28, 220)
    }

class ConfigManager:
    """Gestiona la configuración de la aplicación"""
    
    DEFAULT_CONFIG = {
        "theme": "Dark",
        "font_size": "medium",  # small, medium, large
        "animations_enabled": True,
        "auto_copy_timeout": 30,
        "password_auto_hide_seconds": 15,  # Segundos antes de ocultar contraseña automáticamente
        "password_min_length": 15,  # Longitud mínima de contraseñas
        "password_max_length": 32,  # Longitud máxima de contraseñas
        "show_password_strength": True,
        "compact_view": False,
        "auto_lock_timeout": 300,  # segundos
        "show_notifications": True,
        "language": "es",
        "items_per_page": 20,
        "sort_by": "nombre",  # nombre, fecha_creacion, fecha_modificacion
        "sort_order": "asc"  # asc, desc
    }
    
    THEMES = {
        "Dark": ThemeColors.DARK_THEME,
        "Light": ThemeColors.LIGHT_THEME,
        "Ocean Blue": ThemeColors.BLUE_THEME,
        "Purple Night": ThemeColors.PURPLE_THEME,
        "Forest Green": ThemeColors.GREEN_THEME
    }
    
    def __init__(self, config_file: str = "app_config.json"):
        self.config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.config = self.load_config()
        self.current_theme = self.THEMES[self.config["theme"]]
    
    def load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde el archivo o crea una por defecto"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Mezcla con valores por defecto para nuevas opciones
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(loaded)
                    return config
            except Exception:
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Guarda la configuración actual en el archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def set_theme(self, theme_name: str):
        """Cambia el tema de la aplicación"""
        if theme_name in self.THEMES:
            self.config["theme"] = theme_name
            self.current_theme = self.THEMES[theme_name]
            self.save_config()
            return True
        return False
    
    def get_color(self, color_name: str):
        """Obtiene un color del tema actual"""
        return self.current_theme.get(color_name, (255, 255, 255))
    
    def get_theme_names(self):
        """Retorna la lista de temas disponibles"""
        return list(self.THEMES.keys())
    
    def set_value(self, key: str, value: Any):
        """Establece un valor de configuración"""
        if key in self.config:
            self.config[key] = value
            self.save_config()
            return True
        return False
    
    def get_value(self, key: str, default=None):
        """Obtiene un valor de configuración"""
        return self.config.get(key, default)
    
    def get_font_sizes(self):
        """Retorna los tamaños de fuente según la configuración"""
        size_map = {
            "small": {"title": 32, "subtitle": 20, "normal": 18, "small": 14},
            "medium": {"title": 40, "subtitle": 24, "normal": 22, "small": 16},
            "large": {"title": 48, "subtitle": 28, "normal": 26, "small": 18}
        }
        return size_map.get(self.config["font_size"], size_map["medium"])
    
    def reset_to_defaults(self):
        """Restaura la configuración por defecto"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.current_theme = self.THEMES[self.config["theme"]]
        self.save_config()
