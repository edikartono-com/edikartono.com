from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from corecode.models import Intro, Poster
from corecode import validation as img_val

class FormIntro(forms.ModelForm):
    class Meta:
        model = Intro
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(FormIntro, self).__init__(*args, **kwargs)

    def clean_bg_image(self):
        # maks file gambar 1 MB
        return img_val.image_validator(self.cleaned_data, 'bg_image', 1*1024*1024)

class FormPoster(forms.ModelForm):
    class Meta:
        model = Poster
        fields = '__all__'
    
    def clean_image(self):
        # maks file gambar 100 KB
        return img_val.image_validator(self.cleaned_data, 'image', 102400)

XUser = get_user_model()
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []
    
    users = forms.ModelMultipleChoiceField(
        queryset=XUser.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()
    
    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['users'])
    
    def save(self, *args, **kwargs):
        instance = super(GroupAdminForm, self).save()
        self.save_m2m()
        return instance