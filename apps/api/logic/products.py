from django.utils import translation
from apps.core.models import SaasProduct

class LogicProducts:

    def get_product(self, request):
        if 'product_id' in request.GET:
            products = SaasProduct.objects.filter(id = request.GET['product_id'])
        else:
            products = SaasProduct.objects
        if products.count() == 1:
            return products.first()
        return None
