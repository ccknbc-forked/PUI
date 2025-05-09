from .. import *
from .base import *
from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel

# XXX
# If click handler triggers a model reset, dblclick handler will not be called

class QAbstractItemModelAdapter(QtCore.QAbstractItemModel):
    def __init__(self, model: "BaseTreeAdapter"):
        super().__init__()
        self.model = model
        self.node = None

    def index(self, row, column, parent = QtCore.QModelIndex()):
        parent_node = parent.internalPointer() if parent.isValid() else None
        if 0 <= row and row < self.model.rowCount(parent_node):
            child = self.model.child(parent_node, row)
            return self.createIndex(row, column, child)
        return QtCore.QModelIndex()

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsDropEnabled

        defaultFlags = super().flags(index)

        return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled

    def canDropMimeData(self, data, action, row, column, parent):
        if parent.isValid():
            pass
        else:
            return bool(self.node._onDropped)

    def dropMimeData(self, data, action, row, column, parent):
        if parent.isValid():
            pass
        else:
            event = QtGui.QDropEvent(QtCore.QPoint(0,0), action, data, QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.KeyboardModifier.NoModifier, QtCore.QEvent.Drop)
            self.node._onDropped[0](event, *self.node._onDropped[1], **self.node._onDropped[2])

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        parent_node = self.model.parent(node)
        if parent_node:
            return self.createIndex(0, 0, parent_node)
        return QModelIndex()

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return self.model.data(node)
        return None

    def rowCount(self, parent):
        parent_node = parent.internalPointer() if parent.isValid() else None
        return self.model.rowCount(parent_node)

    def columnCount(self, parent):
        return 1

    def hasChildren(self, parent):
        parent_node = parent.internalPointer() if parent.isValid() else None
        return self.model.rowCount(parent_node) > 0

    def clicked(self, node):
        self.model.clicked(node)

    def dblclicked(self, node):
        self.model.dblclicked(node)

    def expanded(self, node):
        self.model.expanded(node)

    def collapsed(self, node):
        self.model.collapsed(node)

class QTreeNodeModelAdapter(QtCore.QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self.node = None

    def index(self, row, column, parent = QtCore.QModelIndex()):
        parent_node = parent.internalPointer() if parent.isValid() else self.node
        if 0 <= row and row < len(parent_node.children):
            child = parent_node.children[row]
            return self.createIndex(row, column, child)
        return QtCore.QModelIndex()

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsDropEnabled

        defaultFlags = super().flags(index)

        return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled

    def canDropMimeData(self, data, action, row, column, parent):
        if parent.isValid():
            pass
        else:
            return bool(self.node._onDropped)

    def dropMimeData(self, data, action, row, column, parent):
        if parent.isValid():
            pass
        else:
            event = QtGui.QDropEvent(QtCore.QPoint(0,0), action, data, QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.KeyboardModifier.NoModifier, QtCore.QEvent.Drop)
            self.node._onDropped[0](event, *self.node._onDropped[1], **self.node._onDropped[2])

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        parent_node = node.parent
        if not isinstance(parent_node, TreeNode):
            parent_node = None
        if parent_node:
            return self.createIndex(0, 0, parent_node)
        return QModelIndex()

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return node.data
        return None

    def rowCount(self, parent):
        parent_node = parent.internalPointer() if parent.isValid() else self.node
        return len(parent_node.children)

    def columnCount(self, parent):
        return 1

    def hasChildren(self, parent):
        parent_node = parent.internalPointer() if parent.isValid() else self.node
        return len(parent_node.children) > 0

    def clicked(self, node):
        node._clicked(None)

    def dblclicked(self, node):
        node._dblclicked(None)

    def expanded(self, node):
        node._expanded()

    def collapsed(self, node):
        node._collapsed()

class Tree(QtBaseWidget):
    def __init__(self, model=None):
        super().__init__()
        self.layout_weight = 1
        self.model = model
        self.curr_model = None
        self.pendings = []
        self._expand_callback = None
        self._collapse_callback = None

    def update(self, prev):
        if prev and prev.ui:
            self.ui = prev.ui
            self.qt_model = prev.qt_model
            self.curr_model = prev.curr_model

            self.ui.clicked.disconnect()
            self.ui.doubleClicked.disconnect()
            self.ui.expanded.disconnect()
            self.ui.collapsed.disconnect()
        else:
            self.qt_model = None
            self.curr_model = Prop()
            self.ui = QtWidgets.QTreeView()
            self.ui.setHeaderHidden(True)

        self.ui.clicked.connect(self.on_item_clicked)
        self.ui.doubleClicked.connect(self.on_item_double_clicked)
        self.ui.expanded.connect(self.on_item_expanded)
        self.ui.collapsed.connect(self.on_item_collapsed)

        if self.model:
            if self.curr_model.set(self.model):
                self.qt_model = QAbstractItemModelAdapter(self.model)
                self.qt_model.node = self
                self.ui.setModel(self.qt_model)
            else:
                self.qt_model.modelReset.emit()
        else:
            if not self.qt_model:
                self.qt_model = QTreeNodeModelAdapter()
                self.qt_model.node = self
                self.ui.setModel(self.qt_model)
            else:
                self.qt_model.beginResetModel()
                self.qt_model.node = self
                self.qt_model.endResetModel()

        for pending in self.pendings:
            pending[0](*pending[1:])
        self.pendings = []

        super().update(prev)

    def expandAll(self):
        if self.ui:
            self.ui.expandAll()
        else:
            self.pendings.append([self.expandAll])
        return self

    def collapseAll(self):
        if self.ui:
            self.ui.collapseAll()
        else:
            self.pendings.append([self.collapseAll])
        return self

    def expandable(self, enabled):
        if self.ui:
            self.ui.setItemsExpandable(enabled)
        else:
            self.pendings.append([self.expandable, enabled])
        return self

    def expand(self, cb, *args, **kwargs):
        self._expand_callback = (cb, args, kwargs)
        return self

    def _expanded(self):
        if self._expand_callback:
            cb, args, kwargs = self._expand_callback
            cb(*args, **kwargs)

    def collapse(self, cb, *args, **kwargs):
        self._collapse_callback = (cb, args, kwargs)
        return self

    def _collapsed(self):
        if self._collapse_callback:
            cb, args, kwargs = self._collapse_callback
            cb(*args, **kwargs)

    def on_item_clicked(self, index):
        treenode = index.internalPointer()
        self.get_node().qt_model.clicked(treenode)

    def on_item_double_clicked(self, index):
        treenode = index.internalPointer()
        self.get_node().qt_model.dblclicked(treenode)

    def on_item_expanded(self, index):
        treenode = index.internalPointer()
        self.get_node().qt_model.expanded(treenode)

    def on_item_collapsed(self, index):
        treenode = index.internalPointer()
        self.get_node().qt_model.collapsed(treenode)

class TreeNode(PUINode):
    def __init__(self, data=""):
        super().__init__()
        self._set_callback = None
        self.data = data
        self._expand_callback = None
        self._collapse_callback = None

    def expand(self, cb, *args, **kwargs):
        self._expand_callback = (cb, args, kwargs)
        return self

    def _expanded(self):
        if self._expand_callback:
            cb, args, kwargs = self._expand_callback
            cb(*args, **kwargs)

    def collapse(self, cb, *args, **kwargs):
        self._collapse_callback = (cb, args, kwargs)
        return self

    def _collapsed(self):
        if self._collapse_callback:
            cb, args, kwargs = self._collapse_callback
            cb(*args, **kwargs)
