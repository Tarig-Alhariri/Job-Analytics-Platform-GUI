# tests/test_data_analysis.py
import unittest
import os
import sys
import pandas as pd
import tempfile
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_analysis import DataAnalyzer, analyze_job_data_with_charts


class TestDataAnalysis(unittest.TestCase):
    
    def setUp(self):
        self.test_data = {
            'job_title': ['Senior Developer', 'Data Scientist', 'Software Engineer', 'Senior Analyst'],
            'company_name': ['Company A', 'Company B', 'Company C', 'Company D'],
            'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
            'location': ['Cairo', 'Alexandria', 'Giza', 'Cairo'],
            'skills': ['Python, Django', 'ML, Python', 'Java, Spring', 'SQL, Excel'],
            'links': ['link1', 'link2', 'link3', 'link4']
        }
        self.df = pd.DataFrame(self.test_data)
        
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        self.df.to_csv(self.temp_file.name, index=False, sep=';')
        self.temp_file.close()
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_analyzer_initialization(self):
        analyzer = DataAnalyzer()
        self.assertIsNone(analyzer.df)
        self.assertEqual(analyzer.analysis_results, {})

    def test_load_data_success(self):
        analyzer = DataAnalyzer()
        success = analyzer.load_data(self.temp_file.name)
        
        self.assertTrue(success)
        self.assertIsNotNone(analyzer.df)
        self.assertEqual(len(analyzer.df), 4)

    def test_load_data_file_not_found(self):
        analyzer = DataAnalyzer()
        success = analyzer.load_data("nonexistent.csv")
        
        self.assertFalse(success)

    def test_clean_data(self):
        analyzer = DataAnalyzer()
        analyzer.df = self.df.copy()
        analyzer.clean_data()
        
        self.assertIn('job_title', analyzer.df.columns)
        self.assertIsInstance(analyzer.df, pd.DataFrame)

    def test_analyze_with_visualizations(self):
        analyzer = DataAnalyzer()
        analyzer.df = self.df.copy()
        analyzer.clean_data()
        
        results = analyzer.analyze_with_visualizations()
        
        self.assertIn('total_jobs', results)
        self.assertIn('top_categories', results)
        self.assertEqual(results['total_jobs'], 4)

    def test_analyze_empty_data(self):
        analyzer = DataAnalyzer()
        analyzer.df = pd.DataFrame()
        
        results = analyzer.analyze_with_visualizations()
        
        self.assertIn('error', results)

    def test_get_analysis_report(self):
        analyzer = DataAnalyzer()
        analyzer.df = self.df.copy()
        analyzer.clean_data()
        analyzer.analyze_with_visualizations()
        
        report = analyzer.get_analysis_report()
        
        self.assertIsInstance(report, str)
        self.assertIn('Отчет анализа вакансий', report)
        self.assertIn('Общее количество', report)
        self.assertIn('Топ-3 категории', report)

    def test_get_analysis_report_no_analysis(self):
        analyzer = DataAnalyzer()
        report = analyzer.get_analysis_report()
        
        self.assertIn('Анализ недоступен', report)

    def test_analyze_job_data_with_charts_success(self):
        success, report, chart_path = analyze_job_data_with_charts(self.temp_file.name)
        
        self.assertTrue(success)
        self.assertIsInstance(report, str)
        self.assertIsInstance(chart_path, str)
        self.assertIn('Отчет анализа вакансий', report)

    def test_analyze_job_data_file_not_found(self):
        success, report, chart_path = analyze_job_data_with_charts("nonexistent.csv")
        
        self.assertFalse(success)
        # اختبار مرن لأي رسالة خطأ روسية
        self.assertTrue(
            any(keyword in report for keyword in ['Файл', 'не найден', 'Не удалось', 'ошибка']),
            f"رسالة الخطأ غير متوقعة: {report}"
        )

    def test_analyze_job_data_invalid_file(self):
        corrupt_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        corrupt_file.write("invalid,data\ncorrupt,file")
        corrupt_file.close()
        
        success, report, chart_path = analyze_job_data_with_charts(corrupt_file.name)
        
        self.assertFalse(success)
        os.unlink(corrupt_file.name)

    def test_analyze_job_data_empty_file(self):
        empty_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        empty_file.write("")
        empty_file.close()
        
        success, report, chart_path = analyze_job_data_with_charts(empty_file.name)
        
        self.assertFalse(success)
        os.unlink(empty_file.name)


if __name__ == '__main__':
    unittest.main()