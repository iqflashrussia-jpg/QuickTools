import os


def find_fla_files(folder_path, size=None):
    """Находит .fla файлы в папке"""
    found_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if size:
                if file == f"{size}.fla":
                    found_files.append(os.path.join(root, file))
            elif file.endswith('.fla'):
                found_files.append(os.path.join(root, file))
        # небольшой yield для асинхронности
        yield
    return found_files

def open_fla_files(file_paths, log_func):
    """Открывает .fla файлы через системный ассоциированный редактор"""
    for file_path in file_paths:
        try:
            os.startfile(file_path)
            log_func(f"  ✅ Открыт: {os.path.basename(file_path)}")
        except Exception:
            log_func(f"  ❌ Ошибка: {os.path.basename(file_path)}")