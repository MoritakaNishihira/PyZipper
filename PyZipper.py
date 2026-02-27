import os
import zipfile
import shutil
from concurrent.futures import ThreadPoolExecutor

import traceback


def log_message(message: str, level="INFO"):
    formatted_message = f"{level}: {message}"
    with open("process_log.txt", "a", encoding="shift_jis") as log_file:
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
        error_message = f"圧縮中にエラーが発生しました: {e}\n{traceback.format_exc()}"
        log_message(error_message, level="ERROR")
        return False


def delete_folder(folder_path: str) -> bool:
    try:
        shutil.rmtree(folder_path)
        return True
    except Exception as e:
        error_message = f"フォルダ '{os.path.basename(folder_path)}' の削除中にエラーが発生しました: {e}\n{traceback.format_exc()}"
        log_message(error_message, level="ERROR")
        return False


def process_folder(directory_path: str, folder_name: str):
    folder_path = os.path.join(directory_path, folder_name)
    zip_file_path = generate_unique_zip_path(directory_path, folder_name)

    if zip_folder(folder_path, zip_file_path):
        if not delete_folder(folder_path):
            log_message(
                f"'{folder_name}' フォルダの削除に失敗しました。", level="WARNING"
            )

    log_message(f"'{folder_name}' フォルダを処理完了")


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

    log_message("start...")

    with ThreadPoolExecutor() as executor:
        for folder_name in folder_names:
            executor.submit(process_folder, directory_path, folder_name)

    log_message("...complete !!")


if __name__ == "__main__":
    target_directory = "/volume2/Public/jobs/PyZipper"

    if os.path.exists(target_directory) and os.path.isdir(target_directory):
        zip_folders_in_directory(target_directory)
    else:
        log_message(
            f"指定されたディレクトリ '{target_directory}' が存在しないか、ディレクトリではありません。",
            level="ERROR",
        )
