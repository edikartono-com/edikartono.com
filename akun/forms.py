from django.forms import ModelForm

from akun import models as mak
from corecode import validation

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