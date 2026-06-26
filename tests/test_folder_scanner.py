from pathlib import Path

from modules.folder_scanner import find_animate_size_folders


def _by_size(results):
    return {item["size"]: item for item in results}


def test_find_animate_size_folders_returns_expected_metadata(tmp_path):
    campaign = tmp_path / "animate" / "Google Ads" / "Summer Sale"
    size_folder = campaign / "300x250"
    size_folder.mkdir(parents=True)
    (campaign / "assets").mkdir()

    results = find_animate_size_folders(tmp_path)

    assert len(results) == 1
    result = results[0]
    assert Path(result["path"]) == size_folder
    assert result["platform"] == "Google Ads"
    assert result["campaign"] == "Summer Sale"
    assert result["size"] == "300x250"


def test_find_animate_size_folders_supports_cyrillic_spaces_and_nested_paths(tmp_path):
    nested_size = (
        tmp_path
        / "animate"
        / "Яндекс Директ"
        / "Осенняя кампания"
        / "nested group"
        / "240x400"
    )
    nested_size.mkdir(parents=True)

    results = find_animate_size_folders(tmp_path)

    assert len(results) == 1
    result = results[0]
    assert Path(result["path"]) == nested_size
    assert result["platform"] == "Яндекс Директ"
    assert result["campaign"] == "Осенняя кампания"
    assert result["size"] == "240x400"


def test_find_animate_size_folders_uses_unknown_for_direct_size_folder(tmp_path):
    direct_size = tmp_path / "animate" / "320x50"
    direct_size.mkdir(parents=True)

    results = find_animate_size_folders(tmp_path)

    assert len(results) == 1
    result = results[0]
    assert Path(result["path"]) == direct_size
    assert result["platform"] == "unknown"
    assert result["campaign"] == "unknown"
    assert result["size"] == "320x50"


def test_find_animate_size_folders_ignores_non_size_folders(tmp_path):
    animate = tmp_path / "animate" / "platform" / "campaign"
    (animate / "banner").mkdir(parents=True)
    (animate / "300X600").mkdir()

    results = find_animate_size_folders(tmp_path)

    assert list(_by_size(results)) == ["300X600"]


def test_find_animate_size_folders_returns_empty_for_missing_paths(tmp_path):
    assert find_animate_size_folders(tmp_path / "missing") == []
    assert find_animate_size_folders(tmp_path) == []
