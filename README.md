# Python-homework-6

Выполнение домашнего задания №6. Контекстные менеджеры.

Для запуска требуется установить дополнительные сторонние зависимости:

```py
requires-python = ">=3.13,<4"
dependencies = [
    "openpyxl (>=3.1.5,<4.0.0)",
    "reportlab (>=4.4.5,<5.0.0)",
    "docx (>=0.2.4,<0.3.0)",
    "ruff (>=0.14.6,<0.15.0)"
]
```

Составление отчета по анализируемому каталогу осуществляется с помощью класса `ReportManager`, он описан в модуле `/src/Python-homework-6/report_manager/report_manager.py`.

Для создания и вывода информации в файлы используются классы `Writer'ы`, которые наследуются от базового класса `BaseWriter` - `/src/Python-homework-6/report_manager/base/base_writer.py`.

Для различных форматов реализованы разные классы `Writer'ы`:

- `DocxWriter` - `/src/Python-homework-6/report_manager/writers/docx_writer.py` для создания Word файла формата `.docx`

- `XlsxWriter` - `/src/Python-homework-6/report_manager/writers/xlsx_writer.py` для создания Excel файла формата `.xlsx`
  
- `PdfWriter` - `/src/Python-homework-6/report_manager/writers/pdf_writer.py` для создания Pdf файла формата `.pdf`

- `CsvWriter` - `/src/Python-homework-6/report_manager/writers/csv_writer.py` для создания Csv файла формата `.csv`

- `JsonWriter` - `/src/Python-homework-6/report_manager/writers/json_writer.py` для создания Json файла формата `.json`
