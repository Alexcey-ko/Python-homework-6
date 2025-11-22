"""Модуль для вывода отчета о структуре каталога в формате CSV

Содержит класс CsvWriter
"""

from ..base.base_writer import BaseWriter
import csv

class CsvWriter(BaseWriter):
    """Класс Writer для создания отчета в CSV формате"""
    
    def __init__(self, report_path, dir_path):
        super().__init__(report_path, dir_path)
        self._csv_file = None
        self._csv_writer = None

    def create_file(self):
        """Создание файла"""
        self._csv_file = open(self._report_path, 'w', encoding = 'utf-8')
        self._csv_writer = csv.writer(self._csv_file, delimiter = ";")
        self._csv_writer.writerow(['Имя файла', 'Размер', 'Последнее изменение'])

    def write_to_file(self, name, size, last_changed):
        """Сбор CSV данных
        
        Args:
            name (str): имя файла/папки
            size (str): размера файла в читаемом формате
            last_changed (str): дата последнего изменения в читаемом формате
        """
        self._csv_writer.writerow([str(name), str(size), str(last_changed)])
        
    def save_file(self):
        """Сохранение файла"""
        self._csv_file.close()
