from django.urls import path
from . import views

app_name = 'remind'
urlpatterns = [
    path('', views.DashView.as_view(), name='dashboard'),

    # Case Creation Flow
    path('create/', views.CaseCreateView.as_view(), name='create-case'),
    path('case_created/<str:case_number>', views.case_created, name='case_created'),
    path('scheduling/<str:case_number>', views.scheduling, name='scheduling'),

    # Scheduling Order Flow
    path('track/', views.UpdateTrackView.as_view(), name='enter-sched'),
    path('track/<str:case_number>', views.track, name='track'),
    path('trial/<str:case_number>', views.trial, name='trial'),
    path('order/<str:case_number>', views.order, name='order'),

    # Motion Flow
    path('motion/', views.CreateMotionView.as_view(), name='create-motion'),
    path('motion/<str:case_number>', views.CreateMotionViewWithCase.as_view(), name='create-motion-with-case'),
    path('motion_deadline/<int:motion_pk>', views.motion_deadline, name='motion_deadline'),
    path('motion_response/<int:motion_pk>', views.motion_response, name='motion_response'),

    path('update/', views.UpdateCaseView.as_view(), name='update-case'),
    path('update/<str:case_number>', views.update, name='update'),

    path('request_pti/<str:case_number>', views.request_pti, name='request_pti'),
    path('complete/<int:deadline_pk>', views.complete, name='complete'),
    path('extension/<int:deadline_pk>', views.extension, name='extension'),
    path('judge_confirmed/<int:deadline_pk>', views.judge_confirmed, name='judge_confirmed'),
    path('case_closed/<str:case_number>', views.case_closed, name='case_closed'),
    path('stay_case/<str:case_number>', views.stay_case, name='stay_case'),
]
