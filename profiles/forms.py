from django import forms
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")

    class Meta:
        model = Profile
        fields = ['bio', 'avatar']  # Only fields that the user can edit
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        # Save the profile changes first
        profile = super(ProfileEditForm, self).save(commit=False)

        # Save the first_name and last_name separately
        if commit:
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.save()
            profile.save()

        return profile
