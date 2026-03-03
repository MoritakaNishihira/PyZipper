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
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("一覧入力形式の UI")
        self.setGeometry(100, 100, 800, 600)

        # QTableWidget を作成し、列数と行数を設定
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setRowCount(5)

        # 各列の横幅を設定
        column_widths = [200, 250, 250, 60]
        for col in range(self.table.columnCount()):
            self.table.setColumnWidth(col, column_widths[col])

        # 列のヘッダーを設定
        headers = ["設定名", "参照先", "保存先", "保存"]
        self.table.setHorizontalHeaderLabels(headers)

        # テーブルにデータとボタンを入力
        for row in range(self.table.rowCount()):
            self.setup_row(row)

        # 追加ボタンの設定
        add_button = QPushButton("追加")
        add_button.clicked.connect(self.add_row)
        add_button.setFixedWidth(60)  # 横幅を60ピクセルに設定

        # QTableWidget をウィンドウに追加
        layout = QVBoxLayout()
        layout.addWidget(add_button)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_row(self):
        current_row_count = self.table.rowCount()
        self.table.insertRow(current_row_count)
        self.setup_row(current_row_count)

    def setup_row(self, row):
        for col in range(
            self.table.columnCount() - 1
        ):  # 最終列（「保存」）は特別な扱いが必要
            item = QTableWidgetItem(f"データ {row},{col}")

            if col == 1 or col == 2:  # 「参照先」と「保存先」の列にはボタンを追加
                container = QWidget()
                layout = QHBoxLayout(container)

                # 入力エリア
                input_area = QLineEdit()
                input_area.setText(item.text())
                layout.addWidget(input_area)

                # 参照ボタン
                reference_button = QPushButton("参照")
                reference_button.setFixedWidth(60)  # 横幅を60ピクセルに設定
                layout.addWidget(reference_button)
                layout.setContentsMargins(0, 0, 0, 0)  # レイアウトの余白を除去

                self.table.setCellWidget(row, col, container)  # セルにコンテナを配置
            else:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

        # 「保存」ボタンを追加
        save_button = QPushButton("保存")
        self.table.setCellWidget(
            row, 3, save_button
        )  # 最終列（「保存」）にボタンを配置


# アプリケーションの実行
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
