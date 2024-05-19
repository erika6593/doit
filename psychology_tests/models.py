from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

User = get_user_model()
"""カテゴリー"""
class ProductTypes(models.Model):
    name = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'product_types'
    
    def __str__(self):
        return self.name
    
    

"""問題"""
class Quiz(models.Model):
    title = models.CharField(max_length=1000)
    product_type = models.ForeignKey(
        ProductTypes, on_delete=models.CASCADE
    )
    detail = models.TextField()
    template_name = models.CharField(max_length=100, default='default_quiz_template.html')  # デフォルトテンプレート名

    
    class Meta:
        db_table = 'quiz'
        
    def __str__(self):
        return self.title

    
"""写真"""
class ProductPictures(models.Model):
    picture = models.FileField(upload_to='product_pictures/')
    product = models.ForeignKey(
        Quiz, on_delete=models.CASCADE
    )
    order = models.CharField(max_length=50, blank=True, null=True) 

    class Meta:
        db_table = 'product_pictures'
        ordering = ['order'] 
        
    def __str__(self):
        return f'{self.product.title}: {self.order}'
        

"""結果"""
class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)
    result_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'test_results'

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"