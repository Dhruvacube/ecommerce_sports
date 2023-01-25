from django.forms import ModelForm
from .models import FeedBack

class FeedBackForm(ModelForm):
    class Meta:
        model = FeedBack
        fields = ['email', 'feedback']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = "border-0 px-3 py-3 rounded text-sm shadow w-full bg-gray-300 placeholder-black text-gray-800 outline-none focus:bg-gray-400"
        self.fields["email"].widget.attrs["required"] = "true"
        self.fields["email"].widget.attrs["style"] = "transition: all 0.15s ease 0s;"
        
        self.fields["feedback"].widget.attrs["class"] = "border-0 px-3 py-3 bg-gray-300 placeholder-black text-gray-800 rounded text-sm shadow focus:outline-none w-full"
        self.fields["feedback"].widget.attrs["required"] = "true"
        self.fields["feedback"].widget.attrs["rows"] = "4"
        self.fields["feedback"].widget.attrs["cols"] = "80"
        