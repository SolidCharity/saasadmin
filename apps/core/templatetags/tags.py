from django import template
from apps.core.models import SaasConfiguration
import tldextract

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

    servername = request.META['SERVER_NAME']
    # only use the main domain with top level domain, without subdomains
    ext = tldextract.extract(servername)
    if ext.suffix:
        servername = f"{ext.domain}.{ext.suffix}"

    return request.META['HTTP_HOST'][request.META['HTTP_HOST'].find(servername):]

@register.simple_tag
def get_topnav_active(request, active_url, menu=''):
    if menu:
        if active_url in menu:
            return "active"
        return ""
    if active_url in request.path:
        return "active"
    return ""