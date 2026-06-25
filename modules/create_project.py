"""
Создание структуры проекта
"""

import os


def create_project_structure(project_path):
    """Создаёт полную структуру папок проекта"""
    
    # Стандартная структура папок
    folders = [
        'animate',
        'img', 
        'opt',
        'psd',
        'screen',
        'publish',
        'ai',
        'fla'
    ]
    
    for folder in folders:
        folder_path = os.path.join(project_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"📁 Создана папка: {folder}")
    
    return True