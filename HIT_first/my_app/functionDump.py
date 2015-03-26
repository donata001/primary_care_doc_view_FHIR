import urllib2, string, json

def get_patient_conditions_by_id(*args):
    # first argument is pid
    # (optional) second argument is count on number of conditions to return
    if len(args)==1:
        id = args[0]
        urlstring = 'https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Condition?_format=json&subject.reference=Patient/'+id+'&_count=20'
        response = urllib2.urlopen(urlstring)
    elif len(args) == 2:
        id = args[0]
        count = args[1]
        urlstring = 'https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Condition?_format=json&subject.reference=Patient/'+id+'&_count='+count
        response = urllib2.urlopen(urlstring)
    # else:
        # handle error
    data = json.loads(response.read())
    conditions = []
    dict = {}
    for field in data['entry']: #condition, system, code, status, onsetDate
        # print field
        status = field['content']['status']
        if u'dateAsserted' in field['content'].keys():
            dateAsserted = field['content']['dateAsserted']
        else:
            dateAsserted = 'N/A'
        code = field['content']['code']['coding'][0]['code']
        system = field['content']['code']['coding'][0]['system']
        display = field['content']['code']['coding'][0]['display']
        if u'onsetDate' in field['content'].values():
            onsetDate = field['content']['onsetDate']
        else:
            onsetDate = 'N/A'
        dict = {"display": display, "system": system, "code": code, "status": status, "onsetDate": onsetDate}
        conditions.append(dict)
    # print conditions
    return conditions

def get_patient_medications_by_id(*args):
    # first argument is pid
    # (optional) second argument is count on number of conditions to return
    if len(args)==1:
        id = args[0]
        urlstring = 'https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/MedicationPrescription?_format=json&subject.reference=Patient/'+id+'&_count=20'
        response = urllib2.urlopen(urlstring)
    elif len(args) == 2:
        id = args[0]
        count = args[1]
        urlstring = 'https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/MedicationPrescription?_format=json&subject.reference=Patient/'+id+'&_count='+count
        response = urllib2.urlopen(urlstring)
    # else:
        # handle error
    data = json.loads(response.read())
    medications = []
    dict = {}
    for field in data['entry']: #condition, system, code, status, onsetDate
        # print field
        status = field['content']['status']
        medication = field['content']['medication']['display']
        dateWritten = field['content']['dateWritten']
        prescriber = field['content']['prescriber']['display']
        quantity = field['content']['dispense']['quantity']['value']
        code = field['content']['contained'][0]['code']['coding'][0]['code']#['coding']#['code']
        system = field['content']['contained'][0]['code']['coding'][0]['system']
        doseQuantity = field['content']['dosageInstruction'][0]['doseQuantity']
        dict = {"display": medication, "system": system, "code": code, "status": status, "quantity": quantity, "doseQuantity": doseQuantity, "prescriber": prescriber, "dateWritten": dateWritten}
        medications.append(dict)
    # print medications
    return medications

def get_patient_observations_by_id(*args):
    # first argument is pid
    # (optional) second argument is count on number of conditions to return
    if len(args)==1:
        id = args[0]
        urlstring = 'https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Observation?_format=json&subject.reference=Patient/'+id+'&_count=50'
        response = urllib2.urlopen(urlstring)
    elif len(args) == 2:
        id = args[0]
        count = args[1]
        urlstring = 'https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Observation?_format=json&subject.reference=Patient/'+id+'&_count='+count
        response = urllib2.urlopen(urlstring)
    # else:
        # handle error
    data = json.loads(response.read())
    observations = []
    dict = {}
    for field in data['entry']: #condition, system, code, status, onsetDate
        # print field
        status = field['content']['status']
        # print field['content']['name']['coding'][0].keys()
        if u'display' in field['content']['name']['coding'][0].keys():
            display = field['content']['name']['coding'][0]['display']
        else:
            display = 'N/A'

        if u'system' in field['content']['name']['coding'][0].keys():
            system = field['content']['name']['coding'][0]['system']
        else:
            system = 'N/A'

        if u'code' in field['content']['name']['coding'][0].keys():
            code = field['content']['name']['coding'][0]['code']
        else:
            code = 'N/A'

        if u'valueQuantity' in field['content'].keys():
            valueQuantity = field['content']['valueQuantity']
        else:
            valueQuantity = 'N/A'

        # print field['content'].keys()
        if u'appliesDateTime' in field['content'].keys():
            appliesDateTime = field['content']['appliesDateTime']
        else:
            appliesDateTime = 'N/A'
        dict = {"display": display, "system": system, "code": code, "status": status, "valueQuantity": valueQuantity, "appliesDateTime": appliesDateTime}
        observations.append(dict)
    # print observations
    return observations