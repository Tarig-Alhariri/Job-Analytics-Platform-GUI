"""
Data Analysis Module - مختبر 4
وحدة تحليل البيانات - تحليل فئات الوظائف مع الرسوم البيانية
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, Any, List
import csv
import os


class DataAnalyzer:
    """
    Class for analyzing job data with visualizations - فئة لتحليل بيانات الوظائف مع الرسوم البيانية
    Provides statistical analysis and charts - توفر تحليل إحصائي ورسوم بيانية
    """
    
    def __init__(self):
        """Initialize the analyzer - تهيئة المحلل"""
        self.df = None
        self.analysis_results = {}
    
    def load_data(self, file_path: str) -> bool:
        """
        Load and prepare data from CSV file - تحضير البيانات من ملف CSV
        """
        try:
            # Try different encodings - تجربة ترميزات مختلفة
            try:
                self.df = pd.read_csv(file_path, encoding='utf-8', sep=';', quoting=csv.QUOTE_NONE)
            except UnicodeDecodeError:
                try:
                    self.df = pd.read_csv(file_path, encoding='cp1251', sep=';', quoting=csv.QUOTE_NONE)
                except:
                    self.df = pd.read_csv(file_path, encoding='latin-1', sep=';', quoting=csv.QUOTE_NONE)
            
            print(f"Data loaded  : {len(self.df)}")  # Data loaded
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")  # Error loading data
            return False
    
    def clean_data(self) -> None:
        """
        Clean and prepare the dataset - تنظيف وتحضير مجموعة البيانات
        """
        # Remove unwanted columns - إزالة الأعمدة غير المرغوبة
        columns_to_drop = ["Unnamed: 6", ",,,,,,,"]
        for col in columns_to_drop:
            if col in self.df.columns:
                self.df = self.df.drop(columns=[col])
        
        # Rename columns - إعادة تسمية الأعمدة
        column_mapping = {}
        for actual_col in self.df.columns:
            actual_lower = str(actual_col).lower().strip()
            
            if any(word in actual_lower for word in ['job', 'title']):
                column_mapping[actual_col] = 'job_title'
            elif any(word in actual_lower for word in ['company']):
                column_mapping[actual_col] = 'company_name'
            elif any(word in actual_lower for word in ['date']):
                column_mapping[actual_col] = 'date'
            elif any(word in actual_lower for word in ['location']):
                column_mapping[actual_col] = 'location'
            elif any(word in actual_lower for word in ['skills']):
                column_mapping[actual_col] = 'skills'
            elif any(word in actual_lower for word in ['links']):
                column_mapping[actual_col] = 'links'
        
        if column_mapping:
            self.df = self.df.rename(columns=column_mapping)
        
        # Handle missing values - معالجة القيم المفقودة
        if 'job_title' in self.df.columns:
            self.df['job_title'] = self.df['job_title'].replace(r'^\s*$', np.nan, regex=True)
            self.df = self.df.fillna({'job_title': 'unknown'})
    
    def analyze_with_visualizations(self) -> Dict[str, Any]:
        """
        Analyze data and create visualizations - تحليل البيانات وإنشاء رسوم بيانية
        """
        try:
            if self.df is None or 'job_title' not in self.df.columns:
                return {"error": "No job title data available"}
            
            # إنشاء فئات الوظائف
            self.df['job_category'] = self.df['job_title'].apply(
                lambda x: str(x).split()[0].lower() if pd.notnull(x) and len(str(x).split()) > 0 else 'unknown'
            )
            
            # إضافة طول العنوان
            self.df['title_length'] = self.df['job_title'].apply(lambda x: len(str(x)))
            
            # أفضل 3 فئات
            top_categories = self.df['job_category'].value_counts().head(3)
            
            # حساب الإحصائيات
            total_jobs = len(self.df)
            category_stats = {}
            
            for category, count in top_categories.items():
                percentage = (count / total_jobs) * 100
                category_stats[category] = {
                    'count': count,
                    'percentage': round(percentage, 2)
                }
            
            # إنشاء الرسوم البيانية
            self.create_visualizations(top_categories)
            
            # تخزين النتائج
            self.analysis_results = {
                'total_jobs': total_jobs,
                'top_categories': category_stats,
                'categories_list': top_categories.index.tolist(),
                'counts_list': top_categories.values.tolist(),
                'title_lengths': self.df['title_length'].tolist()
            }
            
            return self.analysis_results
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def create_visualizations(self, top_categories: pd.Series) -> None:
        """
        Create three visualization charts - إنشاء ثلاثة رسوم بيانية
        """
        # Set style for better visuals - ضبط النمط لرسوم أفضل
        plt.style.use('seaborn-v0_8')
        
        # Create figure with 3 subplots - إنشاء شكل بثلاثة رسوم فرعية
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(28, 14))  # حجم أكبر بكثير
        
        # زيادة المسافات الداخلية بين الرسوم 
        plt.subplots_adjust(wspace=0.6, hspace=0.4,  # مسافات أكبر
                          left=0.05, right=0.95,    # هوامش أوسع
                          bottom=0.1, top=0.9)      # هوامش أوسع
        
        # Chart 1: Top 3 Categories Bar Chart - الرسم البياني لأفضل 3 فئات
        colors = ['#3498db', '#e74c3c', '#2ecc71']
        bars = ax1.bar(top_categories.index, top_categories.values, color=colors, alpha=0.8)
        
        # إعدادات المخطط 1 - بخطوط أكبر
        ax1.set_title('Top 3 Job Categories\nТоп-3 категории вакансий', 
                     fontsize=20, fontweight='bold', pad=35)  #حجم خط أكبر
        ax1.set_xlabel('Категория', fontsize=16)
        ax1.set_ylabel('Количество', fontsize=16)
        ax1.tick_params(axis='both', labelsize=14)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars - إضافة تسميات القيم على الأعمدة
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom', 
                    fontweight='bold', fontsize=14)  # ⬅️ حجم خط التسميات
        
        # Chart 2: Boxplot of Title Lengths - مخطط الصندوق لطول العناوين
        ax2.boxplot(self.df['title_length'], patch_artist=True, 
                   boxprops=dict(facecolor='#9b59b6', alpha=0.7))
        ax2.set_title('Title Length Distribution\nРаспределение длины заголовков', 
                     fontsize=20, fontweight='bold', pad=35)
        ax2.set_ylabel('Title Length / Длина заголовка', fontsize=16)
        ax2.tick_params(axis='both', labelsize=14)
        ax2.grid(True, alpha=0.3)
        
        # Chart 3: Histogram of Title Lengths - هيستوجرام لطول العناوين
        ax3.hist(self.df['title_length'], bins=20, color='#f39c12', alpha=0.7, edgecolor='black')
        ax3.set_title('Title Length Distribution\nРаспределение длины заголовков', 
                     fontsize=20, fontweight='bold', pad=35)
        ax3.set_xlabel('Title Length / Длина заголовка', fontsize=16)
        ax3.set_ylabel('Frequency / Частота', fontsize=16)
        ax3.tick_params(axis='both', labelsize=14)
        ax3.grid(True, alpha=0.3)
        
        #حفظ الصورة بالإعدادات المحسنة 
        plt.tight_layout(pad=4.0)  # مسافة إضافية حول التخطيط
        
        # Save the figure with high quality
        os.makedirs('analysis_results', exist_ok=True)
        plt.savefig('analysis_results/job_analysis_charts.png', 
                   dpi=400,                    #دقة عالية
                   bbox_inches='tight', 
                   facecolor='white',          #خلفية بيضاء
                   edgecolor='none', 
                   pad_inches=0.5,             # مسافة داخلية
                   transparent=False)          # غير شفاف
        
        plt.close()
        
        print("analysis_results/job_analysis_charts.png")

    
    def get_analysis_report(self) -> str:
        """
        Generate analysis report in both Arabic and Russian
        إنشاء تقرير التحليل باللغتين العربية والروسية
        """
        try:
            if not self.analysis_results:
                return "Анализ недоступен"
            
            results = self.analysis_results
            
            # تقرير تحليل الوظائف 
            report = "Отчет анализа вакансий\n"
            
            # إجمالي الوظائف
            report += f"Общее количество вакансий: {results.get('total_jobs', 0)}\n"
            
            # أفضل 3 فئات
            report += "Топ-3 категории вакансий:\n"
            
            top_categories = results.get('top_categories', {})
            if top_categories:
                for i, (category, stats) in enumerate(top_categories.items(), 1):
                    report += f"\n{i}. {category}:\n"
                    report += f"   Количество: {stats.get('count', 0)} вакансий\n"
                    report += f"   Count: {stats.get('count', 0)} jobs\n"
                    report += f"   Процент: {stats.get('percentage', 0)}%\n"
            else:
                report += " Нет доступных категорий - No categories available\n"
            
            # متوسط طول العناوين
            title_lengths = results.get('title_lengths', [])
            if title_lengths:
                avg_length = sum(title_lengths) / len(title_lengths)
                report += f"Средняя длина заголовков: {avg_length:.1f} символов\n"
            
            return report
            # خطأ في إنشاء التقرير -
        except Exception as e:
            return f" Ошибка создания отчета - Error generating report: {str(e)}" 
          
def analyze_job_data_with_charts(file_path: str) -> Tuple[bool, str, str]:
        """
        Main function to analyze job data with visualizations - الدالة الرئيسية لتحليل بيانات الوظائف مع الرسوم
        """
        # تهيئة جميع المتغيرات بقيم افتراضية
        success = False
        report = " Анализ еще не начался"
        chart_path = ""
        
        try:
            analyzer = DataAnalyzer()
            
            # تحميل البيانات
            if not analyzer.load_data(file_path):
                report = " Не удалось загрузить данные "
                return False, report, chart_path
            
            # تنظيف البيانات
            analyzer.clean_data()
            
            # التحليل وإنشاء الرسوم البيانية
            results = analyzer.analyze_with_visualizations()
            
            # التحقق من وجود أخطاء
            if "error" in results:
                report = f" Ошибка анализа: {results['error']}"
                return False, report, chart_path
            
            # الحصول على التقرير
            report = analyzer.get_analysis_report()
            chart_path = 'analysis_results/job_analysis_charts.png'
            
            # التحقق من وجود ملف الرسوم
            if not os.path.exists(chart_path):
                report += "\n Анализ был проведен, но графики созданы не были"
                chart_path = ""
            
            return True, report, chart_path
            
        except FileNotFoundError:
            # Data file not found
            report = " Файл данных не найден "
            return False, report, chart_path
            
        except pd.errors.EmptyDataError:
            # Data file is empty
            report = " Файл данных пуст "
            return False, report, chart_path
            
        except Exception as e:
            # Unexpected error
            report = f"- Неожиданная ошибка: {str(e)}"
            return False, report, chart_path
    

# Example usage - مثال للاستخدام
if __name__ == "__main__":
    success, report, chart_path = analyze_job_data_with_charts("jobs.csv")
    if success:
        print(report)
        print(f"\n Графики были сохранены в {chart_path}")
        
        # Display the chart - عرض الرسم
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        
        img = mpimg.imread(chart_path)
        plt.figure(figsize=(15, 8))
        plt.imshow(img)
        plt.axis('off')
        plt.title('Результаты анализа вакансий') # Job Analysis Results -
        plt.show()
    else:
        print(f"Ощебка: {report}")