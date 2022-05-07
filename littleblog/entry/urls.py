from django.urls import path
from .views import UserProfileListCreateView, EntryViewSet, RateUpdateView
from rest_framework.routers import DefaultRouter

app_name = 'entry'

router = DefaultRouter()
router.register('entries', EntryViewSet)

urlpatterns = [
    path('profiles/', UserProfileListCreateView.as_view()),
    path('rate_entry/', RateUpdateView.as_view())
]

urlpatterns += router.urls

