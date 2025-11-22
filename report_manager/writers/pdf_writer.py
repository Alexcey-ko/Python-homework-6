"""Модуль для вывода отчета о структуре каталога в формате PDF

Содержит класс PdfWriter
"""

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from ..base.base_writer import BaseWriter

class PdfWriter(BaseWriter):
    """Класс Writer для создания отчета в PDF формате"""

    #Размер шрифта заголовка
    HEADER_FONTSIZE = 14 
    #Размер шрифта структуры 
    BODY_FONTSIZE = 10
    #Начальная точка страницы
    BEGIN_PAGE = (30, 820)
    #Ширина линии структуры
    LINE_WIDTH = 1
    #Границы
    LEFT = 30
    TOP = 810
    BOTTOM = 20

    def __init__(self, report_path, dir_path):
        """Инициализация параметров вывода PDF файла.
        Регистрация шрифта для вывода текста.

        Args:
            report_path (str): путь для создания файла отчета
            dir_path (str): путь анализируемого каталога
        """

        super().__init__(report_path, dir_path)
        #Постраничный список операций для рендера
        self._pages_ops = [[]]
        #Canvas для отрисовки страниц
        self._pdf_canvas = None
        #Регистрирация шрифта Arial для кириллицы
        #Путь к шрифту относительно корня проекта
        base_dir = Path(__file__).resolve().parent.parent.parent
        arial_path = base_dir / 'resources' / 'fonts' / 'Arial.ttf'
        pdfmetrics.registerFont(TTFont('Arial', arial_path))

    def create_file(self):
        """Создание Canvas для отрисовки документа и
        вывод заголовка документа."""

        #Создание PDF canvas с размером страниц A4
        self._pdf_canvas = canvas.Canvas(self._report_path.as_posix(), pagesize = A4)
        
        #Заголовок документа
        self._pdf_canvas.setFont('Arial', type(self).HEADER_FONTSIZE)
        header_text = self._pdf_canvas.beginText(*type(self).BEGIN_PAGE)
        header_text.setLeading(type(self).HEADER_FONTSIZE * 1.1)  
        header_lines = [
            'Отчет о структуре файлов и папок каталога',
            str(self._dir_path),
        ]        
        for line in header_lines:
            header_text.textLine(line)
        self._pdf_canvas.drawText(header_text)

        #Параметры вывода структуры
        self._pdf_canvas.setFont('Arial', type(self).BODY_FONTSIZE)
        self._pdf_canvas.setLineWidth(type(self).LINE_WIDTH)

        #Вывод корневого каталога
        first_page_begin = (type(self).BEGIN_PAGE[0], type(self).BEGIN_PAGE[1] - type(self).HEADER_FONTSIZE * 3)
        self._pdf_canvas.drawString(*first_page_begin, str(self._dir_path))

        #Уровень вложенности
        self._deep_level = 0
        self._root = True
        self._line_height = type(self).BODY_FONTSIZE
        first_node = (first_page_begin[0] + self._line_height / 2, first_page_begin[1] - self._line_height)
        self._cur_page = 0
        self._deep_level_last_pos = [(self._cur_page, *first_node)]
        self._last_x = first_node[0]
        self._last_y = first_node[1]

    def write_to_file(self, name, size, last_changed):
        """Формирование списка операций для дальнейшей отрисовки 
        информации о файле/папке 

        Args:
            name (str): имя файла/папки
            size (str): размера файла в читаемом формате
            last_changed (str): дата последнего изменения в читаемом формате
        """

        #Определение глубины файла/папки относительно корневого каталога
        path = Path(name)
        relative_path = path.relative_to(self._dir_path)
        parts =  relative_path.parts
        new_deep_level = len(parts) - 1

        #Если глубина не изменилась, то необходимо
        if new_deep_level == self._deep_level:
            if not self._root:
                #Верхняя линия для первого узла на странице
                self._pages_ops[self._cur_page].append(('line', (self._last_x, self._last_y + self._line_height, self._last_x, self._last_y)))
            #Запоминание страницы и координат последнего узла на текущем уровне
            self._deep_level_last_pos[new_deep_level] = (self._cur_page, self._last_x, self._last_y)
            
        #Если глубина увеличилась, необходимо сдвинуть координату X на новый уровень и запомнить узел
        elif new_deep_level > self._deep_level:
            self._last_x += self._line_height
            self._deep_level_last_pos.append((self._cur_page, self._last_x, self._last_y))

        #Если глубина уменьшилась, необходимо отрисовать линию от текущего узла, до 
        #последнего запомненного узла на текущем уровне (он может быть на предыдущей странице)
        elif new_deep_level < self._deep_level:
            #Удаляем все уровни глубже, чем новый уровень
            self._deep_level_last_pos = self._deep_level_last_pos[: new_deep_level + 1]
            #Пересчитываем текущую X для нового уровня
            self._last_x = type(self).LEFT + self._line_height * (0.5 + new_deep_level)
            #Получаем сохранённую позицию для этого уровня
            last_page, last_x_saved, last_y_saved = self._deep_level_last_pos[new_deep_level]
            #Если текущая страница больше страницы сохраненнего узла, то нужно отрисовать:
            if self._cur_page > last_page:
                #Линию на текущей странице до TOP
                self._pages_ops[self._cur_page].append(('line', (self._last_x, type(self).TOP + self._line_height / 2, self._last_x, self._last_y)))
                for p in range(self._cur_page - 1, last_page, -1):
                    #Линии на промежуточных страницах от BOTTOM до TOP
                    self._pages_ops[p].append(('line', (last_x_saved, type(self).TOP + self._line_height / 2, last_x_saved, type(self).BOTTOM)))
                #И линию на странице сохраненного узла от BOOTOM до Y узла
                self._pages_ops[last_page].append(('line', (last_x_saved, last_y_saved, last_x_saved, type(self).BOTTOM)))
            else:
                #Если глубина уменьшилась на текущей странице, то нужно отрисовать 
                #только линию от текущего узла до сохраненного
                if self._cur_page == last_page:
                    self._pages_ops[self._cur_page].append(('line', (self._last_x, last_y_saved, self._last_x, self._last_y)))

            #Обновление узла для текущего уровня
            self._deep_level_last_pos[new_deep_level] = (self._cur_page, self._last_x, self._last_y)

        #Отрисовка текущего узла (|_ + текст)
        self._pages_ops[self._cur_page].append(('line', (self._last_x, self._last_y, self._last_x + self._line_height / 2, self._last_y)))
        self._pages_ops[self._cur_page].append(('line', (self._last_x, self._last_y + self._line_height / 2, self._last_x, self._last_y)))
        self._pages_ops[self._cur_page].append(('drawString', (self._last_x + 10, self._last_y - 3, f'{path.name} - {size} - {last_changed}')))

        #Обновление Y для следующего узла
        self._last_y -= self._line_height
        self._root = False

        #Достигнут конец страницы
        if self._last_y < type(self).BOTTOM:
            #Обновление параметров для новой страницы
            self._cur_page += 1
            self._pages_ops.append([])
            self._last_y = type(self).TOP
            self._root = True

        #Сохранение глубины узла
        self._deep_level = new_deep_level
        
    def save_file(self):
        """Отрисовка всех операций и сохранение файла отчета"""
        #Сохранение PDF документа
        self._render_canvas()
        self._pdf_canvas.save()

    def _render_canvas(self):
        """Постраничная отрисовка всех операций."""

        for page_ops in self._pages_ops:
            #Параметры вывода структуры
            self._pdf_canvas.setFont('Arial', type(self).BODY_FONTSIZE)
            self._pdf_canvas.setLineWidth(type(self).LINE_WIDTH)
            #Отрисовка всех операций страницы
            for op in page_ops:
                match op[0]:
                    case 'line':
                        self._pdf_canvas.line(*op[1])
                    case 'drawString':
                        self._pdf_canvas.drawString(*op[1])
            #Вывод страницы
            self._pdf_canvas.showPage()