from PySide6 import QtCore, QtGui
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QSizePolicy

# Coordonées X, Y puis taille du bouton en hauteur puis largeur
BUTTONS = {"C": (1, 0, 1, 1),
           "/": (1, 3, 1, 1),
           "7": (2, 0, 1, 1),
           "8": (2, 1, 1, 1),
           "9": (2, 2, 1, 1),
           "x": (2, 3, 1, 1),
           "4": (3, 0, 1, 1),
           "5": (3, 1, 1, 1),
           "6": (3, 2, 1, 1),
           "-": (3, 3, 1, 1),
           "1": (4, 0, 1, 1),
           "2": (4, 1, 1, 1),
           "3": (4, 2, 1, 1),
           "+": (4, 3, 1, 1),
           "0": (5, 0, 1, 2),
           ".": (5, 2, 1, 1),
           "=": (5, 3, 1, 1)}

OPERATIONS = ["+", "-", "/", "x"]


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculatrice")
        self.setWindowIcon(QtGui.QIcon('res/calculator.png'))
        self.setFixedSize(320, 475)
        self.setStyleSheet("""
            background-color: #0A0A0A;
            color : rgb(220, 220, 220);
            font-size: 22px;
        """)
        self.buttons = {}
        self.main_layout = QGridLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.le_result = QLineEdit("0")
        self.le_result.setMinimumHeight(80)
        self.le_result.setAlignment(QtCore.Qt.AlignRight)
        self.le_result.setEnabled(False)
        self.le_result.setStyleSheet("""
            border: none;
            border-bottom: 2px solid rgb(30, 30, 30);
            padding: 0 8px;
            font-size: 35px;
            font-weight: bold;
        """)
        self.main_layout.addWidget(self.le_result, 0, 0, 1, 4)

        for button_text, button_position in BUTTONS.items():
            button = QPushButton(button_text)
            button.setMinimumSize(48, 48)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.main_layout.addWidget(button, *button_position)  # Unpack method(*)
            button.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    font-weight: bold;
                    background-color: {'#1e1e2d' if button_text in OPERATIONS else 'none'}
                              }}
                    QPushButton:pressed {{background-color: #44AACD;}}        
            """)
            if button_text not in ["=", "C"]:
                button.clicked.connect(self.number_or_operation_pressed)
            self.buttons[button_text] = button

        self.buttons["C"].clicked.connect(self.clear_result)
        self.buttons["="].clicked.connect(self.compute_result)
        self.buttons["="].setStyleSheet("background-color: #f31d58;")

        self.connect_keyboard_shortcut()

    def compute_result(self):
        try:
            result = eval(self.le_result.text().replace("x", "*"))
        except SyntaxError:
            return

        self.le_result.setText(str(result))

    def clear_result(self):
        self.le_result.setText("0")

    def number_or_operation_pressed(self):
        if self.sender().text() in OPERATIONS:
            if self.le_result.text()[-1] in OPERATIONS or self.le_result.text() == "0":
                return

        if self.le_result.text() == "0":
            self.le_result.clear()
        self.le_result.setText(self.le_result.text() + self.sender().text())

    def remove_last_character(self):
        if len(self.le_result.text()) > 1:
            self.le_result.setText(self.le_result.text()[:-1])
        else:
            self.le_result.setText("0")

    def connect_keyboard_shortcut(self):
        for button_text, button in self.buttons.items():
            QShortcut(QKeySequence(button_text), self, button.clicked.emit)

        QShortcut(QKeySequence(QtCore.Qt.Key_Enter), self, self.compute_result)
        QShortcut(QKeySequence(QtCore.Qt.Key_Backspace), self, self.remove_last_character)


app = QApplication()
win = Calculator()
win.show()
app.exec()
