from django.utils import translation
from apps.core.models import SaasProduct

class LogicProducts:

    def get_product(self, request, only_active = True):
        result = None
        if 'product_id' in request.GET:
            products = SaasProduct.objects.filter(id = request.GET['product_id'])
        elif 'product_id' in request.POST:
            products = SaasProduct.objects.filter(id = request.POST['product_id'])
        elif 'product' in request.GET:
            products = SaasProduct.objects.filter(slug = request.GET['product'])
        else:
            products = SaasProduct.objects
        if products.count() == 1:
            result = products.first()
        else:
            # search all projects slugs in the request hostname
            for product in products.all():
                if request.META['HTTP_HOST'].startswith(product.slug + "."):
                    result = product

        if only_active and result is not None:
            if not result.is_active:
                return None

        return result

    def get_products(self, only_active = True):
        if only_active:
            return SaasProduct.objects.filter(is_active=True).order_by('slug')
        else:
            return SaasProduct.objects.order_by('slug').all()
