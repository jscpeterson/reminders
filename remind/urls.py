from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CaseCreateView.as_view()),
    path('update/', views.UpdateHomeView.as_view()),
    path('scheduling/<str:case_number>', views.scheduling, name='scheduling'),
    path('track/<str:case_number>', views.track, name='track'),
    path('trial/<str:case_number>', views.trial, name='trial'),
    path('order/<str:case_number>', views.order, name='order'),
    path('request_pti/<str:case_number>', views.request_pti, name='request_pti'),
    path('update/<str:case_number>', views.update, name='update'),
    path('complete/<int:deadline_pk>', views.complete, name='complete'),
    path('extension/<int:deadline_pk>', views.extension, name='extension'),
    path('judge_confirmed/<int:deadline_pk>', views.judge_confirmed, name='judge_confirmed'),
]
