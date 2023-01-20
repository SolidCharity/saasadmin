from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from apps.core.models import SaasPlan, SaasCustomer, SaasContract, SaasInstance

class SaasPlanHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "get_product", "slug"]
    history_list_display = ["cost_per_period"]
    search_fields = ['slug', 'product__slug']

    @admin.display(ordering='product__slug', description='Product')
    def get_product(self, obj):
        return obj.product.slug

admin.site.register(SaasPlan, SaasPlanHistoryAdmin)

class SaasCustomerHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "last_name", "first_name", "organisation_name"]
    history_list_display = ["email_address"]
    search_fields = ['last_name', 'first_name', 'email_address', 'organisation_name']

admin.site.register(SaasCustomer, SaasCustomerHistoryAdmin)

class SaasContractHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "get_customer", "get_product", "get_plan"]
    history_list_display = ["customer__email_address"]
    search_fields = ['customer__last_name', 'customer__first_name', 'customer__organisation_name', 'customer__email_address']

    @admin.display(ordering='customer__last_name', description='Customer')
    def get_customer(self, obj):
        return obj.customer.get_name()

    @admin.display(ordering='product__slug', description='Product')
    def get_product(self, obj):
        return obj.plan.product.slug

    @admin.display(ordering='plan__slug', description='Plan')
    def get_plan(self, obj):
        return obj.plan.slug

admin.site.register(SaasContract, SaasContractHistoryAdmin)

class SaasInstanceHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "identifier", "get_product"]
    history_list_display = ["additional_storage", "custom_domain"]
    search_fields = ['identifier', 'product__slug']

    @admin.display(ordering='product__slug', description='Product')
    def get_product(self, obj):
        return obj.product.slug

admin.site.register(SaasInstance, SaasInstanceHistoryAdmin)
