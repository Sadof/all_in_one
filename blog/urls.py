from django.urls import path
from .views import *


urlpatterns = [
    path('', PostListView, name="posts_list_url"),
    path('search/', SearchList, name="search_list_url"),
    path('search/<str:search>/', SearchList, name='search_list_url_user'),
    path('tags/', TagListView, name="tags_list_url"),
    path("tags/add/", TagAddView.as_view(), name="tag_add_url"),
    path('tags/<str:slug>/delete/',TagDeleteView.as_view(),name="tag_delete_url"),
    path('tags/<str:slug>/edit/',TagEditView.as_view(), name="tag_edit_url"),
    path('tags/<str:slug>', TagView.as_view(),name="tag_detail_url"),
    path('post/add/',PostAddView.as_view(),name="post_add_url"),
    path('post/commentdelete/', CommentDeleteView, name="comment_delete_url"),
    path('post/commentedit/', CommentEditView, name="comment_edit_url"),
    path('post/<str:slug>',PostView.as_view(),name="post_detail_url"),
    path('post/<str:slug>/delete/',PostDeleteView.as_view(),name="post_delete_url"),
    path('post/<str:slug>/edit/',PostEditView.as_view(), name="post_edit_url"),

]