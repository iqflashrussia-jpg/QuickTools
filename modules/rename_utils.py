import os


def batch_rename(folder_path, find_text, replace_text, log_func):
    """Пакетное переименование файлов и папок"""
    renamed_count = 0
    errors = 0
    
    items = os.listdir(folder_path)
    log_func(f"Найдено объектов: {len(items)}")
    
    for name in items:
        if name == 'zip':
            continue
        
        if find_text in name:
            old_path = os.path.join(folder_path, name)
            new_name = name.replace(find_text, replace_text)
            new_path = os.path.join(folder_path, new_name)
            
            log_func(f"\n{name} → {new_name}")
            
            if os.path.exists(new_path) and old_path != new_path:
                log_func(f"  ⚠️ Пропущен: {new_name} уже существует")
                errors += 1
                continue
            
            try:
                os.rename(old_path, new_path)
                renamed_count += 1
                log_func("  ✅ УСПЕШНО!")
            except Exception as e:
                log_func(f"  ❌ Ошибка: {str(e)}")
                errors += 1
    
    return renamed_count, errors