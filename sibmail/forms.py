from django import forms

class FormGetAllFolders(forms.Form):
    lmt = forms.NumberInput()
    oft = forms.NumberInput()
    srt = forms.TextInput()

class FormCreateContact(forms.Form):
    email = forms.EmailField(label="Email")
    fname = forms.CharField(max_length=50, label="Nama lengkap")
    optin = forms.BooleanField(
        label="Setuju menerima pemberitahuan content terbaru dan promosi",
        help_text="Kamu bisa unsubscribe (berhenti berlangganan) kapan saja"
    )