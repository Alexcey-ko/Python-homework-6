"""Модуль для вывода отчета о структуре каталога в формате JSON

Содержит класс JsonWriter
"""

import json
from ..base.base_writer import BaseWriter

class JsonWriter(BaseWriter):
    """Класс Writer для создания отчета в JSON формате"""

    def __init__(self, report_path, dir_path):
        super().__init__(report_path, dir_path)
        self._json_file = None
        self._json_data = []

    def create_file(self):
        """Создание файла"""
        self._json_file = open(self._report_path, 'w', encoding = 'utf-8')

    def write_to_file(self, name, size, last_changed):
        """Сбор JSON данных
        
        Args:
            name (str): имя файла/папки
            size (str): размера файла в читаемом формате
            last_changed (str): дата последнего изменения в читаемом формате
        """
        self._json_data.append({'name': str(name),
                                'size': size,
                                'last_changed': str(last_changed)})
        
    def save_file(self):
        """Вывод данных в файл и сохранение файла"""
        json.dump(self._json_data, self._json_file, ensure_ascii = False, indent = 4)
        self._json_file.close()
