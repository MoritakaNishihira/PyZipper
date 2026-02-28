import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QSizePolicy,
    QLineEdit,
    QFileDialog,
    QHBoxLayout,
)
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("一覧形式アプリケーション")
        self.setGeometry(100, 100, 800, 600)

        # テーブルウィジェットの初期化
        self.table = QTableWidget()
        self.setup_table()

        container_layout = QVBoxLayout()
        container_layout.addWidget(self.add_button)
        container_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(container_layout)
        self.setCentralWidget(container)

        # JSONファイルから設定を読み込む
        self.settings_list, self.json_rows = self.load_settings()

    def setup_table(self):
        # カラム名を設定
        column_headers = ["設定名", "参照先", "保存先", "保存"]
        self.table.setColumnCount(len(column_headers))
        self.table.setHorizontalHeaderLabels(column_headers)

        # 各カラムの幅を設定（ここでは半角40文字程度）
        col_widths = [120, 150, 150, 80]
        for column, width in enumerate(col_widths):
            self.table.setColumnWidth(column, width)

        # 初期行数を設定（ここでは0）
        self.table.setRowCount(0)

        # 行追加ボタンの追加
        self.add_button = QPushButton("追加")
        self.add_button.clicked.connect(self.add_row)

    def add_row(self):
        current_row_count = self.table.rowCount()
        self.table.insertRow(current_row_count)

        # 各列にアイテムを設定
        for column in range(4):  # ここでは4列分まで処理する
            if column == 0:
                line_edit = QLineEdit()
                self.table.setCellWidget(current_row_count, column, line_edit)
            elif column == 1 or column == 2:
                widget = QWidget()
                layout = QHBoxLayout(widget)
                layout.setContentsMargins(0, 0, 0, 0)

                line_edit = QLineEdit()
                line_edit.setReadOnly(True)
                layout.addWidget(line_edit)

                button = QPushButton("参照")
                button.clicked.connect(
                    lambda row=current_row_count, col=column, le=line_edit: self.select_folder(
                        row, col, le
                    )
                )
                layout.addWidget(button)

                self.table.setCellWidget(current_row_count, column, widget)
            elif column == 3:
                save_button = QPushButton("保存")
                save_button.clicked.connect(
                    lambda row=current_row_count: self.save_settings_for_row(row)
                )
                self.table.setCellWidget(current_row_count, column, save_button)

    def select_folder(self, row, column, line_edit):
        folder_path = QFileDialog.getExistingDirectory()
        if folder_path:
            line_edit.setText(folder_path)

    def save_settings_for_row(self, row):
        # 特定の行のデータのみを保存・更新する
        setting_name_edit = self.table.cellWidget(row, 0)
        source_folder_widget = self.table.cellWidget(row, 1)
        target_folder_widget = self.table.cellWidget(row, 2)

        if (
            isinstance(setting_name_edit, QLineEdit)
            and isinstance(source_folder_widget, QWidget)
            and isinstance(target_folder_widget, QWidget)
        ):
            setting_name = setting_name_edit.text()

            source_line_edit = source_folder_widget.layout().itemAt(0).widget()
            target_line_edit = target_folder_widget.layout().itemAt(0).widget()

            if isinstance(source_line_edit, QLineEdit) and isinstance(
                target_line_edit, QLineEdit
            ):
                source_folder = source_line_edit.text()
                target_folder = target_line_edit.text()

                # 全ての項目が入力されている場合のみ追加・更新
                if setting_name and source_folder and target_folder:
                    data = {
                        "設定名": setting_name,
                        "参照先": source_folder,
                        "保存先": target_folder,
                    }

                    # JSONファイルをスクリプトと同じディレクトリに保存・更新
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    json_path = os.path.join(script_dir, "settings.json")

                    if os.path.exists(json_path):
                        with open(json_path, "r", encoding="utf-8") as f:
                            settings_list = json.load(f)
                    else:
                        settings_list = []

                    # JSON行位置とテーブルの行位置が一致すれば更新、なければ追加
                    if row < len(settings_list):
                        settings_list[row].update(data)
                    else:
                        settings_list.append(data)

                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump(settings_list, f, ensure_ascii=False, indent=4)

    def load_settings(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "settings.json")

        settings_list = []
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                data_list = json.load(f)
                for item in data_list:
                    self.add_row()
                    current_row_count = self.table.rowCount() - 1

                    # 「設定名」を設定
                    setting_name_edit = QLineEdit(item["設定名"])
                    self.table.setCellWidget(current_row_count, 0, setting_name_edit)

                    # 「参照先」を設定
                    source_folder_widget = self.table.cellWidget(current_row_count, 1)
                    if isinstance(source_folder_widget, QWidget):
                        source_line_edit = (
                            source_folder_widget.layout().itemAt(0).widget()
                        )
                        if isinstance(source_line_edit, QLineEdit):
                            source_line_edit.setText(item["参照先"])

                    # 「保存先」を設定
                    target_folder_widget = self.table.cellWidget(current_row_count, 2)
                    if isinstance(target_folder_widget, QWidget):
                        target_line_edit = (
                            target_folder_widget.layout().itemAt(0).widget()
                        )
                        if isinstance(target_line_edit, QLineEdit):
                            target_line_edit.setText(item["保存先"])

        return settings_list, len(data_list)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
