"""ДЗ №6. Работа с файлами и контекстными менеджерами."""

import argparse
from report_manager import ReportManager

#Агрументы командной строки
parser = argparse.ArgumentParser(description="Анализатор каталогов")
parser.add_argument("--path", "-p", type=str,default=".", help="Путь к анализируемому каталогу")
parser.add_argument("--report", "-r", type=str,default="./report.pdf", help="Путь к файлу отчета")
arg_val = parser.parse_args()

try:
    #Инициализация объекта для работы со структурой каталога
    file_sys_rep = ReportManager(arg_val.path, arg_val.report)

    #Создание отчета о структуре файлов и папок
    file_sys_rep.make_report()
except ValueError as e:
    print(e)
except FileNotFoundError as e:
    print(e)