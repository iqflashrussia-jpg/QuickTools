"""
Централизованные стили для всего приложения (адаптивный дизайн)
"""

from PySide6.QtWidgets import QWidget


# Основные цвета
COLORS = {
    "bg": "#090c12",
    "panel": "#0d1118",
    "panel_2": "#0f141d",
    "border": "#1b2230",
    "text": "#f2f5f8",
    "muted": "#7f8b9b",
    "green": "#55c84f",
    "green_dark": "#45b240",
    "terminal_bg": "#0a0f15",
    "terminal_border": "#1a2230",
    "scroll_bg": "#0d1118",
    "scroll_handle": "#55c84f",
    "scroll_handle_hover": "#45b240",
}


def get_main_stylesheet():
    """Общие стили для всего приложения (адаптивные)"""
    return f"""
        /* Глобальные стили */
        QWidget {{
            background-color: {COLORS["bg"]};
            font-family: 'Inter', 'Segoe UI', 'Microsoft YaHei', sans-serif;
            color: {COLORS["text"]};
            font-size: 13px;
        }}
        
        /* ========== СКРОЛЛБАРЫ (зелёные, красивые) ========== */
        QScrollBar:vertical {{
            background-color: #FF0000;  /* ярко-красный фон */
            width: 8px;
            border-radius: 4px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: #00FF00;  /* ярко-зелёная ручка */
            border-radius: 4px;
            min-height: 40px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS["scroll_handle_hover"]};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background-color: {COLORS["scroll_bg"]};
            height: 8px;
            border-radius: 4px;
            margin: 2px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {COLORS["scroll_handle"]};
            border-radius: 4px;
            min-width: 40px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {COLORS["scroll_handle_hover"]};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        /* Специально для QTextEdit (лог) */
        QTextEdit {{
            background-color: {COLORS["terminal_bg"]};
            color: {COLORS["green"]};
            border: 1px solid {COLORS["terminal_border"]};
            border-radius: 12px;
            padding: 12px;
            font-family: 'Consolas', monospace;
            font-size: 12px;
        }}
        
        QTextEdit QScrollBar:vertical {{
            background-color: {COLORS["terminal_bg"]};
            width: 6px;
        }}
        
        QTextEdit QScrollBar::handle:vertical {{
            background-color: {COLORS["scroll_handle"]};
            border-radius: 3px;
        }}
        
        /* ========== ГЛАВНОЕ ОКНО ========== */
        QMainWindow {{
            background-color: {COLORS["bg"]};
        }}
        
        /* ========== ВКЛАДКИ ========== */
        QTabWidget::pane {{
            background-color: transparent;
            border: none;
            border-radius: 0;
        }}
        
        QTabBar::tab {{
            background-color: transparent;
            color: {COLORS["muted"]};
            padding: 8px 16px;
            margin-right: 4px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 500;
        }}
        
        QTabBar::tab:selected {{
            background-color: {COLORS["green"]};
            color: #081108;
            font-weight: 600;
        }}
        
        QTabBar::tab:hover {{
            background-color: #131a24;
            color: {COLORS["text"]};
        }}
        
        /* ========== ГРУППЫ ========== */
        QGroupBox {{
            background-color: rgba(12, 17, 24, 0.55);
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
            margin-top: 10px;
            padding-top: 12px;
            font-size: 10px;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-weight: 700;
            color: {COLORS["muted"]};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 4px;
        }}
        
        /* ========== КНОПКИ ========== */
        QPushButton {{
            background-color: {COLORS["green"]};
            color: #071107;
            border: none;
            border-radius: 10px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: 700;
        }}
        
        QPushButton:hover {{
            background-color: {COLORS["green_dark"]};
        }}
        
        QPushButton:disabled {{
            background-color: #2a3342;
            color: {COLORS["muted"]};
        }}
        
        /* Кнопка смены проекта */
        QPushButton#change_btn {{
            background-color: #2b3340;
            color: {COLORS["text"]};
            border-radius: 8px;
            padding: 6px 14px;
            font-size: 11px;
            font-weight: 500;
        }}
        
        QPushButton#change_btn:hover {{
            background-color: #394354;
        }}
        
        /* Кнопки + и - (компактные) */
        QPushButton#add_btn, QPushButton#remove_btn {{
            background-color: {COLORS["panel_2"]};
            color: {COLORS["text"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 8px;
            font-size: 14px;
            font-weight: normal;
            min-width: 28px;
            min-height: 28px;
            max-width: 28px;
            max-height: 28px;
        }}
        
        QPushButton#add_btn:hover, QPushButton#remove_btn:hover {{
            border-color: {COLORS["green"]};
            color: {COLORS["green"]};
        }}
        
        /* Кнопки в FLA блоке */
        QPushButton#search_btn {{
            background-color: {COLORS["green"]};
            color: #071107;
            border-radius: 10px;
            padding: 8px;
            font-size: 12px;
            font-weight: 700;
        }}
        
        QPushButton#search_all_btn {{
            background-color: #2196F3;
            color: white;
            border-radius: 10px;
            padding: 8px;
            font-size: 12px;
            font-weight: 700;
        }}
        
        QPushButton#search_all_btn:hover {{
            background-color: #1976D2;
        }}
        
        /* Кнопки добавления подканала/креатива */
        QPushButton#add_subchannel_btn, QPushButton#add_creative_btn {{
            background-color: #2b3340;
            color: {COLORS["green"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 8px;
            padding: 4px 12px;
            font-size: 10px;
            font-weight: 500;
        }}
        
        QPushButton#add_subchannel_btn:hover, QPushButton#add_creative_btn:hover {{
            background-color: {COLORS["green"]};
            color: #071107;
        }}
        
        /* ========== ПОЛЯ ВВОДА (компактные) ========== */
        QLineEdit {{
            background-color: {COLORS["panel"]};
            color: {COLORS["text"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 12px;
            min-height: 28px;
        }}
        
        QLineEdit:focus {{
            border-color: {COLORS["green"]};
        }}
        
        /* ========== ЧЕКБОКСЫ ========== */
        QCheckBox {{
            color: {COLORS["text"]};
            font-size: 11px;
            spacing: 6px;
        }}
        
        QCheckBox::indicator {{
            width: 14px;
            height: 14px;
            border-radius: 3px;
            border: 1px solid {COLORS["border"]};
            background-color: {COLORS["panel"]};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {COLORS["green"]};
            border-color: {COLORS["green"]};
        }}
        
        /* ========== СЛАЙДЕР ========== */
        QSlider::groove:horizontal {{
            height: 3px;
            background-color: {COLORS["border"]};
            border-radius: 1.5px;
        }}
        
        QSlider::handle:horizontal {{
            background-color: {COLORS["green"]};
            width: 12px;
            height: 12px;
            margin: -4.5px 0;
            border-radius: 6px;
        }}
        
        /* ========== КАРТОЧКИ ========== */
        QFrame#card {{
            background-color: rgba(12, 17, 24, 0.55);
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
            padding: 12px;
        }}
        
        QFrame#subchannel_card {{
            background-color: {COLORS["panel_2"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 10px;
            padding: 10px;
        }}
        
        QFrame#hint_frame {{
            background-color: rgba(12, 17, 24, 0.55);
            border: 1px solid {COLORS["border"]};
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
        }}
        
        QFrame#separator {{
            background-color: {COLORS["border"]};
            min-height: 1px;
            max-height: 1px;
        }}
        
        /* ========== ЗАГОЛОВКИ ========== */
        QLabel#block_title {{
            font-size: 20px;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: {COLORS["text"]};
            margin-bottom: 6px;
        }}
        
        QLabel#card_title {{
            color: {COLORS["muted"]};
            font-size: 9px;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        QLabel#status_text {{
            color: {COLORS["muted"]};
            font-size: 10px;
            margin-top: 6px;
        }}
        
        QLabel#platforms_label {{
            color: {COLORS["muted"]};
            font-size: 9px;
            margin: 4px 0 2px 0;
        }}
        
        QLabel#hint_title {{
            color: {COLORS["green"]};
            font-weight: 700;
            font-size: 10px;
            margin-bottom: 4px;
        }}
        
        QLabel#hint_text {{
            color: {COLORS["muted"]};
            font-size: 9px;
            line-height: 1.4;
        }}
        
        QLabel#progress_label {{
            color: {COLORS["green"]};
            font-size: 10px;
        }}
        
        /* Путь проекта */
        QLabel#project_path {{
            background-color: {COLORS["panel"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 8px;
            padding: 4px 10px;
            color: {COLORS["muted"]};
            font-size: 11px;
            font-family: monospace;
        }}
        
        /* ========== ПРОГРЕСС-БАР ========== */
        QProgressBar {{
            background-color: {COLORS["panel"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 6px;
            text-align: center;
            color: {COLORS["text"]};
            height: 16px;
            font-size: 10px;
        }}
        
        QProgressBar::chunk {{
            background-color: {COLORS["green"]};
            border-radius: 5px;
        }}
        
        /* ========== SCROLL AREA ========== */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollArea > QWidget > QWidget {{
            background-color: transparent;
        }}
    """


def apply_styles(widget):
    """Применяет общие стили к виджету"""
    if isinstance(widget, QWidget):
        widget.setStyleSheet(get_main_stylesheet())