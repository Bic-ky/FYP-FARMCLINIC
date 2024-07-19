from django.http import Http404
from django.shortcuts import get_object_or_404, render

from account.models import User
from appointment.models import Expert

# Create your views here.

def experts(request):
    experts = Expert.objects.all()
    
    for expert in experts:
        print(expert.user.full_name)
        print(expert.user.user_profile.profile_picture.url)

    context = {
        'experts': experts,
    }
    return render(request, 'experts/experts.html', context)




def expert_detail(request):
    try:
        expert = Expert.objects.all()
    except Expert.DoesNotExist:
        raise Http404("Expert does not exist")

    context = {
        'expert': expert,
    }
    return render(request, 'experts/expert_details.html', context)