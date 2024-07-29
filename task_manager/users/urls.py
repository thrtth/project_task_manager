from django.urls import path

from task_manager.users import views


urlpatterns = [
    path('', views.UsersListView.as_view(), name='users_list'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete', views.UserDeleteView.as_view(), name='user_delete'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
