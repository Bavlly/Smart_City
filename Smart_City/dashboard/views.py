from django.shortcuts import render
from .models import RfidChipReader
from .serializer import SensorsSerializer
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


def index(request): #path('', include(dashboard.urls)
    alldata_sensor = RfidChipReader.objects.all()# this value gets all of the data out off the database
    curr_datetime = datetime.now()
    curr_date = curr_datetime.date()
    current_date = RfidChipReader.objects.dates('created_at', 'day')
    authorised_true = RfidChipReader.objects.filter(authorised=True)
    authorised_false = RfidChipReader.objects.filter(authorised=False)
    if not request.GET:
        curr_datetime = datetime.now()
        curr_date = curr_datetime.date()
        time_diff = timedelta(days=-1)
        req_date_time = curr_date + time_diff

        date = RfidChipReader.objects.filter(created_at__date=curr_date)


    else:
        input_date = request.GET['date']
        date = RfidChipReader.objects.filter(created_at__date=input_date)

    current_data_sensor = RfidChipReader.objects.filter(created_at__date=curr_date)
    data = {
        'alldata_sensor': alldata_sensor,
        'current_data_sensor': current_data_sensor,
        "authorised_true": authorised_true,
        'authorised_false': authorised_false,
        "current_date": current_date,
        "date": date,
    }

    return render(request, "index.html", data) #return the request of index.html


# Create your views here.
@api_view(['GET'])
def sensorList(request):
    sensor = RfidChipReader.objects.all()
    serializer = SensorsSerializer(sensor, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
def sensorDetail(request, pk):
    try:
        pk = RfidChipReader.objects.get(pk=pk)
    except RfidChipReader.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SensorsSerializer(pk)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SensorsSerializer(pk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sensorPost(request):
    if request.method == 'POST':
        serializer = SensorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
