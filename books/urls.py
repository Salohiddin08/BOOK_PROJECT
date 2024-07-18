from django.urls import path
from . import views
from .views import add_book,delete_book,edit_book


urlpatterns = [
    path('', views.books, name='books'),
    path('<int:id>/', views.book_detail, name='book_detail'),
    path('<int:id>/comments', views.book_comments, name='comment'),
    path('<int:book_id>/<int:comment_id>/delete', views.book_delete, name='book_delete'), 
    path('<int:book_id>/<int:comment_id>/edit', views.comment_edit, name='cooment_edit'), 
    path('add_book/', add_book, name='add_book'),
    path('delete_book/<int:book_id>/', delete_book, name='delete_book'),
    path('edit_book/<int:book_id>/', edit_book, name='edit_book'),
]