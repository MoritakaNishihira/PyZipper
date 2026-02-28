import os
import tkinter as tk
from tkinter import filedialog, messagebox
import json


class FolderSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Selector")
        self.root.geometry("600x400")

        # フォント設定
        self.font_label = ("Arial", 12)
        self.font_button = ("Arial", 12)

        # 追加ボタンを固定位置に配置
        self.add_button = tk.Button(
            root, text="+", command=self.show_add_entry, font=self.font_button
        )
        self.add_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)

        self.settings_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # スクロールバーの設定
        self.scrollbar = tk.Scrollbar(self.settings_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # キャンバスの設定
        self.canvas = tk.Canvas(
            self.settings_frame, yscrollcommand=self.scrollbar.set, bg="#f4f4f4"
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.canvas.yview)

        # リストボックスフレームの設定
        self.listbox_frame = tk.Frame(self.canvas, bg="#f4f4f4")
        self.canvas.create_window((0, 0), window=self.listbox_frame, anchor="nw")

        # スクロール範囲を調整
        self.listbox_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # ヘッダーの設定
        tk.Label(
            self.listbox_frame,
            text="設定名",
            borderwidth=1,
            relief="solid",
            width=30,
            font=self.font_label,
        ).grid(row=0, column=0, sticky=tk.W + tk.E)
        tk.Label(
            self.listbox_frame,
            text="",
            borderwidth=1,
            relief="solid",
            width=60,
            font=self.font_label,
        ).grid(row=0, column=1, sticky=tk.W + tk.E)

        self.settings = []
        self.load_settings()

    def show_add_entry(self):
        entry_frame = tk.Frame(self.listbox_frame, bg="#f4f4f4")
        entry_frame.grid(
            row=len(self.settings) + 1, columnspan=2, sticky=tk.W + tk.E, pady=(5, 0)
        )

        name_entry = tk.Entry(entry_frame, width=30, font=("Arial", 12))
        source_entry = tk.Entry(entry_frame, width=30, font=("Arial", 12))
        destination_entry = tk.Entry(entry_frame, width=30, font=("Arial", 12))

        name_entry.grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        source_entry.grid(row=0, column=1, padx=(0, 5), sticky=tk.W)

        # 参照ボタン
        icon_path = os.path.join("icon", "folder_icon.png")
        try:
            icon_image = tk.PhotoImage(file=icon_path)
            image_label = tk.Label(entry_frame, image=icon_image)
            image_label.image = icon_image

            source_button = tk.Button(
                entry_frame,
                image=icon_image,
                text="参照先",
                compound=tk.LEFT,
                command=lambda: self.select_folder(source_entry),
                font=self.font_button,
            )
            source_button.grid(row=0, column=2, padx=(5, 10), sticky=tk.W)

            destination_button = tk.Button(
                entry_frame,
                image=icon_image,
                text="保存先",
                compound=tk.LEFT,
                command=lambda: self.select_folder(destination_entry),
                font=self.font_button,
            )
            destination_button.grid(row=0, column=3, padx=(5, 10), sticky=tk.W)
        except tk.TclError:
            print(f"アイコンファイルが見つかりません: {icon_path}")

        # 保存ボタン
        save_button = tk.Button(
            entry_frame,
            text="保存",
            command=lambda: self.save_setting(
                name_entry.get(),
                source_entry.get(),
                destination_entry.get(),
                entry_frame,
            ),
            font=self.font_button,
        )
        save_button.grid(row=0, column=4, padx=(5, 10), sticky=tk.W)

    def select_folder(self, entry):
        folder_path = filedialog.askdirectory(title="フォルダを選択")
        if folder_path:
            entry.delete(0, tk.END)
            entry.insert(0, folder_path)

    def save_setting(self, name, source, destination, entry_frame):
        if not name or not source or not destination:
            messagebox.showwarning("警告", "すべてのフィールドを入力してください。")
            return

        setting_data = {"name": name, "source": source, "destination": destination}

        self.settings.append(setting_data)
        self.save_settings()
        entry_frame.destroy()
        self.update_listbox()

    def update_listbox(self):
        for widget in self.listbox_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.listbox_frame:
                widget.destroy()

        for idx, setting in enumerate(self.settings):
            frame = tk.Frame(
                self.listbox_frame, borderwidth=1, relief="solid", bg="#f4f4f4"
            )
            frame.grid(row=idx + 2, columnspan=5, sticky=tk.W + tk.E, pady=(0, 5))

            name_label = tk.Label(frame, text=setting["name"], font=self.font_label)
            name_label.grid(row=0, column=0, padx=10)

            path_label = tk.Label(
                frame,
                text=f"{setting['source']} -> {setting['destination']}",
                font=self.font_label,
                wraplength=350,
            )
            path_label.grid(row=0, column=1, padx=(0, 20), sticky=tk.W)

            delete_button = tk.Button(
                frame,
                text="❌",
                command=lambda idx=idx: self.delete_setting(idx),
                font=("Arial", 14),
            )
            delete_button.grid(row=0, column=2, padx=(10, 20))

    def delete_setting(self, index):
        response = messagebox.askyesno("確認", "この設定を削除しますか？")
        if response:
            del self.settings[index]
            self.save_settings()
            self.update_listbox()

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = []

        self.update_listbox()

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f, indent=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = FolderSelectorApp(root)
    root.mainloop()
