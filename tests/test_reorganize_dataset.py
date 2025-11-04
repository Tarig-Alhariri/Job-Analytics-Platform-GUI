import os
import tempfile
import shutil
import unittest
from unittest.mock import patch, MagicMock
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reorganize_dataset import reorganize_dataset


class TestReorganizeDataset(unittest.TestCase):
    
    """إعداد مجلدات اختبار مؤقتة قبل كل اختبار"""
    def setUp(self):
        self.source_dir = tempfile.mkdtemp()
        self.dest_dir = tempfile.mkdtemp()
        self.create_test_structure()
    
    """تنظيف مجلدات الاختبار بعد كل اختبار"""
    def tearDown(self):
        shutil.rmtree(self.source_dir, ignore_errors=True)
        shutil.rmtree(self.dest_dir, ignore_errors=True)
    
    """إنشاء هيكل اختباري مع ملفات ومجلدات"""
    def create_test_structure(self):
        subdir1 = os.path.join(self.source_dir, "subdir1")
        subdir2 = os.path.join(self.source_dir, "subdir2", "nested")
        os.makedirs(subdir1)
        os.makedirs(subdir2)
        
        test_files = [
            os.path.join(self.source_dir, "file1.txt"),
            os.path.join(self.source_dir, "file2.jpg"),
            os.path.join(subdir1, "file3.png"),
            os.path.join(subdir2, "file4.doc"),
            os.path.join(self.source_dir, "data.csv")
        ]
        
        for file_path in test_files:
            with open(file_path, 'w') as f:
                f.write("test content")
    
    """اختبار الوظيفة الأساسية لإعادة التنظيم"""
    @patch('reorganize_dataset.QMessageBox')
    def test_reorganize_basic_functionality(self, mock_msg):
        reorganize_dataset(self.source_dir, self.dest_dir)
        
        self.assertTrue(os.path.exists(self.dest_dir))
        
        expected_files = [
            "file1.txt",
            "file2.jpg",
            os.path.join("subdir1", "file3.png"),
            os.path.join("subdir2", "nested", "file4.doc"),
            "data.csv"
        ]
        
        for file_path in expected_files:
            full_path = os.path.join(self.dest_dir, file_path)
            self.assertTrue(os.path.exists(full_path), f"File {file_path} not copied")
    
    """اختبار عندما لا يوجد ملف CSV في المصدر"""
    @patch('reorganize_dataset.QMessageBox')
    def test_reorganize_without_csv(self, mock_msg):
        csv_file = os.path.join(self.source_dir, "data.csv")
        if os.path.exists(csv_file):
            os.remove(csv_file)
        
        reorganize_dataset(self.source_dir, self.dest_dir)
        mock_msg.warning.assert_called_once()
    
    """اختبار مع مجلد مصدر فارغ"""
    @patch('reorganize_dataset.QMessageBox')
    def test_reorganize_empty_source(self, mock_msg):
        empty_dir = tempfile.mkdtemp()
        
        try:
            reorganize_dataset(empty_dir, self.dest_dir)
            self.assertTrue(os.path.exists(self.dest_dir))
        finally:
            shutil.rmtree(empty_dir, ignore_errors=True)
    
    """اختبار مع مجلد مصدر غير موجود"""
    @patch('reorganize_dataset.QMessageBox')
    def test_reorganize_nonexistent_source(self, mock_msg):
        non_existent_dir = "/non/existent/path"
        reorganize_dataset(non_existent_dir, self.dest_dir)
        mock_msg.critical.assert_called_once()
    
    """اختبار عندما يكون المجلد الوجهة موجوداً مسبقاً"""
    @patch('reorganize_dataset.QMessageBox')
    def test_reorganize_dest_already_exists(self, mock_msg):
        os.makedirs(self.dest_dir, exist_ok=True)
        reorganize_dataset(self.source_dir, self.dest_dir)
        
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "file1.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "data.csv")))

    """اختبار نسخ ملف CSV بشكل منفصل"""
    @patch('reorganize_dataset.QMessageBox')
    def test_csv_file_copied_separately(self, mock_msg):
        reorganize_dataset(self.source_dir, self.dest_dir)
        
        csv_in_dest = os.path.join(self.dest_dir, "data.csv")
        self.assertTrue(os.path.exists(csv_in_dest))
        
        with open(csv_in_dest, 'r') as f:
            content = f.read()
        self.assertEqual(content, "test content")

    """اختبار عندما يكون هناك multiple ملفات CSV"""
    @patch('reorganize_dataset.QMessageBox')
    def test_multiple_csv_files(self, mock_msg):
        extra_csv = os.path.join(self.source_dir, "extra_data.csv")
        with open(extra_csv, 'w') as f:
            f.write("extra csv content")
        
        reorganize_dataset(self.source_dir, self.dest_dir)
        
        csv1 = os.path.join(self.dest_dir, "data.csv")
        csv2 = os.path.join(self.dest_dir, "extra_data.csv")
        
        self.assertTrue(os.path.exists(csv1) or os.path.exists(csv2))


if __name__ == '__main__':
    unittest.main(verbosity=2)