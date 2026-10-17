from django.shortcuts import render

# Dashboard main page
def main_dashboard(request):

    return render(request, "dashboard/main_dashboard.html")
