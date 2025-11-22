"""Модуль для работы со структурой каталога и составления отчета

Содержит классы ReportType(Enum) и ReportManager
"""

from enum import Enum
from pathlib import Path
from zipfile import ZipFile, BadZipFile
import datetime
from .writers import DocxWriter, XlsxWriter, PdfWriter, JsonWriter, CsvWriter

class ReportType(Enum):
    """Набор значений "Тип отчета" - допустимые форматы
    для вывода отчета по структуре каталога

    Args:
        Enum (str): формат файла
    """
    DOCX = "docx"
    XLSX = "xlsx"
    PDF  = "pdf"
    CSV  = "csv"
    JSON = "json"

class ReportManager():
    """Класс структуры каталога, предоставляющий функционал для
    вывода информации о структуре указанного каталога со всеми вложенными
    папками/файлами. Отчет формируется в нескольких форматах в зависимости
    от типа отчета ReportType, определяемого расширением файла"""

    def __init__(self, path, report):
        """Инициализация и проверка корректности пути к каталогу и пути для файла отчета.
        Здесь также определяется тип отчета по расширению файла.

        Args:
            path (str): путь к каталогу для описания структуры
            report (str): путь для создания файла отчета

        Raises:
            FileNotFoundError: указанный каталог path не существует
        """
        self.__path = path
        self.__report = report
        #Инициализация объект Path из pathlib для работы с файловой системой
        self.__file_path = Path(self.__path).absolute()
        self.__file_report = Path(self.__report)
        #Проверка существования файла
        if not self.__file_path.exists():
            raise FileNotFoundError(f'Путь {self.__path} не существует')
        self.__report_type = self.__get_report_type_by_extension(self.__file_report.suffix)

    def __get_report_type_by_extension(self, extension:str)->ReportType:
        """Получение типа отчета по расширению файла отчета

        Args:
            extension (str): расширение файла отчета

        Raises:
            ValueError: недопустимый формат отчета

        Returns:
            ReportType: тип отчета
        """

        extension = extension.lower()
        try:
            return ReportType(extension[1:] if extension[0] == '.' else extension)
        except ValueError:
            raise ValueError(f'Недопустимый тип отчета: {extension}')
        
    def make_report(self):
        """Создание файла отчета с выводом в него информации о всех файлах/папках

        Raises:
            ValueError: неизвестный тип отчета
        """

        #Создание всех промежуточных папок, если их нет
        self.__file_report.parent.mkdir(parents=True, exist_ok=True)

        #Словарь Writer'ов
        REPORT_WRITERS = {
            ReportType.DOCX: DocxWriter,
            ReportType.XLSX: XlsxWriter,
            ReportType.CSV: CsvWriter,
            ReportType.JSON: JsonWriter,
            ReportType.PDF: PdfWriter,
        }

        #Класс Writer'а
        try:
            writer_class = REPORT_WRITERS[self.__report_type]
        except KeyError:
            raise ValueError(f"Writer для типа отчета {self.__report_type} не реализован")

        #Создание Writer'а и вывод файла отчета
        writer = writer_class(self.__file_report, self.__file_path)
        writer.create_file()
        self.__write_dir_structure(writer.write_to_file)
        writer.save_file()

    def __write_dir_structure(self, write_func):
        """Проход всех вложенных в каталог файлов и папок, в том числе ZIP

        Args:
            write_func (func): функция-writer, выводящая информацию о файле/папке в отчет
        """

        #Рекурсивный перебор структуры каталога
        #Сортировка нужна, чтобы выводить папку + все файлы из папки подряд
        for file in sorted(self.__file_path.rglob('*')): 
            #Обработка файлов/папок
            write_func(file, 
                'ПАПКА' if not file.is_file() else self.__readable_size(file.stat().st_size),
                datetime.datetime.fromtimestamp(int(file.stat().st_mtime)))
            #Дополнительная обработка ZIP архивов
            if file.suffix.lower() == '.zip':
                try:
                    with ZipFile(file, 'r') as zipf:
                        #Поскольку данные rglob('*') и infolist() немного отличаются,
                        #в infolist() могут отсутствовать отдельные папки, поэтому
                        #необходимо получить из infolist() данные в нужном виде

                        #1. Сбор всех папок
                        infolist = zipf.infolist()
                        zip_paths = set()
                        for info in infolist:
                            info_parts = Path(info.filename).parts
                            for i in range(1, len(info_parts)):
                                i_path = Path(*info_parts[:i])
                                if not str(i_path).endswith('/'):
                                    zip_paths.add(Path(file).joinpath(Path(str(i_path) + '/')))

                        #Добавление папок в список путей
                        zip_items = []
                        for zp in zip_paths:
                            zip_items.append({
                                'path': Path(file).joinpath(zp),
                                'is_dir': True,
                                'size': 'ПАПКА',
                                'mtime': ''
                            })

                        #Сбор всех файлов и недостающих папок из infolist
                        for info in infolist:
                            zitem_path = Path(file).joinpath(info.filename)
                            if zitem_path not in zip_paths:
                                zip_items.append({
                                    'path': zitem_path,
                                    'is_dir': info.is_dir(),
                                    'size': "ПАПКА" if info.is_dir() else self.__readable_size(info.file_size),
                                    'mtime': datetime.datetime(*info.date_time)
                                })
                        #Сортировка по путям к файлу, чтобы выводить файлы по папкам
                        zip_items.sort(key = lambda x: Path(x['path']).as_posix())

                        #Вывод полученного списка
                        for z_i in zip_items:
                            write_func(str(z_i['path']), z_i['size'], z_i['mtime'])
                except BadZipFile:
                    print(f'{file} - поврежденный .zip')

    def __readable_size(self, bytes):
        """Преобразование размера файла в читаемый формат

        Args:
            bytes (int): количество байт

        Returns:
            str: размер файла в читаемом формате
        """
        for unit in ['Б', 'КБ', 'МБ']:
            if bytes < 1024:
                return f'{bytes:.2f}{unit}'
            bytes /= 1024
        return f'{bytes:.2f}ГБ'