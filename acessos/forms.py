from django.contrib.auth.forms import UserChangeForm as AuthUserChangeForm, UserCreationForm as AuthUserCreationForm
from django.forms import ModelForm
from django.contrib.auth.forms import SetPasswordForm

from .models import Users

class UserChangeForm(AuthUserChangeForm):
    class Meta(AuthUserChangeForm.Meta):
        model = Users
        
class UserCreationForm(AuthUserCreationForm):
    class Meta(AuthUserCreationForm.Meta):
        model = Users
        
class ProfilePictureForm(ModelForm):
    class Meta:
        model = Users
        fields = ['profile_picture']
        
        
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)