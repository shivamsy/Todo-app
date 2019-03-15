from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from . import views

app_name = 'schedule'

urlpatterns = [
	path('', views.signup, name='signup'),
	path('login', views.login, name='login'),
	path('logout', auth_views.LogoutView.as_view(), {'next_page': '/login'}, name='logout'),
	path('dashboard', views.dashboard , name='dashboard'),
	path('addSchedule', views.addSchedule, name='addSchedule'),
	path('updateSchedule/<int:id>', views.updateSchedule, name="updateSchedule"),
	path('deleteSchedule/<int:id>', views.deleteSchedule, name="deleteSchedule"),
	path('mark/<int:id>/<int:val>', views.mark, name="mark"),

]
