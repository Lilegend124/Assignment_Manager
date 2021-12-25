from assignments import models
import json
from urllib.request import urlopen
import datetime


def main(num_classes = None, testing=False):
    url = "https://api.devhub.virginia.edu/v1/courses"
    response = urlopen(url)
    raw_data =json.loads(response.read())
    data = []
    for x in raw_data['class_schedules']['records']: #remove 1:10 for all classes
        data.append(x)
    if num_classes != None:
        data = data[:num_classes]
    for class_idx in range(len(data)):
        startTime = datetime.datetime.strptime(data[class_idx][9], '%H:%M:%S').time()
        endTime = datetime.datetime.strptime(data[class_idx][10], '%H:%M:%S').time()
        if testing==True or 'CS' in data[class_idx][0]:
            modelTest = models.Class_Item.objects.create(class_title=data[class_idx][4], meeting_days=data[class_idx][8], meeting_time_start=startTime, meeting_time_end=endTime,
                                                         mnemonic=data[class_idx][0], class_number=data[class_idx][1], prof=data[class_idx][6],
                                                         semester=data[class_idx][12])
