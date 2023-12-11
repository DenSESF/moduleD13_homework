from django.forms import Form, CharField, Textarea, TextInput


class NewsForm(Form):
    subject = CharField(
        max_length=120,
        strip=True,
        label='Заголовок:',
        widget=TextInput(attrs={
            'class': 'form-control',
        })
    )
    message = CharField(
        label='Текст:',
        widget=Textarea(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        fields = [ 'subject', 'message', ]
