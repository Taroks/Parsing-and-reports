import sys
from PySide6.QtCore import Qt, QTimer, QThread, Signal, Slot, QEvent, QSize
from PySide6.QtWidgets import QApplication, QSizePolicy, QFrame, QScrollArea, QWidget, QFileDialog,  QStyleOptionTab, QStyle, QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, QCheckBox, QTextEdit, QTabBar, QLabel, QLineEdit, QPushButton, QMessageBox, QProgressBar, QDialog, QGridLayout, QListView, QTabWidget
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPalette, QColor, QPainter, QPen
from datetime import datetime
from back import Database, Pathing, Parsing
import json
import os


class DarkTab(QWidget):
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            palette = self.palette()
            if self.windowState() & Qt.WindowActive:
                # Устанавливаем темный цвет фона вкладки при активации окна
                palette.setColor(QPalette.Window, QColor(45, 45, 45))
            else:
                # Устанавливаем темный цвет фона вкладки при деактивации окна
                palette.setColor(QPalette.Window, QColor(45, 45, 45))
            self.setPalette(palette)
        super().changeEvent(event)


class DarkTabBar(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QTabBar::tab {{
                background-color: rgb(45, 45, 45);
                color: rgb(255, 255, 255);
                padding: 8px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}

            QTabBar::tab:selected {{
                background-color: rgb(60, 60, 60);
            }}

            QTabWidget::pane {{
                background-color: rgb(45, 45, 45);
            }}

            QPushButton {{
                background-color: rgb(45, 45, 45);
                color: rgb(255, 255, 255);
                border: none;
                padding: 8px;
                border-radius: 4px;
                selection-background-color: rgb(45, 45, 45);
            }}

            QPushButton:hover {{
                background-color: rgb(60, 60, 60);
            }}

            QPushButton:pressed {{
                background-color: rgb(45, 45, 45);
            }}
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor(255, 255, 255))
        brush = QColor(45, 45, 45)
        selected_brush = QColor(60, 60, 60)

        # Заливка фона вкладки
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawRect(self.rect())

        # Рисование вкладок
        for index in range(self.count()):
            option = self.tabBar().tabRect(index)
            is_selected = self.currentIndex() == index

            if is_selected:
                painter.setBrush(selected_brush)
            else:
                painter.setBrush(brush)

            painter.setPen(Qt.NoPen)
            painter.drawRect(option)

            painter.setPen(pen)
            painter.drawText(option, Qt.AlignCenter, self.tabText(index))

        painter.end()

    def tabSizeHint(self, index):
        size_hint = super().tabSizeHint(index)
        size_hint.setHeight(30)
        size_hint.setWidth(size_hint.width() + 10)
        return size_hint


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простое приложение")
        self.resize(800, 200)  # Устанавливаем начальные размеры окна
        self.database = Database()
        self.checkboxes = {}  # Создаем список для чекбоксов
        self.scroll_area = None  # Ссылка на QScrollArea
        self.first_show_all = True  # Флаг первого вызова show_all_items()
        self.scroll_area = None
        self.scroll_widget = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)  # Создаем вертикальный макет
        self.setLayout(layout)

        self.tab_widget = DarkTabBar()  # Создаем виджет вкладок
        layout.addWidget(self.tab_widget)

        # Создаем и добавляем первую вкладку
        tab1 = DarkTab()
        self.setup_tab1(tab1)
        self.tab_widget.addTab(tab1, "Вкладка 1")

        # Создаем и добавляем вторую вкладку
        tab2 = QWidget()
        self.setup_tab2(tab2)
        self.tab_widget.addTab(tab2, "Вкладка 2")

        # Создаем и добавляем вторую вкладку
        tab3 = QWidget()
        self.setup_tab3(tab3)
        self.tab_widget.addTab(tab3, "Вкладка 3")

        # Применяем стиль к таб-бару
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background-color: rgb(45, 45, 45);
                color: rgb(255, 255, 255);
                padding: 8px;
                margin: 0px;
            }
            QTabBar::tab:selected {
                background-color: rgb(60, 60, 60);
            }
            QTabWidget::pane {
                margin: 20px;
            }
        """)

        # Установка выравнивания вкладок в центр
        self.tab_widget.setContentsMargins(20, 0, 20, 0)

    def setup_tab1(self, tab):
        layout = QGridLayout(tab)  # Создаем сеточный макет для первой вкладки

        label = QLabel("Введите ссылку для добавления")
        layout.addWidget(label, 0, 0, 1, 2)  # Добавляем надпись в макет

        self.input_field = QLineEdit()  # Создаем поле ввода
        layout.addWidget(self.input_field, 1, 0, 1, 2)  # Добавляем поле ввода в макет

        button4 = QPushButton("Добавить путь")  # Создаем кнопку "Добавить путь"
        button4.clicked.connect(self.add_path)  # Подключаем сигнал нажатия кнопки к методу add_path
        layout.addWidget(button4, 2, 0)  # Добавляем кнопку "Добавить путь" в макет

        button1 = QPushButton("Добавить запись")  # Создаем кнопку "Добавить запись"
        button1.clicked.connect(self.add_record)  # Подключаем сигнал нажатия кнопки к методу add_record
        layout.addWidget(button1, 2, 1)  # Добавляем кнопку "Добавить запись" в макет

        button2 = QPushButton("Парсинг")  # Создаем кнопку "Парсинг и отчет"
        button2.clicked.connect(self.open_parsing_dialog)  # Подключаем сигнал нажатия кнопки к методу open_parsing_dialog
        layout.addWidget(button2, 3, 0)  # Добавляем кнопку "Парсинг и отчет" в макет

        button3 = QPushButton("Создать отчет")  # Создаем кнопку "Создать отчет"
        button3.clicked.connect(self.make_report)  # Подключаем сигнал нажатия кнопки к методу make_report
        layout.addWidget(button3, 3, 1)  # Добавляем кнопку "Создать отчет" в макет

        button = QPushButton("Удалить последнюю ссылку", self)
        button.clicked.connect(self.delete_last_link)
        layout.addWidget(button, 4, 0)  # Добавляем кнопку "Удалить последнюю ссылку" в макет

        button5 = QPushButton("Отчет инвалид")
        button5.clicked.connect(self.generate_report)
        layout.addWidget(button5, 4, 1)

        self.record_window = RecordWindow(self.input_field.text())  # Инициализируем атрибут record_window
        palette = tab.palette()
        palette.setColor(QPalette.Window, QColor(45, 45, 45))  # Устанавливаем темный цвет фона вкладки

        tab.setPalette(palette)
        # Изменение выравнивания элементов и стилей окна
        layout.setAlignment(Qt.AlignTop)
        button4.setAutoFillBackground(True)
        button4.setStyleSheet("background-color: rgb(65, 65, 65); color: rgb(255, 255, 255);")

        button1.setAutoFillBackground(True)
        button1.setStyleSheet("background-color: rgb(65, 65, 65); color: rgb(255, 255, 255);")

        button2.setAutoFillBackground(True)
        button2.setStyleSheet("background-color: rgb(65, 65, 65); color: rgb(255, 255, 255);")

        button3.setAutoFillBackground(True)
        button3.setStyleSheet("background-color: rgb(65, 65, 65); color: rgb(255, 255, 255);")

        button.setAutoFillBackground(True)
        button.setStyleSheet("background-color: rgb(65, 65, 65); color: rgb(255, 255, 255);")

        button5.setAutoFillBackground(True)
        button5.setStyleSheet("background-color: rgb(65, 65, 65); color: rgb(255, 255, 255);")

    def setup_tab2(self, tab):
        # Создаем вертикальный макет для второй вкладки
        layout = QGridLayout(tab)

        # Создаем кнопку "Показать все"
        show_all_button = QPushButton("Показать все")
        layout.addWidget(show_all_button)

        # Создаем кнопку "Удалить выбранное"
        delete_selected_button = QPushButton("Удалить выбранное")
        layout.addWidget(delete_selected_button)

        delete_old_button = QPushButton("Удалить 6+ месяцев")
        layout.addWidget(delete_old_button)

        # Создаем виджет, которому будет присвоен макет для списка и чекбоксов
        widget = QWidget()
        widget_layout = QVBoxLayout()
        widget.setLayout(widget_layout)

        # Создаем список элементов
        list_widget = QListWidget()
        widget_layout.addWidget(list_widget)

        # Подключаем сигналы к кнопкам
        show_all_button.clicked.connect(lambda: self.show_all_items(list_widget))
        delete_selected_button.clicked.connect(lambda: self.delete_selected_items(list_widget))
        delete_old_button.clicked.connect(self.delete_old_items)

        # Добавляем виджет с макетом для списка и чекбоксов в общий макет
        layout.addWidget(widget)

        # Создаем QScrollArea и добавляем его в отдельный макет
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.scroll_widget = QFrame()
        self.scroll_widget_layout = QHBoxLayout(self.scroll_widget)
        self.scroll_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_widget_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        scroll_area.setWidget(self.scroll_widget)
        scroll_area.setMinimumWidth(self.width())

        # Добавляем QScrollArea в отдельный макет
        layout.addWidget(scroll_area)

        # Устанавливаем макет во вторую вкладку
        tab.setLayout(layout)

        palette = tab.palette()
        palette.setColor(QPalette.Window, QColor(45, 45, 45))  # Устанавливаем темный цвет фона вкладки

        tab.setPalette(palette)
        # Изменение выравнивания элементов и стилей окна
        layout.setAlignment(Qt.AlignTop)
        delete_selected_button.setAutoFillBackground(True)
        delete_selected_button.setStyleSheet("background-color: rgb(65, 65, 65); color: rgb(255, 255, 255);")

        show_all_button.setAutoFillBackground(True)
        show_all_button.setStyleSheet("background-color: rgb(65, 65, 65); color: rgb(255, 255, 255);")

        delete_old_button.setAutoFillBackground(True)
        delete_old_button.setStyleSheet("background-color: rgb(65, 65, 65); color: rgb(255, 255, 255);")

        self.adjustSize()

    def setup_tab3(self, tab):
        keys_data = []
        items_data = []
        # Создаем вертикальный макет для третьей вкладки
        layout = QVBoxLayout(tab)

        # Читаем содержимое файла "известные тэги.json"
        if os.path.exists(f"{os.path.dirname(__file__)}/известные тэги.json"):
            if os.path.getsize(f"{os.path.dirname(__file__)}/известные тэги.json") != 0:
                with open(f"{os.path.dirname(__file__)}/известные тэги.json", "r", encoding='utf8') as file:
                    data = json.load(file)
            else:
                data = {}

        # Извлекаем надпись из данных файла
        label_text = "- Введите хэштег (его можно скопировать из ссылки. Например для хэштега идеи для бизнеса необходимая часть ссылки выглядит так idei-dlya-biznesa). \n так же вы можете указать цифру, если тэг есть в списке уже известных: " + str(data) + "\n- Также можете ввести название раздела. В таком случае нажмите вторую кнопку"

        # Создаем надпись
        label = QLabel(label_text)
        layout.addWidget(label)

        # Создаем строку ввода
        line_edit = QLineEdit()
        layout.addWidget(line_edit)

        # Создаем кнопку "parse_tags"
        parse_tags_button = QPushButton("parse_tags")
        parse_tags_button.clicked.connect(lambda: self.parse_tags_clicked(line_edit))
        layout.addWidget(parse_tags_button)

        # Применяем стили CSS с использованием палитры для элементов
        palette = tab.palette()
        palette.setColor(QPalette.Window, QColor(45, 45, 45))  # Устанавливаем темный цвет фона вкладки

        label.setAutoFillBackground(True)
        label.setPalette(palette)
        label.setStyleSheet("color: rgb(255, 255, 255);")

        line_edit.setAutoFillBackground(True)
        line_edit.setPalette(palette)
        line_edit.setStyleSheet("color: rgb(255, 255, 255);")

        parse_tags_button.setAutoFillBackground(True)
        parse_tags_button.setPalette(palette)
        parse_tags_button.setStyleSheet("background-color: rgb(65, 65, 65); color: rgb(255, 255, 255);")




        # Устанавливаем макет в третью вкладку
        tab.setLayout(layout)

    def delete_old_items(self):
        database = Database()
        result = database.delete_old()

        if result:
            QMessageBox.information(self, "Успех", "Все старые ссылки удалены")
        else:
            QMessageBox.warning(self, "Внимание", "Старых ссылок нет")

    def parse_tags_clicked(self, line_edit):
        tag = line_edit.text()

        parsing_tags_window = ParsingTagsWindow(tag, self)
        parsing_tags_window.exec_()

    def add_path(self):
        path_window = PathWindow()
        path_window.exec_()

    def add_record(self):
        record_window = RecordWindow(self.input_field.text())  # Создаем экземпляр окна RecordWindow, передавая текст из поля ввода
        record_window.exec_()  # Отображаем окно записи

    def make_report(self):
        report_window = MakeReportWindow()  # Создаем экземпляр окна MakeReportWindow

    def open_parsing_dialog(self):
        dialog = ParsingDialog(self)
        dialog.exec()

    def delete_last_link(self):
        if self.record_window is None:
            QMessageBox.warning(self, "Ошибка", "Окно записи не создано")
            return

        last_link = self.record_window.get_last_added_link()
        if last_link:
            self.record_window.delete_last_link()
        else:
            QMessageBox.warning(self, "Ошибка", "Последняя добавленная ссылка не найдена")

    def show_all_items(self, list_widget):
        items = self.database.show_all()  # Получение списка всех элементов из базы данных
        list_widget.clear()  # Очистка списка

        # Отображение каждого элемента и добавление чекбокса
        checkbox_style = """
             QCheckBox {
                 spacing: 5px;
                 margin-left: 0px;
                 margin-right: 0px;
             }
             QCheckBox::indicator {
                 width: 20px;
                 height: 20px;
             }
         """
        self.checkboxes = {}  # Используем словарь для хранения чекбоксов и элементов

        for item in items:
            item_widget = QWidget()  # Создаем виджет для элемента списка
            item_layout = QHBoxLayout(item_widget)  # Создаем горизонтальный макет для элемента
            item_layout.setContentsMargins(0, 0, 0, 0)  # Устанавливаем отступы макета в 0
            item_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Выравнивание по левому краю

            checkbox = QCheckBox()
            checkbox.setStyleSheet(checkbox_style)  # Применяем стиль к чекбоксу
            checkbox.setChecked(False)
            item_layout.addWidget(checkbox)
            self.checkboxes[checkbox] = item  # Добавляем чекбокс в словарь

            label = QLabel(item)
            item_layout.addWidget(label)

            # Устанавливаем выравнивание для надписи справа от чекбокса
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            list_item = QListWidgetItem()  # Создаем элемент списка
            list_item.setSizeHint(item_widget.sizeHint())  # Устанавливаем размер элемента
            list_widget.addItem(list_item)  # Добавляем элемент в QListWidget
            list_widget.setItemWidget(list_item, item_widget)  # Устанавливаем виджет элемента

        if self.scroll_widget_layout:
            self.scroll_widget_layout.addStretch()  # Добавляем растяжку
        self.adjustSize()

    def delete_selected_items(self, list_widget):
        """
        Метод для удаления выбранных элементов.
        Принимает параметры:
        - checkboxes: список объектов QCheckBox, представляющих флажки.
        """
        items_to_delete = []  # Список элементов, которые нужно удалить

        # Поиск выбранных элементов и добавление их в список items_to_delete
        for checkbox, item in self.checkboxes.items():
            if checkbox.isChecked():
                items_to_delete.append(item)

        success = self.database.delete_chosen(items_to_delete)  # Удаление выбранных элементов из базы данных

        if success:
            # Вывод всплывающего окна с сообщением "Успешно удалены" и списком ссылок
            message = "Успешно удалены:\n\n"
            message += "\n".join(items_to_delete)
            QMessageBox.information(self, "Успешное удаление", message)
            self.show_all_items(list_widget)
        else:
            QMessageBox.warning(self, "Ошибка удаления", "Ошибка при удалении элементов.")

    def generate_report(self):
        progress_window = ProgressWindow(self)
        progress_window.exec_()

    def update_progress(self, progress):
        print(f"Progress: {progress}%")


class PathWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Путь для файлов")
        layout = QVBoxLayout()  # Создаем вертикальный макет
        self.setLayout(layout)

        text_layout = QHBoxLayout()  # Создаем горизонтальный макет для кнопок
        layout.addLayout(text_layout)  # Добавляем горизонтальный макет в вертикальный макет

        label = QLabel("Задайте путь, по которому будет находиться файл отчета")
        text_layout.addWidget(label)

        input_layout = QHBoxLayout()  # Создаем горизонтальный макет для кнопок
        layout.addLayout(input_layout)  # Добавляем горизонтальный макет в вертикальный макет

        self.input_field = QLineEdit(self)  # Создаем поле ввода
        default_path = os.path.expanduser("~/Desktop")  # Стандартный путь рабочего стола для macOS
        self.input_field.setText(default_path)  # Предзаполняем поле ввода стандартным путем
        input_layout.addWidget(self.input_field)  # Добавляем поле ввода в макет

        button_layout = QHBoxLayout()  # Создаем горизонтальный макет для кнопки
        layout.addLayout(button_layout)  # Добавляем горизонтальный макет в вертикальный макет

        ok_button = QPushButton("ОК")  # Создаем кнопку "ОК"
        ok_button.clicked.connect(
            self.on_ok_button_clicked)  # Подключаем сигнал нажатия кнопки к методу on_ok_button_clicked
        button_layout.addWidget(ok_button)  # Добавляем кнопку "ОК" в горизонтальный макет

    def on_ok_button_clicked(self):
        path = self.input_field.text()  # Получаем текст из поля ввода\
        if path:
            c = Pathing(path)
            p = c.save_path(path)
            if not p:
                QMessageBox.warning(self, "Ошибка", "Путь уже задан")
                self.accept()  # Закрываем окно
                return
            else:
                QMessageBox.warning(self, "результат", f"Путь {p} успешно задан")
                self.accept()  # Закрываем окно
                return
        else:
            try:
                with open(f"{os.path.dirname(__file__)}/ways.json", "r", encoding='utf8') as file:
                    p = json.load(file)
            except:
                return "путь файла не задан"
        # Делаем что-то с полученным путем, например, передаем его в другой метод или сохраняем
        self.accept()  # Закрываем окно
        return p


class MakeReportWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание отчета")
        print("aaaaaaaa")
        ways_file_path = os.path.join(os.path.dirname(__file__), 'ways.json')

        if not os.path.isfile(ways_file_path) or os.stat(ways_file_path).st_size == 0:
            QMessageBox.warning(self, "Ошибка", "Путь файла не задан")
            self.reject()  # Закрываем окно
        else:
            with open(ways_file_path, 'r') as file:
                ways_content = file.read()

            way = ways_content.strip('"')  # Удаление внешних кавычек из строки пути

            self.database = Database()
            self.database.create_report(way)
            QMessageBox.information(self, "Результат", "Отчет создан")
            self.accept()  # Закрываем окно


class RecordWindow(QMessageBox):
    last_added_link = ""  # Переменная класса для хранения последней добавленной ссылки

    def __init__(self, record):
        super().__init__()
        self.setWindowTitle("Запись")  # Устанавливаем заголовок окна
        self.database = Database()
        # Проверяем наличие повторяющейся ссылки
        is_repeating = self.database.search_repeating(record)
        if is_repeating:
            self.setText("Ссылка уже введена")
        else:
            # Вызываем метод add_link класса Database и получаем результат
            result = self.database.add_link(record)

            if result == "Успех":
                # Сохраняем последнюю добавленную ссылку в переменную класса
                self.last_added_link = record
            if result.startswith("Ссылка"):
                self.__class__.last_added_link = record

            self.setText(f"Результат: {result}")

    @classmethod
    def save_last_added_link(cls, link):
        cls.last_added_link = link

    @classmethod
    def get_last_added_link(cls):
        return cls.last_added_link

    @Slot()
    def delete_last_link(self):
        last_link = RecordWindow.get_last_added_link()
        if last_link:
            success = self.database.quick_deleting(last_link)
            if success:
                QMessageBox.information(self, "Успех", f"Удалена последняя ссылка: {last_link}")
            else:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении ссылки: {last_link}")
        else:
            QMessageBox.warning(self, "Ошибка", "Последняя добавленная ссылка не найдена")


# Класс диалогового окна парсинга
class ParsingDialog(QDialog):
    progressChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Parsing Progress")
        self.resize(300, 200)

        self.progress_bar = QProgressBar(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_bar)

        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.parsing_thread = ParsingThread(self)
        self.parsing_thread.progressChanged.connect(self.update_progress)
        self.parsing_thread.finished.connect(self.parsing_finished)
        self.parsing_thread.errorOccurred.connect(self.show_error_message)

        self.start_parsing()

    def start_parsing(self):
        self.parsing_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        self.progressChanged.emit(progress)

    def parsing_finished(self, less_then_month, success_parsing):
        if less_then_month:
            message = f"Для ссылок из списка less_then_month с последнего парсинга не прошел месяц:\n" + "\n".join(less_then_month)
            if success_parsing:
                message += "\n\nОстальные ссылки успешно спаршены"
        elif success_parsing:
            message = "Все ссылки успешно спаршены"
        else:
            message = "Для всех ссылок с последнего парсинга не прошел месяц"

        self.progress_bar.setValue(100)
        QMessageBox.information(self, "Parsing Finished", message)

    def show_error_message(self, error_message):
        QMessageBox.critical(self, "Parsing Error", error_message)


# Класс выполнения парсинга в фоновом режиме
class ParsingThread(QThread):
    progressChanged = Signal(int)
    finished = Signal(list, list)
    errorOccurred = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        try:
            parsing = Parsing(self.update_progress)
            less_then_month, success_parsing = parsing.parsing()
            self.finished.emit(less_then_month, success_parsing)
        except Exception as e:
            error_message = str(e)
            self.errorOccurred.emit(error_message)

    def update_progress(self, progress):
        self.progressChanged.emit(progress)


class ProgressWindow(QDialog):
    progressChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Parsing Progress")
        self.resize(300, 200)

        self.progress_bar = QProgressBar(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_bar)

        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.parsing_thread = ProgressThread(self)
        self.parsing_thread.progressChanged.connect(self.update_progress)
        self.parsing_thread.finished.connect(self.parsing_finished)

        self.start_parsing()

    def start_parsing(self):
        self.parsing_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def parsing_finished(self, success_parsing):
        message = "Все ссылки успешно спаршены"
        self.progress_bar.setValue(100)

        # Закомментируйте или удалите следующую строку
        # success_parsing = self.parsing_thread.parsing_instance.up_to_date_report(way)

        QMessageBox.information(self, "Parsing Finished", message)

        # Добавьте self.parsing_thread.quit() для завершения потока
        self.parsing_thread.quit()

        # Добавьте self.parsing_thread.wait() для ожидания завершения потока
        self.parsing_thread.wait()

    def get_way_from_file(self):
        ways_file_path = os.path.join(os.path.dirname(__file__), 'ways.json')
        if not os.path.isfile(ways_file_path) or os.stat(ways_file_path).st_size == 0:
            QMessageBox.warning(self, "Ошибка", "Путь файла не задан")
            self.reject()  # Закрываем окно
        else:
            with open(ways_file_path, 'r') as file:
                ways_content = file.read()

            return ways_content.strip('"')  # Удаление внешних кавычек из строки пути


class ProgressThread(QThread):
    progressChanged = Signal(int)
    finished = Signal(list)
    errorOccurred = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parsing_instance = Parsing(self.update_progress)

    def run(self):
        try:
            way = self.get_way_from_file()
            self.parsing_instance.up_to_date_report(way)
            self.finished.emit([])  # Отправляем пустой список вместо success_parsing
        except Exception as e:
            error_message = str(e)
            self.errorOccurred.emit(error_message)

    def update_progress(self, progress):
        self.progressChanged.emit(progress)

    def get_way_from_file(self):
        ways_file_path = os.path.join(os.path.dirname(__file__), 'ways.json')
        if not os.path.isfile(ways_file_path) or os.stat(ways_file_path).st_size == 0:
            raise Exception("Путь файла не задан")
        else:
            with open(ways_file_path, 'r') as file:
                ways_content = file.read()

            return ways_content.strip('"')  # Удаление внешних кавычек из строки пути


class ParsingTagsWindow(QDialog):
    def __init__(self, tag, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Parsing Tags")
        self.resize(300, 200)

        self.progress_bar = QProgressBar(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_bar)

        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.tag = tag  # Сохраняем значение тега

        self.parsing_thread = ParsingTagsThread(self.tag)
        self.parsing_thread.progressChanged.connect(self.update_progress)
        self.parsing_thread.finished.connect(self.parsing_finished)

        self.start_parsing()

    def start_parsing(self):
        self.parsing_thread.tag = self.tag  # Передаем значение self.tag в поток
        self.parsing_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def parsing_finished(self, success_parsing):
        message = "Все ссылки успешно спаршены"
        self.progress_bar.setValue(100)

        # Закомментируйте или удалите следующую строку
        # success_parsing = self.parsing_thread.parsing_instance.up_to_date_report(way)

        QMessageBox.information(self, "Parsing Finished", message)

        # Добавьте self.parsing_thread.quit() для завершения потока
        self.parsing_thread.quit()

        # Добавьте self.parsing_thread.wait() для ожидания завершения потока
        self.parsing_thread.wait()


class ParsingTagsThread(QThread):
    progressChanged = Signal(int)
    finished = Signal(list)
    errorOccurred = Signal(str)

    def __init__(self, tag, parent=None):
        super().__init__(parent)
        self.tag = tag  # Добавляем атрибут self.tag
        self.parsing_instance = Parsing(self.update_progress)

    def run(self):
        try:
            way = self.get_way_from_file()
            self.parsing_instance.parse_tags(self.tag, way)  # Передаем значение self.tag в метод parse_tags()
            self.finished.emit([])  # Отправляем пустой список вместо success_parsing
        except Exception as e:
            error_message = str(e)
            self.errorOccurred.emit(error_message)

    def update_progress(self, progress):
        self.progressChanged.emit(progress)

    def get_way_from_file(self):
        ways_file_path = os.path.join(os.path.dirname(__file__), 'ways.json')
        if not os.path.isfile(ways_file_path) or os.stat(ways_file_path).st_size == 0:
            raise Exception("Путь файла не задан")
        else:
            with open(ways_file_path, 'r') as file:
                ways_content = file.read()

            return ways_content.strip('"')  # Удаление внешних кавычек из строки пути

