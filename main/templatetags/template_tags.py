from django import template
from eshop.models import Category

register = template.Library()


@register.inclusion_tag('template_tags/category.html')
def list_category():
    return {
        'object_list': Category.objects.filter(active=True)
    }
