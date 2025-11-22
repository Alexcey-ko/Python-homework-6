"""Модуль для вывода отчета о структуре каталога в формате XLSX.

Содержит класс XlsxWriter.
"""

from openpyxl import Workbook
from openpyxl.styles import Border, Font, Side

from python_homework_6.report_manager.base.base_writer import BaseWriter


class XlsxWriter(BaseWriter):
    """Класс Writer для создания отчета в XLSX формате."""

    def __init__(self, report_path, dir_path):
        """Инициализация параметров вывода XLSX файла.

        Создание стилей/шрифтов для вывода.

        Args:
            report_path (str): путь для создания файла отчета
            dir_path (str): путь анализируемого каталога
        """
        super().__init__(report_path, dir_path)

        self._header_font = Font(name = 'Calibri', size = 12, bold=True, color='000000')
        side_medium = Side(border_style='medium', color='000000')
        self._border_medium = Border(left = side_medium, 
                                    right = side_medium, 
                                    top = side_medium, 
                                    bottom = side_medium)

    def create_file(self):
        """Создание WorkBook + WorkSheet и вывод заголовка."""
        #Создание рабочей книги с листом и названием
        self.__excel_wb = Workbook()
        self.__excel_ws =  self.__excel_wb.active
        self.__excel_ws.title = 'Иерархия каталога'

        #Строка с заголовком
        self.__excel_ws.append(['', f'Отчет о структуре файлов и папок каталога {self._dir_path}'])
        self.__excel_ws[1][1].font = self._header_font

        self.__excel_ws.append([])
        self.__excel_ws.row_dimensions[2].height = 7
        self.__excel_ws.column_dimensions['A'].width = 1

        #Заголовчная строка таблицы с данными
        self.__excel_ws.append(['', 'Имя файла/папки', 'Размер файла', 'Последнее изменение'])
        for i in range(3):
            self.__excel_ws[3][i + 1].font = self._header_font
            self.__excel_ws[3][i + 1].border = self._border_medium
        self.__excel_ws.column_dimensions['B'].width = 100
        self.__excel_ws.column_dimensions['C'].width = 25
        self.__excel_ws.column_dimensions['D'].width = 25

    def write_to_file(self, name, size, last_changed):
        """Вывод новой строки с данными в WorkSheet."""
        self.__excel_ws.append(['', str(name), size, last_changed])
        
    def save_file(self):
        """Сохранение файла отчета."""
        #Сохранение Excel документа
        self.__excel_wb.save(self._report_path)
