from django import forms
from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
from cloudinary.forms import CloudinaryFileField


from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from modules.customers.models import Customer

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type': 'text','name':'username', 'placeholder':'Email or Username', 'class' :'sizefull s-text7 p-l-18 p-r-18'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'type': 'Password','name':'password', 'placeholder':'Password', 'class' :'sizefull s-text7 p-l-18 p-r-18'}))

    #username = forms.CharField()
    #password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)



class UserRegisterForm(forms.ModelForm):
    email2 = forms.EmailField(label='Confirm Email', widget=forms.TextInput(attrs={'type':'email','placeholder':'Confirm Email ', 'class' :'sizefull s-text7 p-l-18 p-r-18'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'type':'password', 'placeholder':'Confirm Password ', 'class' :'sizefull s-text7 p-l-18 p-r-18'}))

    class Meta:
        model = User
        fields = [

            'first_name',
            'last_name',
            'username',
            'email',
            'email2',
            'password',
            'password2',
        ]
        widgets={
            'username':forms.TextInput(attrs={'placeholder':'User Name', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'first_name':forms.TextInput(attrs={'placeholder':'First Name ', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'last_name':forms.TextInput(attrs={'placeholder':'Last Name ', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'email':forms.TextInput(attrs={'placeholder':'Email','type':'email', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'password':forms.TextInput(attrs={'placeholder':'Password ','type':'password', 'class' :'sizefull s-text7 p-l-18 p-r-18'})
        }

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        return email
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("password must match")
        return password


class CustomerRegisterForm(forms.ModelForm):
    user = UserRegisterForm()
    class Meta:
        model = Customer
        fields = [
            'user_image',
            'phone_number',
            'date_of_birth',
            'country',
            'city',
            'address',
        ]
        widgets={

            'phone_number':forms.TextInput(attrs={'placeholder':'Phone Number', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'date_of_birth':forms.TextInput(attrs={'placeholder':'Date of Birth','type':'date', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'country':forms.TextInput(attrs={'placeholder':'Country ', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'city':forms.TextInput(attrs={'placeholder':'City', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'address':forms.TextInput(attrs={'placeholder':'Street Address ', 'class' :'sizefull s-text7 p-l-18 p-r-18'})
        }


from string import Template
from django.utils.safestring import mark_safe
from django.conf import settings


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html = Template("""<img src="$media$link"/>""")
        return mark_safe(html.substitute(media=settings.MEDIA_URL, link=value))

class editProfileForm(forms.ModelForm):
    # user_image = forms.ImageField(  label=('User image'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    # image_tag = forms.ImageField(widget=mark_safe(Template("<img src=""/>")))
    class Meta:
        model=Customer
        # user_image = CloudinaryFileField()
        fields = [


            'user_image',
            'phone_number',
            'date_of_birth',
            'country',
            'city',
            'address',
        ]
        widgets={


            'phone_number':forms.TextInput(attrs={'placeholder':'Phone Number', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'date_of_birth':forms.DateInput(attrs={ 'placeholder':'Date of Birth','type':'date', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'country':forms.TextInput(attrs={'placeholder':'Country ', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'city':forms.TextInput(attrs={'placeholder':'City', 'class' :'sizefull s-text7 p-l-18 p-r-18'}),
            'address':forms.TextInput(attrs={'placeholder':'Street Address ', 'class' :'sizefull s-text7 p-l-18 p-r-18'})
        }

