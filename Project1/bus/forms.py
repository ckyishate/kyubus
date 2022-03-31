from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm




User = get_user_model()

class RegisterForm(forms.ModelForm):


    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs= User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is taken")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if  password is not None and password != password_2:
            self.add_error("password_2", "Your password must much")
        return cleaned_data


class UserAdminCreationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Comfirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if  password is not None and password != password_2:
            self.add_error("password_2", "Your password must much")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email','password','is_active','admin']

    def clean_password(self):
        return self.initial["password"]



#user 
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(
        required = True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'class':'form-control'}),
    )
    first_Name = forms.CharField(
        required = True,
        help_text='Enter First Name',
        widget=forms.TextInput(attrs={ 'placeholder': 'First Name', 'class':'form-control'}),
    )
    last_Name = forms.CharField(
        required = True,
        help_text='Enter Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class':'form-control'}),
    )
    contact = forms.CharField(
        required = True,
        help_text='Enter Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Insert your contact telephone number', 'class':'form-control'}),
    )
   
    sex = forms.CharField(
        required = True,
        widget=forms.Select(attrs= {'class':'form-control'}, choices=((('Select your Gender','Select your Gender')),('Male','Male'),('Female','Female'))),
    )   
    
    password1 = forms.CharField(
    help_text='Enter Password',
    required = True,
    widget=forms.PasswordInput(attrs={ 'placeholder': 'Password', 'class':'form-control'}),
    )
    password2 = forms.CharField(
    required = True,
    help_text='Enter Password Again',
    widget=forms.PasswordInput(attrs={ 'placeholder': 'Password Again', 'class':'form-control'}),
    )


    class Meta:
        model = User
        fields = ['first_Name','last_Name','sex','contact','email','password1','password2']

       