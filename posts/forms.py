from django.forms import ModelForm

from corecode import validation as img_val
from posts.models import Posts, Page

class FormPage(ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
    
    def clean_image(self):
        return img_val.image_validator(self.cleaned_data, 'image', 1*1024*1024)

class FormPosts(ModelForm):
    class Meta:
        model = Posts
        exclude = ['author','status']
    
    def clean_image(self):
        return img_val.image_validator(self.cleaned_data, 'image', 1*1024*1024)