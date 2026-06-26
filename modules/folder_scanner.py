import os


def find_size_folders(base_path):
    """Находит все папки с 'x' в имени (размеры)"""
    folders = []
    for platform in os.listdir(base_path):
        platform_path = os.path.join(base_path, platform)
        if not os.path.isdir(platform_path) or platform == 'zip':
            continue
        
        for campaign in os.listdir(platform_path):
            campaign_path = os.path.join(platform_path, campaign)
            if not os.path.isdir(campaign_path):
                continue
            
            for size_folder in os.listdir(campaign_path):
                size_path = os.path.join(campaign_path, size_folder)
                if os.path.isdir(size_path) and 'x' in size_folder.lower():
                    folders.append({
                        'path': size_path,
                        'platform': platform,
                        'campaign': campaign,
                        'size': size_folder
                    })
    return folders


def find_animate_size_folders(project_path):
    """Recursively find optimizer size folders inside a project's animate folder."""
    folders = []
    if not os.path.exists(project_path):
        return folders

    animate_path = os.path.join(project_path, "animate")
    if not os.path.exists(animate_path):
        return folders

    for root, dirs, files in os.walk(animate_path):
        for dir_name in dirs:
            if 'x' not in dir_name.lower():
                continue

            folder_path = os.path.join(root, dir_name)
            rel_path = os.path.relpath(root, animate_path)
            parts = rel_path.split(os.sep) if rel_path != '.' else []
            platform = parts[0] if len(parts) > 0 else "unknown"
            campaign = parts[1] if len(parts) > 1 else "unknown"

            folders.append({
                'path': folder_path,
                'platform': platform,
                'campaign': campaign,
                'size': dir_name
            })

    return folders
