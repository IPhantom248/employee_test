from django.shortcuts import render


def get_all_employees(request):
    return render(request, 'home.html', {})
