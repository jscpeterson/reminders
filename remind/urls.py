from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('create/', views.CaseCreateView.as_view()),
    path('update/', views.UpdateHomeView.as_view()),
    path('<str:case_number>/scheduling/', views.scheduling, name='scheduling'),
    path('<str:case_number>/track/', views.track, name='track'),
    path('<str:case_number>/trial/', views.trial, name='trial'),
    path('<str:case_number>/order/', views.order, name='order'),
    path('<str:case_number>/request_pti/', views.request_pti, name='request_pti'),
    path('<str:case_number>/update/', views.update, name='update'),
    path('<int:deadline_pk>/complete/', views.complete, name='complete'),
    path('<int:deadline_pk>/extension/', views.extension, name='extension'),
    path('<int:deadline_pk>/judge_confirmed/', views.judge_confirmed, name='judge_confirmed'),
]
