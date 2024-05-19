from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Quiz, ProductPictures, ProductTypes, TestResult

class QuizAdmin(admin.ModelAdmin):
    # list_display = ('link_to_quiz',)
    list_display = ('title', 'template_name', 'link_to_quiz')  # `template_name` を表示
    fields = ('title', 'product_type', 'detail', 'template_name')  # 編集可能フィールドに追加

    def link_to_quiz(self, obj):
        url = reverse('psychology_tests:quiz_detail', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.title)
    link_to_quiz.short_description = "Quiz Title"

class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'date_taken')  # 一覧に表示するフィールド
    list_filter = ('user', 'quiz')  # フィルターを追加
    search_fields = ('user__username', 'quiz__title') 

admin.site.register(Quiz, QuizAdmin)
admin.site.register(ProductTypes)
admin.site.register(ProductPictures)
admin.site.register(TestResult)
