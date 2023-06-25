# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import Library
from django.contrib.admin.templatetags.admin_list import (results,
                                                          result_headers,
                                                          result_hidden_fields,)
from vidtrest.apps.vid.models import Vid

register = Library()


@register.inclusion_tag("admin/vid/change_list_results.html")
def vid_result_list(cl):
    """
    Displays the headers and data list together
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': cl.result_list}


@register.inclusion_tag("vid/recent_vids.html")
def recent_vids(limit=5):
    """
    Displays the headers and data list together
    """
    return {"results": Vid.objects.filter().order_by('-created')[0:limit]}