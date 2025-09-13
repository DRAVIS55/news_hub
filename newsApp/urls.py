
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index,name='home'),
    path('index/', views.index, name='index'),
    path('api_responses/', views.api_responses, name='api_responses'),
    path('chat_ai/', views.chat_ai, name='chat_ai'),  # must match fetch("/chat_ai/")
    path('news/<int:pk>/', views.news_detail, name='news_detail'),  # Detail page
    path('contacts/', views.contact_list, name='contact-list'),
    path('scrape-news/manual/', views.scrape_news_manually,name='scrape-news-manually'),
    path('scrape-news/', views.scrape_news_,name='scrape-news'),
    path('admin-panel/', views.admin_panel,name='admin-panel'),
    path('contact/', views.submit_contact, name='submit_contact'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
