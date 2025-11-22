"""Моудль с базовым классом для создания Writer'ов."""

from abc import abstractmethod


class BaseWriter:
    """Базовый класс для классов Wirter'ов.

    Они предоставляют методы для создания/заполнения/сохранения файла отчета.
    """

    def __init__(self, report_path, dir_path):
        """Инициализация путей для анализируемого каталога и для сохранения отчета.

        Args:
            report_path (str): путь для создания файла отчета
            dir_path (str): путь анализируемого каталога
        """
        self._report_path = report_path
        self._dir_path = dir_path

    @abstractmethod
    def create_file(self):
        """Создание файла отчета."""
        ...

    @abstractmethod
    def write_to_file(self, name:str, size:str, last_changed:str):
        """Вывод информации о файле/папке в файл отчета.

        Args:
            name (str): имя файла/папки
            size (str): размера файла в читаемом формате
            last_changed (str): дата последнего изменения в читаемом формате
        """
        ...

    @abstractmethod
    def save_file(self):
        """Сохранение файла отчета."""
        ...