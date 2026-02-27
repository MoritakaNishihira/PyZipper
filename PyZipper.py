import os
import zipfile
import shutil
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from tkinter import Tk, filedialog

import traceback


def log_message(message: str, level="INFO"):
    formatted_message = f"{level}: {message}"
    with open("process_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(formatted_message + "\n")
    print(formatted_message)


def zip_folder(folder_path: str, zip_file_path: str) -> bool:
    try:
        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)
                    zipf.write(file_path, arcname)
        return True
    except Exception as e:
        log_message(
            f"圧縮中にエラーが発生しました: {e}\n{traceback.format_exc()}",
            level="ERROR",
        )
        return False


def delete_folder(folder_path: str) -> bool:
    try:
        shutil.rmtree(folder_path)
        return True
    except Exception as e:
        log_message(
            f"フォルダ '{os.path.basename(folder_path)}' の削除中にエラーが発生しました: {e}\n{traceback.format_exc()}",
            level="ERROR",
        )
        return False


def process_folder(
    directory_path: str,
    folder_name: str,
    progress_queue: Queue,
    total_folders: int,
):
    folder_path = os.path.join(directory_path, folder_name)
    zip_file_path = generate_unique_zip_path(directory_path, folder_name)

    if zip_folder(folder_path, zip_file_path):
        delete_folder(folder_path)

    progress_queue.put(1)  # 進捗を通知
    completed = progress_queue.qsize()
    percent = (completed / total_folders) * 100

    # 進捗の出力
    progress_message = f"フォルダ圧縮中 {completed} / {total_folders} ({percent:.1f}%) "
    log_message(progress_message)


def generate_unique_zip_path(directory_path: str, folder_name: str) -> str:
    base_zip_file_path = os.path.join(directory_path, f"{folder_name}.zip")
    count = 1
    while os.path.exists(base_zip_file_path):
        base_zip_file_path = os.path.join(directory_path, f"{folder_name}_{count}.zip")
        count += 1
    return base_zip_file_path


def zip_folders_in_directory(directory_path: str):
    folder_names = sorted(
        [
            name
            for name in os.listdir(directory_path)
            if os.path.isdir(os.path.join(directory_path, name))
        ]
    )

    total = len(folder_names)
    progress_queue = Queue()

    log_message("start...")

    with ThreadPoolExecutor() as executor:
        for folder_name in folder_names:
            executor.submit(
                process_folder, directory_path, folder_name, progress_queue, total
            )

    log_message("...complete !!")


def select_directory():
    root = Tk()
    root.withdraw()
    directory_path = filedialog.askdirectory(title="フォルダを選択")

    if directory_path:
        zip_folders_in_directory(directory_path)
    else:
        log_message("ディレクトリが選択されませんでした。", level="INFO")


if __name__ == "__main__":
    select_directory()
