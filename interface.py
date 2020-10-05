from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import db


class UiDialog(QtWidgets.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 384)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 10, 101, 61))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 341))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.name_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.name_input.setObjectName("name_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name_input)
        self.label_name = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_name.setObjectName("label_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_name)
        self.label_price = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_price.setObjectName("label_price")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_price)
        self.price_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.price_input.setObjectName("price_input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.price_input)
        self.label_link = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_link.setObjectName("label_link")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_link)
        self.label_description = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_description.setObjectName("label_description")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_description)
        self.link_input = QtWidgets.QTextEdit(self.formLayoutWidget)
        self.link_input.setObjectName("link_input")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.link_input)
        self.description_input = QtWidgets.QTextEdit(self.formLayoutWidget)
        self.description_input.setObjectName("description_input")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.description_input)

        self.retranslateUi(Dialog)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.show()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_name.setText(_translate("Dialog", "Name"))
        self.label_price.setText(_translate("Dialog", "Price"))
        self.label_link.setText(_translate("Dialog", "Link"))
        self.label_description.setText(_translate("Dialog", "Description"))


class AddItemWindow(UiDialog):
    def __init__(self, parent=None, db=None):
        super(UiDialog, self).__init__()
        self.parent = parent
        self.db = db
        self.setupUi(self)
        self.setup_events(self)

    def setup_events(self, dialog):
        """Set up events for accepted and rejected buttons"""
        self.buttonBox.accepted.connect(self.add_item)
        self.buttonBox.rejected.connect(dialog.reject)

    def add_item(self):
        """
        Add new wish to database
        """
        if self.name_input.text() != "":
            for i in range(self.parent.tableWidget.rowCount()):
                if self.name_input.text() == self.parent.tableWidget.item(i, 0).text():
                    alert = QMessageBox()
                    alert.setWindowTitle('Error')
                    alert.setText('Wish with this name already exist')
                    alert.exec_()
                    self.close_window()
                    return
            name, price, link, description = self.name_input.text(), self.price_input.text(), \
                                             self.link_input.toPlainText(), self.description_input.toPlainText()

            if self.db.add_wish(name, price, link, description):
                alert = QMessageBox()
                alert.setWindowTitle('Saving...')
                alert.setText("Wish has been successfully added")
                alert.exec_()
                self.close_window()
                return
            else:
                alert = QMessageBox()
                alert.setWindowTitle('Error')
                alert.setText('DataBase Error')
                alert.exec_()
                return
        else:
            alert = QMessageBox()
            alert.setWindowTitle('Error')
            alert.setText('Give a name to your wish')
            alert.exec_()
            return

    def close_window(self):
        """
        Close dialog window
        """
        self.parent.load_wishes()
        self.close()


class ChangeItemWindow(UiDialog):
    def __init__(self, item_name, parent, db):
        super(UiDialog, self).__init__()
        self.item_name = item_name
        self.parent = parent
        self.db = db
        self.setupUi(self)
        self.setup_events(self)

    def setup_events(self, dialog):
        """Set up events for accepted and rejected buttons"""
        self.buttonBox.accepted.connect(self.edit_item)
        self.buttonBox.rejected.connect(dialog.reject)

    def edit_item(self):
        """
        Edit selected wish in database
        """
        if self.name_input.text() != "":
            for i in range(self.parent.tableWidget.rowCount()):
                if self.item_name == self.parent.tableWidget.item(i, 0).text():
                    continue
                if self.name_input.text() == self.parent.tableWidget.item(i, 0).text():
                    alert = QMessageBox()
                    alert.setWindowTitle('Error')
                    alert.setText('Wish with this name already exist')
                    alert.exec_()
                    self.close_window()
                    return
            fields = (self.name_input.text(), self.price_input.text(),
                      self.link_input.toPlainText(), self.description_input.toPlainText())

            if self.db.edit_wish(self.item_name, fields):
                alert = QMessageBox()
                alert.setWindowTitle('Saving...')
                alert.setText("Wish has been successfully added")
                alert.exec_()
                self.close_window()
                return
            else:
                alert = QMessageBox()
                alert.setWindowTitle('Error')
                alert.setText('DataBase Error')
                alert.exec_()
                return

        else:
            alert = QMessageBox()
            alert.setWindowTitle('Error')
            alert.setText('Give a name to your wish')
            alert.exec_()
            return

    def close_window(self):
        """
        Close dialog window
        """
        self.parent.load_wishes()
        self.close()


class UiMainWindow:
    def __init__(self, database, table_name, username, password, host):
        self.db = db.DatabaseManager(database, table_name, username, password, host)
        self.dialog = None

    def setupUi(self, MainWindow):

        # Main windows settings
        MainWindow.setObjectName("WishList")
        MainWindow.resize(750, 420)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Table settings
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 1, 751, 331))
        self.tableWidget.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().setHidden(True)
        self.tableWidget.itemSelectionChanged.connect(self.selected_item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(187)

        # Layout for buttons settings
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 340, 731, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Add button settings
        self.add_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.add_pushButton.setObjectName("add_pushButton")
        self.horizontalLayout.addWidget(self.add_pushButton)

        # Edit button settings
        self.edit_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.edit_pushButton.setObjectName("edit_pushButton")
        self.edit_pushButton.setEnabled(False)
        self.horizontalLayout.addWidget(self.edit_pushButton)

        # Delete button settings
        self.delete_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.delete_pushButton.setObjectName("delete_pushButton")
        self.delete_pushButton.setEnabled(False)

        # Set up buttons events
        self.add_pushButton.clicked.connect(self.add_item)
        self.edit_pushButton.clicked.connect(self.edit_item)
        self.delete_pushButton.clicked.connect(self.delete_item)

        self.horizontalLayout.addWidget(self.delete_pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.load_wishes()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Price"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Link"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Description"))
        self.add_pushButton.setText(_translate("MainWindow", "Add new item"))
        self.edit_pushButton.setText(_translate("MainWindow", "Edit item"))
        self.delete_pushButton.setText(_translate("MainWindow", "Delete item"))

    def add_item(self):
        """
        Open dialog window for create new item
        """
        self.dialog = AddItemWindow(self, self.db)

    def edit_item(self):
        """
        Open dialog window for edit item
        """
        item = self.selected_item()
        if item:
            item_name = item.text()
            self.dialog = ChangeItemWindow(item_name=item_name, parent=self, db=self.db)

    def delete_item(self):
        """
        Delete selected item
        """
        item = self.selected_item()
        if item:
            item_name = item.text()
        reply = QMessageBox.question(self, 'Удалить желание',
                                     'Вы хотите удалить {0}?'.format(item_name),
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_wish(item_name)
            alert = QMessageBox()
            alert.setWindowTitle('Удаление')
            alert.setText("Желание удалено")
            alert.exec_()
            self.load_wishes()

    def load_wishes(self):
        """
        Load all wishes
        """
        rows = self.db.get_wishes()
        self.tableWidget.setRowCount(len(rows))
        for row in range(len(rows)):
            for col in range(1, 5):  # Ignoring 'ID' column
                item = QtWidgets.QTableWidgetItem(rows[row][col])
                self.tableWidget.setItem(row, col - 1, item)  # Columns starts from 0

    def selected_item(self):
        """
        Method for changing button status when some item was selected
        :return selected table item
        """
        selected = self.tableWidget.selectedItems()
        if selected:
            self.edit_pushButton.setEnabled(True)
            self.delete_pushButton.setEnabled(True)
            item = selected[0]
            return item
        else:
            self.edit_pushButton.setEnabled(False)
            self.delete_pushButton.setEnabled(False)
            return None


