from django.template import Library

register = Library()


@register.inclusion_tag("vid/vid_thumbs.html", takes_context=False)
def vid_thumbs(vid):
    return {
        'vid': vid
    }


@register.inclusion_tag("vid/vid_metadata.html", takes_context=False)
def vid_metadata(vid):
    return {
        'vid': vid
    }
