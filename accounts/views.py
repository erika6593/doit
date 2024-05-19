from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from psychology_tests.models import TestResult

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('psychology_tests:quiz_list')
        return super().dispatch(request, *args, **kwargs)



class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm

# class UserLoginView(FormView):
#     template_name = 'user_login.html'
#     form_class = UserLoginForm

#     def post(self, request, *args, **kwargs):
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(email=email, password=password)
#         next_url = request.POST['next']
#         if user is not None and user.is_active:
#             login(request, user)
#         if next_url:
#             return redirect(next_url)
#         return redirect('accounts:home')

class UserLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(1200000)
        return super().form_valid(form)



# class UserLoginView(LoginView):
#     template_name = 'user_login.html'
#     authentication_form = UserLoginForm

#     def form_valid(self, form):
#         remember = form.cleaned_data['remember']
#         if remember:
#             self.request.session.set_expiry(1200000)
#         return super().form_valid(form)

# class UserLogoutView(View):
    
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return redirect('accounts:user_login')

class UserLogoutView(LogoutView):
    pass

class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            test_results = TestResult.objects.filter(user=user)
            # print("Test Results:", test_results)  # デバッグ情報を出力
            context['test_results'] = test_results
        else:
            print("User is not authenticated")  # ユーザー認証がされていない場合のデバッグ
        return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # ログインユーザーのテスト結果を取得
    #     context['test_results'] = TestResult.objects.filter(user=self.request.user)
    #     return context
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # ログインしているユーザーに関連するテスト結果を取得
    #     context['test_results'] = TestResult.objects.filter(user=self.request.user)
    #     return context

    

# @method_decorator(login_required, name='dispatch')
"""元のコード"""
# class UserView(LoginRequiredMixin, TemplateView):
#     template_name = 'user.html'

#     # @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)