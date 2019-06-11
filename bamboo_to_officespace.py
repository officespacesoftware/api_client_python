#!/usr/bin/python
import requests
import json
import math
import sys

#####################
# Bamboo API Config #
#####################

Site = "<YOUR_BAMBOO_INSTANCE>"
Key = "<YOUR_BAMBOO_API_KEY>"
Auth = (Key, 'x')
Headers = {"Accept": "application/json"}
BaseUrl = "https://api.bamboohr.com/api/gateway.php/%s/v1/" % (Site)
EmployeeDirectory = "employees/directory"


##########################
# OfficeSpace API Config #
##########################
Hostname = "<YOUR_OFFICESPACE_SUBDOMAIN>.officespacesoftware.com"
Token = "<YOUR_OFFICESPACE_API_KEY>"
BatchUrl = "/api/1/employee_batch_imports"
ImportUrl = "/api/1/employee_directory"
Protocol = "https://"
Headers = {'Authorization': "Token token=%s" % Token}
JsonHeaders = {'Authorization': "Token token=%s" % Token, 'Content-Type': 'application/json; charset=utf-8'}
Source = "BambooHR"
EmployeeBatchUrl  = Protocol + Hostname + BatchUrl
EmployeeBatchStagingUrl  = Protocol + Hostname + ImportUrl + "/" + Source
EmployeeImportUrl  = Protocol + Hostname + ImportUrl
BatchSize = 1000
##########################

Response = requests.get(BaseUrl + EmployeeDirectory, auth=Auth, headers=Headers)

if Response.status_code == 200:
    Data = json.loads(Response.text)
    print("Got %d employees from Bamboo" % (len(Data['employees'])))

    # OfficeSpace to BambooHR mapping
    EmployeeId = "id"
    FirstName = "firstName"
    LastName = "lastName"
    Title = "jobTitle"
    WorkPhone = "workPhone"
    Extension = "workPhoneExtension"
    Photo = "photoUrl"
    Department = "department"
    Bio = ""
    Email = "workEmail"
    StartDate = ""
    EndDate = ""
    ShowInVd = ""
    Udf0 = "location"
    Udf1 = "division"
    Udf2 = "mobilePhone"
    Udf3 = "preferredName"
    Udf4 = ""
    Udf5 = ""
    Udf6 = ""
    Udf7 = ""
    Udf8 = ""
    Udf9 = ""
    Udf10 = ""
    Udf11 = ""
    Udf12 = ""
    Udf13 = ""
    Udf14 = ""
    Udf15 = ""
    Udf16 = ""
    Udf17 = ""
    Udf18 = ""
    Udf19 = ""
    Udf20 = ""
    Udf21 = ""
    Udf22 = ""
    Udf23 = ""
    Udf24 = ""

    BambooEmployees = Data['employees']

    Batches = math.floor(len(BambooEmployees)/BatchSize) + 1
    Start = 0
    End = BatchSize - 1
    Batch = 1

    print("Staging records in OfficeSpace...")
    try:
        Response = requests.delete(EmployeeBatchStagingUrl, headers=JsonHeaders)
    except Exception, e:
        print("Delete Staging Records Error: %s" % str(e))
    else:
        Array = []

        while True:
            for BambooEmployee in BambooEmployees[Start:End]:
                Person = {}
                Person["EmployeeId"] = BambooEmployee[EmployeeId] if BambooEmployee.has_key(EmployeeId) else ''
                Person["Source"] = Source
                Person["FirstName"] = BambooEmployee[FirstName] if BambooEmployee.has_key(FirstName) else ''
                Person["LastName"] = BambooEmployee[LastName] if BambooEmployee.has_key(LastName) else ''
                Person["Title"] = BambooEmployee[Title] if BambooEmployee.has_key(Title) else ''
                Person["WorkPhone"] = BambooEmployee[WorkPhone] if BambooEmployee.has_key(WorkPhone) else ''
                Person["Extension"] = BambooEmployee[Extension] if BambooEmployee.has_key(Extension) else ''
                Person["Photo"] = BambooEmployee[Photo] if BambooEmployee.has_key(Photo) else ''
                Person["Department"] = BambooEmployee[Department] if BambooEmployee.has_key(Department) else ''
                Person["Bio"] = BambooEmployee[Bio] if BambooEmployee.has_key(Bio) else ''
                Person["Email"] = BambooEmployee[Email] if BambooEmployee.has_key(Email) else ''
                Person["StartDate"] = BambooEmployee[StartDate] if BambooEmployee.has_key(StartDate) else ''
                Person["EndDate"] = BambooEmployee[EndDate] if BambooEmployee.has_key(EndDate) else ''
                Person["ShowInVd"] = BambooEmployee[ShowInVd] if BambooEmployee.has_key(ShowInVd) else ''
                Person["Udf0"] = BambooEmployee[Udf0] if BambooEmployee.has_key(Udf0) else ''
                Person["Udf1"] = BambooEmployee[Udf1] if BambooEmployee.has_key(Udf1) else ''
                Person["Udf2"] = BambooEmployee[Udf2] if BambooEmployee.has_key(Udf2) else ''
                Person["Udf3"] = BambooEmployee[Udf3] if BambooEmployee.has_key(Udf3) else ''
                Person["Udf4"] = BambooEmployee[Udf4] if BambooEmployee.has_key(Udf4) else ''
                Person["Udf5"] = BambooEmployee[Udf5] if BambooEmployee.has_key(Udf5) else ''
                Person["Udf6"] = BambooEmployee[Udf6] if BambooEmployee.has_key(Udf6) else ''
                Person["Udf7"] = BambooEmployee[Udf7] if BambooEmployee.has_key(Udf7) else ''
                Person["Udf8"] = BambooEmployee[Udf8] if BambooEmployee.has_key(Udf8) else ''
                Person["Udf9"] = BambooEmployee[Udf9] if BambooEmployee.has_key(Udf9) else ''
                Person["Udf10"] = BambooEmployee[Udf10] if BambooEmployee.has_key(Udf10) else ''
                Person["Udf11"] = BambooEmployee[Udf11] if BambooEmployee.has_key(Udf11) else ''
                Person["Udf12"] = BambooEmployee[Udf12] if BambooEmployee.has_key(Udf12) else ''
                Person["Udf13"] = BambooEmployee[Udf13] if BambooEmployee.has_key(Udf13) else ''
                Person["Udf14"] = BambooEmployee[Udf14] if BambooEmployee.has_key(Udf14) else ''
                Person["Udf15"] = BambooEmployee[Udf15] if BambooEmployee.has_key(Udf15) else ''
                Person["Udf16"] = BambooEmployee[Udf16] if BambooEmployee.has_key(Udf16) else ''
                Person["Udf17"] = BambooEmployee[Udf17] if BambooEmployee.has_key(Udf17) else ''
                Person["Udf18"] = BambooEmployee[Udf18] if BambooEmployee.has_key(Udf18) else ''
                Person["Udf19"] = BambooEmployee[Udf19] if BambooEmployee.has_key(Udf19) else ''
                Person["Udf20"] = BambooEmployee[Udf20] if BambooEmployee.has_key(Udf20) else ''
                Person["Udf21"] = BambooEmployee[Udf21] if BambooEmployee.has_key(Udf21) else ''
                Person["Udf22"] = BambooEmployee[Udf22] if BambooEmployee.has_key(Udf22) else ''
                Person["Udf23"] = BambooEmployee[Udf23] if BambooEmployee.has_key(Udf23) else ''
                Person["Udf24"] = BambooEmployee[Udf24] if BambooEmployee.has_key(Udf24) else ''
                Array.append(Person)
            JSONArray = json.dumps(Array)
            JSONArrayUTF8 = JSONArray.encode()
            #print(JSONArrayUTF8)
            #print("")
            try:
                Response = requests.post(EmployeeBatchUrl, data=JSONArrayUTF8, headers=JsonHeaders)
            except Exception, e:
                print("Batch No. %d Update Records Error: %s" % (Batch, str(e)))
                sys.exit(1)
            else:
                Start+=BatchSize
                End+=BatchSize
                Batch=Batch+1
            if (Batch >= Batches):
                break
    print("Triggering migration")
    ImportUrlPostBody = '{ "Source" :  "' + Source + '" }'
    print(ImportUrlPostBody)
    try:
        Response = requests.post(EmployeeImportUrl, data=ImportUrlPostBody, headers=Headers)
    except Exception, e:
        print("Trigger Migration Error: %s" % str(e))
    else:
        print("Completed")
else:
    print("Error %s for request %s" % (str(Response.status_code), BaseUrl + EmployeeDirectory))
