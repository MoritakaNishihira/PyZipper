from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QFileDialog,
)
from PySide6.QtCore import Qt
import json


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("設定")
        self.setGeometry(100, 100, 800, 600)

        self.table = QTableWidget()
        self.setup_table()

        add_button = QPushButton("追加")
        add_button.clicked.connect(self.add_row)
        add_button.setFixedWidth(60)

        layout = QVBoxLayout()
        layout.addWidget(add_button)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_settings_from_json()

    def setup_table(self):
        self.table.setColumnCount(4)
        column_widths = [200, 250, 250, 60]
        for col in range(self.table.columnCount()):
            self.table.setColumnWidth(col, column_widths[col])

        headers = ["設定名", "参照先", "保存先", ""]
        self.table.setHorizontalHeaderLabels(headers)

    def add_row(self):
        current_row_count = self.table.rowCount()
        self.table.insertRow(current_row_count)
        self.setup_row(current_row_count)

    def setup_row(self, row):
        for col in range(self.table.columnCount() - 1):
            item = QTableWidgetItem(f"")

            if col == 0:
                input_area = QLineEdit()
                input_area.setText(item.text())
                self.table.setCellWidget(row, col, input_area)
            elif col in (1, 2):
                self.setup_input_with_button(row, col, item.text())
            else:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

        save_button = QPushButton("保存")
        save_button.clicked.connect(lambda: self.save_row_data(row))
        save_button.setFixedWidth(60)

        self.table.setCellWidget(row, 3, save_button)

    def setup_input_with_button(self, row, col, text):
        container = QWidget()
        layout = QHBoxLayout(container)

        input_area = QLineEdit()
        input_area.setText(text)
        input_area.setReadOnly(True)
        layout.addWidget(input_area)

        reference_button = QPushButton("参照")
        reference_button.setFixedWidth(60)

        reference_button.clicked.connect(
            lambda _, r=row, c=col: self.open_folder_dialog(r, c)
        )

        layout.addWidget(reference_button)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table.setCellWidget(row, col, container)

    def open_folder_dialog(self, row, col):
        folder_path = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        if folder_path:
            input_area = self.table.cellWidget(row, col).layout().itemAt(0).widget()
            input_area.setText(folder_path)

    def save_row_data(self, row):
        row_data = {
            "行番号": row,
            "設定名": self.get_cell_text(row, 0),
            "参照先": self.get_cell_text(row, 1),
            "保存先": self.get_cell_text(row, 2),
        }

        file_path = "PyZipper_Settings.json"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                settings_data = json.load(f)
        except FileNotFoundError:
            settings_data = []

        updated = False
        for entry in settings_data:
            if entry.get("行番号") == row:
                entry.update(row_data)
                updated = True
                break

        if not updated:
            settings_data.append(row_data)

        sorted_settings_data = sorted(settings_data, key=lambda x: x.get("行番号", 0))

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(sorted_settings_data, f, ensure_ascii=False, indent=4)

        print(f"データを {file_path} に保存しました。")

    def get_cell_text(self, row, col):
        widget = self.table.cellWidget(row, col)
        if isinstance(widget, QLineEdit):
            return widget.text()
        elif (
            isinstance(widget, QWidget)
            and widget.layout().itemAt(0).widget() is not None
        ):
            return widget.layout().itemAt(0).widget().text()
        else:
            return ""

    def load_settings_from_json(self):
        file_path = "PyZipper_Settings.json"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                settings_data = json.load(f)

            for entry in settings_data:
                self.add_row()
                row = entry.get("行番号")
                if row is not None and 0 <= row < self.table.rowCount():
                    self.set_cell_widget(row, 0, QLineEdit(entry["設定名"]))
                    self.setup_input_with_button_and_text(row, 1, entry["参照先"])
                    self.setup_input_with_button_and_text(row, 2, entry["保存先"])
                    save_button = QPushButton("保存")
                    save_button.clicked.connect(lambda _, r=row: self.save_row_data(r))
                    self.table.setCellWidget(row, 3, save_button)
        except FileNotFoundError:
            pass

    def set_cell_widget(self, row, col, widget):
        self.table.setCellWidget(row, col, widget)

    def setup_input_with_button_and_text(self, row, col, text):
        container = QWidget()
        layout = QHBoxLayout(container)
        input_area = QLineEdit(text)
        input_area.setReadOnly(True)
        reference_button = QPushButton("参照")
        reference_button.setFixedWidth(60)
        reference_button.clicked.connect(
            lambda _, r=row: self.open_folder_dialog(r, col)
        )
        layout.addWidget(input_area)
        layout.addWidget(reference_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.table.setCellWidget(row, col, container)


# アプリケーションの実行
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
