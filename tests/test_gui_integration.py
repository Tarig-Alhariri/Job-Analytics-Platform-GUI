import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from PySide6.QtWidgets import QApplication

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_window import MainWindow


class TestGUIIntegration(unittest.TestCase):
    """اختبارات تكامل واجهة المستخدم مع المنطق الداخلي"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
    
    def setUp(self):
        self.window = MainWindow()
    
    def tearDown(self):
        self.window.close()
    
    @patch('main_window.create_annotation_file')
    @patch('main_window.QFileDialog.getSaveFileName')
    def test_complete_annotation_workflow(self, mock_dialog, mock_create):
        """اختبار سير عمل إنشاء annotation كامل"""
        self.window.source_folder = "/test/source"
        mock_dialog.return_value = ("/test/annotation.csv", "")
        
        self.window.create_annotation()
        
        mock_create.assert_called_once_with("/test/source", "/test/annotation.csv")
    
    @patch('main_window.reorganize_dataset')
    @patch('main_window.QFileDialog.getExistingDirectory')
    def test_complete_reorganize_workflow(self, mock_dialog, mock_reorganize):
        """اختبار سير عمل إعادة التنظيم كامل"""
        self.window.source_folder = "/test/source"
        mock_dialog.return_value = "/test/dest"
        
        self.window.reorganize_dataset()
        
        mock_reorganize.assert_called_once_with("/test/source", "/test/dest")
    
    @patch('main_window.save_jobs_to_csv')
    @patch('main_window.QFileDialog.getSaveFileName')
    def test_complete_scraping_save_workflow(self, mock_dialog, mock_save):
        """اختبار سير عمل حفظ البيانات المستخرجة"""
        test_data = [
            ["Job1", "Job2"],
            ["Company1", "Company2"], 
            ["Date1", "Date2"],
            ["Location1", "Location2"],
            ["Skills1", "Skills2"],
            ["Link1", "Link2"]
        ]
        self.window.scraped_data = test_data
        mock_dialog.return_value = ("/test/jobs.csv", "")
        mock_save.return_value = True
        
        self.window.save_data()
        
        mock_save.assert_called_once_with(test_data, "/test/jobs.csv")
    
    def test_analysis_tab_functionality(self):
        """اختبار وظائف تبويب التحليل الأساسية"""
        # الانتقال إلى تبويب التحليل
        tab_widget = self.window.centralWidget()
        tab_widget.setCurrentIndex(2)
        
        # التحقق من وجود العناصر
        self.assertIsNotNone(self.window.analysis_file)
        self.assertIsNotNone(self.window.analyze_btn)
        self.assertIsNotNone(self.window.analysis_result)
        
        # التحقق من أن الزر مفعل
        self.assertTrue(self.window.analyze_btn.isEnabled())


if __name__ == '__main__':
    unittest.main(verbosity=2)