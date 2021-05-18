import sys
import os
import os.path
import csv
from applib import nexusiq, fileIO, util

iqHost = sys.argv[1]
iqUser = sys.argv[2]
iqPwd = sys.argv[3]

iq = nexusiq.NexusIQData(iqHost, iqUser, iqPwd)

appReportsJsonFile = fileIO.appReportsJsonFile
appReportsUrlsCsvFile = fileIO.appReportsUrlsCsvFile
reportsDb = []


def getApplicationEvaluationReports():
  statusCode, applicationEvaluations = iq.getData('/api/v2/reports/applications')

  print(statusCode)
  if statusCode == 200:
    fileIO.writeJsonFile(appReportsJsonFile, applicationEvaluations)
    print(appReportsJsonFile)
    
    for applicationEvaluation in applicationEvaluations:
      applicationId = applicationEvaluation["applicationId"]

      applicationName = util.getApplicationName(applicationEvaluation["reportDataUrl"])
      applicationReportUrl = applicationEvaluation["reportDataUrl"]
      stage = applicationEvaluation["stage"]

      line = applicationName + "," + applicationId + "," + applicationReportUrl + "," + stage + "\n"
      reportsDb.append(line)

  fileIO.writeCSVFile(appReportsUrlsCsvFile, "", reportsDb)

  print(appReportsUrlsCsvFile)
  return 


def main():
  getApplicationEvaluationReports()


if __name__ == '__main__':
  main()
