from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, QMimeData, QByteArray, QDataStream, QIODevice, QPoint
from PyQt5.QtGui import QDrag, QDropEvent


class TreeProject(QTreeWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project

        # self.setDragEnabled(True)
        # self.setAcceptDrops(True)
        self.setSelectionMode(QTreeWidget.SingleSelection)
        self.setDragDropMode(QTreeWidget.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)

        # self.setDropIndicatorShown(True)
        self.setHeaderLabel("Project Structure")

    def startDrag(self, supportedActions):
        # Получаем текущий элемент
        drag_item = self.currentItem()
        if not drag_item:
            return

        # Создаем MIME данные для передачи
        mime_data = QMimeData()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)

        # Сериализуем данные элемента (например, текст)
        stream.writeQString(drag_item.text(0))
        mime_data.setData("application/x-treeitem", data)

        # Настраиваем и запускаем перетаскивание
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.source() == self:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.source() == self:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.source() != self:
            return

        # Получаем элемент для перемещения
        drag_item = self.currentItem()
        if not drag_item:
            return

        # Определяем позицию вставки
        pos = event.pos()
        drop_target = self.itemAt(pos)
        parent = drop_target.parent() if drop_target else self.invisibleRootItem()

        # Определяем положение вставки относительно элементов
        indicator = self.dropIndicatorPosition()
        target_index = self.indexAt(pos)

        # Проверка на валидность целевой позиции
        if not target_index.isValid():
            # Вставка в конец корневого уровня
            new_parent = self.invisibleRootItem()
            new_parent.addChild(drag_item.clone())
        else:
            target_item = self.itemFromIndex(target_index)
            target_parent = target_item.parent() or self.invisibleRootItem()

            # Проверяем, не пытаемся ли переместить элемент в самого себя
            if self._is_ancestor(drag_item, target_item):
                event.ignore()
                return

            # Определяем позицию вставки
            if indicator == QAbstractItemView.AboveItem:
                target_parent.insertChild(target_parent.indexOfChild(target_item), drag_item.clone())
            elif indicator == QAbstractItemView.BelowItem:
                target_parent.insertChild(target_parent.indexOfChild(target_item) + 1, drag_item.clone())
            elif indicator == QAbstractItemView.OnItem:
                target_item.addChild(drag_item.clone())
            else:
                target_parent.addChild(drag_item.clone())

        (drag_item.parent() or self.invisibleRootItem()).removeChild(drag_item)
        event.accept()

    def _is_ancestor(self, parent, child):
        """Проверяет, является ли parent предком child"""
        while child is not None:
            child = child.parent()
            if child == parent:
                return True
        return False
