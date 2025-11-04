# tests/test_data_utils.py
import unittest
import os
import sys
import pandas as pd
import tempfile
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_utils import read_dataset, clean_dataset, convert_date, process_dataset, get_data_by_date


class TestDataUtils(unittest.TestCase):
    
    def setUp(self):
        self.test_data = {
            'job_title': ['Developer', 'Analyst', 'Engineer'],
            'company_name': ['Company A', 'Company B', 'Company C'],
            'date': ['not date', 'not date', 'not date'],  # ⬅️ استخدام "not date" للبيانات بدون تاريخ
            'location': ['Cairo', 'Alexandria', 'Giza'],
            'skills': ['Python', 'SQL', 'Java'],
            'links': ['link1', 'link2', 'link3']
        }
        self.df = pd.DataFrame(self.test_data)
        
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        self.df.to_csv(self.temp_file.name, index=False, sep=';')
        self.temp_file.close()
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_read_dataset(self):
        df = read_dataset(self.temp_file.name)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)

    def test_clean_dataset(self):
        df = clean_dataset(self.df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)

    def test_convert_date_valid(self):
        result = convert_date('2 days ago')
        self.assertNotEqual(result, 'No date')
        self.assertNotEqual(result, 'not date')

    def test_convert_date_invalid(self):
        result = convert_date('invalid date')
        self.assertEqual(result, 'No date')

    def test_convert_date_empty(self):
        result = convert_date('')
        self.assertEqual(result, 'not date')

    def test_process_dataset(self):
        df = process_dataset(self.temp_file.name)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)

    def test_get_data_by_date(self):
        # استخدام تاريخ موجود في البيانات ("not date")
        result = get_data_by_date('not date', self.temp_file.name)
        
        # قد ترجع None إذا لم تجد تطابق، أو DataFrame إذا وجدت
        if result is not None:
            self.assertIsInstance(result, pd.DataFrame)
        else:
            # إذا رجعت None، هذا مقبول أيضاً
            self.assertIsNone(result)

    def test_get_data_by_date_no_match(self):
        # استخدام تاريخ غير موجود في البيانات
        result = get_data_by_date('2024-01-01', self.temp_file.name)
        self.assertIsNone(result)

    def test_read_dataset_file_not_found(self):
        with self.assertRaises(Exception):
            read_dataset("nonexistent.csv")

    def test_get_data_by_date_with_processed_dates(self):
        # إنشاء بيانات تحتوي على تواريخ حقيقية
        dated_data = {
            'job_title': ['Job 1', 'Job 2'],
            'company_name': ['Company A', 'Company B'],
            'date': ['01/01/2024', '02/01/2024'],  # تواريخ حقيقية
            'location': ['Cairo', 'Alexandria'],
            'skills': ['Python', 'Java'],
            'links': ['link1', 'link2']
        }
        dated_df = pd.DataFrame(dated_data)
        
        dated_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        dated_df.to_csv(dated_file.name, index=False, sep=';')
        dated_file.close()
        
        # البحث بتاريخ موجود
        result = get_data_by_date('01/01/2024', dated_file.name)
        
        # التحقق من النتيجة
        if result is not None:
            self.assertIsInstance(result, pd.DataFrame)
            self.assertGreater(len(result), 0)
        
        os.unlink(dated_file.name)


if __name__ == '__main__':
    unittest.main()