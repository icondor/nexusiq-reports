import sys
import os
import os.path
import csv
from applib import nexusiq, fileIO, util

iqHost = sys.argv[1]
iqUser = sys.argv[2]
iqPwd = sys.argv[3]

iq = nexusiq.NexusIQData(iqHost, iqUser, iqPwd)

outputDir = fileIO.outputDir
workdir = fileIO.licenceWorkdir

appReportsUrlsCsvFile = fileIO.appReportsUrlsCsvFile
licenseOverridesCsvFile = fileIO.licenseOverridesCsvFile


def getLicenseOverrides():

  with open(licenseOverridesCsvFile, 'w') as fd:
    fd.write('Service Name, Component Name, Version, Licence Name\n')
    fd.close()

  with open(appReportsUrlsCsvFile) as csvfile:
    r = csv.reader(csvfile, delimiter=',')
    for row in r:
      applicationName = row[0]
      url = row[2]

      statusCode, policyReportData = iq.getData('/' + url)

      if statusCode == 200:

        components = policyReportData["components"]
        count=0;
        with open(licenseOverridesCsvFile, 'a') as fd:
          for component in components:


            licenseData = component["licenseData"]
            if not licenseData:
              continue


            #exclude Sdl. packages, they are not relevant for licences
            packageUrl = component["packageUrl"]
            if packageUrl.find("Sdl.") != -1:
              continue

            status = component["licenseData"]["status"]
            libName= component["componentIdentifier"]["coordinates"].get("artifactId", "");
            if not libName:
              libName= component["componentIdentifier"]["coordinates"].get("packageId", "");
            if not libName:
              libName= component["componentIdentifier"]["coordinates"].get("name", "");



            libVersion= component["componentIdentifier"]["coordinates"]["version"]

            effectiveLicencesName = component["licenseData"]["effectiveLicenses"][0]["licenseName"]

            if effectiveLicencesName.find("No Source License") == -1:
              effectiveLicencesName = component["licenseData"]["declaredLicenses"][0]["licenseName"]
              count=count+1




            line = applicationName + "," + libName + "," + libVersion + "," + effectiveLicencesName + "\n"
            fd.write(line)
      
            lic_json = workdir + "/" + applicationName + ".json"
            fileIO.writeJsonFile(lic_json, policyReportData)

  print(licenseOverridesCsvFile)
  print(count)
  return


def main():

  getLicenseOverrides()


if __name__ == '__main__':
  main()
