from django.shortcuts import render
from .models import RfidChipReader
from .serializer import SensorsSerializer
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


def index(request): #path('', include(dashboard.urls)
    alldata_sensor = RfidChipReader.objects.all()  # this value gets all of the data out off the database
    curr_datetime = datetime.now()
    curr_date = curr_datetime.date()
    current_data_sensor = RfidChipReader.objects.filter(created_at__date=curr_date)
    return render(request, "index.html", {'alldata_sensor': alldata_sensor, 'current_data_sensor': current_data_sensor}) #return the request of index.html


# Create your views here.
@api_view(['GET'])
def sensorList(request):
    sensor = RfidChipReader.objects.all()
    serializer = SensorsSerializer(sensor, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
def sensorDetail(request, pk):
    try:
        sensor_id = RfidChipReader.objects.get(pk=pk)
    except RfidChipReader.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SensorsSerializer(sensor_id)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SensorsSerializer(sensor_id, data=request.data)
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
