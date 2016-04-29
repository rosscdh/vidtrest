# -*- coding: utf-8 -*-
from django import forms

from django_select2.forms import HeavySelect2MultipleWidget

from vidtrest.apps.vid.forms import AnyChoiceMultipleChoiceField

SELECT_2_WIDGET = HeavySelect2MultipleWidget(data_view='public:search_autocomplete')


class SearchForm(forms.Form):
    query = AnyChoiceMultipleChoiceField(widget=SELECT_2_WIDGET,
                                         label='',
                                         required=False)
