
"""إنشاء ملف annotation بناءً على ملفات dataset.
Создание файла аннотации на основе файлов набора данных"""

import os
import pandas as pd
from typing import List, Dict, Any


def create_annotation_file(source_folder: str, save_path: str) -> None:
    """
    إنشاء ملف CSV يحتوي على قائمة الملفات في مجلد المصدر وتفاصيلها
    
    Args:
        source_folder (str): مسار مجلد المصدر الذي يحتوي على الملفات
        save_path (str): مسار حفظ ملف annotation الناتج
        
    Raises:
        RuntimeError: إذا حدث خطأ أثناء إنشاء الملف أو لم توجد ملفات
        FileNotFoundError: إذا لم يكن المجلد المصدري موجوداً
        
    Returns:
        None: يتم حفظ الملف في المسار المحدد
    """
    # التحقق من وجود المجلد المصدر أولاً
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"المجلد المصدر غير موجود: {source_folder}")
    
    # التحقق من أن المسار هو مجلد وليس ملف
    if not os.path.isdir(source_folder):
        raise ValueError(f"المسار المحدد ليس مجلد: {source_folder}")
    
    try:
        files: List[Dict[str, Any]] = []
        for root, _, filenames in os.walk(source_folder):
            for name in filenames:
                file_path = os.path.join(root, name)
                try:
                    file_size = os.path.getsize(file_path)
                    files.append({
                        "filename": name,
                        "path": file_path,
                        "size_bytes": file_size
                    })
                except (OSError, PermissionError) as e:
                    print(f"تحذير: لا يمكن الوصول إلى الملف {file_path}: {e}")
                    continue

        # التحقق من وجود ملفات فعلاً
        if not files:
            raise RuntimeError("لم يتم العثور على أي ملفات في المجلد المصدر")
            
        df = pd.DataFrame(files)
        df.to_csv(save_path, index=False, encoding="utf-8-sig")
        print(f"تم إنشاء ملف annotation بنجاح: {save_path}")
        
    except Exception as e:
        # إعادة رفع الاستثناءات المحددة التي نعرفها
        if isinstance(e, (FileNotFoundError, RuntimeError)):
            raise e
        else:
            raise RuntimeError(f"حدث خطأ أثناء إنشاء annotation: {e}")



# """ إنشاء ملف annotation بناءً على ملفات dataset.
#    Создание файла аннотации на основе файлов набора данных"""

# import os
# import pandas as pd


# def create_annotation_file(source_folder: str, save_path: str) -> None:

#     # إنشاء ملف CSV يحتوي على قائمة الملفات في مجلد المصدر وتفاصيلها
#     # Создание CSV-файла, содержащего список файлов в исходной папке и их детали.
#     # مسار مجلد المصدر
#     # Путь к исходной папке
#     # Путь для сохранения файла аннотации
#     # مسار حفظ ملف annotation

#     try:
#         files = []
#         for root, _, filenames in os.walk(source_folder):
#             for name in filenames:
#                 file_path = os.path.join(root, name)
#                 file_size = os.path.getsize(file_path)
#                 files.append({
#                     "filename": name,
#                     "path": file_path,
#                     "size_bytes": file_size
#                 })

#         df = pd.DataFrame(files)
#         df.to_csv(save_path, index=False, encoding="utf-8-sig")

#     except Exception as e:
#         # حدث خطأ أثناء إنشاء annotation:
#         raise RuntimeError(f"Произошла ошибка при создании аннотации: {e}")

