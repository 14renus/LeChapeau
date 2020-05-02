from django.shortcuts import render

# Create your views here.
def create_room(request):
    return render(request, 'startup.html', {})


