from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST,  require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Quiz, TestResult, ProductPictures
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import logging
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import ExtractHour
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from .forms import EmailForm  
from django.conf import settings


logger = logging.getLogger('usage')




class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz

    def get_template_names(self):
        if self.object.template_name:
            return [self.object.template_name]
        else:
            return ['psychology_tests/default_quiz_template.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 関連する画像を取得
        context['pictures'] = ProductPictures.objects.filter(product=self.object).order_by('order')
        return context
        
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # オブジェクトを取得
        if request.user.is_authenticated:
            result_data = {"sample_key": "sample_value"}
            result = TestResult.objects.create(user=request.user, quiz=self.object)
            # print("TestResult created:", result)  # デバッグ情報を出力
            
            # ログ記録
            logger.debug(f'Quiz accessed: {self.object.title}, Category: {self.object.product_type.name}, Time: {timezone.now()}')
        else:
            # print("User is not authenticated")  # ユーザー認証がされていない場合のデバッグ
            logger.debug(f'Unauthorized access attempt to quiz: {self.object.title} at {timezone.now()}')
        return super().get(request, *args, **kwargs)        

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if request.user.is_authenticated:
    #         logger.debug(f'Quiz accessed: {self.object.title}, Category: {self.object.product_type.name}, Time: {timezone.now()}')
    #     else:
    #         logger.debug(f'Unauthorized access attempt to quiz: {self.object.title} at {timezone.now()}')
    #     return super().get(request, *args, **kwargs)



@staff_member_required
def view_usage_log(request):
    # カテゴリ別の集計
    category_usage = TestResult.objects.values('quiz__product_type__name').annotate(total=Count('id')).order_by('-total')
    
    # 時間帯別の集計
    hour_usage = TestResult.objects.annotate(hour=ExtractHour('created_at')).values('hour').annotate(total=Count('id')).order_by('hour')
    
    return render(request, "psychology_tests/view_usage_log.html", {
        'category_usage': category_usage,
        'hour_usage': hour_usage
    })

    
# @staff_member_required
# def view_usage_log(request):
#     log_content = "Log file not found."
#     try:
#         with open('usage.log', 'r') as file:
#             log_content = file.read()
#     except IOError:
#         pass
#     return render(request, "psychology_tests/view_usage_log.html", {'log_content': log_content})


class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'psychology_tests/quiz_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        product_type_name = self.request.GET.get('product_type_name', '')
        if product_type_name:
            queryset = queryset.filter(product_type__name__icontains=product_type_name)
        return queryset
    
    # def get(self, request, *args, **kwargs):
    #     quiz = self.get_object()
    #     TestResult.objects.create(user=request.user, quiz=quiz)
    #     return super().get(request, *args, **kwargs)
    
# @require_http_methods(["POST"])
# def send_share_email(request):
#     form = EmailForm(request.POST)
#     if form.is_valid():
#         recipient_email = form.cleaned_data['email']
#         message_body = form.cleaned_data['message']
#         quiz_id = request.POST.get('quiz_id')  # フォームからではなくリクエストから取得します
#         page_url = request.build_absolute_uri(reverse('psychology_tests:quiz_detail', args=[quiz_id]))
#         subject = '心理テストの結果が共有されました！'
#         message = f"{message_body}\n\n以下のリンクから心理テストのページを確認できます: {page_url}"
#         sender_email = 'your-email@gmail.com'

#         try:
#             send_mail(subject, message, sender_email, [recipient_email])
#             quiz_list_url = reverse('psychology_tests:quiz_list')
#             return HttpResponse(f"""
#                 メールが送信されました！<br><br>
#                 <a href="{request.build_absolute_uri(quiz_list_url)}">心理テスト一覧に戻る</a>
#             """)
#         except Exception as e:
#             return HttpResponse(f"メール送信中にエラーが発生しました: {str(e)}")
#     else:
#         # フォームが無効な場合、エラーメッセージを表示する
#         error_messages = "<br>".join([f"{field.label}: {error}" for field in form for error in field.errors])
#         quiz_list_url = reverse('psychology_tests:quiz_list')
#         return HttpResponse(f"""
#             入力されたアドレスに誤りがあります、正しく入力してください！<br>
#             {error_messages}<br><br>
#             <a href="{request.build_absolute_uri(quiz_list_url)}">心理テスト一覧に戻る</a>
#         """)

# こっちがよしこ　簡易的に遅れる感じ
@require_http_methods(["POST"])
def send_share_email(request):
    if request.method == 'POST':
        recipient_email = request.POST.get('email')
        page_url = request.POST.get('page_url')
        subject = '心理テストが共有されました！'
        sender_email = recipient_email# 送信者のメールアドレス

        # full_page_url = f'{settings.BASE_URL}{page_url}'
        page_url = reverse('psychology_tests:quiz_detail', kwargs={'pk': 4})
        full_page_url = request.build_absolute_uri(page_url)

        message = f"以下のリンクから心理テストを確認できます。アカウント登録がまだの方は新規ユーザー登録をお願いします！: {full_page_url}"
        # message = f"以下のリンクから心理テストを確認できます: {page_url}"
        # sender_email = 'your-email@gmail.com'  # 送信者のメールアドレス


        send_mail(subject, message, sender_email, [recipient_email])

        # リンクを含むメッセージを返す
        return HttpResponse(f"メールが送信されました！<br><br>"
                            f"<a href='{settings.LINK_URL_1}'>心理テスト一覧に戻る</a>")
        # return HttpResponse("""
        #     メールが送信されました！<br><br>
        #     <a href="http://127.0.0.1:8000/psychology_tests/quizzes/quiz_list/">心理テスト一覧に戻る</a>
        # """)
    else:
        return HttpResponse("アドレスを間違えています。")


@login_required
def my_page(request):
    test_results = TestResult.objects.filter(user=request.user)
    return render(request, 'user.html', {'test_results': test_results})

@login_required
@require_POST
def delete_result(request, result_id):
    result = get_object_or_404(TestResult, id=result_id, user=request.user)  # ユーザーが所有する履歴のみ削除可能
    result.delete()
    return HttpResponse(f"削除しました！<br><br>"
                        f"<a href='{settings.LINK_URL_2}'>マイページに戻る</a>")  # 削除後にリダイレクトするページ
    # return HttpResponse("""
    #     削除しました！<br><br>
    #     <a href="http://127.0.0.1:8000/accounts/user/">マイページに戻る</a>
    # """)  # 削除後にリダイレクトするページ

@login_required
@require_POST
def delete_all_results(request):
    # ユーザーが所有する全履歴を削除
    TestResult.objects.filter(user=request.user).delete()
    # 削除後のメッセージを表示し、特定のページにリダイレクト
    return HttpResponse(f"削除しました！<br><br>"
                        f"<a href='{settings.LINK_URL_2}'>マイページに戻る</a>")  # 削除後にリダイレクトするページ
    # return HttpResponse("""
    #     全ての履歴を削除しました！<br><br>
    #     <a href="http://127.0.0.1:8000/accounts/user/">マイページに戻る</a>
    # """)