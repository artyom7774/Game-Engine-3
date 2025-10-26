from src.modules.dialogs import CreateProject, CreateFromTemplateProject, OpenProject, Settings

from src.modules import functions


def create(project) -> None:
    project.dialog = CreateProject(project, parent=project)
    project.dialog.exec_()


def createFromTemplate(project) -> None:
    project.dialog = CreateFromTemplateProject(project, parent=project)
    project.dialog.exec_()


def open(project) -> None:
    project.dialog = OpenProject(project, parent=project)
    project.dialog.exec_()


def close(project) -> None:
    for key, value in project.objects.items():
        try:
            value.hide()

        except BaseException:
            pass

    if "main" in project.objects:
        for key, value in project.objects["main"].items():
            try:
                value.hide()

            except BaseException:
                pass

    else:
        pass

    functions.project.projectClose(project)

    project.menues["project_menu"].setDisabled(True)

    project.initialization()


def settings(project) -> None:
    project.dialog = Settings(project, parent=project)
    project.dialog.exec_()
