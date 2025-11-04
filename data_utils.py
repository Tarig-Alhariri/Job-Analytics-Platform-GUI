""" Содержит все функции для чтения, очистки и преобразования данных с
 помощью pandas. يحتوي على جميع الدوال الخاصة بقراءة وتنظيف وتحويل
 البيانات باستخدام pandas.
"""

import csv
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd
from dateutil.relativedelta import relativedelta

""" Чтение CSV-файла с правильной кодировкой и разделителем قراءة ملف CSV
    باستخدام الترميز والفاصل الصحيح."""


def read_dataset(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(
        csv_path,
        encoding='macroman',
        sep=';',
        quoting=csv.QUOTE_NONE)
    return df

    """Очистка данных: تنظيف البيانات:"""


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    # Удаление ненужных столбцов, если они присутствуют حذف الأعمدة غير
    # المرغوبة إذا كانت موجودة
    for col in ["Unnamed: 6", ",,,,,,,"]:
        if col in df.columns:
            df = df.drop(columns=[col])
    # Удаление дубликатов и пустых значений إزالة التكرارات والقيم الفارغة
    df = df.drop_duplicates()
    df = df.dropna(how="all")
    return df

    """ Преобразование даты из текстового формата в фактическую дату в формате
    # день/месяц/год.تحويل التاريخ من نصي إلى تاريخ فعلي بصيغة يوم/شهر/سنة."""


def convert_date(text_date: str) -> str:
    if pd.isna(text_date) or text_date == '' or str(
            text_date).strip().lower() in ['nan', 'null', 'none', 'not date']:
        return "not date"
    today = datetime.now()
    text_date = str(text_date).strip().lower()

    try:
        parts = text_date.split()
        if len(parts) < 2:
            return "No date"

        number = int(parts[0])
        unit = parts[1]

        if 'day' in unit:
            new_date = today - timedelta(days=number)
        elif 'week' in unit:
            new_date = today - timedelta(weeks=number)
        elif 'month' in unit:
            new_date = today - relativedelta(months=number)
        elif 'year' in unit:
            new_date = today - relativedelta(years=number)
        else:
            return "No date"

        return new_date.strftime('%d/%m/%Y')

    except (ValueError, TypeError, IndexError):
        return "No date"

    """  Чтение файла, его очистка и применение преобразования даты. قراءة الملف
     وتنظيفه وتطبيق تحويل التاريخ."""


def process_dataset(csv_path: str) -> pd.DataFrame:
    df = read_dataset(csv_path)
    df = clean_dataset(df)
    if "date" in df.columns:
        df["date"] = df["date"].apply(convert_date)
    return df

    """Возврат строк, соответствующих определенной дате, после обработки
    # данных. إرجاع الصفوف المطابقة لتاريخ معين بعد تجهيز البيانات."""


def get_data_by_date(date_value: str, csv_path: str) -> Optional[pd.DataFrame]:
    df = process_dataset(csv_path)
    if "date" not in df.columns:
        # عمود 'date' غير موجود في الملف بعد المعالجة.
        raise ValueError("Столбец 'date' отсутствует в файле после обработки")
    print("columns:", df.columns)

    filtered = df[df["date"] == date_value]
    if filtered.empty:
        return None
    return filtered
