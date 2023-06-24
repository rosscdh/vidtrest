# -*- coding: utf-8 -*-
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from queryset_sequence import QuerySetSequence

from taggit.models import Tag
from .models import VideoCat


class CategoryAndTagsAutocompleteView(Select2QuerySetSequenceView):
    """
    Autocomplete view for tags/categories lookup field
    """
    def get_result_value(self, result):
        """Override to return the plain name and not the cid-pk"""
        return u'%s' % (result.name)

    def get_queryset(self):
        self.q = self.request.GET.get('term', None)

        template_cats = VideoCat.objects.all()
        tags = Tag.objects.all()

        if self.q:
            template_cats = template_cats.filter(name__icontains=self.q)
            tags = tags.filter(name__icontains=self.q)

        # Aggregate querysets
        qs = QuerySetSequence(template_cats, tags)
        # qs = QuerySetSequence(tags)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(name__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs
