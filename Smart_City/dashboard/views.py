from django.shortcuts import render
from .models import RFIDChipReader
from .serializer import RFIDSerializer
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


def index(request): #path('', include(dashboard.urls)
    alldata_sensor = RFIDChipReader.objects.all()# this value gets all of the data out off the database
    curr_datetime = datetime.now()
    curr_date = curr_datetime.date()
    current_date = RFIDChipReader.objects.dates('created_at', 'day')
    authorised_true = RFIDChipReader.objects.filter(authorised=True)
    authorised_false = RFIDChipReader.objects.filter(authorised=False)
    if not request.GET:
        curr_datetime = datetime.now()
        curr_date = curr_datetime.date()
        time_diff = timedelta(days=-1)
        req_date_time = curr_date + time_diff

        date = RFIDChipReader.objects.filter(created_at__date=curr_date)


    else:
        input_date = request.GET['date']
        date = RFIDChipReader.objects.filter(created_at__date=input_date)

    current_data_sensor = RFIDChipReader.objects.filter(created_at__date=curr_date)
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
def RFIDList(request):
    sensor = RFIDChipReader.objects.all()
    serializer = RFIDSerializer(sensor, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
def RFIDDetail(request, pk):
    try:
        sensor_id = RFIDChipReader.objects.get(pk=pk)
    except RFIDChipReader.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RFIDSerializer(sensor_id)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RFIDSerializer(sensor_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def RFIDPost(request):
    if request.method == 'POST':
        serializer = RFIDSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
