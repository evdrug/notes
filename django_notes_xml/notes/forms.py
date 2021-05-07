from django import forms


class CreateNoteForm(forms.Form):
    add_text_area = forms.CharField(label='Добавление заметки', widget=forms.Textarea(
        attrs={'class': 'form-control mb-2 mr-sm-2'}))