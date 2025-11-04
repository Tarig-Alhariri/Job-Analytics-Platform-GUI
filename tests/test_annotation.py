"""Unit tests for annotation.py module using unittest"""

import os
import unittest
import pandas as pd
import tempfile
import shutil
import sys

# إضافة المسار الحالي لاستيراد annotation
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from annotation import create_annotation_file


class TestAnnotationFile(unittest.TestCase):
    """Test class for annotation file creation functionality"""
    
    def setUp(self):
        """Setup temporary directories and files for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, "source_dataset")
        os.makedirs(self.source_dir)
        
        # إنشاء ملفات اختبارية
        self.test_files = [
            ("file1.txt", "This is test file 1"),
            ("file2.csv", "col1,col2\n1,2\n3,4"),
            ("image.jpg", "fake image data"),
        ]
        
        for filename, content in self.test_files:
            file_path = os.path.join(self.source_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def tearDown(self):
        """Clean up temporary directories after tests"""
        shutil.rmtree(self.test_dir)
    
    def test_create_annotation_success(self):
        """Positive test: successful annotation file creation"""
        # Arrange
        output_path = os.path.join(self.test_dir, "annotation.csv")
        
        # Act
        create_annotation_file(self.source_dir, output_path)
        
        # Assert
        self.assertTrue(os.path.exists(output_path))
        
        df = pd.read_csv(output_path)
        self.assertEqual(len(df), len(self.test_files))
        self.assertSetEqual(set(df['filename']), {f[0] for f in self.test_files})
        self.assertIn('path', df.columns)
        self.assertIn('size_bytes', df.columns)
    
    def test_create_annotation_nonexistent_source(self):
        """Negative test: non-existent source folder"""
        # Arrange
        non_existent_dir = os.path.join(self.test_dir, "non_existent")
        output_path = os.path.join(self.test_dir, "annotation.csv")
        
        # Act & Assert
        with self.assertRaises(FileNotFoundError):
            create_annotation_file(non_existent_dir, output_path)
    
    def test_create_annotation_empty_folder(self):
        """Negative test: empty source folder"""
        # Arrange
        empty_dir = os.path.join(self.test_dir, "empty_dir")
        os.makedirs(empty_dir)
        output_path = os.path.join(self.test_dir, "annotation.csv")
        
        # Act & Assert
        with self.assertRaises(RuntimeError) as context:
            create_annotation_file(empty_dir, output_path)
        
        # التحقق من رسالة الخطأ أيضاً
        self.assertIn("لم يتم العثور على أي ملفات", str(context.exception))
    
    def test_create_annotation_file_instead_of_folder(self):
        """Negative test: source path is a file, not a folder"""
        # Arrange
        file_path = os.path.join(self.source_dir, "test_file.txt")
        with open(file_path, 'w') as f:
            f.write("test")
        output_path = os.path.join(self.test_dir, "annotation.csv")
        
        # Act & Assert
        with self.assertRaises(ValueError):
            create_annotation_file(file_path, output_path)
    
    def test_annotation_file_content(self):
        """Test the content and structure of generated annotation file"""
        # Arrange
        output_path = os.path.join(self.test_dir, "annotation.csv")
        
        # Act
        create_annotation_file(self.source_dir, output_path)
        
        # Assert
        df = pd.read_csv(output_path)
        
        # التحقق من بنية البيانات
        expected_columns = ['filename', 'path', 'size_bytes']
        for col in expected_columns:
            self.assertIn(col, df.columns)
        
        # التحقق من أن أحجام الملفات موجبة
        self.assertTrue(all(df['size_bytes'] > 0))
        
        # التحقق من أن المسارات موجودة فعلياً
        for _, row in df.iterrows():
            self.assertTrue(os.path.exists(row['path']))
    
    def test_annotation_file_encoding(self):
        """Test file encoding and special characters"""
        # Arrange
        output_path = os.path.join(self.test_dir, "annotation.csv")
        
        # إنشاء ملف باسم يحتوي على أحخاص خاصة
        special_file = "file_with_arabic_العربية.txt"
        special_path = os.path.join(self.source_dir, special_file)
        with open(special_path, 'w', encoding='utf-8') as f:
            f.write("test content")
        
        # Act
        create_annotation_file(self.source_dir, output_path)
        
        # Assert
        df = pd.read_csv(output_path, encoding='utf-8-sig')
        self.assertIn(special_file, df['filename'].values)
    
    def test_annotation_with_nested_folders(self):
        """Test with nested folder structure"""
        # Arrange
        nested_dir = os.path.join(self.source_dir, "subfolder", "deep_folder")
        os.makedirs(nested_dir)
        
        nested_file = os.path.join(nested_dir, "nested_file.txt")
        with open(nested_file, 'w') as f:
            f.write("nested content")
        
        output_path = os.path.join(self.test_dir, "annotation.csv")
        
        # Act
        create_annotation_file(self.source_dir, output_path)
        
        # Assert
        df = pd.read_csv(output_path)
        self.assertIn("nested_file.txt", df['filename'].values)


def test_permission_handling():
    """Test that function handles permission errors gracefully"""
    # هذا الاختبار قد يحتاج صلاحيات خاصة للتشغيل
    # يمكن تخطيه في البيئات العادية
    pass


if __name__ == '__main__':
    unittest.main()