import os
import json
import pandas

from django.http import HttpResponse
from django.shortcuts import render

from .form import UploadFileForm
from .models import IncomingFile, Patient


def init_valid_data_from_file():
    df = pandas.read_excel(os.path.join(os.path.dirname(__file__), r'valid_data\ValidData.xlsx'))[
        ['Sex', 'Status', 'Hospitalization Status', 'Ward list', 'Sample Result', 'Testing Labs']]
    return df


def index(request):
    try:
        os.remove(os.path.join(os.path.dirname(__file__), r'incoming\IncomingData.xlsx'))
    finally:
        return render(request, 'validate_data/upload.html', {'form': UploadFileForm()})


def filter_valid_data_from_file():
    check_dict = {
        3: 'Sex',
        4: 'Status',
        5: 'Hospitalization Status',
        6: 'Ward list',
        7: 'Sample Result',
        8: 'Testing Labs'
    }
    error_dict = {}

    valid_data = init_valid_data_from_file()
    df = pandas.read_excel(
        os.path.join(os.path.dirname(__file__), r'incoming\IncomingData.xlsx'))
    for item in df.iterrows():
        for i in range(len(df.columns)):
            try:
                if item[1][i] not in list(valid_data[check_dict[i]]) or item[1][i] != item[1][i]:
                    if item[1][i] != item[1][i]:
                        item[1][i] = '!Empty Cell!'
                    if item[1][1] not in error_dict:  # name is chosen as key for simplicity, make item[1][0] for Sr.No.
                        error_dict[item[1][1]] = {}
                    error_dict[item[1][1]][df.columns[i]] = item[1][i]
            except KeyError:
                ...

        if item[1][1] not in error_dict:
            if Patient.objects.filter(sr_no=int(item[1][0])).first() is None:
                patient = Patient()
                patient.sr_no = item[1][0]
                patient.name = item[1][1]
                patient.age = item[1][2]
                patient.sex = item[1][3]
                patient.patient_status = item[1][4]
                patient.hospitalization_status = item[1][5]
                patient.ward = item[1][6]
                patient.sample_result = item[1][7]
                patient.testing_lab = item[1][8]
                patient.save()
    return error_dict


def check_data(request):
    if request.method == 'POST':
        file = IncomingFile()
        file.file = request.FILES['file']
        file.save()
        error_dict = json.dumps(filter_valid_data_from_file())
        return HttpResponse(error_dict)
