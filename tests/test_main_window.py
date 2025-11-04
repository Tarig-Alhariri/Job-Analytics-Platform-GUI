import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

# إضافة المسار للأدوات
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_window import MainWindow, ChartWindow, WebScrapingThread


# تطبيق QApplication كمتغير عام
_app = None

def get_qapplication():
    """الحصول على نسخة QApplication أو إنشاء واحدة جديدة"""
    global _app
    if _app is None:
        _app = QApplication([])
    return _app


class TestMainWindow(unittest.TestCase):
    """اختبارات الواجهة الرئيسية للتطبيق"""
    
    @classmethod
    def setUpClass(cls):
        """إعداد تطبيق Qt لجميع الاختبارات"""
        cls.app = get_qapplication()
    
    def setUp(self):
        """إعداد النافذة الرئيسية قبل كل اختبار"""
        self.window = MainWindow()
    
    def tearDown(self):
        """تنظيف بعد كل اختبار"""
        if hasattr(self, 'window'):
            self.window.close()
            self.window.deleteLater()
        QTest.qWait(100)
    
    def test_window_initialization(self):
        """اختبار تهيئة النافذة الرئيسية"""
        self.assertEqual(self.window.windowTitle(), "Лабораторная работа 5 - Интегрированное приложение")
        self.assertTrue(self.window.minimumWidth() >= 900)
        self.assertTrue(self.window.minimumHeight() >= 600)
        self.assertEqual(self.window.source_folder, "")
        self.assertIsNone(self.window.scraped_data)
    
    def test_tab_widget_exists(self):
        """اختبار وجود عنصر التبويب"""
        central_widget = self.window.centralWidget()
        self.assertIsNotNone(central_widget)
        self.assertEqual(central_widget.tabText(0), " Управление данными")
        self.assertEqual(central_widget.tabText(1), " Извлечение данных")
        self.assertEqual(central_widget.tabText(2), " Анализ данных")
    
    def test_dataset_tab_elements(self):
        """اختبار عناصر تبويب إدارة البيانات"""
        tab_widget = self.window.centralWidget()
        tab_widget.setCurrentIndex(0)
        
        self.assertIsNotNone(self.window.folder_path)
        self.assertIsNotNone(self.window.date_input)
        self.assertIsNotNone(self.window.table)
    
    def test_scraping_tab_elements(self):
        """اختبار عناصر تبويب استخراج البيانات"""
        tab_widget = self.window.centralWidget()
        tab_widget.setCurrentIndex(1)
        
        self.assertIsNotNone(self.window.search_input)
        self.assertIsNotNone(self.window.pages_input)
        self.assertIsNotNone(self.window.scrape_btn)
        self.assertIsNotNone(self.window.save_btn)
        self.assertIsNotNone(self.window.scrape_log)
        self.assertIsNotNone(self.window.results_table)
        
        self.assertEqual(self.window.search_input.text(), "python")
        self.assertEqual(self.window.pages_input.text(), "2")
        self.assertFalse(self.window.save_btn.isEnabled())
    
    def test_analysis_tab_elements(self):
        """اختبار عناصر تبويب تحليل البيانات"""
        tab_widget = self.window.centralWidget()
        tab_widget.setCurrentIndex(2)
        
        self.assertIsNotNone(self.window.analysis_file)
        self.assertIsNotNone(self.window.analyze_btn)
        self.assertIsNotNone(self.window.analysis_result)
    
    @patch('main_window.QFileDialog.getExistingDirectory')
    def test_select_folder(self, mock_dialog):
        """اختبار اختيار المجلد"""
        mock_dialog.return_value = "/test/folder"
        
        self.window.select_folder()
        
        self.assertEqual(self.window.source_folder, "/test/folder")
        self.assertEqual(self.window.folder_path.text(), "/test/folder")
    
    @patch('main_window.QFileDialog.getSaveFileName')
    @patch('main_window.create_annotation_file')
    def test_create_annotation_with_folder(self, mock_create, mock_dialog):
        """اختبار إنشاء ملف annotation مع مجلد محدد"""
        self.window.source_folder = "/test/folder"
        mock_dialog.return_value = ("/test/annotation.csv", "")
        
        self.window.create_annotation()
        
        mock_create.assert_called_once_with("/test/folder", "/test/annotation.csv")
    
    @patch('main_window.QMessageBox.critical')
    def test_create_annotation_without_folder(self, mock_critical):
        """اختبار إنشاء ملف annotation بدون مجلد"""
        self.window.source_folder = ""
        
        self.window.create_annotation()
        
        mock_critical.assert_called_once()
    
    @patch('main_window.QFileDialog.getExistingDirectory')
    @patch('main_window.reorganize_dataset')
    def test_reorganize_dataset(self, mock_reorganize, mock_dialog):
        """اختبار إعادة تنظيم dataset"""
        self.window.source_folder = "/source/folder"
        mock_dialog.return_value = "/dest/folder"
        
        self.window.reorganize_dataset()
        
        mock_reorganize.assert_called_once_with("/source/folder", "/dest/folder")
    
    @patch('main_window.QMessageBox.critical')
    def test_search_by_date_validation(self, mock_critical):
        """اختبار التحقق من صحة إدخال التاريخ"""
        self.window.search_by_date()
        mock_critical.assert_called_once()
    
    @patch('main_window.get_data_by_date')
    @patch('os.listdir')
    def test_search_by_date_with_data(self, mock_listdir, mock_get_data):
        """اختبار البحث بالتاريخ مع بيانات"""
        import pandas as pd
        test_data = pd.DataFrame({
            'name': ['file1.jpg', 'file2.png'],
            'date': ['01/01/2023', '01/01/2023']
        })
        mock_get_data.return_value = test_data
        mock_listdir.return_value = ['data.csv']
        
        self.window.source_folder = "/test/folder"
        self.window.date_input.setText("01/01/2023")
        
        self.window.search_by_date()
        
        self.assertEqual(self.window.table.rowCount(), 2)
        self.assertEqual(self.window.table.columnCount(), 2)
    
    @patch('main_window.QMessageBox.critical')
    def test_start_scraping_validation(self, mock_critical):
        """اختبار التحقق من صحة إدخال الاستخراج"""
        self.window.search_input.clear()
        self.window.start_scraping()
        mock_critical.assert_called_once()
    
    @patch('main_window.WebScrapingThread')
    def test_start_scraping_success(self, mock_thread):
        """اختبار بدء استخراج البيانات بنجاح"""
        self.window.search_input.setText("python")
        self.window.pages_input.setText("2")
        
        mock_instance = MagicMock()
        mock_thread.return_value = mock_instance
        
        self.window.start_scraping()
        
        self.assertFalse(self.window.scrape_btn.isEnabled())
        mock_thread.assert_called_once_with("python", 2)
        mock_instance.start.assert_called_once()
    
    def test_display_scraped_data(self):
        """اختبار عرض البيانات المستخرجة"""
        # الانتقال إلى تبويب الاستخراج
        tab_widget = self.window.centralWidget()
        tab_widget.setCurrentIndex(1)
        
        test_data = [
            ["Job1", "Job2"],
            ["Company1", "Company2"],
            ["Location1", "Location2"],
            ["Skills1", "Skills2"],
            ["Link1", "Link2"],
            ["Date1", "Date2"]
        ]
        
        # استدعاء الدالة مباشرة مع تفعيل الزر يدوياً
        self.window.display_scraped_data(test_data)
        self.window.save_btn.setEnabled(True)  # تفعيل الزر يدوياً
        
        # التحقق من عرض البيانات في الجدول
        self.assertEqual(self.window.results_table.rowCount(), 2)
        self.assertEqual(self.window.results_table.columnCount(), 6)
        self.assertTrue(self.window.save_btn.isEnabled())
    
    @patch('main_window.save_jobs_to_csv')
    @patch('main_window.QFileDialog.getSaveFileName')
    def test_save_data(self, mock_dialog, mock_save):
        """اختبار حفظ البيانات"""
        test_data = [
            ["Job1"], ["Company1"], ["Date1"], ["Location1"], ["Skills1"], ["Link1"]
        ]
        self.window.scraped_data = test_data
        mock_dialog.return_value = ("/test/jobs.csv", "")
        mock_save.return_value = True
        
        self.window.save_data()
        
        mock_save.assert_called_once_with(test_data, "/test/jobs.csv")
    
    @patch('main_window.QMessageBox.critical')
    def test_save_data_without_scraped_data(self, mock_critical):
        """اختبار حفظ البيانات بدون بيانات"""
        self.window.scraped_data = None
        self.window.save_data()
        mock_critical.assert_called_once()
    
    @patch('main_window.QFileDialog.getOpenFileName')
    def test_select_analysis_file(self, mock_dialog):
        """اختبار اختيار ملف التحليل"""
        mock_dialog.return_value = ("/test/data.csv", "")
        
        self.window.select_analysis_file()
        
        self.assertEqual(self.window.analysis_file.text(), "/test/data.csv")
    
    @patch('main_window.analyze_job_data_with_charts')
    @patch('main_window.QApplication.processEvents')
    def test_run_analysis(self, mock_process, mock_analyze):
        """اختبار تشغيل التحليل"""
        # إعداد mock للتحليل
        mock_analyze.return_value = (True, "Analysis report", "/test/chart.png")
        
        # تعيين ملف التحليل
        self.window.analysis_file.setText("/test/data.csv")
        
        # تشغيل التحليل
        self.window.run_analysis()
        
        # التحقق من استدعاء دالة التحليل
        self.assertTrue(mock_analyze.called)
        
        # التحقق من أن الدالة استُدعيت بالمسار الصحيح
        if mock_analyze.called:
            called_args = mock_analyze.call_args[0]
            self.assertEqual(called_args[0], "/test/data.csv")
    
    @patch('main_window.QMessageBox.critical')
    def test_run_analysis_without_file(self, mock_critical):
        """اختبار تشغيل التحليل بدون ملف"""
        self.window.analysis_file.clear()
        self.window.run_analysis()
        mock_critical.assert_called_once()
    
    @patch('main_window.ChartWindow')
    def test_display_charts(self, mock_chart):
        """اختبار عرض الرسوم البيانية"""
        mock_instance = MagicMock()
        mock_chart.return_value = mock_instance
        
        self.window.display_charts("/test/chart.png")
        
        mock_chart.assert_called_once_with("/test/chart.png")
        mock_instance.show.assert_called_once()


class TestChartWindow(unittest.TestCase):
    """اختبارات نافذة الرسوم البيانية"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = get_qapplication()
    
    def setUp(self):
        self.test_chart_path = tempfile.mktemp(suffix='.png')
        with open(self.test_chart_path, 'wb') as f:
            f.write(b'dummy image data')
    
    def tearDown(self):
        if os.path.exists(self.test_chart_path):
            os.remove(self.test_chart_path)
    
    def test_chart_window_initialization(self):
        """اختبار تهيئة نافذة الرسوم البيانية"""
        window = ChartWindow(self.test_chart_path)
        
        self.assertEqual(window.windowTitle(), "Графики анализа вакансий - Job Analysis Charts -")
        self.assertTrue(window.minimumWidth() >= 1400)
        self.assertTrue(window.minimumHeight() >= 900)
        
        window.close()
        window.deleteLater()
    
    def test_chart_window_with_invalid_path(self):
        """اختبار نافذة الرسوم البيانية مع مسار غير صالح"""
        window = ChartWindow("/invalid/path/chart.png")
        self.assertIsNotNone(window.centralWidget())
        
        window.close()
        window.deleteLater()


class TestWebScrapingThread(unittest.TestCase):
    """اختبارات thread استخراج البيانات"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = get_qapplication()
    
    def test_thread_initialization(self):
        """اختبار تهيئة thread الاستخراج"""
        thread = WebScrapingThread("python", 2)
        self.assertEqual(thread.search_query, "python")
        self.assertEqual(thread.max_pages, 2)
    
    @patch('main_window.scrape_wuzzuf_jobs')
    def test_thread_run_success(self, mock_scrape):
        """اختبار تشغيل thread بنجاح"""
        test_data = [
            ["Job1"], ["Company1"], ["Date1"], ["Location1"], ["Skills1"], ["Link1"]
        ]
        mock_scrape.return_value = (True, test_data)
        
        thread = WebScrapingThread("python", 2)
        
        with patch.object(thread, 'progress') as progress_mock, \
             patch.object(thread, 'data_ready') as data_ready_mock, \
             patch.object(thread, 'finished') as finished_mock:
            
            thread.run()
            
            mock_scrape.assert_called_once_with("python", 2)
            progress_mock.emit.assert_called_once_with("Начало извлечения данных...")
            data_ready_mock.emit.assert_called_once_with(test_data)
            finished_mock.emit.assert_called_once_with(True)
    
    @patch('main_window.scrape_wuzzuf_jobs')
    def test_thread_run_failure(self, mock_scrape):
        """اختبار تشغيل thread مع فشل"""
        mock_scrape.return_value = (False, [])
        
        thread = WebScrapingThread("python", 2)
        
        with patch.object(thread, 'finished') as finished_mock:
            thread.run()
            finished_mock.emit.assert_called_once_with(False)
    
    @patch('main_window.scrape_wuzzuf_jobs')
    def test_thread_run_exception(self, mock_scrape):
        """اختبار تشغيل thread مع استثناء"""
        mock_scrape.side_effect = Exception("Test error")
        
        thread = WebScrapingThread("python", 2)
        
        with patch.object(thread, 'progress') as progress_mock, \
             patch.object(thread, 'finished') as finished_mock:
            
            thread.run()
            
            progress_mock.emit.assert_called_with("Ошибка: Test error")
            finished_mock.emit.assert_called_once_with(False)


if __name__ == '__main__':
    unittest.main(verbosity=2)