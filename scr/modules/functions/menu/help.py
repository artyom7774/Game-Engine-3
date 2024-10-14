from scr.modules.dialogs import Help


def help_(project, page) -> None:
    project.dialog = Help(project, page, parent=project)
    project.dialog.exec_()
