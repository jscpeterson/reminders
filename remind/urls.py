from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CaseCreateView.as_view()),
    path('update/', views.UpdateHomeView.as_view()),
    # path('<str:case_number>/scheduling/', views.SchedulingView.as_view(), name='scheduling'),
    path('<str:case_number>/scheduling/', views.scheduling_view, name='scheduling'),
    path('<str:case_number>/track/', views.TrackView.as_view(), name='track'),
    path('<str:case_number>/trial/', views.TrialView.as_view(), name='trial'),
    path('<str:case_number>/order/', views.OrderView.as_view(), name='order'),
    path('<str:case_number>/request_pti/', views.RequestPTIView.as_view(), name='request_pti'),
    path('<str:case_number>/update/', views.UpdateView.as_view(), name='update'),
    path('<int:deadline_pk>/complete/', views.CompleteView.as_view(), name='complete')
]
