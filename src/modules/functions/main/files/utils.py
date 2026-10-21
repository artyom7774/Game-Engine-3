from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer



def destroyLink(link: dict) -> None:
    for value in (link or {}).values():
        destroyWidgetLike(value)


def hideWidgetLike(obj):
    if obj is None:
        return

    try:
        if isinstance(obj, dict):
            for value in obj.values():
                hideWidgetLike(value)

            return

        if isinstance(obj, (list, tuple, set)):
            for value in obj:
                hideWidgetLike(value)

            return

        if isinstance(obj, QTimer):
            obj.stop()

            return

        if hasattr(obj, "objects"):
            try:
                hideWidgetLike(obj.objects)

            except Exception:
                pass

        if hasattr(obj, "create"):
            try:
                hideWidgetLike(obj.create)

            except Exception:
                pass

        if isinstance(obj, QWidget):
            obj.hide()

    except RuntimeError:
        pass

    except Exception:
        pass


def destroyWidgetLike(obj):
    if obj is None:
        return

    try:
        hideWidgetLike(obj)

    except Exception:
        pass

    try:
        if isinstance(obj, dict):
            for value in list(obj.values()):
                destroyWidgetLike(value)

            obj.clear()

            return

        if isinstance(obj, (list, tuple, set)):
            for value in obj:
                destroyWidgetLike(value)

            return

        if hasattr(obj, "objects"):
            try:
                destroyWidgetLike(obj.objects)

            except Exception:
                pass

        if hasattr(obj, "create"):
            try:
                destroyWidgetLike(obj.create)

            except Exception:
                pass

        if isinstance(obj, (QWidget, QTimer)):
            obj.deleteLater()

    except RuntimeError:
        pass

    except Exception:
        pass


def hideOtherLinks(project, currentFile):
    main = project.objects.get("main", {})

    for key, link in list(main.items()):
        if key == currentFile:
            continue

        hideWidgetLike(link)


def destroyFileLink(project, file=None):
    if file is None:
        file = project.selectFile

    main = project.objects.get("main", {})
    link = main.pop(file, None)

    if link is not None:
        destroyWidgetLike(link)
