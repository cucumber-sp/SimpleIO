from __future__ import annotations
import os
import shutil
import sys
from types import NoneType
from typing import Generator

class BasePath: #Abstract path

    __path: str

    @property
    def path(self) -> str:
        return str(os.path.abspath(self.__path)).replace("\\", "/").rstrip("/")

    @path.setter
    def path(self, value: str) -> NoneType:
        self.__path = str(os.path.abspath(value)).replace("\\", "/").rstrip("/")

    def __init__(self, init_path: str) -> None:
        self.path = init_path

    @property
    def parent_path(self) -> str:
        return os.path.dirname(self.path)

    def __str__(self) -> str:
        return self.path

    def __eq__(self, __o: object) -> bool:
        return str(self) == str(__o)

    def __ne__(self, __o: object) -> bool:
        return not self == __o


class FolderPath(BasePath):

    @property
    def folder_name(self) -> str:
        return os.path.basename(self.path)

    def __init__(self, init_path: str) -> None:
        super().__init__(init_path)
    
    def extend(self, *value: str) -> FolderPath:
        self.path = os.path.join(self.path, *value)
        return self

    def clone(self) -> FolderPath:
        return FolderPath(self.path)
    
    def clone_and_extend(self, *value: str) -> FolderPath:
        return self.clone().extend(*value)
    
    def create_folder(self) -> FolderPath:
        if (not os.path.exists(self.path)):
            os.makedirs(self.path)
        return self

    def rename_folder(self, value: str) -> FolderPath:
        os.rename(self.path, self.parent.extend(value))
        self.path = self.parent.extend(value).path
        return self
    
    def delete_folder(self) -> FolderPath:
        shutil.rmtree(self.path, True)
        return self

    def extend_to_file(self, value: str) -> FilePath:
        return FilePath(self.clone_and_extend(value).path)

    @property
    def parent(self) -> FolderPath:
        return FolderPath(self.parent_path)

    def get_relative_path(self, root: str) -> str:
        return os.path.relpath(self.path, root)

    def get_folders_in_folder(self) -> Generator[FolderPath, NoneType, NoneType]:
        childs: list[os.DirEntry] = list(filter(lambda x: os.path.isdir(x.path), os.scandir(self.path)))
        for folder in childs:
            yield FolderPath(folder.path)
    
    def get_files_in_folder(self) -> Generator[FilePath, NoneType, NoneType]:
        childs: list[os.DirEntry] = list(filter(lambda x: os.path.isfile(x.path), os.scandir(self.path)))
        for file in childs:
            yield FilePath(file.path)
    
    @property
    def folder_exist(self) -> bool:
        return os.path.exists(self.path)
    
    def move_folder(self, path: FolderPath) -> FolderPath:
        shutil.move(self.path, path.path)
        return path

class FilePath(BasePath):
    
    def __init__(self, init_path: str) -> None:
        super().__init__(init_path)

    @property
    def file_name(self) -> str:
        return os.path.basename(self.path)

    def rename_file(self, name_with_extension: str):
        os.rename(self.path, self.parent.extend_to_file(name_with_extension).path)
        self.path = self.parent.extend_to_file(name_with_extension).path
        return self

    @property
    def clean_file_name(self) -> str:
        return os.path.splitext(self.file_name)[0]

    @property
    def file_extension(self) -> str:
        return os.path.splitext(self.file_name)[1][1:]
    
    @property
    def parent(self) -> FolderPath:
        return FolderPath(self.parent_path)

    @property
    def file_exists(self) -> bool:
        return os.path.exists(self.path)

    def write_text(self, text: str) -> FilePath:
        with open(self.create_file().path, "w") as f:
            f.write(text)
        return self
    
    def append_text(self, text: str) -> FilePath:
        with open(self.create_file().path, "a") as f:
            f.write(text)
        return self
    
    def read_text(self) -> str:
        with open(self.create_file().path, "r") as f:
            text = f.read()
        return text

    def read_bytes(self) -> bytes:
        with open(self.create_file().path, "rb") as f:
            bytes = f.read()
        return bytes
    
    def write_bytes(self, data: bytes) -> FilePath:
        with open(self.create_file().path, "wb") as f:
            f.write(bytes)
        return self

    def create_file(self) -> FilePath:
        self.parent.create_folder()
        if (not self.file_exists):
            f = open(self.path, "w")
            f.close()
        return self
    
    def delete_file(self) -> FilePath:
        os.remove(self.path)
        return self
    
    def copy(self, path: FilePath) -> FilePath:
        path.create_file()
        shutil.copyfile(self.path, path.path)
        return path
    
    def move(self, path: FilePath) -> FilePath:
        self.copy(path)
        self.delete_file()
        return path

if __name__ == "__main__":
    script_folder = FolderPath(sys.path[0])
    text_file = script_folder.extend_to_file("info.txt").write_text("hello world")
    input("press any key")
    text_file.move(text_file.parent.extend("Some Directory").extend_to_file("new file.txt"))
