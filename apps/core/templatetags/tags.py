from django import template
from apps.core.models import SaasConfiguration

register = template.Library()

@register.simple_tag
def get_brand(request):
    conf = SaasConfiguration.objects.filter(name='brand').first()
    if not conf:
        return None
    return conf.value


@register.simple_tag
def get_main_url(request):
    hostname = request.META['HTTP_HOST']
    if hostname.startswith("www."):
        hostname = hostname.replace('www.','')
    print(request.META['HTTP_HOST'][request.META['HTTP_HOST'].find(request.META['SERVER_NAME']):])
    print(hostname)

    return "//" + request.META['HTTP_HOST'][request.META['HTTP_HOST'].find(request.META['SERVER_NAME']):]
