import os
import zipfile
import shutil
from concurrent.futures import ThreadPoolExecutor
import json
import traceback


def log_message(message: str, level="INFO"):
    with open("process_log.txt", "a", encoding="shift-jis") as log_file:
        log_file.write(f"{level}: {message}\n")
    print(message)


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


def process_folder(folder_path: str, zip_file_path: str):
    if zip_folder(folder_path, zip_file_path):
        if not delete_folder(folder_path):
            log_message(
                f"'{os.path.basename(folder_path)}' フォルダの削除に失敗しました。",
                level="WARNING",
            )

    log_message(f"'{os.path.basename(folder_path)}' フォルダを処理完了")


def zip_folders_from_config(config_file: str):
    if not os.path.exists(config_file):
        log_message(f"設定ファイル '{config_file}' が存在しません。", level="ERROR")
        return

    with open(config_file, "r", encoding="utf-8") as f:
        folder_pairs = json.load(f)

    log_message("start...")

    with ThreadPoolExecutor() as executor:
        for folder_path, zip_file_path in folder_pairs:
            if not os.path.isdir(folder_path):
                log_message(
                    f"読み込み対象フォルダ '{folder_path}' が存在しません。",
                    level="ERROR",
                )
                continue

            executor.submit(process_folder, folder_path, zip_file_path)

    log_message("...complete !!")


if __name__ == "__main__":
    config_file = "config.json"  # 自動的に読み取る設定ファイル名
    if os.path.exists(config_file):
        zip_folders_from_config(config_file)
    else:
        log_message(f"設定ファイル '{config_file}' が存在しません。", level="ERROR")
