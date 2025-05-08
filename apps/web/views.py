from django.shortcuts import render, redirect
import requests

def create_shipment(request):
    if request.method == 'POST':
        # Preparar los datos del formulario
        data = {
            'sender': request.POST.get('sender'),
            'recipient': request.POST.get('recipient'),
            'phone': request.POST.get('phone'),
        }
        
        # Realizar la petición POST a la API
        response = requests.post('http://localhost:8000/api/v1/shipments/', data=data)
        
        if response.status_code == 201:
            return redirect('shipment_success')
        
    # Si es GET o si hubo error, mostrar el formulario
    return render(request, 'pages/shipment.html')