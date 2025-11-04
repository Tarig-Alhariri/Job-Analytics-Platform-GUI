"""
Лабораторная работа 5 - Интегрированное приложение
Упрощенный главный интерфейс с 3 вкладками

Laboratory Work 5 - Integrated Application  
Simplified main interface with 3 tabs

العمل المخبري 5 - التطبيق المتكامل
واجهة رئيسية مبسطة بثلاثة تبويبات
"""

import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QPixmap

from data_utils import get_data_by_date
from annotation import create_annotation_file
from reorganize_dataset import reorganize_dataset
from web_scraping import scrape_wuzzuf_jobs, save_jobs_to_csv
from data_analysis import analyze_job_data_with_charts


class WebScrapingThread(QThread):
    """
    Поток для веб-скрапинга для предотвращения зависания GUI
    Web scraping thread to prevent GUI freezing
    ثريد استخراج البيانات من الويب لمنع تجمد الواجهة
    """
    
    finished = Signal(bool)
    progress = Signal(str)
    data_ready = Signal(list)
    
    def __init__(self, search_query: str, max_pages: int):
        """
        Инициализация потока веб-скрапинга
        Initialization of web scraping thread
        تهيئة ثريد استخراج البيانات من الويب
        
        Args:
            search_query: Поисковый запрос для вакансий
            search_query: Search query for job vacancies
            search_query: استعلام البحث للوظائف
            
            max_pages: Максимальное количество страниц для скрапинга
            max_pages: Maximum number of pages to scrape
            max_pages: الحد الأقصى لعدد الصفحات لاستخراج البيانات
        """
        super().__init__()
        self.search_query = search_query
        self.max_pages = max_pages
    
    def run(self):
        """
        Основное выполнение потока
        Main thread execution
        التنفيذ الرئيسي للثريد
        """
        try:
            self.progress.emit("Начало извлечения данных...")
            success, data_lists = scrape_wuzzuf_jobs(self.search_query, self.max_pages)
            if success:
                self.data_ready.emit(data_lists)
                self.finished.emit(True)
            else:
                self.finished.emit(False)
        except Exception as e:
            self.progress.emit(f"Ошибка: {str(e)}")
            self.finished.emit(False)


class ChartWindow(QMainWindow):
    """
    Окно для отображения графиков анализа
    Window for displaying analysis charts
    نافذة لعرض رسوم التحليل البياني
    """
    
    def __init__(self, chart_path: str):
        """
        Инициализация окна графиков
        Initialization of chart window
        تهيئة نافذة الرسوم البيانية
        
        Args:
            chart_path: Путь к файлу с графиками
            chart_path: Path to chart file
            chart_path: مسار ملف الرسوم البيانية
        """
        super().__init__()
        self.chart_path = chart_path
        self.setup_ui()
    
    def setup_ui(self):
        """
        Настройка интерфейса окна графиков
        Setup of chart window interface
        إعداد واجهة نافذة الرسوم البيانية
        """
        self.setWindowTitle("Графики анализа вакансий - Job Analysis Charts -")
        self.setMinimumSize(1400, 900)  # увеличение размера окна / increased window size / زيادة حجم النافذة
        
        central = QWidget()
        layout = QVBoxLayout(central)
        
        # Отображение изображения графиков
        # Displaying chart images
        # عرض صور الرسوم البيانية
        if os.path.exists(self.chart_path):
            image_label = QLabel()
            pixmap = QPixmap(self.chart_path)
            
            # Основная модификация - большой размер изображения
            # Main modification - large image size
            # التعديل الرئيسي - حجم الصورة الكبير
            image_label.setPixmap(pixmap.scaled(1200, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)
        else:
            error_label = QLabel("Файл графиков не найден - Charts file not found ")
            error_label.setStyleSheet("color: red; font-size: 16px; text-align: center; padding: 20px;")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)
        
        # Информация о графиках
        # Information about charts
        # معلومات عن الرسوم البيانية
        info_label = QLabel(
            "Создано 3 графика:\n"
            "Столбчатая диаграмма для топ-3 категорий вакансий\n" 
            "Ящик с усами для длин заголовков\n"
            "Гистограмма распределения длин заголовков\n\n"
        )
        info_label.setStyleSheet("background-color: #f8f9fa; padding: 15px; border-radius: 5px; font-size: 14px; margin: 10px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Кнопка закрытия
        # Close button
        # زر الإغلاق
        close_btn = QPushButton("Закрыть окно - Close Window - ")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("QPushButton { background-color: #e74c3c; color: white; font-weight: bold; padding: 12px; font-size: 14px; }")
        layout.addWidget(close_btn)
        
        self.setCentralWidget(central)


class MainWindow(QMainWindow):
    """
    Главное окно приложения 
    Main application window
    النافذة الرئيسية للتطبيق
    """
    
    def __init__(self):
        """
        Инициализация главного окна
        Main window initialization
        تهيئة النافذة الرئيسية
        """
        super().__init__()
        self.setWindowTitle("Лабораторная работа 5 - Интегрированное приложение")
        self.setMinimumSize(900, 600)
        self.source_folder = ""
        self.scraped_data = None
        self.setup_ui()

    def setup_ui(self):
        """
        Настройка пользовательского интерфейса
        User interface setup
        إعداد واجهة المستخدم
        """
        # Основные вкладки
        # Main tabs
        # التبويبات الرئيسية
        tabs = QTabWidget()
        
        # Вкладка управления данными
        # Data management tab
        # تبويب إدارة البيانات
        dataset_tab = QWidget()
        self.setup_dataset_tab(dataset_tab)
        
        # Вкладка извлечения данных
        # Data extraction tab
        # تبويب استخراج البيانات
        scraping_tab = QWidget()
        self.setup_scraping_tab(scraping_tab)
        
        # Вкладка анализа данных
        # Data analysis tab
        # تبويب تحليل البيانات
        analysis_tab = QWidget()
        self.setup_analysis_tab(analysis_tab)
        
        tabs.addTab(dataset_tab, " Управление данными")
        tabs.addTab(scraping_tab, " Извлечение данных")
        tabs.addTab(analysis_tab, " Анализ данных")
        
        self.setCentralWidget(tabs)

    def setup_dataset_tab(self, tab):
        """
        Настройка вкладки управления данными
        Setup of data management tab
        إعداد تبويب إدارة البيانات
        
        Args:
            tab: Виджет вкладки
            tab: Tab widget
            tab: عنصر تبويب الواجهة
        """
        layout = QVBoxLayout(tab)

        # Выбор папки
        # Folder selection
        # اختيار المجلد
        folder_layout = QHBoxLayout()
        self.folder_path = QLineEdit()
        folder_btn = QPushButton("Выбрать папку")
        folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(QLabel("Исходная папка:"))
        folder_layout.addWidget(self.folder_path)
        folder_layout.addWidget(folder_btn)

        # Кнопки управления
        # Control buttons
        # أزرار التحكم
        btn1 = QPushButton("Создать файл аннотации")
        btn1.clicked.connect(self.create_annotation)
        
        btn2 = QPushButton("Создать новый Dataset")
        btn2.clicked.connect(self.reorganize_dataset)

        # Поиск по дате
        # Search by date
        # البحث بالتاريخ
        date_layout = QHBoxLayout()
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("ДД/ММ/ГГГГ")
        date_btn = QPushButton("Получить данные по дате")
        date_btn.clicked.connect(self.search_by_date)
        date_layout.addWidget(QLabel("Введите дату:"))
        date_layout.addWidget(self.date_input)
        date_layout.addWidget(date_btn)

        # Таблица данных
        # Data table
        # جدول البيانات
        self.table = QTableWidget()

        layout.addLayout(folder_layout)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addLayout(date_layout)
        layout.addWidget(QLabel("Отображение данных:"))
        layout.addWidget(self.table)

    def setup_scraping_tab(self, tab):
        """
        Настройка вкладки извлечения данных
        Setup of data extraction tab
        إعداد تبويب استخراج البيانات
        
        Args:
            tab: Виджет вкладки
            tab: Tab widget
            tab: عنصر تبويب الواجهة
        """
        layout = QVBoxLayout(tab)

        # Параметры поиска
        # Search parameters
        # معايير البحث
        input_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setText("python")
        self.search_input.setPlaceholderText("Введите поисковый запрос")
        self.pages_input = QLineEdit()
        self.pages_input.setText("2")
        self.pages_input.setPlaceholderText("Количество страниц")
        input_layout.addWidget(QLabel("Поисковый запрос:"))
        input_layout.addWidget(self.search_input)
        input_layout.addWidget(QLabel("Страницы:"))
        input_layout.addWidget(self.pages_input)

        # Кнопки управления
        # Control buttons
        # أزرار التحكم
        btn_layout = QHBoxLayout()
        self.scrape_btn = QPushButton("Начать извлечение данных")
        self.scrape_btn.clicked.connect(self.start_scraping)
        self.scrape_btn.setStyleSheet("QPushButton { background-color: #e67e22; color: white; font-weight: bold; padding: 10px; }")
        
        self.save_btn = QPushButton("Сохранить данные в CSV")
        self.save_btn.clicked.connect(self.save_data)
        self.save_btn.setEnabled(False)
        self.save_btn.setStyleSheet("QPushButton { background-color: #27ae60; color: white; font-weight: bold; padding: 10px; }")
        
        btn_layout.addWidget(self.scrape_btn)
        btn_layout.addWidget(self.save_btn)

        # Результаты
        # Results
        # النتائج
        self.scrape_log = QTextEdit()
        self.scrape_log.setMaximumHeight(100)
        self.scrape_log.setPlaceholderText("Здесь будет отображаться журнал выполнения...")
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            "Должность", "Компания", "Местоположение", "Навыки", "Ссылка", "Дата"
        ])

        layout.addLayout(input_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("Журнал выполнения:"))
        layout.addWidget(self.scrape_log)
        layout.addWidget(QLabel("Результаты:"))
        layout.addWidget(self.results_table)

    def setup_analysis_tab(self, tab):
        """
        Настройка вкладки анализа данных
        Setup of data analysis tab
        إعداد تبويب تحليل البيانات
        
        Args:
            tab: Виджет вкладки
            tab: Tab widget
            tab: عنصر تبويب الواجهة
        """
        layout = QVBoxLayout(tab)

        # Выбор файла
        # File selection
        # اختيار الملف
        file_layout = QHBoxLayout()
        self.analysis_file = QLineEdit()
        self.analysis_file.setPlaceholderText("Выберите CSV файл с данными вакансий")
        file_btn = QPushButton("Выбрать файл CSV")
        file_btn.clicked.connect(self.select_analysis_file)
        file_layout.addWidget(QLabel("Файл данных:"))
        file_layout.addWidget(self.analysis_file)
        file_layout.addWidget(file_btn)

        # Кнопка анализа
        # Analysis button
        # زر التحليل
        self.analyze_btn = QPushButton("Запустить анализ с графиками")
        self.analyze_btn.clicked.connect(self.run_analysis)
        self.analyze_btn.setStyleSheet("QPushButton { background-color: #9b59b6; color: white; font-weight: bold; padding: 12px; }")

        # Результаты
        # Results
        # النتائج
        self.analysis_result = QTextEdit()
        self.analysis_result.setPlaceholderText("Здесь будут отображаться результаты анализа...")

        # Информационное сообщение
        # Information message
        # رسالة معلوماتية
        note_label = QLabel(" Примечание: Будут созданы 3 графика и отображены в отдельном окне\n")
        note_label.setStyleSheet("color: #7f8c8d; font-size: 12px; background-color: #f8f9fa; padding: 10px; border-radius: 5px;")
        note_label.setWordWrap(True)

        layout.addLayout(file_layout)
        layout.addWidget(self.analyze_btn)
        layout.addWidget(QLabel("Отчет анализа:"))
        layout.addWidget(self.analysis_result)
        layout.addWidget(note_label)

    #МЕТОДЫ УПРАВЛЕНИЯ ДАННЫМИ / DATA MANAGEMENT METHODS / طرق إدارة البيانات

    def select_folder(self):
        """
        Выбор исходной папки
        Select source folder
        اختيار المجلد المصدر
        """
        folder = QFileDialog.getExistingDirectory(self, "Выберите исходную папку")
        if folder:
            self.source_folder = folder
            self.folder_path.setText(folder)

    def create_annotation(self):
        """
        Создание файла аннотации
        Create annotation file
        إنشاء ملف التعليقات التوضيحية
        """
        if not self.source_folder:
            self.show_error("Пожалуйста, сначала выберите исходную папку")
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Сохранить файл аннотации", 
            "", 
            "CSV Files (*.csv)"
        )
        
        if save_path:
            try:
                create_annotation_file(self.source_folder, save_path)
                self.show_info(f"Файл аннотации успешно создан:\n{save_path}")
            except Exception as e:
                self.show_error(f"Не удалось создать файл:\n{str(e)}")

    def reorganize_dataset(self):
        """
        Реорганизация набора данных
        Reorganize dataset
        إعادة تنظيم مجموعة البيانات
        """
        if not self.source_folder:
            self.show_error("Пожалуйста, сначала выберите исходную папку")
            return
        
        dest_folder = QFileDialog.getExistingDirectory(
            self, 
            "Выберите целевую папку"
        )
        
        if dest_folder:
            try:
                reorganize_dataset(self.source_folder, dest_folder)
                self.show_info("Новый набор данных успешно создан")
            except Exception as e:
                self.show_error(f"Не удалось создать набор данных:\n{str(e)}")

    def search_by_date(self):
        """
        Поиск данных по дате
        Search data by date
        البحث في البيانات حسب التاريخ
        """
        date = self.date_input.text().strip()
        if not date:
            self.show_error("Пожалуйста, введите дату")
            return
        
        if not self.source_folder:
            self.show_error("Пожалуйста, сначала выберите исходную папку")
            return
        
        # Поиск CSV файла в папке
        # Search for CSV file in folder
        # البحث عن ملف CSV في المجلد
        csv_path = None
        for file in os.listdir(self.source_folder):
            if file.endswith(".csv"):
                csv_path = os.path.join(self.source_folder, file)
                break
        
        if not csv_path:
            self.show_error("CSV файл не найден в выбранной папке")
            return
        
        try:
            data = get_data_by_date(date, csv_path)
            self.display_table_data(data)
        except Exception as e:
            self.show_error(f"Не удалось загрузить данные:\n{str(e)}")

    def display_table_data(self, data):
        """
        Отображение данных в таблице
        Display data in table
        عرض البيانات في الجدول
        
        Args:
            data: Данные для отображения
            data: Data to display
            data: البيانات لعرضها
        """
        if data is None or data.empty:
            self.show_info("Нет данных за эту дату")
            return
        
        self.table.setColumnCount(len(data.columns))
        self.table.setRowCount(len(data))
        self.table.setHorizontalHeaderLabels(data.columns)

        for i in range(len(data)):
            for j in range(len(data.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))

        self.table.resizeColumnsToContents()

    #МЕТОДЫ ИЗВЛЕЧЕНИЯ ДАННЫХ / DATA EXTRACTION METHODS / طرق استخراج البيانات

    def start_scraping(self):
        """
        Начало процесса извлечения данных
        Start data extraction process
        بدء عملية استخراج البيانات
        """
        search = self.search_input.text().strip()
        if not search:
            self.show_error("Пожалуйста, введите поисковый запрос")
            return
        
        try:
            pages = int(self.pages_input.text())
            if pages <= 0:
                raise ValueError
        except ValueError:
            self.show_error("Пожалуйста, введите положительное целое число для страниц")
            return

        self.scrape_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.scrape_log.clear()
        self.scrape_log.append("Начало процесса извлечения")

        self.scraping_thread = WebScrapingThread(search, pages)
        self.scraping_thread.progress.connect(self.scrape_log.append)
        self.scraping_thread.data_ready.connect(self.on_scraping_done)
        self.scraping_thread.finished.connect(self.on_scraping_finished)
        self.scraping_thread.start()

    def on_scraping_done(self, data):
        """
        Обработка завершения извлечения данных
        Handle scraping completion
        معالجة انتهاء استخراج البيانات
        
        Args:
            data: Извлеченные данные
            data: Extracted data
            data: البيانات المستخرجة
        """
        self.scraped_data = data
        self.save_btn.setEnabled(True)
        self.display_scraped_data(data)

    def on_scraping_finished(self, success):
        """
        Обработка завершения потока извлечения
        Handle scraping thread completion
        معالجة انتهاء ثريد الاستخراج
        
        Args:
            success: Успешность выполнения
            success: Success status
            success: حالة النجاح
        """
        self.scrape_btn.setEnabled(True)
        if success:
            self.scrape_log.append("Извлечение данных завершено успешно")
        else:
            self.scrape_log.append("Не удалось извлечь данные")

    def display_scraped_data(self, data):
        """
        Отображение извлеченных данных в таблице
        Display scraped data in table
        عرض البيانات المستخرجة في الجدول
        
        Args:
            data: Извлеченные данные
            data: Scraped data
            data: البيانات المستخرجة
        """
        job_titles, companies, dates, locations, skills, links = data
        row_count = len(job_titles)
        
        self.results_table.setRowCount(row_count)
        
        for i in range(row_count):
            self.results_table.setItem(i, 0, QTableWidgetItem(job_titles[i]))
            self.results_table.setItem(i, 1, QTableWidgetItem(companies[i]))
            self.results_table.setItem(i, 2, QTableWidgetItem(locations[i]))
            self.results_table.setItem(i, 3, QTableWidgetItem(skills[i]))
            self.results_table.setItem(i, 4, QTableWidgetItem(links[i]))
            self.results_table.setItem(i, 5, QTableWidgetItem(dates[i]))
        
        self.results_table.resizeColumnsToContents()
        self.scrape_log.append(f"Отображено {row_count} записей в таблице")

    def save_data(self):
        """
        Сохранение извлеченных данных в CSV
        Save extracted data to CSV
        حفظ البيانات المستخرجة في CSV
        """
        if not self.scraped_data:
            self.show_error("Нет данных для сохранения")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Сохранить данные", 
            "jobs.csv", 
            "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                if save_jobs_to_csv(self.scraped_data, file_path):
                    self.show_info(f"Данные успешно сохранены в:\n{file_path}")
                else:
                    self.show_error("не удалось сохранить данные")
            except Exception as e:
                self.show_error(f"не удалось сохранить данные:\n{str(e)}")

    #МЕТОДЫ АНАЛИЗА ДАННЫХ / DATA ANALYSIS METHODS / طرق تحليل البيانات

    def select_analysis_file(self):
        """
        Выбор файла для анализа
        Select file for analysis
        اختيار ملف للتحليل
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Выберите файл данных", 
            "", 
            "CSV Files (*.csv)"
        )
        
        if file_path:
            self.analysis_file.setText(file_path)

    def run_analysis(self):
        """
        Запуск анализа данных с графиками
        Run data analysis with charts
        تشغيل تحليل البيانات مع الرسوم البيانية
        """
        file_path = self.analysis_file.text()
        if not file_path or not os.path.exists(file_path):
            self.show_error("Пожалуйста, выберите правильный файл данных")
            return
        
        self.analysis_result.clear()
        self.analyze_btn.setEnabled(False)
        self.analysis_result.append("Анализ данных и создание графиков...")
        
        try:
            success, report, chart_path = analyze_job_data_with_charts(file_path)
            
            if success:
                self.analysis_result.append(report)
                self.analysis_result.append("\n" + "="*50)
                self.analysis_result.append("Анализ и создание графиков завершены успешно")
                
                # Отображение графиков
                # Display charts
                # عرض الرسوم البيانية
                if chart_path and os.path.exists(chart_path):
                    self.display_charts(chart_path)
                else:
                    self.analysis_result.append("\nНе удалось автоматически отобразить графики")
            else:
                self.analysis_result.append(f"{report}")
        
        except Exception as e:
            self.analysis_result.append(f"Ошибка анализа:\n{str(e)}")
        
        finally:
            self.analyze_btn.setEnabled(True)

    def display_charts(self, chart_path: str):
        """
        Отображение графиков анализа
        Display analysis charts
        عرض رسوم التحليل البياني
        
        Args:
            chart_path: Путь к файлу с графиками
            chart_path: Path to chart file
            chart_path: مسار ملف الرسوم البيانية
        """
        try:
            self.chart_window = ChartWindow(chart_path)
            self.chart_window.show()
            self.analysis_result.append("\nГрафики отображены в новом окне")
        except Exception as e:
            self.analysis_result.append(f"Не удалось отобразить графики: {str(e)}")

    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ / HELPER METHODS / الطرق المساعدة

    def show_error(self, message):
        """
        Показать сообщение об ошибке
        Show error message
        عرض رسالة خطأ
        
        Args:
            message: Текст сообщения
            message: Message text
            message: نص الرسالة
        """
        QMessageBox.critical(self, "Ошибка", message)

    def show_info(self, message):
        """
        Показать информационное сообщение
        Show information message
        عرض رسالة معلومات
        
        Args:
            message: Текст сообщения
            message: Message text
            message: نص الرسالة
        """
        QMessageBox.information(self, "Информация", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Лабораторная работа 5")
    app.setApplicationVersion("1.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())