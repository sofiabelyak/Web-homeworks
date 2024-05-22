from django.urls import path

from app import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
    path('', views.index, name ='index'),
    path('hot/', views.hot, name ='hot'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('signup/',views.signup, name='signup'),
    path('settings/',views.settings, name='settings'),
    path('tag/<str:tag_name>',views.tag, name='tag'),
    path('question/<int:question_id>', views.question, name='question')
]
