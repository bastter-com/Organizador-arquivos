import magic
import os
from sys import argv
from pprint import pprint


FOLDER_NAMES_TYPES = {
    "image/jpeg": "Imagens",
    "image/png": "Imagens",
    "image/gif": "Imagens",
    "image/tiff": "Imagens",
    "application/pdf": "PDFs",
    "application/msword": "Documentos",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "Documentos",
    "text/plain": "Documentos",
    "application/vnd.ms-powerpoint": "Powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "Powerpoint",
    "application/vnd.ms-excel": "Excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "Excel",
    "text/csv": "Excel",
}

PATH_SEP = os.path.sep

BASE_PATH = argv[1]


def get_files_info(path):
    """
    Get files info.
    """
    files = os.listdir(path)
    files = [os.path.join(path, file) for file in files]
    results = []
    for file_path in files:
        try:
            ftype = magic.from_file(file_path, mime=True)
        except IsADirectoryError:
            continue
        else:
            filename = file_path.split(PATH_SEP)[-1]
            results.append(
                {"path_file": file_path, "filetype": ftype, "filename": filename}
            )
    return results


def get_folder_name(file_info):
    """
    Get the folder name to put the file.
    """
    return FOLDER_NAMES_TYPES.get(file_info["filetype"]) or "Outros"


def check_and_create_new_directory(folder_name):
    target_path_folder = os.path.join(BASE_PATH, folder_name)
    dir_exist = os.path.exists(target_path_folder)
    if not dir_exist:
        print(f"Creating directory {folder_name}...")
        os.mkdir(target_path_folder)
        print(f"Folder {folder_name} created successfully!")
    else:
        print(f"Folder {folder_name} already exists!")


def put_files_into_directories(files_info):
    """
    Move files to new directories accordingly with mimetypes
    """
    for file_info in files_info:
        folder_name = get_folder_name(file_info)
        check_and_create_new_directory(folder_name)
        filename = file_info["filename"]
        print(f"Moving file {filename} to new folder {folder_name}")
        os.rename(
            file_info["path_file"],
            os.path.join(BASE_PATH, folder_name, filename)
        )
        print(f"File {filename} moved to folder {folder_name}!")


def main():
    results = get_files_info(BASE_PATH)
    put_files_into_directories(results)
    print("Finished!")


main()
