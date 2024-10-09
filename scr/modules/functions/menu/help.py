from scr.modules.dialogs import Help


def help_(project, value) -> None:
    project.dialog = Help(project, value, parent=project)
    project.dialog.exec_()
