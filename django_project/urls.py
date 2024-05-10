
from django.contrib import admin
from django.urls import path
from documents import views as documents_views
from search import views as search_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test1/', documents_views.mi_vista1, name='test1'),
    path('test2/', documents_views.mi_vista2, name='test2'),
    path('test4/', documents_views.mi_vista4, name='test4'),
    path('test5/', documents_views.mi_vista5, name='test5'),
    path('searchusers/', search_views.search_users, name='searchusers'),
    path('gethistory/', search_views.get_history, name='gethistory'),
    path('registerclient/', search_views.register_client, name='registerclient'),
]
