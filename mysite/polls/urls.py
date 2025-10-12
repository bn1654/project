from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='registration'),
    path('accounts/login/', views.PollsLogin.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/change/', views.ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/delete', views.DeleteUserView.as_view(), name='user_delete'),
    path('accounts/avatar/change/', views.avatar_change, name='avatar_change'),
    path('accounts/password/change/', views.PollsPasswordChangeView.as_view(), name='password_change'),
]