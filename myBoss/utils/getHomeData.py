from myBoss.models import User, JobInfo
from .getPublicData import *
import time
import json


def getNowTime():
    timeFormat = time.localtime()
    year = timeFormat.tm_year
    month = timeFormat.tm_mon
    day = timeFormat.tm_mday
    monthList = ['January', 'Februry', 'Marth', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                 'November', 'December']
    return year, monthList[month - 1], day


def getTagData():
    jobs = getAllJobs()
    educationsTop = "学历不限"
    salaryTop = 0
    salaryMonthTop = 0
    address = {}
    pratice = {}
    for job in jobs:
        if educations[job.educational] < educations[educationsTop]:
            educationsTop = job.educational
        if not job.pratice:
            salary = json.loads(job.salary)[1]
            if salaryTop < salary:
                salaryTop = salary
        if int(job.salaryMonth) > salaryMonthTop:
            salaryMonthTop = int(job.salaryMonth)
        if address.get(job.address, -1) == -1:
            address[job.address] = 1
        else:
            address[job.address] += 1
        if pratice.get(job.pratice, -1) == -1:
            pratice[job.pratice] = 1
        else:
            address[job.address] += 1
    addressStr = sorted(address.items(), key=lambda x: x[1], reverse=True)[:3]
    addressTop = ""
    for i in addressStr:
        addressTop += i[0] + ","
    praticeMax = sorted(pratice.items(), key=lambda x: x[1], reverse=True)
    # a = "普通岗位" ? praticeMax[0][0] == False : "实习岗位"
    return len(jobs), educationsTop, salaryTop, salaryMonthTop, addressTop, praticeMax[0][0]


def getTableData():
    jobs = getAllJobs().order_by('id')
    for i in jobs:
        i.workTag = '/'.join(json.loads(i.workTag))
        if i.companyTags != "无":
            i.companyTags = str(json.loads(i.companyTags)[0].split('，')[:5])
        if i.companyPeople == '[0, 10000]':
            i.companyPeople = '10000人以上'
        else:
            i.companyPeople = json.loads(i.companyPeople)
            i.companyPeople = list(map(lambda x: str(x) + '人', i.companyPeople))
            i.companyPeople = '-'.join(i.companyPeople)
        i.salary = json.loads(i.salary)[1]
    return jobs
