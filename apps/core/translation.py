from modeltranslation.translator import register, TranslationOptions
from .models import SaasPlan, SaasConfiguration

@register(SaasPlan)
class SaasPlanTranslationOptions(TranslationOptions):
    fields = ('name', 'descr_target', 'descr_caption', 'descr_1', 'descr_2', 'descr_3', 'descr_4')

@register(SaasConfiguration)
class SaasConfigurationTranslationOptions(TranslationOptions):
    fields = ('value',)
