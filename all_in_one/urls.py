from django.urls import path, include
from . import views
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', include('tests.urls')),
    path('blog/',include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/v1/', include('api.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)