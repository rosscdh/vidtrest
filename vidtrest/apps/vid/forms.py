# -*- coding: utf-8 -*-
from django import forms

from django.contrib.contenttypes.models import ContentType

from dal.forms import FutureModelForm
from dal_select2.widgets import TagSelect2
from taggit.models import Tag
from vidtrest.apps.categories.models import VideoCat

from .models import Vid
from .services import ExtractcombinedTagsCategoriesService

import re

CONTENT_TYPES = {
    'cat': ContentType.objects.get_for_model(VideoCat),
    'tag': ContentType.objects.get_for_model(Tag),
}


class VidForm(FutureModelForm):
    combined_tags = forms.MultipleChoiceField(widget=TagSelect2('categories:autocomplete'), required=False)

    class Meta:
        model = Vid
        fields = (
            'name',
            'video',
        )

    def __init__(self, *args, **kwargs):
        super(VidForm, self).__init__(*args, **kwargs)

        # Setup the initial values for the combined_tags field
        if self.instance:
            cats = [('%s-%s' % (CONTENT_TYPES['cat'].pk, cat.get('pk')), cat.get('name')) for cat in self.instance.categories.all().values('pk', 'name')]
            tags = [('%s-%s' % (CONTENT_TYPES['tag'].pk, tag.get('pk')), tag.get('name')) for tag in self.instance.tags.all().values('pk', 'name')]

            self.fields['combined_tags'].widget.attrs.update({'data-tags': ','.join([item[0] for item in cats + tags])})
            self.fields['combined_tags'].initial = [item[0] for item in cats + tags]
            self.fields['combined_tags'].choices = cats + tags

    def transform_to_content_objects(self, content_type_objects):
        response = []
        # perform magic getting the content_type-model_pk split
        content_type_pks, model_pks = zip(*[tuple(item.split('-')) for item in content_type_objects])

        content_type_models = {}
        for content_type in ContentType.objects.filter(pk__in=content_type_pks):
            content_type_models[content_type.pk] = content_type.model_class()

        # rezip the content_type-model_pk
        for content_type_pk, model_pk in zip(content_type_pks, model_pks):
            obj = content_type_models[int(content_type_pk)].objects.get(pk=model_pk)
            response.append(obj.name)

        return response

    def save(self, **kwargs):
        # pop the tags so we dont try save it to the model
        combined_tags = self.cleaned_data.pop('combined_tags', '').split(',')

        new_items = set([item for item in combined_tags if re.match('^(\d+)-(\d+)$', item) is None])
        existing_items = [item for item in combined_tags if re.match('^(\d+)-(\d+)$', item) is not None]
        existing_items = set(self.transform_to_content_objects(content_type_objects=existing_items))

        combined_tags = existing_items.union(new_items)

        # start a service to perform that function of adding cats and tags
        service = ExtractcombinedTagsCategoriesService(vid=self.instance,
                                                       combined_tags=combined_tags)
        self.instance = service.process()

        return super(VidForm, self).save(**kwargs)
