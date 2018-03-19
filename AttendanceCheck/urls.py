from django.conf.urls import url
from AttendanceCheck import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test/', views.test, name='test'),
    url(r'^(?P<user_id>[\w-]+)/dash_board/', views.dash_board, name='dash_board'),
    url(r'^quick_dashboard/([\w-]+)', views.quick_dashboard, name='quick_dashboard'),
    url(r'^begin_checking/([\w-]+)', views.begin_checking, name='begin_checking'),
    url(r'^(?P<enrollment_id>[\w-]+)/history/', views.history, name='history'),
    url(r'^(?P<enrollment_id>[\w-]+)/update/', views.enrollment_update, name='update'),
    url(r'^(?P<enrollment_id>[\w-]+)/setting/', views.enrollment_setting, name='setting'),
]
