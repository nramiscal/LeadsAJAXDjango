from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
import datetime


def index(request):
    leads = Leads.objects.all()
    return render(request, 'index.html', {'leads':leads})


@csrf_exempt
def search(request):
    print("*"*100)
    print("INSIDE SEARCH METHOD IN VIEWS")
    print("Receiving from data:", request.POST)

    # set search_string variable
    if not request.POST['name']:
        search_string = ""
    else:
        search_string = request.POST['name']


    # set start_date variable
    if not request.POST['date_from']:
        start_date = Leads.objects.first().created_at
    else:
        date_from = request.POST['date_from']
        print("DATE_FROM", date_from)

        start = str(date_from).split("-")
        print("START", start)

        start_year = start[0]
        start_month = start[1]
        start_day = start[2]

        start_date = datetime.date(int(start_year), int(start_month), int(start_day))


    # set end_date variable
    if not request.POST['date_to']:
        end_date = datetime.datetime.now()
    else:
        date_to = request.POST['date_to']
        print("DATE_TO", date_to)

        end = str(date_to).split("-")
        print("END", end)

        end_year = end[0]
        end_month = end[1]
        end_day = end[2]

        end_date = datetime.date(int(end_year), int(end_month), int(end_day))

    # generate leads list
    leads1 = Leads.objects.filter(created_at__range=(start_date, end_date)).filter(fname__startswith=search_string)
    leads2 = Leads.objects.filter(created_at__range=(start_date, end_date)).filter(lname__startswith=search_string)
    
    leads = leads1 | leads2
    print("Sending through context:", leads)

    print("*"*100)
    return render(request, 'table.html', {'leads':leads})
