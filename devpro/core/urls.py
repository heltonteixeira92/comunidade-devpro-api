from django.urls import path

from devpro.core.views import authors, book_list_create, book_read_update_delete

app_name = 'core'

urlpatterns = [
    path('authors/', authors, name='list-authors'),
    path('books/', book_list_create, name='create-list-book'),
    path('books/<int:pk>/', book_read_update_delete, name='read-update-book'),
]
