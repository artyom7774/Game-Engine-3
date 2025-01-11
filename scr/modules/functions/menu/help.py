from scr.modules.dialogs import About
from scr.modules.dialogs import Help


def help_(project) -> None:
    project.dialog = Help(project, parent=project)
    project.dialog.exec_()


def about(project) -> None:
    project.dialog = About(project, parent=project)
    project.dialog.exec_()
