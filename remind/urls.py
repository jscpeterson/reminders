from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CaseCreate.as_view()),
    path('<str:case_num>/scheduling/', views.SchedulingView.as_view(), name='scheduling'),
    path('<str:case_num>/track/', views.TrackView.as_view(), name='track'),
    path('<str:case_num>/trial/', views.TrialView.as_view(), name='trial'),
    path('<str:case_num>/order/', views.OrderView.as_view(), name='order')
]
