from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views as app_views
from django.contrib.auth import views as auth_views



urlpatterns = [
  path('admin/', admin.site.urls),
  path('', app_views.index, name="home"),
  path('signup/', app_views.signup_view, name="register"),
  path('accounts/login/',app_views.login,name='login'),
  path('accounts/profile/',app_views.profile,name='profile'),
  path('update/',app_views.update_profile,name='update_profile'),
  path('logout/',auth_views.LogoutView.as_view(template_name = 'registration/logout.html'),name='logout'),
  path('search',app_views.search,name='search'),
  path('neighborhood/<int:neighborhood_id>/',app_views.neighborhood,name='neighborhood'),
  path('create_neighborhood',app_views.create_neighborhood,name='create_neighborhood'),
  path('create_business/<int:neighborhood_id>/',app_views.create_business,name='create_business'),
  path('choose_neighborhood/<int:neighborhood_id>/',app_views.choose_neighborhood,name='choose_neighborhood'),
  path('leave_neighborhood/<int:neighborhood_id>/',app_views.leave_neighborhood,name='leave_neighborhood'),
  path('create_post/<int:neighborhood_id>/',app_views.create_post,name='create_post'),
  path('delete_business/<business_id>',app_views.delete_business,name='delete_business'),
  path('update_business/<business_id>',app_views.update_business,name='update_business'),
  path('delete_post/<post_id>',app_views.delete_post,name='delete_post'),
  path('update_post/<post_id>',app_views.update_post,name='update_post'),
  path('update_neighborhood/<neighborhood_id>',app_views.update_neighborhood,name='update_neighborhood'),
  path('delete_neighborhood/<neighborhood_id>',app_views.delete_neighborhood,name='delete_neighborhood'),
  path('users/<pk>',app_views.users_profile,name='users_profile'),
]