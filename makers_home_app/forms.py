from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserMembership



class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']



class UserRegistrationExtraFieldForm(forms.ModelForm):
	class Meta:
		model = UserMembership
		fields = ['phone_number']



class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']



class UserDashboardUpdateForm(forms.ModelForm):
	class Meta:
		model = UserMembership
		fields = ['phone_number']



class MemberActivatioForm(forms.Form):
	User_Name = forms.CharField(max_length=100, widget=forms.TextInput( attrs={
													'placeholder' : 'Enter Subscriber Username',
													}
													)
							)
	subscription_Type = forms.CharField(max_length=100, widget=forms.TextInput( attrs={
													'placeholder' : 'Weekly, Monthly or Annual',
													}
													)
							)



class BulkEmailForm(forms.Form):
	Subject = forms.CharField(max_length=200)
							
	Messege = forms.CharField(max_length=500, widget=forms.Textarea( 
													))
													


class MemberContactForm(forms.Form):
	Subject = forms.CharField(max_length=200)
	email = forms.CharField(max_length=100, widget=forms.EmailInput( 
													))
	Messege = forms.CharField(max_length=500, widget=forms.Textarea( 
													))
