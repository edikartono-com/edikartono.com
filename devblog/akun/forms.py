from django.forms import ModelForm

from akun import models as mak

class FormCommentUser(ModelForm):
    class Meta:
        model = mak.Comments
        fields = ['teks']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FormCommentUser, self).__init__(*args, **kwargs)

class FormCommentAnonym(ModelForm):
    class Meta:
        model = mak.Comments
        fields = ['nama','email','teks']