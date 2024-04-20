from django.conf import settings

def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}

def get_soil_api(request):
    return {'SOIL_NARC_API': settings.SOIL_NARC_API}


