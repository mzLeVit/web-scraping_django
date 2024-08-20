from django.urls import path
from quotes_project.mysite.mysite import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-author/', views.add_author, name='add_author'),
    path('add-quote/', views.add_quote, name='add_quote'),
    path('tags/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('top-tags/', views.top_tags, name='top_tags'),
]
