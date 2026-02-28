import os
import tkinter as tk
from tkinter import filedialog, messagebox
import json


class FolderSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Selector")

        # 追加ボタンを固定位置に配置
        self.add_button = tk.Button(root, text="+", command=self.show_add_entry)
        self.add_button.pack(side=tk.TOP, anchor=tk.NW)

        self.settings_frame = tk.Frame(self.root)
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.settings_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.settings_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.canvas.yview)

        self.listbox_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.listbox_frame, anchor="nw")
        self.listbox_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # ラベルを2行目から始める
        self.labels = ["設定名", "読込先", "保存先"]
        for idx, label in enumerate(self.labels):
            tk.Label(
                self.listbox_frame, text=label, borderwidth=1, relief="solid", width=30
            ).grid(row=1, column=idx + 1)

        self.settings = []
        self.load_settings()

    def show_add_entry(self):
        # 新しいエントリーフィールドを表示
        entry_frame = tk.Frame(self.listbox_frame)
        entry_frame.grid(row=len(self.settings) + 2, columnspan=len(self.labels) + 1)

        name_entry = tk.Entry(entry_frame, width=30)
        source_entry = tk.Entry(entry_frame, width=30)
        destination_entry = tk.Entry(entry_frame, width=30)

        name_entry.grid(row=0, column=1)
        source_entry.grid(row=0, column=2)
        destination_entry.grid(row=0, column=3)

        # 参照ボタン
        icon_path = os.path.join("icon", "folder_icon.png")
        icon_image = tk.PhotoImage(file=icon_path)
        image_label = tk.Label(entry_frame, image=icon_image)
        image_label.image = icon_image

        source_button = tk.Button(
            entry_frame,
            image=icon_image,
            command=lambda: self.select_folder(source_entry),
        )
        source_button.grid(row=0, column=4)

        destination_button = tk.Button(
            entry_frame,
            image=icon_image,
            command=lambda: self.select_folder(destination_entry),
        )
        destination_button.grid(row=0, column=6)

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
        )
        save_button.grid(row=0, column=7)

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
            frame = tk.Frame(self.listbox_frame, borderwidth=1, relief="solid")
            frame.grid(row=idx + 2, columnspan=len(self.labels) + 1)

            tk.Label(frame, text=setting["name"], width=30).grid(row=0, column=1)

            source_icon_path = os.path.join("icon", "folder_icon.png")
            source_icon_image = tk.PhotoImage(file=source_icon_path)
            source_icon_label = tk.Label(frame, image=source_icon_image)
            source_icon_label.image = source_icon_image
            source_icon_label.grid(row=0, column=2)

            tk.Label(frame, text=setting["source"], width=30).grid(row=0, column=3)

            destination_icon_path = os.path.join("icon", "folder_icon.png")
            destination_icon_image = tk.PhotoImage(file=destination_icon_path)
            destination_icon_label = tk.Label(frame, image=destination_icon_image)
            destination_icon_label.image = destination_icon_image
            destination_icon_label.grid(row=0, column=4)

            tk.Label(frame, text=setting["destination"], width=30).grid(row=0, column=5)

            delete_button = tk.Button(
                frame, text="❌", command=lambda idx=idx: self.delete_setting(idx)
            )
            delete_button.grid(row=0, column=6)

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
