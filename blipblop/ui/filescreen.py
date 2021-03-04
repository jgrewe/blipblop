from PyQt5.QtWidgets import QComboBox, QFrame, QGroupBox, QHBoxLayout, QLabel, QSplitter, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QItemSelectionModel, Qt

from nixview.util.file_handler import FileHandler
from nixview.util.descriptors import ItemDescriptor
import nixview.communicator as comm
import nixview.constants as cnst
from nixview.data_models.tree_model import NixTreeView, TreeModel, TreeType


class FileScreen(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._file_handler = FileHandler()
        
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        
        main_splitter = QSplitter(Qt.Vertical)
        self.layout().addWidget(main_splitter)
        
        self._info = EntityInfo(self)
        main_splitter.addWidget(self._info)
       
        self._data_tree = NixTreeView(self)
        
        self._tree_type_combo = QComboBox()
        self._tree_type_combo.adjustSize()
        self._tree_type_combo.addItems([TreeType.Data.value, TreeType.Full.value, TreeType.Metadata.value])
        self._tree_type_combo.currentTextChanged.connect(self.update)
        
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Tree type:"))
        hbox.addWidget(self._tree_type_combo)
        hbox.addStretch()
        data_group = QGroupBox("Data")
        data_vbox = QVBoxLayout()
        data_vbox.setContentsMargins(1, 10, 1, 1)
        
        data_vbox.addLayout(hbox)
        data_vbox.addWidget(self._data_tree)
        data_group.setLayout(data_vbox)
        
        main_splitter.addWidget(data_group)
        main_splitter.setSizes([200, 600])
        vbox.addWidget(main_splitter)

    def dataTreeSelection(self, current_index, last_index):
        if not current_index.isValid():
            return
        item = current_index.internalPointer()
        comm.communicator.item_selected.emit(item)
        self._info.setEntityInfo(item.node_descriptor)

    def update(self):
        tt = TreeType.Data
        if self._tree_type_combo.currentText() == TreeType.Data.value:
            tt = TreeType.Data
        elif self._tree_type_combo.currentText() == TreeType.Full.value:
            tt = TreeType.Full
        elif self._tree_type_combo.currentText() == TreeType.Metadata.value:
            tt = TreeType.Metadata
        self._info.setEntityInfo(None)
        data_model = TreeModel(self._file_handler, tt)
        self._data_tree.setModel(data_model)
        selection_model = QItemSelectionModel(data_model)
        self._data_tree.setSelectionModel(selection_model)
        selection_model.currentChanged.connect(self.dataTreeSelection)
        for i in range(data_model.columnCount(None)):
            self._data_tree.resizeColumnToContents(i)
        self._info.setFileInfo(self._file_handler.file_descriptor)
        
    def reset(self):
        pass


class EntityInfo(QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self._file_handler = FileHandler()
        self.setLayout(QHBoxLayout())
        
        self._metadata_tree = NixTreeView()
    
        mdata_grp = QGroupBox("Metadata")
        mdata_grp.setLayout(QVBoxLayout())
        mdata_grp.layout().setContentsMargins(1, 10, 1, 1)
        mdata_grp.layout().addWidget(self._metadata_tree)
        
        file_info_grp = QGroupBox("File info")
        file_info_grp.setLayout(QVBoxLayout())
        file_info_grp.layout().setContentsMargins(1, 10, 1, 1)
        self._file_info = QTextEdit("File information")
        self._file_info.setEnabled(True)
        self._file_info.setTextInteractionFlags(Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
        self._file_info.setFrameShape(QFrame.NoFrame)
        self._file_info.setLineWrapMode(QTextEdit.WidgetWidth)
        file_info_grp.layout().addWidget(self._file_info)

        entity_info_grp = QGroupBox("Entity info")
        entity_info_grp.setLayout(QVBoxLayout())
        entity_info_grp.layout().setContentsMargins(1, 10, 1, 1)
        self._entity_info = QTextEdit("Entity information")
        self._file_info.setEnabled(True)
        self._file_info.setTextInteractionFlags(Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
        self._file_info.setFrameShape(QFrame.NoFrame)
        self._file_info.setLineWrapMode(QTextEdit.WidgetWidth)
        entity_info_grp.layout().addWidget(self._entity_info)
 
        self._splitter = QSplitter(Qt.Horizontal)
        self._splitter.addWidget(file_info_grp)
        self._splitter.addWidget(entity_info_grp)
        self._splitter.addWidget(mdata_grp)
        self._splitter.setSizes([200, 400, 0])
        self._splitter.setStretchFactor(0, 0)
        self._splitter.setStretchFactor(1, 1)
        self._splitter.setStretchFactor(2, 1)
        
        self.layout().addWidget(self._splitter)
        

    def setFileInfo(self, file_info):
        if file_info is not None:
            self._file_info.setText(file_info.toHtml())
            
    def setEntityInfo(self, entity_info):
        if entity_info is None or not isinstance(entity_info, ItemDescriptor):
            self._splitter.setSizes([200, 400, 0])
            self._entity_info.setText("")
            self._metadata_tree.setModel(None)
            return

        if entity_info.metadata_id is not None:
            self._splitter.setSizes([200, 400, 400])
        else:
            self._splitter.setSizes([200, 400, 0])
        self._entity_info.setText(entity_info.to_html())
        metadata_model = TreeModel(self._file_handler, TreeType.Metadata, root_section_id=entity_info.metadata_id)
        self._metadata_tree.setModel(metadata_model)
        for i in range(metadata_model.columnCount(None)):
            self._metadata_tree.resizeColumnToContents(i)
