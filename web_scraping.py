"""
Web Scraping Module - مختبر 1
وحدة استخراج بيانات الوظائف من موقع Wuzzuf
Модуль веб-скрапинга для извлечения данных о вакансиях с Wuzzuf
"""

import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
from typing import List, Tuple


def scrape_wuzzuf_jobs(search_query: str = "python", max_pages: int = 2) -> Tuple[bool, List]:
    """
    Scrape job data from Wuzzuf website - استخراج بيانات الوظائف من موقع Wuzzuf
    Скрапинг данных о вакансиях с сайта Wuzzuf
    
    Args:
        search_query (str): Job search term - مصطلح البحث عن الوظائف
        max_pages (int): Maximum pages to scrape - الحد الأقصى لعدد الصفحات
        
    Returns:
        Tuple[bool, List]: (Success status, Data lists) - (حالة النجاح، قوائم البيانات)
    """
    job_title = []
    company_name = []
    location_name = []
    skills = []
    links = []
    date = []
    page_num = 0

    # Starting data extraction
    print("Начало извлечения данных с Wuzzuf...")
    
    try:
        while page_num < max_pages:
            # Extracting page
            print(f"Извлечение страницы {page_num + 1}...")
            
            result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q={search_query}&start={page_num}")
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            
            # Check page limit - التحقق من حد الصفحات
            page_limit_elem = soup.find("strong")
            if page_limit_elem:
                page_limit = int(page_limit_elem.text)
                if page_num > page_limit // 30:
                    # تم الوصول إلى نهاية الصفحات" Reached end of pages
                    print("Достигнут конец страниц")
                    break
            
            # Extract job elements - استخراج عناصر الوظائف
            jop_titles = soup.find_all("h2", {"class": "css-193uk2c"})
            company_names = soup.find_all("a", {"class": "css-ipsyv7"})
            locations_names = soup.find_all("span", {"class": "css-16x61xq"})
            jop_skills = soup.find_all("div", {"class": "css-1rhj4yg"})
            posted_new = soup.find_all("div", {"class": "css-eg55jf"})
            posted_old = soup.find_all("div", {"class": "css-1jldrig"})
            posted = [*posted_new, *posted_old]
            
            # Store data - تخزين البيانات
            for i in range(len(jop_titles)):
                job_title.append(jop_titles[i].text)
                links.append(jop_titles[i].find("a").attrs['href'])
                company_name.append(company_names[i].text)
                location_name.append(locations_names[i].text)
                skills.append(jop_skills[i].text)
                date.append(posted[i].text)
            
            page_num += 1
        
        # تم استخراج وظيفة بنجاح Successfully extracted jobs
        print(f"Успешно извлечено {len(job_title)} вакансий")
        
        data_lists = [job_title, company_name, date, location_name, skills, links]
        return True, data_lists
        
    except Exception as e:
        #حدث خطأ أثناء الاستخراج  Error during extraction
        print(f"Произошла ошибка при извлечении: {e}")
        return False, []


# def save_jobs_to_csv(data_lists: List, file_path: str = "jobs.csv") -> bool:
#     """
#     Save scraped data to CSV file - حفظ البيانات المستخرجة في ملف CSV
#     Сохранение извлеченных данных в CSV файл
    
#     Args:
#         data_lists (List): Lists of job data - قوائم بيانات الوظائف
#         file_path (str): Output file path - مسار ملف الإخراج
        
#     Returns:
#         bool: Success status - حالة النجاح
#     """

#     try:
#         exported = zip_longest(*data_lists)
#         with open(file_path, "w", encoding="utf-8", newline="") as myfile:
#             wr = csv.writer(myfile)
#             wr.writerow(["job title", "company name", "date", "location", "skills", "links"])
#             wr.writerows(exported)
        
#         # Data saved to
#         print(f"Данные сохранены в: {file_path}")
#         return True
        
#     except Exception as e:
#         # Error saving data
#         print(f"Ошибка сохранения данных: {e}")
#         return False
def save_jobs_to_csv(data_lists: List, file_path: str = "jobs.csv") -> bool:
    """
    Save scraped data to CSV file
    """
    try:
        # التحقق من صحة البيانات قبل الحفظ
        if not data_lists or len(data_lists) == 0:
            print(" Нет данных для сохранения")
            return False
        
        # التحقق من أن جميع القوائم تحتوي على بيانات
        for data_list in data_lists:
            if not data_list or len(data_list) == 0:
                print("Неполные данные для сохранения")
                return False
        
        exported = zip_longest(*data_lists)
        with open(file_path, "w", encoding="utf-8", newline="") as myfile:
            wr = csv.writer(myfile)
            wr.writerow(["job title", "company name", "date", "location", "skills", "links"])
            wr.writerows(exported)
        
        print(f"Данные были сохранены в: {file_path}")
        return True
        
    except Exception as e:
        print(f"Ошибка сохранения данных: {e}")
        return False


# Main execution block - كتلة التنفيذ الرئيسية
if __name__ == "__main__":
    success, data = scrape_wuzzuf_jobs("python", 2)
    if success:
        save_jobs_to_csv(data, "jobs.csv")