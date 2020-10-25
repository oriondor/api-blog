
from .views import AllArticlesView, AuthView, SubsribedArticlesView, ReadView, FollowView
from django.urls import path

urlpatterns = [
    path('auth/', AuthView.as_view()),
    path('all/', AllArticlesView.as_view(), name='show-view'),
    path('all/<article>', AllArticlesView.as_view(), name='show-view'),
    path('subscribed/', SubsribedArticlesView.as_view(), name='show-subsc-view'),
    path('follow/', FollowView.as_view(), name='follow-view'),
    path('read/', ReadView.as_view(), name='read-view'),
]
