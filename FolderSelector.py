import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Listbox, Button, END
import json


class FolderSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("フォルダセレクタ")

        self.folder_pairs = []

        self.listbox = Listbox(root)
        self.listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        frame = tk.Frame(root)
        frame.pack(pady=5)

        btn_add_pair = Button(frame, text="ペア追加", command=self.add_folder_pair)
        btn_add_pair.grid(row=0, column=0, padx=5)

        btn_remove_pair = Button(
            frame, text="選択削除", command=self.remove_selected_pair
        )
        btn_remove_pair.grid(row=0, column=1, padx=5)

        btn_save_config = Button(frame, text="設定保存", command=self.save_config)
        btn_save_config.grid(row=0, column=2, padx=5)

    def add_folder_pair(self):
        folder_path = filedialog.askdirectory(title="読み込みフォルダを選択")
        if not folder_path:
            return

        zip_path = filedialog.asksaveasfilename(
            title="ZIP保存先を選択",
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip")],
        )
        if not zip_path:
            return

        self.folder_pairs.append((folder_path, zip_path))
        self.listbox.insert(END, f"読み込み: {folder_path} -> 保存: {zip_path}")

    def remove_selected_pair(self):
        try:
            index = self.listbox.curselection()[0]
            self.folder_pairs.pop(index)
            self.listbox.delete(index)
        except IndexError:
            messagebox.showwarning("警告", "削除するアイテムを選択してください")

    def save_config(self):
        config_file = filedialog.asksaveasfilename(
            title="設定ファイル保存",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
        )
        if not config_file:
            return

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(self.folder_pairs, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("成功", f"設定ファイルが {config_file} に保存されました。")


if __name__ == "__main__":
    root = tk.Tk()
    app = FolderSelector(root)
    root.mainloop()
