from django.urls import path
from .views import get_highlights, check_highlights_existence

urlpatterns = [
    path('get_highlights/<str:report_code>', get_highlights, name='get_highlights'),
    path('check_highlights_existence/<str:report_code>', check_highlights_existence, name='check_highlights_existence'),
]