# -*- coding: utf-8 -*-
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from queryset_sequence import QuerySetSequence

from taggit.models import Tag
from .models import VideoCat


class CategoryAndTagsAutocompleteView(Select2QuerySetSequenceView):
    """
    Autocomplete view for tags/categories lookup field
    """
    def get_queryset(self):
        template_cats = VideoCat.objects.all()
        tags = Tag.objects.all()

        if self.q:
            template_cats = template_cats.filter(name__icontains=self.q)
            tags = tags.filter(name__icontains=self.q)

        # Aggregate querysets
        qs = QuerySetSequence(template_cats, tags)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(name__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs
