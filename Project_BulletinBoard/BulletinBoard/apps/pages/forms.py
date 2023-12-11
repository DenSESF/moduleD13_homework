from django import forms
from django.forms import ModelForm
from posts.models import Advert, Reply


class MultipleFileInput(forms.ClearableFileInput):
    # allow_multiple_selected = True
    input_text = 'Заменить'
    initial_text = 'Текущий'
    clear_checkbox_label = 'Удалить'

    def __init__(self, attrs=None, multifile=True):
        if attrs is None:
            attrs = { 'class': 'form-control' }
            self.allow_multiple_selected = multifile
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"].update(
            {
                "input_text": self.input_text,
                "initial_text": self.initial_text,
                "clear_checkbox_label": self.clear_checkbox_label,
            }
        )
        return context


class MultipleFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class PostCreateForm(ModelForm):
    images = MultipleFileField(
        label='Прикрепить картинки:',
        required=False,
    )
    class Meta:
        model = Advert
        fields = ['header', 'category', 'text', 'video', 'images']
        labels = {
            'header': 'Заголовок:',
            'category': 'Категория:',
            'text': 'Объявление:',
            'video': 'Прикрепить видеo:',
            }
        widgets = {
            'header': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'maxlength': 120,
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5'
            }),
            'video': MultipleFileInput(attrs={
                'class': 'form-control',
                },
                multifile=False
            ),
        }


class PostUpdateForm(PostCreateForm):
    clear_images = forms.MultipleChoiceField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance is not None and instance.image.exists():
            choice_gen = ((f'{img.pk}', f'{img.image}') for img in instance.image.all())
            self.fields.update({'clear_images': forms.MultipleChoiceField(
                    choices=[*choice_gen],
                    widget=forms.CheckboxSelectMultiple(),
                    label='Текущие:',
                    required=False,
                )}
            )

    class Meta:
        model = PostCreateForm.Meta.model
        fields = ['header', 'category', 'text', 'video', 'clear_images', 'images']
        labels = PostCreateForm.Meta.labels
        widgets = PostCreateForm.Meta.widgets


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        # fields = '__all__'
        fields = [
            'text',
        ]
        labels = {
            'text': 'Сообщение:',
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
            }),
        }
