"""
Просмотр всех стандартных иконок Qt
"""

import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QStyle,
    QVBoxLayout,
    QWidget,
)


class IconViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Стандартные иконки Qt")
        self.resize(500, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll_layout = QVBoxLayout(content)
        
        # Список всех доступных иконок
        icons_list = [
            ('add (новая папка)', 'SP_FileDialogNewFolder'),
            ('remove (корзина)', 'SP_TrashIcon'),
            ('play (воспроизведение)', 'SP_MediaPlay'),
            ('search (поиск)', 'SP_FileDialogContentsView'),
            ('folder (папка)', 'SP_DirIcon'),
            ('file (файл)', 'SP_FileIcon'),
            ('settings (настройки)', 'SP_FileDialogDetailedView'),
            ('apply (применить)', 'SP_DialogApplyButton'),
            ('cancel (отмена)', 'SP_DialogCancelButton'),
            ('save (сохранить)', 'SP_DialogSaveButton'),
            ('open (открыть)', 'SP_DialogOpenButton'),
            ('close (закрыть)', 'SP_DialogCloseButton'),
            ('reset (обновить)', 'SP_BrowserReload'),
            ('info (информация)', 'SP_MessageBoxInformation'),
            ('warning (предупреждение)', 'SP_MessageBoxWarning'),
            ('error (ошибка)', 'SP_MessageBoxCritical'),
            ('computer (компьютер)', 'SP_ComputerIcon'),
            ('drive (диск)', 'SP_DriveHDIcon'),
            ('home (домой)', 'SP_DirHomeIcon'),
        ]
        
        style = QApplication.instance().style()
        
        for name, sp_name in icons_list:
            row = QHBoxLayout()
            
            # Получаем иконку
            sp_enum = getattr(QStyle.StandardPixmap, sp_name)
            icon = style.standardIcon(sp_enum)
            
            # Показываем иконку
            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(QSize(32, 32)))
            icon_label.setFixedSize(50, 50)
            icon_label.setAlignment(Qt.AlignCenter)
            row.addWidget(icon_label)
            
            # Показываем название
            name_label = QLabel(name)
            row.addWidget(name_label)
            
            row.addStretch()
            scroll_layout.addLayout(row)
        
        scroll_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)


def main():
    app = QApplication(sys.argv)
    
    # Применяем тёмную тему для наглядности
    app.setStyle("Fusion")
    
    window = IconViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()