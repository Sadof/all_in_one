from django.urls import path
from .views import *



app_name = "tests"


urlpatterns =[
    path('createtest/', TestCreateView.as_view(), name='create_test_url'),
    path('edit/<int:test_id>/', TestPagesEditView.as_view(), name='edit_test'),
    path('edit/<int:test_id>/add_page', PageCreateView.as_view(), name='add_page'),
    path('edit/<int:test_id>/<int:page_order>/', TestPagesEditView.as_view(), name='edit_page'),
    path('edit/page_delete/<int:page_id>/', page_delete, name='page_delete'),
    path('edit/pageorder/', PageOrder, name='page_order'),
    path('edit/questionorder/', QuestionOrder, name='question_order'),
    # path('edit/question_save/', question_save, name='question_save'),
    path('pagedelete/', PageDelete, name='delete_page'),
    path('delete/<int:test_id>/', TestDeleteView.as_view(), name='test_delete_view'),
    path('edit/<int:test_id>/preview/', TestPreview.as_view(), name='test_preview'),
    path('edit/<int:test_id>/check_test/',check_test, name='check_test'),
    path('test_like', test_like, name='test_like'),
    path('', TestList.as_view(), name='test_list'),
    path('search/<str:username>/', TestList.as_view(), name='test_list_search'),
    path('<slug:test_slug>/', TestCompletion.as_view(), name='test'),
    path('compelete_test', test_complete, name='test_complete'),
    # path('chech_answers', check_answers, name='check_answers'),
]