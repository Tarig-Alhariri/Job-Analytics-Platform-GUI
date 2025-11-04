# Лабораторная работа 5 - Интегрированное приложение  
# Laboratory Work 5 - Integrated Application  
# العمل المخبري 5 - التطبيق المتكامل

##  Описание / Description / الوصف

### Русский
Интегрированное десктопное приложение с графическим интерфейсом, объединяющее функционал веб-скрапинга, управления данными и анализа datasets. Приложение предоставляет удобный интерфейс для работы с вакансиями и файловыми системами.

### English
Integrated desktop application with graphical interface that combines web scraping, data management, and dataset analysis functionality. The application provides a user-friendly interface for working with job vacancies and file systems.

### العربية
تطبيق سطح مكتب متكامل بواجهة رسومية يجمع بين وظائف استخراج البيانات من الويب، إدارة البيانات، وتحليل مجموعات البيانات. التطبيق يوفر واجهة سهلة الاستخدام للعمل على الوظائف وأنظمة الملفات.

## Функционал / Features / الوظائف

### Русский
- **Управление данными**: Создание аннотаций, реорганизация датасетов
- **Веб-скрапинг**: Извлечение вакансий с Wuzzuf
- **Анализ данных**: Статистический анализ и визуализация
- **Графический интерфейс**: Интуитивный интерфейс с вкладками

### English
- **Data Management**: Annotation creation, dataset reorganization
- **Web Scraping**: Job vacancies extraction from Wuzzuf
- **Data Analysis**: Statistical analysis and visualization
- **Graphical Interface**: Intuitive tab-based interface

### العربية
- **إدارة البيانات**: إنشاء التعليقات التوضيحية، إعادة تنظيم مجموعات البيانات
- **استخراج البيانات من الويب**: استخراج الوظائف من موقع Wuzzuf
- **تحليل البيانات**: التحليل الإحصائي والتصور البياني
- **واجهة رسومية**: واجهة بديهية بنظام التبويبات

## Установка и запуск / Installation & Run / التثبيت والتشغيل

### Русский
1. Скачайте файлы проекта
2. Запустите `run.bat` (Windows) или `run.sh` (Linux/Mac)
3. Приложение автоматически создаст виртуальное окружение и установит зависимости

### English
1. Download project files
2. Run `run.bat` (Windows) or `run.sh` (Linux/Mac)
3. Application will automatically create virtual environment and install dependencies

### العربية
1. حمّل ملفات المشروع
2. شغّل `run.bat` (لـWindows) أو `run.sh` (لـLinux/Mac)
3. التطبيق سينشئ بيئة افتراضية تلقائياً ويقوم بتثبيت المتطلبات

## Технологии / Technologies / التقنيات

### Русский
- **PySide6**: Графический интерфейс
- **pandas**: Анализ и обработка данных
- **matplotlib**: Визуализация и графики
- **requests/BeautifulSoup**: Веб-скрапинг
- **Pillow**: Работа с изображениями

### English
- **PySide6**: Graphical user interface
- **pandas**: Data analysis and manipulation
- **matplotlib**: Visualization and charts
- **requests/BeautifulSoup**: Web scraping
- **Pillow**: Image processing

### العربية
- **PySide6**: واجهة المستخدم الرسومية
- **pandas**: تحليل البيانات ومعالجتها
- **matplotlib**: التصور البياني والرسوم
- **requests/BeautifulSoup**: استخراج البيانات من الويب
- **Pillow**: معالجة الصور

## Структура проекта / Project Structure / هيكل المشروع

### Русский


## Тестирование / Testing / الاختبار

### Русский
- 41 unit-теста покрывают весь функционал
- Запуск тестов: `python -m unittest discover tests/ -v`
- Покрытие: позитивные, негативные и исключительные сценарии

### English
- 41 unit tests cover all functionality
- Run tests: `python -m unittest discover tests/ -v`
- Coverage: positive, negative, and exceptional scenarios

### العربية
- 41 اختبار تغطي جميع الوظائف
- تشغيل الاختبارات: `python -m unittest discover tests/ -v`
- التغطية: سيناريوهات إيجابية، سلبية، واستثنائية

## Поддержка / Support / الدعم

### Русский
При возникновении проблем:
1. Убедитесь, что установлен Python 3.12.0+
2. Проверьте подключение к интернету для веб-скрапинга
3. Запустите тесты для диагностики

### English
If you encounter issues:
1. Ensure Python 3.12.0+ is installed
2. Check internet connection for web scraping
3. Run tests for diagnostics

### العربية
إذا واجهت مشاكل:
1. تأكد من تثبيت Python 3.12.0+
2. تحقق من الاتصال بالإنترنت لاستخراج البيانات
3. شغّل الاختبارات للتشخيص

## Лицензия / License / الترخيص

### Русский
Учебный проект для лабораторной работы

### English
Educational project for laboratory work

### العربية
مشروع تعليمي للعمل المخبري