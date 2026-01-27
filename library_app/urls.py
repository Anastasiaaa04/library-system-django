from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('issue-book/', views.issue_book, name='issue_book'),
    path('return-book/<int:issue_id>/', views.return_book, name='return_book'),
    path('reading-history/', views.reading_history, name='reading_history'),
    path('statistics/', views.statistics, name='statistics'),
    path('reminders/', views.reminders, name='reminders'),
    path('authors/', views.authors_list, name='authors_list'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('genres/', views.genres_list, name='genres_list'),
]