from django.contrib.auth.models import User
from django.conf import settings

from django.shortcuts import get_object_or_404, render, redirect
import datetime
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
					UserRegistrationForm,
					 UserRegistrationExtraFieldForm,
					  MemberActivatioForm,UserDashboardUpdateForm,
					  UserUpdateForm,
					  MemberContactForm,
					  BulkEmailForm,
					  )
from django.core.mail import send_mail
from .models import Subscription, UserMembership 





global PHONE_NUMBER ########A golabal Variable that holds The Phone Number

################# Gets Phone Number Helper Function ##################
#********returns phone number to signal.py where the function is called
def get_phone_number():
	return PHONE_NUMBER
################# End Gets And return Phone Number ##################




################# Phone Number Validator Helper Function ###################
def validatePhoneNumber(p_number):
	return True  #*************needs some improvement later
################# End Of  Phone Number Validator Function ##################




################# Home View ######################################
def home_view(request):
	context = {

	}
	return render(request, 'makers_home_app/home.html', context)
################# End of Home View ################################



################# Member Contact View ######################################
def contact_view(request):
	if request.method == 'POST':
		Member_Contact_F = MemberContactForm()
		print(request.POST.get('Subject', 'not available'))
		print(request.POST.get('email', 'not available'))
		print(request.POST.get('Messege', 'not available'))
		send_mail(
			request.POST.get('Subject'), 
			request.POST.get('Messege') + " " + 'reply via this email' + "  " + request.POST.get('email', 'not available'),
			settings.EMAIL_HOST_USER,
			['iolabmakespace@gmail.com',settings.EMAIL_HOST_USER],
			fail_silently=True
			)
		messages.success(request, f'Your messege have been sent, we will get back to you as soon as possible')

	else:
		Member_Contact_F = MemberContactForm()
	context = {
		'Member_Contact_F':Member_Contact_F
	}
	return render(request, 'makers_home_app/contact.html', context)
################# End of Member Contact View ################################



################# donate View ######################################
def about_view(request):
	context = {

	}
	return render(request, 'makers_home_app/about.html', context)
################# End of donate View ################################




################# membership View ######################################
def membership_view(request):
	context = {

	}
	return render(request, 'makers_home_app/membership.html', context)
################# End of membership View ################################



################# donate View ######################################
def donate_view(request):
	context = {

	}
	return render(request, 'makers_home_app/donate.html', context)
################# End of donate View ################################



################# Registration View ################################
def registration_view(request):
	if request.method == 'POST':
		regF1 = UserRegistrationForm(request.POST)
		regF2 = UserRegistrationExtraFieldForm(request.POST)
		print(request.POST)

		## Checks for form Validation By Calling the Default is_valid() and the user Defined validatePhoneNumber() function  ##
		if regF1.is_valid() and validatePhoneNumber(request.POST.get('phone_number')):
			print('they are all Valid')
			global PHONE_NUMBER
			PHONE_NUMBER = request.POST.get('phone_number')
			regF1.save()
			
			messages.success(request, f'Your account has been created! You are now able to log into your dashboard')
			return redirect('login')
		else:
			messages.warning(request, f'Invalid please do enter a valid data')      
	else:
		regF1 = UserRegistrationForm()
		regF2 = UserRegistrationExtraFieldForm()

	context = {
		'regF1' : regF1,
		'regF2' : regF2
	}
	return render(request, 'makers_home_app/registration.html', context)
############ End Of Registration View ###############################





################# Dashboard View ################################
@login_required
def dashboard_view(request):
	if request.user.usermembership.exp_date <= timezone.now():
			request.user.usermembership.active = False
			request.user.usermembership.save()


	if request.user.usermembership.active:
		sub_date = request.user.usermembership.subscription_date
		expiry_date = request.user.usermembership.exp_date
		sub_type = request.user.usermembership.subscription_type
		sub_duration = request.user.usermembership.subscription_type.duration
		d_remaining = expiry_date - timezone.now()
		p_number = request.user.usermembership.phone_number
		activated = request.user.usermembership.active
		percentage = d_remaining.days/sub_duration * 100
		# print(sub_date)
		# print(expiry_date)
		# print(sub_type)
		# print(sub_duration)
		# print(d_remaining)
		context = {
			'sub_date':sub_date,
			'expiry_date':expiry_date,
			'sub_type':sub_type,
			'sub_duration':sub_duration,
			'd_remaining':d_remaining,
			'p_number':p_number,
			'activated':activated,
			'percentage':percentage
		}
		
		return render(request, 'makers_home_app/dashboard.html', context)
	else:
		return render(request, 'makers_home_app/dashboard.html')
	
################# End Dashboard View ################################




################# Dashboard Update View ################################
@login_required
def dashboard_update_view(request):
	if request.method == 'POST':
		u_u_form = UserUpdateForm(request.POST, instance=request.user)
		u_d_form = UserDashboardUpdateForm(request.POST, instance=request.user.usermembership)

		if u_u_form.is_valid() and u_d_form.is_valid():
			u_u_form.save()
			u_d_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('makers_dashboard')
	else:
		u_u_form = UserUpdateForm()
		u_d_form = UserDashboardUpdateForm()
	context = {
		'u_u_form':u_u_form,
		'u_d_form':u_d_form,
	}

	return render(request, 'makers_home_app/dashboard_update.html', context)
################# End of Dashboard Update View ################################





################# members_activation View ################################
@login_required
def members_activation_view(request):
	if request.user.is_superuser:
		if request.method == 'POST':
			m_activation_f = MemberActivatioForm()

			username_entered = request.POST.get('User_Name')
			user_sub_type_entered = request.POST.get('subscription_Type')


			user_to_be_activated = get_object_or_404(User, username__exact=username_entered)
			user_to_be_activated.usermembership.active = True
			user_to_be_activated.usermembership.subscription_type = get_object_or_404(Subscription, subscription_types__exact=user_sub_type_entered)
			user_to_be_activated.usermembership.subscription_date = timezone.now()
			user_to_be_activated.usermembership.exp_date = user_to_be_activated.usermembership.subscription_date + datetime.timedelta(days = user_to_be_activated.usermembership.subscription_type.duration)
			user_to_be_activated.save()
			messages.success(request, f'{user_to_be_activated} successfully subscribed to the {user_to_be_activated.usermembership.subscription_type} plan!!!')


			context = {
				'm_activation_f' : m_activation_f,
			}


			send_mail(
			"Subscription Status Alert", 
			f"Hi {user_to_be_activated} you have been successfully subscribed to our {user_sub_type_entered} plan, check your dashboard for subscription details",
			settings.EMAIL_HOST_USER,
			[user_to_be_activated.email],
			fail_silently=True
			)


		else:
			m_activation_f = MemberActivatioForm()

			context = {
				'm_activation_f' : m_activation_f,
			}
		return render(request, 'makers_home_app/members_activation.html', context)
	else:
		messages.warning(request, f'you dont have access to this page fuck off!!!')
		return redirect('makers_dashboard')
################# End of members_activation View ################################





#########*****************The Three subscription View**************########################


#########*****************Weekly Sub View**************########################
@login_required
def weekly_sub_view(request):
	send_mail(
			"Subscription Alert",
			f"A User with the username: {request.user.username}, Phone Number:{request.user.usermembership.phone_number} and email: {request.user.email} request to be subscribed to the Weekly plan",
			settings.EMAIL_HOST_USER,
			[settings.EMAIL_HOST_USER],
			fail_silently=True
			)
	context={

	}
	return render(request, 'makers_home_app/weekly_sub.html', context)
#########*****************End Of Weekly Sub View**************#################




#########*****************Monthly Sub View**************########################
@login_required
def monthly_sub_view(request):
	
	send_mail(
			"Subscription Alert",
			f"A User with the username: {request.user.username}, Phone Number:{request.user.usermembership.phone_number} and email: {request.user.email} request to be subscribed to the Monthly plan",
			settings.EMAIL_HOST_USER,
			[settings.EMAIL_HOST_USER],
			fail_silently=True
			)
	context={
	
	}
	return render(request, 'makers_home_app/monthly_sub.html', context)
#########*****************End Of Monthly Sub View**************#################




#########*****************Annual Sub View**************########################
@login_required
def annual_sub_view(request):
	send_mail(
			"Subscription Alert",
			f"A User with the username: {request.user.username}, Phone Number:{request.user.usermembership.phone_number} and email: {request.user.email} request to be subscribed to the Annual plan",
			settings.EMAIL_HOST_USER,
			[settings.EMAIL_HOST_USER],
			fail_silently=True
			)
	context={
	
	}
	return render(request, 'makers_home_app/annual_sub.html', context)
#########*****************End Of Annual Sub View**************#################


#########***************** End The Three subscription View**************###################

############################### Bulk Email View ############################################
@login_required
def bulk_email_view(request):
	print(User.objects.all().count())
	if request.user.is_superuser:
		if request.method == 'POST':
			B_Email_F = BulkEmailForm(request.POST)
			subject = request.POST.get('Subject')
			messege = request.POST.get('Messege')
			for usermember in User.objects.all():
				send_mail(
					subject,
					messege,
					settings.EMAIL_HOST_USER,
					[usermember.email],
					fail_silently=True
					)
			messages.success(request, f'Bulk email successfully sent to all {User.objects.all().count()} users!!!')
			context = {
				'B_Email_F' : B_Email_F,
			}



		else:
			B_Email_F = BulkEmailForm()

			context = {
				'B_Email_F' : B_Email_F,
			}
		return render(request, 'makers_home_app/bulk_email.html', context)
	else:
		messages.warning(request, f'you dont have access to this page fuck off!!!')
		return redirect('makers_dashboard')
		

############################### Bulk Email View ############################################
