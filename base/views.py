from django.shortcuts import render


def mi_vista(request):
    return render(request, 'principio.html')
def mi_vista2(request):
    return render(request, 'inicio.html')
