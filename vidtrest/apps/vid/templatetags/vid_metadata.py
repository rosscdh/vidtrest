from django.template import Library

register = Library()

@register.inclusion_tag("vid/vid_metadata.html", takes_context=False)
def show_vid_metadata(vid):
  return { 'vid': vid }
