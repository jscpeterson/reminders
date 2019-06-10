from django.urls import path
from . import views

app_name = 'remind'
urlpatterns = [
    path('', views.DashView.as_view(), name='dashboard'),
    path('create/', views.CaseCreateView.as_view()),
    path('motion/', views.CreateMotionView.as_view()),
    path('update/', views.UpdateHomeView.as_view()),
    path('case_created/<str:case_number>', views.case_created, name='case_created'),
    path('scheduling/<str:case_number>', views.scheduling, name='scheduling'),
    path('track/<str:case_number>', views.track, name='track'),
    path('trial/<str:case_number>', views.trial, name='trial'),
    path('order/<str:case_number>', views.order, name='order'),
    path('request_pti/<str:case_number>', views.request_pti, name='request_pti'),
    path('update/<str:case_number>', views.update, name='update'),
    path('complete/<int:deadline_pk>', views.complete, name='complete'),
    path('extension/<int:deadline_pk>', views.extension, name='extension'),
    path('judge_confirmed/<int:deadline_pk>', views.judge_confirmed, name='judge_confirmed'),
    path('motion_deadline/<int:motion_pk>', views.motion_deadline, name='motion_deadline'),
    path('motion_response/<int:motion_pk>', views.motion_response, name='motion_response')
]
