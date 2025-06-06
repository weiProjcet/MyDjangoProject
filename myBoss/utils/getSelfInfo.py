from .getPublicData import *


def getPageData():
    jobs = getAllJobs()
    jobsType = []
    for job in jobs:
        if job.type not in jobsType:
            jobsType.append(job.type)
    return list(educations.keys()), workExperience, jobsType
