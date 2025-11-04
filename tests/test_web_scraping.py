import unittest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_scraping import scrape_wuzzuf_jobs, save_jobs_to_csv


class TestWebScraping(unittest.TestCase):
    """Test cases for web scraping module"""
    
    def setUp(self):
        """إعداد بيانات اختبار"""
        self.test_data = [
            ["Job Title 1", "Job Title 2"],  # عناوين
            ["Company 1", "Company 2"],       # شركات
            ["Date 1", "Date 2"],             # تواريخ
            ["Location 1", "Location 2"],     # مواقع
            ["Skills 1", "Skills 2"],         # مهارات
            ["Link 1", "Link 2"]              # روابط
        ]
    
    @patch('web_scraping.requests.get')
    # اختبار استخراج البيانات بنجاح (محاكاة
    def test_scrape_jobs_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b'''
        <html>
            <body>
                <div>
                    <h2 class="css-193uk2c"><a href="/job1">Job 1</a></h2>
                    <a class="css-ipsyv7">Company 1</a>
                    <span class="css-16x61xq">Location 1</span>
                    <div class="css-1rhj4yg">Skills 1</div>
                    <div class="css-eg55jf">Date 1</div>
                </div>
                <div>
                    <h2 class="css-193uk2c"><a href="/job2">Job 2</a></h2>
                    <a class="css-ipsyv7">Company 2</a>
                    <span class="css-16x61xq">Location 2</span>
                    <div class="css-1rhj4yg">Skills 2</div>
                    <div class="css-1jldrig">Date 2</div>
                </div>
            </body>
        </html>
        '''
        mock_get.return_value = mock_response
        
        success, data = scrape_wuzzuf_jobs("python", 1)
        
        self.assertTrue(success)
        self.assertIsInstance(data, list)
        # البيانات يجب أن تحتوي على 6 قوائم
        if data:
            self.assertEqual(len(data), 6)
    
    # اختبار حفظ البيانات في CSV بنجاح
    def test_save_jobs_to_csv_success(self):
        test_file = "test_jobs.csv"
        
        success = save_jobs_to_csv(self.test_data, test_file)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(test_file))
        
        # تنظيف
        if os.path.exists(test_file):
            os.remove(test_file)

    # اختبار حفظ بيانات فارغة 
    def test_save_jobs_to_csv_empty_data(self):
        success = save_jobs_to_csv([], "test.csv")
        self.assertFalse(success)  # يجب أن تعيد False
    
    # اختبار حفظ بيانات None
    def test_save_jobs_to_csv_none_data(self):
        success = save_jobs_to_csv(None, "test.csv")
        self.assertFalse(success)  # يجب أن تعيد False
    
    # اختبار خطأ في الشبكة
    def test_scrape_jobs_network_error(self):
        with patch('web_scraping.requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            success, data = scrape_wuzzuf_jobs("python", 1)
            
            self.assertFalse(success)
            self.assertEqual(data, [])


if __name__ == '__main__':
    unittest.main()