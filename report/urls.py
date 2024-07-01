from django.urls import path
from .views import get_highlights

urlpatterns = [
    path('get_highlights/<str:reportcode>', get_highlights, name='get_highlights'),
]