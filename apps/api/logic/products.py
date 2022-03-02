from django.utils import translation
from apps.core.models import SaasProduct

class LogicProducts:

    def get_product(self, request):
        if 'product_id' in request.GET:
            products = SaasProduct.objects.filter(id = request.GET['product_id'])
        elif 'product_id' in request.POST:
            products = SaasProduct.objects.filter(id = request.POST['product_id'])
        elif 'product' in request.GET:
            products = SaasProduct.objects.filter(slug = request.GET['product'])
        else:
            products = SaasProduct.objects
        if products.count() == 1:
            return products.first()
        else:
            # search all projects slugs in the request hostname
            for product in products.all():
                if request.META['HTTP_HOST'].startswith(product.slug + "."):
                    return product

        return None

    def get_products(self):
        # TODO only get active products
        return SaasProduct.objects.all()
