from django.shortcuts import render

# Create your views here.
def modbus(request):
    return render(
        request,
        'modbus/modbus.html'
    )