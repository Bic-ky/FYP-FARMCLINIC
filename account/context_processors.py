from django.conf import settings

from account.models import UserProfile

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)


def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}

# def get_soil_api(request):
#     return {'SOIL_NARC_API': settings.SOIL_NARC_API}


def get_video_call_id(request):
    return {'VIDEO_CALL_ID': settings.VIDEO_CALL_ID}

def get_video_call_key(request):
    return {'VIDEO_CALL_ID_KEY': settings.VIDEO_CALL_ID_KEY}

def get_weather_api(request):
    return {'WEATHER_API': settings.WEATHER_API}


def visualcrossing_api(request):
    return {'VISUALCROSSING_API': settings.VISUALCROSSING_API}