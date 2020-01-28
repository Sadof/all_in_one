from django.urls import path, include
from . import views
from tests.views import MyTestList, delete_test_ajax

app_name='accounts'



urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', views.AccountRegistrationView.as_view(), name='registration'),
    path('home/', views.UserPageView.as_view(), name='home_page'),
    path('edit/', views.UserEditView.as_view(), name='edit_profile'),
    path('home/my_test_list/', MyTestList.as_view(), name='my_test_list'),
    path('delete_test/', delete_test_ajax, name='delete_test_ajax'),
    path('<slug:username>/', views.UserPageView.as_view(), name='user_page'),
]

