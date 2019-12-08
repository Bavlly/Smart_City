from django.shortcuts import render
from .models import RFIDChipReader
from .serializer import RFIDSerializer
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


def index(request): #path('', include(dashboard.urls)
    alldata_sensor = RFIDChipReader.objects.all()  # this value gets all of the data out off the database
    curr_datetime = datetime.now()
    curr_date = curr_datetime.date()
    current_data_sensor = RFIDChipReader.objects.filter(created_at__date=curr_date)
    return render(request, "index.html", {'alldata_sensor': alldata_sensor, 'current_data_sensor': current_data_sensor}) #return the request of index.html


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
