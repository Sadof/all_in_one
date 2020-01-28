from django.urls import path, include
from . import views


app_name = 'api'


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('tests/', views.TestListView.as_view(), name='test_list'),
    path('tests/<int:pk>/', views.TestDetailView.as_view(), name='test_view'),
    path('tests/<int:pk>/edit/', views.TestEditView.as_view(), name='test_edit'),
    # path('tests/<int:pk>/admin/', views.TestAdminView.as_view()),

]