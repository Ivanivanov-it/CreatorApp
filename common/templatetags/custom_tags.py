from django import template
register = template.Library()


@register.inclusion_tag('show_roles.html')
def show_roles(obj):
    return {'roles': obj.roles.all()}

