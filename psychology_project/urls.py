from django.contrib import admin
from django.urls import path, include
from . import settings
from accounts.views import HomeView
from django.contrib.staticfiles.urls import static


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('psychology_tests/quizzes/', include(('psychology_tests.urls', 'psychology_tests'), namespace='psychology_tests')),
    path('psychology_tests/', include('psychology_tests.urls')),
    # path('quizzes/', include('quizzes.urls')),
    # path('psychology_tests/', include('psychology_tests.urls', namespace='psychology_tests'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
