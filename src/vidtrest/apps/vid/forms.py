# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from django_select2.forms import HeavySelect2MultipleWidget

from vidtrest.apps.categories.models import VideoCat
from .models import Vid
from .services import ExtractcombinedTagsCategoriesService


SELECT_2_WIDGET = HeavySelect2MultipleWidget(data_view='categories:autocomplete')


class AnyChoiceMultipleChoiceField(forms.MultipleChoiceField):
    """
    Allows a choice of any value, for select2
    """
    def validate(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')


class VidForm(forms.ModelForm):
    combined_tags = AnyChoiceMultipleChoiceField(widget=SELECT_2_WIDGET,
                                                 required=False)

    categories = forms.ModelMultipleChoiceField(queryset=VideoCat.objects.all(),
                                                widget=forms.CheckboxSelectMultiple(),
                                                required=False)

    class Meta:
        model = Vid
        fields = (
            'video',
            'name',
            'categories',
        )

    def __init__(self, *args, **kwargs):
        super(VidForm, self).__init__(*args, **kwargs)

        # Setup the initial values for the combined_tags field
        # @TODO clean this nastiness up move into form or widget
        self.fields['combined_tags'].widget.attrs.update({'data-tags': 'true'})  # V important for taking multiple and creating new

        if self.instance.pk:
            cats = [(cat.get('name'), cat.get('name')) for cat in self.instance.categories.all().values('pk', 'name')]
            tags = [(tag.get('name'), tag.get('name')) for tag in self.instance.tags.all().values('pk', 'name')]
            combined_tags = cats + tags
            self.fields['combined_tags'].initial = [item[0] for item in combined_tags]
            self.fields['combined_tags'].choices = combined_tags

    def save(self, **kwargs):
        self.instance = super(VidForm, self).save(**kwargs)

        if self.current_user and self.instance.pk is None or self.instance.uploaded_by is None:
            self.instance.uploaded_by = self.current_user

        self.instance.save()

        # pop the tags so we dont try save it to the model
        combined_tags = self.cleaned_data.pop('combined_tags', '')

        # start a service to perform that function of adding cats and tags
        service = ExtractcombinedTagsCategoriesService(vid=self.instance,
                                                       combined_tags=combined_tags)
        self.instance = service.process()

        return self.instance
