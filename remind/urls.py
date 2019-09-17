from django.urls import path
from . import views

app_name = 'remind'
urlpatterns = [
    # TODO Fix up the inconsistencies with these URLs (some use snake_case some use kebab-case)
    path('', views.DashView.as_view(), name='dashboard'),
    path('first_time_user/', views.first_time_user, name='first-time-user'),

    # Case Creation Flow
    path('create_case/', views.create_case, name='create-case'),
    path('create_case/<str:defendant_pk>', views.create_case, name='create-case-with-ssn'),
    path('case_created/<str:case_number>', views.case_created, name='case_created'),
    path('scheduling/<str:case_number>', views.scheduling, name='scheduling'),

    # Scheduling Order Flow
    path('track/', views.scheduling_order_select_case, name='enter-sched'),
    path('track/<str:case_number>', views.scheduling_order_track, name='track'),
    path('trial/<str:case_number>', views.scheduling_order_trial, name='trial'),
    path('order/<str:case_number>', views.scheduling_order_deadlines, name='order'),

    # Motion Flow
    path('motion/', views.create_motion_select_case, name='create-motion'),
    path('motion/<str:case_number>', views.CreateMotionViewWithCase.as_view(), name='create-motion-with-case'),
    path('motion_deadline/<int:motion_pk>', views.motion_deadline, name='motion_deadline'),
    path('motion_created/<int:motion_pk>', views.motion_created, name='motion_created'),
    path('motion_response/<int:motion_pk>', views.motion_response, name='motion_response'),

    # Update Flow
    path('update/', views.update_select_case, name='update-case'),
    path('update/<str:case_number>', views.update, name='update'),
    path('update_confirm/<str:case_number>', views.update_confirm, name='update_confirm'),

    # Supervisor Actions
    path('reassign/', views.reassign_cases, name='reassign-cases'),
    path('reassign/<str:user_pk>', views.reassign_cases_with_user, name='reassign-cases-with-user'),
    path('change_staff/', views.change_staff, name='change-staff'),
    path('change_staff/<str:user_pk>', views.change_staff_with_user, name='change-staff-with-user'),

    # Miscellaneous
    path('request_pti/<str:case_number>', views.request_pti, name='request_pti'),
    path('complete/<int:deadline_pk>', views.complete, name='complete'),
    path('extension/<int:deadline_pk>', views.extension, name='extension'),
    path('judge_confirmed/<int:deadline_pk>', views.judge_confirmed, name='judge_confirmed'),
    path('case_closed/<str:case_number>', views.case_closed, name='case_closed'),
    path('stay_case/<str:case_number>', views.stay_case, name='stay_case'),
    path('resume_case/<str:case_number>', views.resume_case, name='resume_case'),
]
