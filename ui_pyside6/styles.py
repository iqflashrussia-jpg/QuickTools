# ui_pyside6/styles.py
"""
ДИЗАЙН-СИСТЕМА QUICKTOOLS
================================
ВСЕ визуальные параметры приложения управляются из этого файла.

КАК МЕНЯТЬ ДИЗАЙН:
1. Меняй значения в словаре COLORS (цвета)
2. Меняй значения в словаре SIZES (размеры, отступы, скругления)
3. Меняй значения в словаре SHADOWS (тени)
4. Перезапусти программу

Ничего больше менять не нужно!
"""

from PySide6.QtWidgets import QWidget

# ============================================================================
# 1. ЦВЕТОВАЯ СХЕМА - меняй здесь ВСЕ цвета приложения
# ============================================================================

COLORS = {
    # ---------------------- ФОНЫ ----------------------
    "bg_main": "#16191D",           # Главный фон окна (самый тёмный)
    "bg_card": "#181B20",           # Фон карточек/блоков
    "bg_card_secondary": "#181B20", # Фон вторичных карточек (подканалы)
    "bg_input": "#171A1F",          # Фон полей ввода
    "bg_terminal": "#0a0f15",       # Фон окна лога
    "bg_scroll": "#0d1118",         # Фон скроллбара
    "bg_tab_hover": "#131a24",      # Фон вкладки при наведении
    
    # ---------------------- ГРАНИЦЫ ----------------------
    "border_default": "#787E89",    # Цвет границ по умолчанию
    "border_terminal": "#1a2230",   # Граница окна лога
    "border_focus": "#4CAF50",      # Граница при фокусе (зелёная)
    "border_hover": "#55c84f",      # Граница при наведении
    
    # ---------------------- ТЕКСТ ----------------------
    "text_primary": "#ffffff",      # Основной текст (яркий белый) - для полей ввода
    "text_secondary": "#7f8b9b",    # Второстепенный текст (серый)
    "text_muted": "#787E89",        # Неактивный/приглушённый текст (для disabled кнопок и заголовков блоков)
    "text_disabled": "#4a5568",     # Полностью неактивный текст
    "text_on_accent": "#071107",    # Текст на акцентных кнопках (тёмный)
    "text_on_blue": "#ffffff",      # Текст на синих кнопках (белый)
    "text_terminal": "#4CAF50",     # Текст в окне лога (зелёный)
    "text_input": "#ffffff",        # Текст в полях ввода (яркий белый)
    
    # ---------------------- ИКОНКИ ----------------------
    "icon_default": "#ffffff",      # Цвет иконок по умолчанию
    "icon_hover": "#4CAF50",        # Цвет иконок при наведении на кнопку
    "icon_disabled": "#4a5568",     # Цвет неактивных иконок
    "icon_tab_selected": "#071107", # Цвет иконки на выбранной вкладке
    "icon_tab_default": "#787E89",  # Цвет иконки на обычной вкладке
    "icon_compact_default": "#7f8b9b",   # Цвет иконки на компактных кнопках (+/-)
    "icon_compact_hover": "#4CAF50",     # Цвет иконки при наведении на компактную кнопку
    
    # ---------------------- АКЦЕНТЫ (можно сменить на любой цвет) ----------------------
    "accent": "#4CAF50",            # Основной акцентный цвет (кнопки, выделения)
    "accent_hover": "#45b240",      # Акцент при наведении
    "accent_pressed": "#3da337",    # Акцент при нажатии
    "accent_disabled": "#2a3342",   # Акцент на неактивных кнопках
    
    # ---------------------- СКРОЛЛБАРЫ ----------------------
    "scroll_handle": "#4CAF50",     # Ручка скроллбара
    "scroll_handle_hover": "#45b240", # Ручка при наведении
    
    # ---------------------- КНОПКИ ----------------------
    "btn_primary_bg": "#4CAF50",    # Фон главной кнопки
    "btn_primary_hover": "#45b240", # Фон главной кнопки при наведении
    "btn_primary_text": "#071107",  # Текст главной кнопки
    
    "btn_secondary_bg": "#2b3340",  # Фон второстепенной кнопки
    "btn_secondary_hover": "#394354", # Фон второстепенной при наведении
    "btn_secondary_text": "#f2f5f8",  # Текст второстепенной кнопки
    
    "btn_compact_bg": "#0f141d",    # Фон компактных кнопок (+/-)
    "btn_compact_border": "#1b2230", # Граница компактных кнопок
    "btn_compact_hover_border": "#4CAF50", # Граница при наведении
    "btn_compact_hover_text": "#4CAF50",   # Текст при наведении
    
    # ---------------------- FLA КНОПКИ ----------------------
    "btn_fla_search_bg": "#4CAF50",  # Кнопка поиска (зелёная)
    "btn_fla_search_text": "#071107",
    "btn_fla_search_all_bg": "#2196F3",  # Кнопка "Искать всё" (синяя)
    "btn_fla_search_all_hover": "#1976D2",
    "btn_fla_search_all_text": "#ffffff",
    
    # ---------------------- ЧЕКБОКСЫ ----------------------
    "checkbox_bg": "#0d1118",        # Фон чекбокса
    "checkbox_border": "#1b2230",    # Граница чекбокса
    "checkbox_checked_bg": "#4CAF50", # Фон отмеченного чекбокса
    "checkbox_size": "14px",         # Размер чекбокса
    "checkbox_radius": "3px",        # Скругление чекбокса
    
    # ---------------------- СЛАЙДЕР ----------------------
    "slider_groove_bg": "#1b2230",   # Фон дорожки слайдера
    "slider_handle_bg": "#4CAF50",   # Цвет ползунка
    "slider_groove_height": "3px",   # Высота дорожки
    "slider_handle_size": "12px",    # Размер ползунка
    
    # ---------------------- ПРОГРЕСС-БАР ----------------------
    "progress_bg": "#0d1118",        # Фон прогресс-бара
    "progress_border": "#1b2230",    # Граница прогресс-бара
    "progress_chunk_bg": "#4CAF50",  # Заполненная часть
    "progress_text_align": "center", # Выравнивание текста
    
    # ---------------------- РАЗДЕЛИТЕЛИ ----------------------
    "separator_bg": "#1b2230",       # Цвет линии-разделителя
    
    # ---------------------- СТАТУСЫ ----------------------
    "status_success": "#2ea043",     # Зелёный (успех)
    "status_warning": "#e3b341",     # Жёлтый (предупреждение)
    "status_error": "#f85149",       # Красный (ошибка)
    "status_info": "#58a6ff",        # Синий (информация)
    
    # ---------------------- ЭФЕКТЫ ----------------------
    "card_overlay": "rgba(12, 17, 24, 0.55)",  # Прозрачный слой для карточек
    
    # ---------------------- ТЕНИ ----------------------
    "shadow_color": "0, 0, 0",      # Цвет тени (RGB без скобок)
    "shadow_opacity": 80,            # Прозрачность тени (0-255, 80 = полупрозрачная)
}


# ============================================================================
# 2. РАЗМЕРЫ И ОТСТУПЫ - меняй здесь ВСЕ размеры
# ============================================================================

SIZES = {
    # ---------------------- СКРУГЛЕНИЯ ----------------------
    "radius_small": "4px",      # Маленькие элементы (кнопки +/-)
    "radius_medium": "8px",     # Средние (поля ввода, обычные кнопки)
    "radius_large": "10px",     # Большие (кнопка "Создать")
    "radius_xl": "12px",        # Очень большие (карточки, лог)
    "radius_circle": "6px",     # Полностью круглые (ползунки)
    "radius_scrollbar": "4px",  # Скругление скроллбара
    "radius_scrollbar_handle": "3px", # Скругление ручки скроллбара внутри лога
    
    # ---------------------- ОТСТУПЫ (padding) ----------------------
    "padding_none": "0px",
    "padding_tiny": "2px 4px",
    "padding_small": "4px 8px",      # Маленькие элементы
    "padding_small_wide": "4px 12px", # Широкие маленькие отступы (для кнопок)
    "padding_medium": "6px 10px",    # Поля ввода
    "padding_large": "8px 12px",     # Обычные кнопки
    "padding_xl": "12px 16px",       # Карточки
    "padding_xxl": "12px 20px",      # Крупные кнопки
    
    # ---------------------- ОТСТУПЫ (margin) ----------------------
    "margin_scrollbar": "2px",       # Отступ скроллбара
    "margin_groupbox_top": "10px",   # Отступ сверху у GroupBox
    "margin_tab_right": "4px",       # Отступ между вкладками
    "margin_slider_handle": "-4.5px 0", # Отступ ползунка слайдера
    
    # ---------------------- РАЗМЕРЫ ЭЛЕМЕНТОВ ----------------------
    "input_height": "28px",          # Высота полей ввода
    "input_min_height": "28px",
    
    "btn_height": "32px",            # Высота обычных кнопок
    "btn_min_height": "32px",
    
    "btn_compact_size": "28px",      # Размер кнопок +/- (ширина и высота)
    "btn_compact_icon_size": "14px", # Размер иконки на компактных кнопках
    
    "btn_large_height": "40px",      # Высота большой кнопки "Создать"
    
    "scrollbar_width": "8px",        # Ширина вертикального скроллбара
    "scrollbar_height": "8px",       # Высота горизонтального скроллбара
    "scrollbar_handle_min": "40px",  # Минимальная высота ручки
    
    "checkbox_size": "14px",         # Размер чекбокса
    "checkbox_radius": "3px",        # Скругление чекбокса
    
    "slider_groove_height": "3px",   # Высота дорожки слайдера
    "slider_handle_size": "12px",    # Размер ползунка
    
    "progress_height": "16px",       # Высота прогресс-бара
    "progress_radius": "6px",        # Скругление прогресс-бара
    "progress_chunk_radius": "5px",  # Скругление заполненной части
    
    "terminal_padding": "12px",      # Отступы в логе
    "terminal_max_height": "150px",  # Максимальная высота лога
    
    # ---------------------- ШРИФТЫ ----------------------
    "font_family": "'Inter', 'Segoe UI', 'Microsoft YaHei', sans-serif",
    "font_family_mono": "'Consolas', 'Courier New', monospace",
    
    "font_size_tiny": "9px",         # Очень мелкий текст (подписи)
    "font_size_small": "11px",       # Мелкий текст (вкладки, кнопки)
    "font_size_normal": "11px",      # Обычный текст
    "font_size_body": "12px",        # Текст в полях ввода
    "font_size_medium": "13px",      # Основной текст
    "font_size_large": "14px",       # Крупный текст
    "font_size_xl": "16px",          # Заголовки вкладок
    "font_size_xxl": "20px",         # Заголовки блоков
    "font_size_compact_btn": "14px", # Размер иконки на компактных кнопках
    "font_size_tab": "12px",         # Размер шрифта вкладок (отдельно)
    
    "font_weight_normal": "400",
    "font_weight_medium": "500",
    "font_weight_semibold": "600",
    "font_weight_bold": "700",
    "font_weight_extrabold": "800",
    
    "letter_spacing_tiny": "1px",    # Межбуквенное расстояние для заголовков
    "letter_spacing_block": "-0.5px", # Межбуквенное расстояние для block_title
    
    "line_height_default": "1.4",    # Стандартная высота строки
    
    # ---------------------- ОТСТУПЫ МЕЖДУ ЭЛЕМЕНТАМИ (spacing) ----------------------
    "spacing_tiny": "4px",
    "spacing_small": "6px",
    "spacing_normal": "8px",
    "spacing_medium": "10px",
    "spacing_large": "12px",
    "spacing_xl": "15px",
    "spacing_xxl": "20px",
    
    # ---------------------- ГРАНИЦЫ (border width) ----------------------
    "border_width_default": "1px",
    "border_width_focus": "1px",
    "border_width_hover": "1px",
    
    # ---------------------- ДРУГОЕ ----------------------
    "terminal_font_size": "12px",
    "progress_text_align": "center", # Выравнивание текста в прогресс-баре
}


# ============================================================================
# 2.5. ТЕНИ - меняй здесь ВСЕ параметры теней
# ============================================================================

SHADOWS = {
    # Тень для карточек (основные блоки)
    "card": {
        "blur": 15,                 # Размытие тени (пиксели, больше = мягче)
        "offset_x": 0,              # Смещение по X (0 = по центру)
        "offset_y": 4,              # Смещение по Y (положительное = вниз)
        "opacity": 80,              # Прозрачность (0-255, 80 = полупрозрачная)
    },
    
    # Тень для карточек подканалов (вторичные блоки)
    "subchannel": {
        "blur": 10,
        "offset_x": 0,
        "offset_y": 2,
        "opacity": 80,
    },
    
    # Тень для кнопок при наведении (эффект поднятия)
    "button_hover": {
        "blur": 8,
        "offset_x": 0,
        "offset_y": 2,
        "opacity": 60,
    },
}


# ============================================================================
# 3. ГЕНЕРАЦИЯ СТИЛЕЙ (не трогать, если не уверен)
# ============================================================================

def get_main_stylesheet():
    """Генерирует полный CSS/QSS из словарей COLORS и SIZES"""
    
    c = COLORS
    s = SIZES
    
    return f"""
        /* ----------------------------------------------------------------------
           ГЛОБАЛЬНЫЕ СТИЛИ
        ---------------------------------------------------------------------- */
        QWidget {{
            background-color: {c["bg_main"]};
            font-family: {s["font_family"]};
            color: {c["text_primary"]};
            font-size: {s["font_size_medium"]};
        }}
        
        /* ----------------------------------------------------------------------
           ИКОНКИ (глобальные настройки)
        ---------------------------------------------------------------------- */
        TablerQIcon {{
            color: {c["icon_default"]};
        }}
        
        /* ----------------------------------------------------------------------
           СКРОЛЛБАРЫ
        ---------------------------------------------------------------------- */
        QScrollBar:vertical {{
            background-color: {c["bg_scroll"]};
            width: {s["scrollbar_width"]};
            border-radius: {s["radius_scrollbar"]};
            margin: {s["margin_scrollbar"]};
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {c["scroll_handle"]};
            border-radius: {s["radius_scrollbar"]};
            min-height: {s["scrollbar_handle_min"]};
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {c["scroll_handle_hover"]};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background-color: {c["bg_scroll"]};
            height: {s["scrollbar_height"]};
            border-radius: {s["radius_scrollbar"]};
            margin: {s["margin_scrollbar"]};
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {c["scroll_handle"]};
            border-radius: {s["radius_scrollbar"]};
            min-width: {s["scrollbar_handle_min"]};
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {c["scroll_handle_hover"]};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        /* Стили скроллбаров внутри QTextEdit */
        QTextEdit QScrollBar:vertical {{
            background-color: {c["bg_terminal"]};
            width: {s["scrollbar_width"]};
        }}
        
        QTextEdit QScrollBar::handle:vertical {{
            background-color: {c["scroll_handle"]};
            border-radius: {s["radius_scrollbar_handle"]};
        }}
        
        /* ----------------------------------------------------------------------
           ТЕКСТОВЫЕ ПОЛЯ (лог)
        ---------------------------------------------------------------------- */
        QTextEdit {{
            background-color: {c["bg_terminal"]};
            color: {c["text_terminal"]};
            border: {s["border_width_default"]} solid {c["border_terminal"]};
            border-radius: {s["radius_xl"]};
            padding: {s["terminal_padding"]};
            font-family: {s["font_family_mono"]};
            font-size: {s["terminal_font_size"]};
            line-height: {s["line_height_default"]};
        }}
        
        /* ----------------------------------------------------------------------
           ВКЛАДКИ (Tabs)
        ---------------------------------------------------------------------- */
        QTabWidget::pane {{
            background-color: transparent;
            border: none;
        }}
        
        QTabBar::tab {{
            background-color: transparent;
            color: {c["text_muted"]};
            padding: {s["padding_large"]};
            margin-right: {s["margin_tab_right"]};
            border-radius: {s["radius_medium"]};
            font-size: {s["font_size_tab"]};
            font-weight: {s["font_weight_medium"]};
        }}
        
        QTabBar::tab:selected {{
            background-color: {c["accent"]};
            color: {c["text_on_accent"]};
            font-weight: {s["font_weight_semibold"]};
        }}
        
        QTabBar::tab:hover {{
            background-color: {c["bg_tab_hover"]};
            color: {c["text_primary"]};
        }}
        
        QTabBar::tab:disabled {{
            color: {c["text_muted"]};
        }}
        
        /* Иконки на вкладках */
        QTabBar::tab TablerQIcon {{
            color: {c["icon_tab_default"]};
        }}
        
        QTabBar::tab:selected TablerQIcon {{
            color: {c["icon_tab_selected"]};
        }}
        
        QTabBar::tab:hover TablerQIcon {{
            color: {c["icon_hover"]};
        }}
        
        /* ----------------------------------------------------------------------
           ГРУППЫ (GroupBox)
        ---------------------------------------------------------------------- */
        QGroupBox {{
            background-color: {c["bg_card"]};
            border: {s["border_width_default"]} solid {c["border_default"]};
            border-radius: {s["radius_xl"]};
            margin-top: {s["margin_groupbox_top"]};
            padding-top: {s["spacing_large"]};
            font-size: {s["font_size_tiny"]};
            letter-spacing: {s["letter_spacing_tiny"]};
            text-transform: uppercase;
            font-weight: {s["font_weight_bold"]};
            color: {c["text_muted"]};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {s["spacing_large"]};
            padding: 0 {s["spacing_tiny"]};
            background-color: transparent;
            color: {c["text_muted"]};
        }}
        
        /* ----------------------------------------------------------------------
           КНОПКИ (ОСНОВНЫЕ)
        ---------------------------------------------------------------------- */
        QPushButton {{
            background-color: {c["btn_primary_bg"]};
            color: {c["btn_primary_text"]};
            border: none;
            border-radius: {s["radius_large"]};
            padding: {s["padding_large"]};
            font-size: {s["font_size_normal"]};
            font-weight: {s["font_weight_bold"]};
            min-height: {s["btn_min_height"]};
        }}
        
        QPushButton:hover {{
            background-color: {c["btn_primary_hover"]};
        }}
        
        QPushButton:pressed {{
            background-color: {c["accent_pressed"]};
        }}
        
        QPushButton:disabled {{
            background-color: {c["accent_disabled"]};
            color: {c["text_muted"]};
        }}
        
        /* Иконки на основных кнопках */
        QPushButton TablerQIcon {{
            color: {c["btn_primary_text"]};
        }}
        
        QPushButton:hover TablerQIcon {{
            color: {c["icon_hover"]};
        }}
        
        QPushButton:disabled TablerQIcon {{
            color: {c["icon_disabled"]};
        }}
        
        /* Кнопка "Сменить проект" */
        QPushButton#change_btn {{
            background-color: {c["btn_secondary_bg"]};
            color: {c["btn_secondary_text"]};
            border-radius: {s["radius_small"]};
            padding: {s["padding_tiny"]};
            font-size: {s["font_size_normal"]};
            font-weight: {s["font_weight_medium"]};
        }}
        
        QPushButton#change_btn:hover {{
            background-color: {c["btn_secondary_hover"]};
        }}
        
        /* Иконки на кнопке "Сменить проект" */
        QPushButton#change_btn TablerQIcon {{
            color: {c["btn_secondary_text"]};
        }}
        
        QPushButton#change_btn:hover TablerQIcon {{
            color: {c["icon_hover"]};
        }}
        
        /* Компактные кнопки (+ и -) */
        QPushButton#add_btn, QPushButton#remove_btn {{
            background-color: {c["btn_compact_bg"]};
            color: {c["text_secondary"]};
            border: {s["border_width_default"]} solid {c["btn_compact_border"]};
            border-radius: {s["radius_small"]};
            font-size: {s["font_size_compact_btn"]};
            font-weight: {s["font_weight_normal"]};
            min-width: {s["btn_compact_size"]};
            min-height: {s["btn_compact_size"]};
            max-width: {s["btn_compact_size"]};
            max-height: {s["btn_compact_size"]};
        }}
        
        QPushButton#add_btn:hover, QPushButton#remove_btn:hover {{
            border-color: {c["btn_compact_hover_border"]};
            color: {c["btn_compact_hover_text"]};
        }}
        
        /* Иконки на компактных кнопках */
        QPushButton#add_btn TablerQIcon, QPushButton#remove_btn TablerQIcon {{
            color: {c["icon_compact_default"]};
        }}
        
        QPushButton#add_btn:hover TablerQIcon, QPushButton#remove_btn:hover TablerQIcon {{
            color: {c["icon_compact_hover"]};
        }}
        
        /* Кнопки в FLA блоке */
        QPushButton#search_btn {{
            background-color: {c["btn_fla_search_bg"]};
            color: {c["btn_fla_search_text"]};
            border-radius: {s["radius_large"]};
            padding: {s["padding_large"]};
            font-size: {s["font_size_normal"]};
            font-weight: {s["font_weight_bold"]};
        }}
        
        QPushButton#search_all_btn {{
            background-color: {c["btn_fla_search_all_bg"]};
            color: {c["btn_fla_search_all_text"]};
            border-radius: {s["radius_large"]};
            padding: {s["padding_large"]};
            font-size: {s["font_size_normal"]};
            font-weight: {s["font_weight_bold"]};
        }}
        
        QPushButton#search_all_btn:hover {{
            background-color: {c["btn_fla_search_all_hover"]};
        }}
        
        /* Иконки на FLA кнопках */
        QPushButton#search_btn TablerQIcon {{
            color: {c["btn_fla_search_text"]};
        }}
        
        QPushButton#search_all_btn TablerQIcon {{
            color: {c["btn_fla_search_all_text"]};
        }}
        
        QPushButton#search_all_btn:hover TablerQIcon {{
            color: {c["icon_hover"]};
        }}
        
        /* Кнопки добавления подканала/креатива */
        QPushButton#add_subchannel_btn, QPushButton#add_creative_btn {{
            background-color: {c["btn_secondary_bg"]};
            color: {c["accent"]};
            border: {s["border_width_default"]} solid {c["border_default"]};
            border-radius: {s["radius_small"]};
            padding: {s["padding_small_wide"]};
            font-size: {s["font_size_small"]};
            font-weight: {s["font_weight_medium"]};
        }}
        
        QPushButton#add_subchannel_btn:hover, QPushButton#add_creative_btn:hover {{
            background-color: {c["accent"]};
            color: {c["text_on_accent"]};
        }}
        
        /* Иконки на кнопках добавления */
        QPushButton#add_subchannel_btn TablerQIcon, QPushButton#add_creative_btn TablerQIcon {{
            color: {c["accent"]};
        }}
        
        QPushButton#add_subchannel_btn:hover TablerQIcon, QPushButton#add_creative_btn:hover TablerQIcon {{
            color: {c["text_on_accent"]};
        }}
        
        /* ----------------------------------------------------------------------
           ПОЛЯ ВВОДА
        ---------------------------------------------------------------------- */
        QLineEdit {{
            background-color: {c["bg_input"]};
            color: {c["text_input"]};
            border: {s["border_width_default"]} solid {c["border_default"]};
            border-radius: {s["radius_medium"]};
            padding: {s["padding_medium"]};
            font-size: {s["font_size_body"]};
            min-height: {s["input_min_height"]};
        }}
        
        QLineEdit:focus {{
            border-color: {c["border_focus"]};
            border-width: {s["border_width_focus"]};
        }}
        
        QLineEdit:hover {{
            border-color: {c["border_hover"]};
        }}
        
        /* ----------------------------------------------------------------------
           ЧЕКБОКСЫ
        ---------------------------------------------------------------------- */
        QCheckBox {{
            color: {c["text_primary"]};
            font-size: {s["font_size_normal"]};
            spacing: {s["spacing_small"]};
        }}
        
        QCheckBox::indicator {{
            width: {c["checkbox_size"]};
            height: {c["checkbox_size"]};
            border-radius: {c["checkbox_radius"]};
            border: {s["border_width_default"]} solid {c["checkbox_border"]};
            background-color: {c["checkbox_bg"]};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {c["checkbox_checked_bg"]};
            border-color: {c["checkbox_checked_bg"]};
        }}
        
        /* ----------------------------------------------------------------------
           СЛАЙДЕР
        ---------------------------------------------------------------------- */
        QSlider::groove:horizontal {{
            height: {s["slider_groove_height"]};
            background-color: {c["slider_groove_bg"]};
            border-radius: {s["radius_circle"]};
        }}
        
        QSlider::handle:horizontal {{
            background-color: {c["slider_handle_bg"]};
            width: {s["slider_handle_size"]};
            height: {s["slider_handle_size"]};
            margin: {s["margin_slider_handle"]};
            border-radius: {s["radius_circle"]};
        }}
        
        /* ----------------------------------------------------------------------
           КАРТОЧКИ И КОНТЕЙНЕРЫ
        ---------------------------------------------------------------------- */
        QFrame#card {{
            background-color: {c["bg_card"]};
            border: none;
            border-radius: {s["radius_xl"]};
            padding: {s["padding_xl"]};
        }}
        
        QFrame#subchannel_card {{
            background-color: {c["bg_card_secondary"]};
            border: {s["border_width_default"]} solid {c["border_default"]};
            border-radius: {s["radius_large"]};
            padding: {s["padding_large"]};
        }}
        
        QFrame#hint_frame {{
            background-color: {c["bg_card"]};
            border: {s["border_width_default"]} solid {c["border_default"]};
            border-radius: {s["radius_large"]};
            padding: {s["padding_large"]};
            margin-top: {s["spacing_large"]};
        }}
        
        QFrame#separator {{
            background-color: {c["separator_bg"]};
            min-height: {s["border_width_default"]};
            max-height: {s["border_width_default"]};
        }}
        
        /* ----------------------------------------------------------------------
           ЗАГОЛОВКИ И ТЕКСТОВЫЕ МЕТКИ
        ---------------------------------------------------------------------- */
        QLabel#block_title {{
            font-size: {s["font_size_xxl"]};
            font-weight: {s["font_weight_extrabold"]};
            letter-spacing: {s["letter_spacing_block"]};
            color: {c["text_primary"]};
            margin-bottom: {s["spacing_small"]};
        }}
        
        QLabel#card_title {{
            color: {c["text_muted"]};
            font-size: {s["font_size_tiny"]};
            letter-spacing: {s["letter_spacing_tiny"]};
            text-transform: uppercase;
            font-weight: {s["font_weight_bold"]};
            margin-bottom: {s["spacing_large"]};
            background-color: transparent;
            border: none;
        }}
        
        QLabel#status_text {{
            color: {c["text_secondary"]};
            font-size: {s["font_size_small"]};
            margin-top: {s["spacing_small"]};
        }}
        
        QLabel#platforms_label {{
            color: {c["text_secondary"]};
            font-size: {s["font_size_tiny"]};
            margin: {s["spacing_tiny"]} 0 {s["spacing_tiny"]} 0;
        }}
        
        QLabel#hint_title {{
            color: {c["accent"]};
            font-weight: {s["font_weight_bold"]};
            font-size: {s["font_size_small"]};
            margin-bottom: {s["spacing_tiny"]};
        }}
        
        QLabel#hint_text {{
            color: {c["text_secondary"]};
            font-size: {s["font_size_tiny"]};
            line-height: {s["line_height_default"]};
        }}
        
        QLabel#progress_label {{
            color: {c["accent"]};
            font-size: {s["font_size_small"]};
        }}
        
        /* Путь к проекту */
        QLabel#project_path {{
            background-color: {c["bg_input"]};
            border: {s["border_width_default"]} solid {c["border_default"]};
            border-radius: {s["radius_medium"]};
            padding: {s["padding_small"]};
            color: {c["text_secondary"]};
            font-size: {s["font_size_normal"]};
            font-family: {s["font_family_mono"]};
        }}
        
        /* ----------------------------------------------------------------------
           ПРОГРЕСС-БАР
        ---------------------------------------------------------------------- */
        QProgressBar {{
            background-color: {c["progress_bg"]};
            border: {s["border_width_default"]} solid {c["progress_border"]};
            border-radius: {s["progress_radius"]};
            text-align: {s["progress_text_align"]};
            color: {c["text_primary"]};
            height: {s["progress_height"]};
            font-size: {s["font_size_small"]};
        }}
        
        QProgressBar::chunk {{
            background-color: {c["progress_chunk_bg"]};
            border-radius: {s["progress_chunk_radius"]};
        }}
        
        /* ----------------------------------------------------------------------
           SCROLL AREA
        ---------------------------------------------------------------------- */
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