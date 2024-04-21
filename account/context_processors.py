from django.conf import settings

def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}

# def get_soil_api(request):
#     return {'SOIL_NARC_API': settings.SOIL_NARC_API}


def get_video_call_id(request):
    return {'VIDEO_CALL_ID': settings.VIDEO_CALL_ID}

def get_video_call_key(request):
    return {'VIDEO_CALL_ID_KEY': settings.VIDEO_CALL_ID_KEY}