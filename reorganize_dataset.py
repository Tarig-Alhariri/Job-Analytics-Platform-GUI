""" Реорганизация данных в новой папке и копирование исходного CSV-файла.
    إعادة تنظيم البيانات في مجلد جديد ونسخ ملف CSV الأصلي."""

import os
import shutil
from PySide6.QtWidgets import QMessageBox


def reorganize_dataset(source_folder: str, dest_folder: str):

    # Реорганизует файлы из исходной папки в целевую папку. يعيد تنظيم الملفات من المجلد المصدر إلى المجلد الوجهة.
    # А также копирует исходный CSV-файл, чтобы не потерять данные даты. ويقوم بنسخ ملف CSV الأصلي أيضًا حتى لا تضيع بيانات التاريخ.
    # Путь к исходной папке  مسار المجلد المصدر
    # Путь к новой целевой папке مسار المجلد الوجهة الجديد

    try:
        # Создать целевую папку, если она не существует إنشاء مجلد الوجهة إذا
        # لم يكن موجودًا
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            # تم إنشاء المجلد الوجهة:
            print(f"Целевая папка создана: {dest_folder}")

        # Копировать все файлы из источника в назначение (кроме CSV временно)
        # نسخ جميع الملفات من المصدر إلى الوجهة (باستثناء CSV مؤقتًا)
        copied_count = 0
        for root, _, files in os.walk(source_folder):
            for file in files:
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(root, source_folder)
                dest_path = os.path.join(dest_folder, rel_path)

                # Создать подпапку, если она не существует إنشاء المجلد الفرعي
                # إذا لم يكن موجودًا
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)

                # Копировать файл نسخ الملف
                dest_file = os.path.join(dest_path, file)
                shutil.copy2(src_file, dest_file)
                copied_count += 1

        # تم نسخ {} ملفًا من {} إلى {}
        print(
            f"Скопировано {copied_count} файлов из {source_folder} в {dest_folder}")

        # Копировать исходный CSV-файл из исходной папки в целевую نسخ ملف CSV
        # الأصلي من المجلد المصدر إلى الوجهة
        csv_copied = False
        for file in os.listdir(source_folder):
            if file.lower().endswith(".csv"):
                src_csv = os.path.join(source_folder, file)
                dest_csv = os.path.join(dest_folder, file)
                shutil.copy2(src_csv, dest_csv)
                csv_copied = True
                # تم نسخ ملف CSV
                print(f"CSV-файл скопирован: {src_csv} → {dest_csv}")
                break

        if not csv_copied:
            # لم يتم العثور على ملف CSV في المجلد المصدر.
            print("CSV-файл не найден в исходной папке.")
            try:
                # تحذير", "لم يتم العثور على ملف CSV في المجلد المصدر.
                QMessageBox.warning(
                    None,
                    "Предупреждение",
                    "CSV-файл не найден в исходной папке.")
            except Exception:
                pass

        # تمت إعادة تنظيم البيانات بنجاح.
        print("Данные успешно реорганизованы.")
        try:
            # نجاح", "تم إنشاء الـ Dataset الجديد ونسخ ملف CSV بنجاح."
            QMessageBox.information(
                None, "Новый набор данных создан и CSV-файл успешно скопирован.")
        except Exception:
            pass

    except Exception as e:
        # خطأ أثناء إعادة تنظيم البيانات:
        print(f"Ошибка при реорганизации данных: {e}")
        try:
            QMessageBox.critical(None, "Ошибка", str(e))
        except Exception:
            pass
