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
        for col in range(
            self.table.columnCount() - 1
        ):  # 最終列（「保存」）は特別な扱いが必要
            item = QTableWidgetItem(f"sample")

            if col == 0:  # 「設定名」の列にはQLineEditを使用し、編集可にする
                input_area = QLineEdit()
                input_area.setText(item.text())
                self.table.setCellWidget(row, col, input_area)
            elif col in (1, 2):  # 「参照先」と「保存先」の列にはボタンを追加
                self.setup_input_with_button(row, col, item.text())
            else:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

        # 「保存」ボタンを追加
        save_button = QPushButton("保存")
        self.table.setCellWidget(
            row, 3, save_button
        )  # 最終列（「保存」）にボタンを配置

    def setup_input_with_button(self, row, col, text):
        container = QWidget()
        layout = QHBoxLayout(container)

        input_area = QLineEdit()
        input_area.setText(text)
        input_area.setReadOnly(True)  # 参照先と保存先は読み取り専用に設定
        layout.addWidget(input_area)

        reference_button = QPushButton("参照")
        reference_button.setFixedWidth(60)  # 横幅を60ピクセルに設定
        layout.addWidget(reference_button)
        reference_button.clicked.connect(
            lambda: self.open_folder_dialog(row, col)
        )  # 追加

        layout.setContentsMargins(0, 0, 0, 0)  # レイアウトの余白を除去

        self.table.setCellWidget(row, col, container)  # セルにコンテナを配置

    def open_folder_dialog(self, row, col):
        folder_path = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        if folder_path:
            input_area = self.table.cellWidget(row, col).layout().itemAt(0).widget()
            input_area.setText(folder_path)


# アプリケーションの実行
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
