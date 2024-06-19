from django.urls import path
from django.views.decorators.cache import cache_page

from recipient.apps import RecepientConfig
from recipient.views import (RecipientListView, RecipientCreateView, RecipientDeleteView,
                             RecipientDetailView, RecipientUpdateView)

app_name = RecepientConfig.name

urlpatterns = [
    path('', RecipientListView.as_view(), name='list'),
    path('create/', RecipientCreateView.as_view(), name='create'),
    path('view/<int:pk>/', cache_page(60)(RecipientDetailView.as_view()), name='view'),
    path('update/<int:pk>/', RecipientUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', RecipientDeleteView.as_view(), name='delete'),
]
