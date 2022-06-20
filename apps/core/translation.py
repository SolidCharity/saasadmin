from modeltranslation.translator import translator, register, TranslationOptions
from .models import SaasPlan, SaasProduct, SaasConfiguration
import simple_history

#@register(SaasPlan)
class SaasPlanTranslationOptions(TranslationOptions):
    fields = ('name', 'descr_target', 'descr_caption', 'descr_1', 'descr_2', 'descr_3', 'descr_4')

translator.register(SaasPlan, SaasPlanTranslationOptions)
simple_history.register(SaasPlan, inherit=True)

@register(SaasConfiguration)
class SaasConfigurationTranslationOptions(TranslationOptions):
    fields = ('value',)

@register(SaasProduct)
class SaasProductTranslationOptions(TranslationOptions):
    fields = ('description', 'upstream_url')
