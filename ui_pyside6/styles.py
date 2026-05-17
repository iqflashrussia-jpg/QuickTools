"""
Централизованные стили для всего приложения
"""

from PySide6.QtWidgets import QWidget


# Основные цвета
COLORS = {
    "primary": "#4CAF50",
    "primary_hover": "#45a049",
    "error": "#FF453A",
    "error_hover": "#E03A2E",
    "warning": "#FFA500",
    "success": "#4CAF50",
    "info": "#2196F3",
    "info_hover": "#1976D2",
    
    "bg_main": "#0A0A0A",
    "bg_card": "#1E1E1E",
    "bg_input": "#2A2A2A",
    "bg_hover": "#3A3A3A",
    "bg_log": "#1A1A1A",
    "border": "#3A3A3A",
    
    "text_primary": "#FFFFFF",
    "text_secondary": "#888888",
    "text_log": "#00FF00",
}


def get_main_stylesheet():
    """Общие стили для всего приложения"""
    return f"""
        QTabWidget::pane {{
            background-color: {COLORS["bg_card"]};
            border-radius: 8px;
            border: 1px solid {COLORS["border"]};
        }}
        
        QTabBar::tab {{
            background-color: {COLORS["bg_input"]};
            color: {COLORS["text_primary"]};
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {COLORS["primary"]};
        }}
        
        QTabBar::tab:hover {{
            background-color: {COLORS["bg_hover"]};
        }}
        
        QGroupBox {{
            color: {COLORS["text_primary"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            font-size: 14px;
            font-weight: bold;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
        
        QPushButton#run_btn, QPushButton#create_btn, 
        QPushButton#archive_btn, QPushButton#rename_btn,
        QPushButton#search_btn {{
            background-color: {COLORS["primary"]};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
        }}
        
        QPushButton#run_btn:hover, QPushButton#create_btn:hover,
        QPushButton#archive_btn:hover, QPushButton#rename_btn:hover,
        QPushButton#search_btn:hover {{
            background-color: {COLORS["primary_hover"]};
        }}
        
        QPushButton#run_btn:disabled, QPushButton#create_btn:disabled,
        QPushButton#archive_btn:disabled, QPushButton#rename_btn:disabled,
        QPushButton#search_btn:disabled {{
            background-color: #666;
        }}
        
        QPushButton#delete_btn {{
            background-color: {COLORS["error"]};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
        }}
        
        QPushButton#delete_btn:hover {{
            background-color: {COLORS["error_hover"]};
        }}
        
        QPushButton#search_all_btn {{
            background-color: {COLORS["info"]};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
        }}
        
        QPushButton#search_all_btn:hover {{
            background-color: {COLORS["info_hover"]};
        }}
        
        QPushButton#change_btn {{
            background-color: {COLORS["bg_hover"]};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
        }}
        
        QPushButton#add_btn {{
            background-color: {COLORS["success"]};
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
            min-width: 30px;
            min-height: 30px;
            max-width: 30px;
            max-height: 30px;
        }}
        
        QPushButton#add_btn:hover {{
            background-color: {COLORS["primary_hover"]};
        }}
        
        QPushButton#remove_btn {{
            background-color: {COLORS["error"]};
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
            min-width: 30px;
            min-height: 30px;
            max-width: 30px;
            max-height: 30px;
        }}
        
        QPushButton#remove_btn:hover {{
            background-color: {COLORS["error_hover"]};
        }}
        
        QPushButton#add_subchannel_btn, QPushButton#add_creative_btn {{
            background-color: {COLORS["bg_hover"]};
            color: {COLORS["primary"]};
            border: 1px solid {COLORS["primary"]};
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 12px;
        }}
        
        QPushButton#add_subchannel_btn:hover, QPushButton#add_creative_btn:hover {{
            background-color: {COLORS["primary"]};
            color: white;
        }}
        
        QLineEdit, QSlider {{
            background-color: {COLORS["bg_input"]};
            color: {COLORS["text_primary"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
        }}
        
        QLineEdit:focus {{
            border: 1px solid {COLORS["primary"]};
        }}
        
        QTextEdit#log {{
            background-color: {COLORS["bg_log"]};
            color: {COLORS["text_log"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 6px;
            font-family: monospace;
            font-size: 12px;
        }}
        
        QCheckBox {{
            color: {COLORS["text_primary"]};
            font-size: 12px;
        }}
        
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
        }}
        
        QLabel#project_path {{
            color: {COLORS["primary"]};
            font-family: monospace;
        }}
        
        QLabel#block_title {{
            font-size: 18px;
            font-weight: bold;
            color: {COLORS["primary"]};
        }}
        
        QLabel#card_title {{
            color: {COLORS["primary"]};
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        QLabel#platforms_label {{
            color: {COLORS["text_secondary"]};
            font-size: 12px;
            margin-top: 5px;
        }}
        
        QLabel#status_text {{
            color: {COLORS["text_secondary"]};
            font-size: 12px;
            margin-top: 10px;
        }}
        
        QFrame#card {{
            background-color: {COLORS["bg_card"]};
            border-radius: 12px;
            padding: 15px;
        }}
        
        QFrame#subchannel_card {{
            background-color: {COLORS["bg_input"]};
            border-radius: 8px;
            border: 1px solid {COLORS["border"]};
        }}
        
        QFrame#hint_frame {{
            background-color: {COLORS["bg_log"]};
            border-radius: 8px;
            padding: 10px;
            margin-top: 10px;
        }}
        
        QLabel#hint_title {{
            color: {COLORS["warning"]};
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        QLabel#hint_text {{
            color: {COLORS["text_secondary"]};
            font-size: 11px;
        }}
        
        QLabel#progress_label {{
            color: {COLORS["primary"]};
            font-size: 11px;
        }}
        
        QProgressBar {{
            background-color: {COLORS["bg_input"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 4px;
            text-align: center;
            color: {COLORS["text_primary"]};
        }}
        
        QProgressBar::chunk {{
            background-color: {COLORS["primary"]};
            border-radius: 3px;
        }}
    """


def apply_styles(widget):
    """Применяет общие стили к виджету"""
    if isinstance(widget, QWidget):
        widget.setStyleSheet(get_main_stylesheet())