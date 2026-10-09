from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
    def save(self, commit =True):
        user=super().save(commit=False) 
        user.email=self.cleaned_data["email"] #  validating specific fields and removeing invalidate data items of dict value
        if commit:
            user.save()
        return user       
class CheckoutForm(forms.Form):
    shipping_address=forms.CharField(max_length=255)
    widget=forms.Textarea(attrs={"row":3})
    label="Shipping address" 

