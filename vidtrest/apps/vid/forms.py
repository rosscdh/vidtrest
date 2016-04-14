# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from django_select2.forms import HeavySelect2MultipleWidget

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
    combined_tags = AnyChoiceMultipleChoiceField(widget=SELECT_2_WIDGET)

    class Meta:
        model = Vid
        fields = (
            'name',
            'video',
        )

    def __init__(self, *args, **kwargs):
        super(VidForm, self).__init__(*args, **kwargs)

        # Setup the initial values for the combined_tags field
        # @TODO clean this nastiness up move into form or widget
        if self.instance.pk:
            cats = [(cat.get('name'), cat.get('name')) for cat in self.instance.categories.all().values('pk', 'name')]
            tags = [(tag.get('name'), tag.get('name')) for tag in self.instance.tags.all().values('pk', 'name')]
            combined_tags = cats + tags
            self.fields['combined_tags'].widget.attrs.update({'data-tags': ','.join([item[0] for item in combined_tags])})
            self.fields['combined_tags'].initial = [item[0] for item in combined_tags]
            self.fields['combined_tags'].choices = combined_tags


    def save(self, **kwargs):
        # pop the tags so we dont try save it to the model
        combined_tags = self.cleaned_data.pop('combined_tags', '')

        # start a service to perform that function of adding cats and tags
        service = ExtractcombinedTagsCategoriesService(vid=self.instance,
                                                       combined_tags=combined_tags)
        self.instance = service.process()

        return super(VidForm, self).save(**kwargs)
