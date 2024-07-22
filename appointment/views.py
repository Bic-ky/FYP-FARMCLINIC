from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from account.models import User
from appointment.models import Expert

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm

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


def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.farmer = request.user  # Set the logged-in user as the farmer
            appointment.save()
            messages.success(request, 'Appointment booked successfully')
            return redirect('account:myAccount')  # Redirect to a success page or another view
        else:
            messages.error(request, 'Error booking appointment')
    else:
        form = AppointmentForm()

    context = {
        'form': form,
    }
    return render(request, 'appointment.html', context)



def appointment_date(request):
    appointments = Appointment.objects.all()[:5]
    print(appointments)

    context = {
        'appointments' : appointments ,
    }

    
    return render(request, "experts/appoint_date.html" , context)


def appointment_list(request):
    appointments = Appointment.objects.all()
    data = []
    for appointment in appointments:
        data.append({
            'title': f"Appointment with {appointment.expert.user.full_name}",
            'start': appointment.sent_date.isoformat(),
            'end': appointment.sent_date.isoformat(),  # Assuming it is a one-day event
            'allDay': True,
        })
    return JsonResponse(data, safe=False)