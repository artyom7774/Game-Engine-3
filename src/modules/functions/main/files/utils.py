from PyQt5.QtWidgets import QWidget


def hideWidgetLike(obj) -> None:
    """Скрывает любой объект, похожий на виджет: как обычный QWidget,
    так и кастомные обёртки (CollisionAdditions, ConfigAdditionsVarsType и т.п.),
    которые хранят внутри себя .create / .objects."""

    if obj is None:
        return

    if isinstance(obj, QWidget):
        obj.hide()
        return

    if hasattr(obj, "hide") and callable(obj.hide):
        try:
            obj.hide()

        except Exception:
            pass

    if hasattr(obj, "create") and isinstance(obj.create, QWidget):
        obj.create.hide()

    if hasattr(obj, "objects") and isinstance(obj.objects, dict):
        for value in obj.objects.values():
            hideWidgetLike(value)


def destroyWidgetLike(obj) -> None:
    """Скрывает и планирует удаление (deleteLater) любого виджетоподобного объекта."""

    if obj is None:
        return

    hideWidgetLike(obj)

    if isinstance(obj, QWidget):
        obj.deleteLater()
        return

    if hasattr(obj, "create") and isinstance(obj.create, QWidget):
        obj.create.deleteLater()

    if hasattr(obj, "objects") and isinstance(obj.objects, dict):
        for value in obj.objects.values():
            destroyWidgetLike(value)


def hideLink(link: dict) -> None:
    for value in (link or {}).values():
        hideWidgetLike(value)


def destroyLink(link: dict) -> None:
    for value in (link or {}).values():
        destroyWidgetLike(value)


def hideOtherLinks(project, currentFile) -> None:
    """Прячет виджеты всех остальных открытых файлов, чтобы при
    переключении между вкладками/файлами старая графика не оставалась
    на экране поверх новой."""

    for file, link in project.objects.get("main", {}).items():
        if file == currentFile:
            continue

        hideLink(link)
