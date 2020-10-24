
from .views import AllArticlesView, AuthView, SubsribedArticlesView
from django.urls import path

urlpatterns = [
    path('auth/', AuthView.as_view()),
    path('all/', AllArticlesView.as_view(), name='show-view'),
    path('subscribed/', SubsribedArticlesView.as_view(), name='show-subsc-view'),


]
