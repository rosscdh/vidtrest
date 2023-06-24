# -*- coding: utf-8 -*-
from django import forms
from django.urls import reverse
from django.utils.translation import gettext as _

from django_select2.forms import HeavySelect2MultipleWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Field, Submit

from vidtrest.apps.vid.forms import AnyChoiceMultipleChoiceField

SELECT_2_WIDGET = HeavySelect2MultipleWidget(data_view='public:search_autocomplete')


class SearchForm(forms.Form):
    query = AnyChoiceMultipleChoiceField(widget=SELECT_2_WIDGET,
                                         label='',
                                         required=True)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        # Setup the initial values for the combined_tags field
        # @TODO clean this nastiness up move into form or widget
        self.fields['query'].widget.attrs.update({'data-tags': 'true'})  # V important for taking multiple and creating new

    @property
    def helper(self):
        helper = FormHelper(self)

        helper.form_action = reverse('vid:search')
        helper.form_method = 'GET'
        helper.form_show_errors = True
        helper.render_unmentioned_fields = True

        helper.layout = Layout(Field('query', css_class='col-sm-6'),
                               ButtonHolder(Submit('submit', _('Search'), css_class='btn btn-success btn-lg'),))
        return helper
