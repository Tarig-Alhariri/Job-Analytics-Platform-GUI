# Руководство пользователя / User Guide / دليل المستخدم

## Быстрый старт / Quick Start / البدء السريع

### Русский
1. Скачайте все файлы проекта
2. Запустите `run.bat` (Windows) или `run.sh` (Linux/Mac)
3. Приложение запустится автоматически

### English
1. Download all project files
2. Run `run.bat` (Windows) or `run.sh` (Linux/Mac)
3. Application will start automatically

### العربية
1. حمّل جميع ملفات المشروع
2. شغّل `run.bat` (لـWindows) أو `run.sh` (لـLinux/Mac)
3. التطبيق سيبدأ تلقائياً

---

## Вкладка "Управление данными" / "Data Management" Tab / تبويب "إدارة البيانات"

### Русский
**Функции:**
- **Выбор папки**: Выберите исходную папку с данными
- **Создание аннотации**: Создает CSV файл с метаданными
- **Создание Dataset**: Реорганизует файлы в новую структуру
- **Поиск по дате**: Фильтрует данные по указанной дате

**Формат даты:** ДД/ММ/ГГГГ (например: 23/10/2023)

### English
**Functions:**
- **Select Folder**: Choose source data folder
- **Create Annotation**: Creates CSV file with metadata
- **Create Dataset**: Reorganizes files into new structure
- **Search by Date**: Filters data by specified date

**Date Format:** DD/MM/YYYY (e.g.: 23/10/2023)

### العربية
**الوظائف:**
- **اختيار المجلد**: اختر مجلد البيانات المصدر
- **إنشاء تعليقات توضيحية**: ينشئ ملف CSV مع البيانات الوصفية
- **إنشاء مجموعة بيانات**: يعيد تنظيم الملفات في هيكل جديد
- **البحث بالتاريخ**: يرشح البيانات حسب التاريخ المحدد

**صيغة التاريخ:** يوم/شهر/سنة (مثال: 23/10/2023)

---

## Вкладка "Извлечение данных" / "Data Extraction" Tab / تبويب "استخراج данных"

### Русский
**Функции:**
- **Поиск вакансий**: Введите ключевые слова (например: "python", "data science")
- **Количество страниц**: Укажите сколько страниц сканировать (1-5)
- **Запуск сканирования**: Начните процесс извлечения данных
- **Сохранение**: Сохраните результаты в CSV файл

**Рекомендации:**
- Используйте конкретные запросы для лучших результатов
- Начинайте с 1-2 страниц для тестирования

### English
**Functions:**
- **Job Search**: Enter keywords (e.g.: "python", "data science")
- **Number of Pages**: Specify how many pages to scan (1-5)
- **Start Scraping**: Begin data extraction process
- **Save**: Save results to CSV file

**Recommendations:**
- Use specific queries for better results
- Start with 1-2 pages for testing

### العربية
**الوظائف:**
- **بحث الوظائف**: أدخل الكلمات المفتاحية (مثال: "python", "data science")
- **عدد الصفحات**: حدد عدد الصفحات للمسح (1-5)
- **بدء الاستخراج**: ابدأ عملية استخراج البيانات
- **حفظ**: احفظ النتائج في ملف CSV

**التوصيات:**
- استخدم استعلامات محددة لنتائج أفضل
- ابدأ بصفحة أو صفحتين للاختبار

---

## Вкладка "Анализ данных" / "Data Analysis" Tab / تبويب "تحليل البيانات"

### Русский
**Функции:**
-  **Выбор файла**: Выберите CSV файл с данными вакансий
-  **Запуск анализа**: Создает 3 графика анализа
-  **Просмотр графиков**: Открывает отдельное окно с визуализацией

**Создаваемые графики:**
1. Столбчатая диаграмма - топ-3 категории вакансий
2. Ящик с усами - распределение длин заголовков
3. Гистограмма - частотное распределение заголовков

### English
**Functions:**
-  **Select File**: Choose CSV file with job data
-  **Run Analysis**: Creates 3 analysis charts
-  **View Charts**: Opens separate window with visualization

**Generated Charts:**
1. Bar chart - top 3 job categories
2. Box plot - title length distribution
3. Histogram - frequency distribution of titles

### العربية
**الوظائف:**
-  **اختيار الملف**: اختر ملف CSV ببيانات الوظائف
-  **تشغيل التحليل**: ينشئ 3 رسوم بيانية للتحليل
-  **عرض الرسوم**: يفتح نافذة منفصلة مع التصور البياني

**الرسوم الم generatedة:**
1. مخطط أعمدة - أفضل 3 فئات للوظائف
2. مخطط الصندوق - توزيع أطوال العناوين
3. المدرج التكراري - التوزيع التكراري للعناوين

---

## ⚠️ Решение проблем / Troubleshooting / استكشاف الأخطاء وإصلاحها

### Русский
**Проблема**: Приложение не запускается
**Решение**: Убедитесь, что установлен Python 3.12.0+

**Проблема**: Веб-скрапинг не работает
**Решение**: Проверьте подключение к интернету

**Проблема**: Графики не отображаются
**Решение**: Закройте и перезапустите приложение

### English
**Problem**: Application won't start
**Solution**: Ensure Python 3.12.0+ is installed

**Problem**: Web scraping not working
**Solution**: Check internet connection

**Problem**: Charts not displaying
**Solution**: Close and restart application

### العربية
**المشكلة**: التطبيق لا يبدأ
**الحل**: تأكد من تثبيت Python 3.12.0+

**المشكلة**: استخراج البيانات من الويب لا يعمل
**الحل**: تحقق من الاتصال بالإنترنت

**المشكلة**: الرسوم لا تظهر
**الحل**: أغلق التطبيق وأعد تشغيله

---

## Поддержка / Support / الدعم

### Русский
**Для дополнительной помощи:**
- Проверьте файл README.md
- Запустите тесты: `python -m unittest discover tests/ -v`
- Убедитесь, что все зависимости установлены

### English
**For additional help:**
- Check README.md file
- Run tests: `python -m unittest discover tests/ -v`
- Ensure all dependencies are installed

### العربية
**لمساعدة إضافية:**
- راجع ملف README.md
- شغّل الاختبارات: `python -m unittest discover tests/ -v`
- تأكد من تثبيت جميع المتطلبات

---

## Обновления / Updates / التحديثات

### Русский
**Версия 1.0.0:**
- Полная интеграция всех модулей
- 33 успешных теста
- Стабильная работа всех функций

### English
**Version 1.0.0:**
- Full integration of all modules
- 33 successful tests
- Stable operation of all functions

### العربية
**الإصدار 1.0.0:**
- تكامل كامل لجميع الوحدات
- 33 اختبار ناجح
- عمل مستقر لجميع الوظائف