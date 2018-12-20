from django.urls import path
from . import views as makers_home_app_views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', makers_home_app_views.home_view, name='makers_home'),
	path('about/', makers_home_app_views.about_view, name='about'),
    path('contact/', makers_home_app_views.contact_view, name='contact'),



	path('dashboard/', makers_home_app_views.dashboard_view, name='makers_dashboard'),
	path('dashboard-update/', makers_home_app_views.dashboard_update_view, name='makers_dashboard_update'),
	path('activator/', makers_home_app_views.members_activation_view, name='makers_activator'),
    path('bulk-email/', makers_home_app_views.bulk_email_view, name='bulk_email'),
    path('membership/', makers_home_app_views.membership_view, name='membership'),

    path('weekly/', makers_home_app_views.weekly_sub_view, name='weekly'),
    path('monthly/', makers_home_app_views.monthly_sub_view, name='monthly'),
    path('annual/', makers_home_app_views.annual_sub_view, name='annual'),

    path('donate/', makers_home_app_views.donate_view, name='donate'),
    path('registration/', makers_home_app_views.registration_view, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='makers_home_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='makers_home_app/logout.html'), name='logout'),
    

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='makers_home_app/password_reset.html'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='makers_home_app/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='makers_home_app/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='makers_home_app/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]