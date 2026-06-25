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