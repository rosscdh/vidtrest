# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django_select2.forms import HeavySelect2MultipleWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Field, Submit

from vidtrest.apps.vid.forms import AnyChoiceMultipleChoiceField

SELECT_2_WIDGET = HeavySelect2MultipleWidget(data_view='public:search_autocomplete')


class SearchForm(forms.Form):
    query = AnyChoiceMultipleChoiceField(widget=SELECT_2_WIDGET,
                                         label='',
                                         required=True)
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
