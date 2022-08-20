from django.conf import settings

def get_info_email(request):

    return {
       'info_email': settings.INFO_EMAIL,
    }
