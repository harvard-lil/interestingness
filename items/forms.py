from items.models import Organization, Contributor, Item

from django import forms
from django.forms import FileInput

from items.models import InterUser

class AddItemForm(forms.ModelForm):
    
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'maxlength':117}))

    class Meta:
        model = Item
        #exclude = ('contributed_date', 'bookmarklet_key')
        fields = ["description"]



class BookmarkletKeyForm(forms.ModelForm):
    """
    A form that helps users update their profiles
    """
    class Meta:
        model = Contributor
        exclude = ('key', 'is_active', 'organization',)
        widgets = {
            'profile_pic': FileInput(),
            'display_name': forms.TextInput(attrs={'placeholder': 'your name'}),
        }

class CreateUserForm(forms.ModelForm):

    """
    stripped down user reg form
    This is mostly a django.contrib.auth.forms.UserCreationForm
    """

    class Meta:
        model = InterUser
        fields = ["first_name", "last_name", "email"]


    error_messages = {
        'duplicate_email': "A user with that email address already exists.",
    }

    email = forms.EmailField()

    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM.

        email = self.cleaned_data["email"]
        try:
            InterUser.objects.get(email=email)
        except InterUser.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])


class UserRegForm(forms.ModelForm):
    """
    stripped down user reg form
    This is mostly a django.contrib.auth.forms.UserCreationForm
    """
    error_messages = {
        'duplicate_email': "A user with that email address already exists.",
    }

    email = forms.EmailField()

    #password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = InterUser
        fields = ("email", "first_name", "last_name")

    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM.

        email = self.cleaned_data["email"]
        try:
            InterUser.objects.get(email=email)
        except InterUser.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])
        
        
class OrganizationFormSelfRegistration(forms.ModelForm):

    error_messages = {
        'duplicate_slug': "Somebody already claimed that address.",
    }
            
    class Meta:
        model = Organization
        fields = ("name", "slug")
        
    def clean_slug(self):
        # Since slug is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        slug = self.cleaned_data["slug"]
        try:
            Organization.objects.get(slug=slug)
        except Organization.DoesNotExist:
            return slug
        raise forms.ValidationError(self.error_messages['duplicate_slug'])
        
    def __init__(self, *args, **kwargs):
            super(OrganizationFormSelfRegistration, self).__init__(*args, **kwargs)
            self.fields['slug'].label = "Your Signal Back address"
            #self.fields['slug'].help_text = "signalback.com"
            self.fields['name'].label = "Name of your organization"
            self.fields.keyOrder = [
            'name',
            'slug']


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without entering the
    old password
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="New password confirmation",
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                logger.debug('mismatch')
                raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user