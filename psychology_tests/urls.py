from django.urls import path
from .views import (QuizDetailView, QuizListView, 
                send_share_email,my_page, delete_result,
                delete_all_results, view_usage_log)
                


app_name = 'psychology_tests'

urlpatterns = [
    path('quiz_list/', QuizListView.as_view(), name='quiz_list'),
    path('quiz/detail/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('send_email/', send_share_email, name='send_share_email'),
    path('my_page/', my_page, name='my_page'),
    path('delete_result/<int:result_id>/', delete_result, name='delete_result'),
    path('delete_all_results/', delete_all_results, name='delete_all_results'),
    path('view_usage_log/', view_usage_log, name='view_usage_log'),
]

