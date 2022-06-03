from django.contrib.auth.models import User
from django.forms import ModelForm

from akun import models as mak
from corecode import validation
from corecode.widgets import TagAutoComplete

class FormCommentUser(ModelForm):
    class Meta:
        model = mak.Comments
        fields = ['teks']
    
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(FormCommentUser, self).__init__(*args, **kwargs)

class FormCommentAnonym(FormCommentUser):
    class Meta(FormCommentUser.Meta):
        fields = ['nama','email','teks']
    
    def __init__(self, *args, **kwargs):
        super(FormCommentAnonym, self).__init__(*args, **kwargs)
        self.fields['nama'].validators = [validation.huruf_saja]

class FormUserGen1(ModelForm):
    class Meta:
        prefix = 'user_form'
        model = User
        fields = ['first_name','last_name']
    
    def __init__(self, *args, **kwargs):
        super(FormUserGen1, self).__init__(*args, **kwargs)
        self.fields['first_name'].validators = [validation.huruf_saja]
        self.fields['last_name'].validators = [validation.huruf_saja]

class FormUserGen2(ModelForm):
    class Meta:
        model = mak.MyAkun
        fields = ['gender','alamat']

class FormBio(ModelForm):
    class Meta:
        model = mak.BioAccount
        exclude = ['akun']
        widgets = {
            'skills': TagAutoComplete('taggit.tag')
        }