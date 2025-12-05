from typing import Dict


def analyze_file_metadata(meta: Dict) -> str:

    size = meta.get("file_size", 0)
    version = meta.get("version", 1)
    name = meta.get("file_name", "file")

    if size < 50_000:
        size_desc = "относительно небольшой"
    elif size < 2_000_000:
        size_desc = "среднего размера"
    else:
        size_desc = "довольно большой"

    if version == 1:
        ver_desc = "Это первая версия документа."
    elif version <= 3:
        ver_desc = f"Версия {version}: изменения выглядят несущественными."
    else:
        ver_desc = f"Версия {version}: документ активно дорабатывается."

    return (
        f"Документ «{name}» {size_desc} (≈{size} байт). "
        f"{ver_desc} "
        f"Рекомендуется сверить критичные разделы перед использованием в проде."
    )
