from django import forms
from .models import File

# Regular form
class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["xlsx"]:
            raise forms.ValidationError("仅允许上传 xlsx 格式文件")
        # return cleaned data is very important.
        return file

# Model form
class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)
        widgets = {
            # 'upload_method': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["xlsx"]:
            raise forms.ValidationError("仅允许上传 xlsx 格式文件")
        # return cleaned data is very important.
        return file