import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_window import MainWindow


class TestEndToEndWorkflows(unittest.TestCase):
    """اختبارات سيناريوهات استخدام شاملة من البداية للنهاية"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
    
    def setUp(self):
        self.window = MainWindow()
        # إنشاء مجلد اختبار مؤقت
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        self.window.close()
        # تنظيف مجلد الاختبار
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_dataset(self):
        """إنشاء مجموعة بيانات اختبارية"""
        # إنشاء ملفات اختبارية
        os.makedirs(os.path.join(self.test_dir, "subfolder"))
        
        test_files = [
            os.path.join(self.test_dir, "image1.jpg"),
            os.path.join(self.test_dir, "image2.png"),
            os.path.join(self.test_dir, "subfolder", "image3.jpeg"),
            os.path.join(self.test_dir, "data.csv")
        ]
        
        for file_path in test_files:
            with open(file_path, 'w') as f:
                f.write("test content")
        
        return self.test_dir
    
    @patch('main_window.QFileDialog.getSaveFileName')
    @patch('main_window.create_annotation_file')
    def test_e2e_annotation_workflow(self, mock_create, mock_dialog):
        """اختبار سيناريو إنشاء annotation من البداية للنهاية"""
        # إعداد البيئة
        source_dir = self.create_test_dataset()
        self.window.source_folder = source_dir
        mock_dialog.return_value = (os.path.join(self.test_dir, "annotation.csv"), "")
        
        # تنفيذ السيناريو
        self.window.create_annotation()
        
        # التحقق من النتائج
        mock_create.assert_called_once()
        args = mock_create.call_args[0]
        self.assertEqual(args[0], source_dir)
        self.assertTrue(args[1].endswith("annotation.csv"))
    
    @patch('main_window.QFileDialog.getExistingDirectory')
    @patch('main_window.reorganize_dataset')
    def test_e2e_reorganization_workflow(self, mock_reorganize, mock_dialog):
        """اختبار سيناريو إعادة التنظيم من البداية للنهاية"""
        # إعداد البيئة
        source_dir = self.create_test_dataset()
        dest_dir = os.path.join(self.test_dir, "reorganized")
        os.makedirs(dest_dir)
        
        self.window.source_folder = source_dir
        mock_dialog.return_value = dest_dir
        
        # تنفيذ السيناريو
        self.window.reorganize_dataset()
        
        # التحقق من النتائج
        mock_reorganize.assert_called_once_with(source_dir, dest_dir)
    
    @patch('main_window.WebScrapingThread')
    def test_e2e_scraping_workflow(self, mock_thread_class):
        """اختبار سيناريو استخراج البيانات من البداية للنهاية"""
        # إعداد mock thread
        mock_thread = MagicMock()
        mock_thread_class.return_value = mock_thread
        
        # إعداد واجهة المستخدم
        self.window.search_input.setText("data science")
        self.window.pages_input.setText("1")
        
        # تنفيذ الاستخراج
        self.window.start_scraping()
        
        # محاكاة انتهاء الاستخراج
        test_data = [
            ["Data Scientist", "Machine Learning Engineer"],
            ["Tech Co", "AI Startup"],
            ["Cairo", "Remote"],
            ["Python, SQL", "ML, Deep Learning"],
            ["http://job1.com", "http://job2.com"],
            ["2023-01-01", "2023-01-02"]
        ]
        self.window.on_scraping_done(test_data)
        
        # التحقق من النتائج
        self.assertEqual(self.window.results_table.rowCount(), 2)
        self.assertTrue(self.window.save_btn.isEnabled())
        self.assertEqual(self.window.scraped_data, test_data)


if __name__ == '__main__':
    unittest.main(verbosity=2)