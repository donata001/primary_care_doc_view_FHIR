#MY IMPORTS
import urllib2, string
import json
from itertools import islice
from random import randint


# Create your views here.

from django.shortcuts import render_to_response, RequestContext, HttpResponse, Http404, render
import datetime
from django.template import Template, Context
from my_app.models import Publisher

from DataDump import *
from functionDump import *

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from my_app.serializers import PublisherSerializer
# Create your views here.


#############HIT Functions

def getPatientByID(pid, name):
    temp_dict = getDummyDataByID(pid)
    return temp_dict
    
    
    patient_dict = {}
    
    obs = get_patient_observations_by_id(pid)
    cond = get_patient_conditions_by_id(pid)
    med = get_patient_medications_by_id(pid)

    dict = {"pid": pid, "name": name, "conditions": cond, "observations": obs, "medications": med}      
    patient_dict[pid] = dict
    
    return patient_dict


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def getPatients(count):
    
    final_dict = getDummyData()
    return take(count, final_dict.iteritems()) 


    
    final_dict = {}
    patient_dict = {}
    # print count

    # dict = {}
    # print len(dict)
    current_url = "https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Patient?_format=json"
    
    
    while (len(patient_dict)<count):
        
        # headers = response.info()
        response = urllib2.urlopen(current_url)
        data = json.loads( response.read() )
        
        
        next_url = data['link'][1]['href']
        #print data['link'][1]['rel']
        
        for field in data['entry']:
            # print field
            first_name = field['content']['name'][0]['given'][0]
            last_name = field['content']['name'][0]['family'][0]
            name = first_name + " "  + last_name
                        
            pid = field['content']['identifier'][0]['value']
            
            # print len(dict)
            if (len(patient_dict)<count):
                
                obs = get_patient_observations_by_id(pid)
                cond = get_patient_conditions_by_id(pid)
                med = get_patient_medications_by_id(pid)

                dict = {"pid": pid, "name": name, "conditions": cond, "observations": obs, "medications": med}
                # print obs[0]
                # print dict
                # dict[name] = pid
                patient_dict[pid] = dict
                # print patientlist
                # print ("Name: " + name + ", PID: " + pid )

        
        
        current_url = next_url
        
        
    return take(count, patient_dict.iteritems()) 

def appendtoDict (patients_dict):
    print patients_dict
    
    reason_dictionary_list = [{'reason': "General Checkup", 'color': "green"},
                              {'reason': "Follow-up", 'color': "yellow"},
                              {'reason': "Consultation", 'color': "aqua"},
                              {'reason': "Urgent Visit", 'color': "red"},
                              {'reason': "Work Related", 'color': "purple"}
                              ]

    return_dict = {}
    #Meeting Tme Stuff
    now = datetime.datetime.now()
    i=0
    for k, patient_dict in patients_dict:
        temp_dict = patient_dict

        random_no = randint(0,len(reason_dictionary_list)-1)
        temp_dict['reason'] = reason_dictionary_list[random_no]['reason']
        temp_dict['color'] = reason_dictionary_list[random_no]['color']
        temp_dict['meeting_time'] = now + datetime.timedelta(minutes = i*15)
        i+=1
        
        return_dict[k] = temp_dict
     
    return return_dict 
##########################








#############HIT VIEWS

def PCPView(request):
    final_dict = {}
    
    patients_dict = appendtoDict( getPatients(10) )
    final_dict['patients_dict'] = patients_dict
    
    
    
    return render(request, 'Admin-master/HIT_pages/pcpview.html', final_dict)



def PatientView(request):
    
    requested_pid = request.GET['pid']
    requested_name = request.GET['name']
    
    #patient_dict = appendtoDict( getPatientByID(requested_pid, requested_name) )
    patient_dict = ( getPatientByID(requested_pid, requested_name) )
    
    print patient_dict[requested_pid]
    final_dict = {}
    final_dict['patient_dict'] = patient_dict[requested_pid]
    
    
    
    
    return render(request, 'Admin-master/HIT_pages/patientview.html', final_dict)


##########################

PCP_TEMPLATE = 'Admin-master/pcp_view.html'

from django.views.decorators.csrf import csrf_exempt


class PCPViewPage(View):
    def get(self, request):
        pid = u'3.666867671-01'
        name = patient_dict[pid]['name']
        conditions = patient_dict[pid].get('conditions')
        if conditions:
            con_list = [_['display'] for _ in conditions]
        name_list, dose_list, date_list = fetch_data(pid, 'medication')
        matrix_list, date_list2, value_list2 = fetch_data(pid, 'vital')

        context = {'name_list': name_list,
                  'dose_list': dose_list,
                  'date_list': date_list,
                  'matrix_list': matrix_list,
                  'date_list2': date_list2,
                  'pid': pid,
                  'name': name,
                  'con_list': con_list
                  }
        rmap = {}
        for idx, m in enumerate(matrix_list[::-1]):
            if m not in rmap:
                rmap[m] = idx

        show_case = []
        for _, idx in rmap.iteritems():
            show_case.append([matrix_list[::-1][idx], value_list2[::-1][idx],
                              date_list2[::-1][idx]])
        context['show_case'] = show_case
        return render(request, PCP_TEMPLATE, context)


@csrf_exempt
def lookup(request):
    data = request.POST or {}
    pid = data.get('patientid', '')
    data_type = data.get('data_type', '')
    cmap = fetch_data(pid, data_type)
    key = data.get('key', '')
    val = cmap.get(key)
    return HttpResponse(json.dumps({"ok":1, "x":val[0], 'y':val[1], 'title': key}))


def fetch_data(pid, data_type):
    if not pid or not pid in patient_dict:
        return None
    date_pat = re.compile(r'(?P<date>.*)T', re.UNICODE | re.IGNORECASE)
    if data_type in ['medication', 'mmap']:
        medication_list = patient_dict[pid]['medications']
        name_list = []
        med_list = []
        for i in xrange(len(medication_list)):
            name = medication_list[i]['display'].encode('utf-8')
            if name not in name_list:
                name_list.append(name)
            if name_list and name == name_list[0]:
                # don't know how ML will work, so med1 point to condition1 and med2 point to cond2
                dose_list = [_['doseQuantity'][u'value'] for _ in medication_list]
                date_list = [date_pat.search(_['dateWritten']).group('date').encode('utf-8') for _ in medication_list]
            med_list.append(name)
        if data_type == 'medication':
            return name_list, dose_list, date_list
        else:
            mmap = {}
            for idx, m in enumerate(med_list[::-1]):
                if m not in mmap:
                    mmap[m] = [[dose_list[idx]],
                                [date_list[idx]]]
                else:
                    mmap[m][0].append(dose_list[idx])
                    mmap[m][1].append(date_list[idx])
            return mmap
    elif data_type in ['vital', 'cmap']:
        ob_list = patient_dict[pid]['observations']
        matrix_list = [_['display'].encode('utf-8') for _ in ob_list]
        value_list1 = [_['valueQuantity'][u'value'] for _ in ob_list]
        unit_list = []
        for x in ob_list:
            if x['valueQuantity'].get(u'units'):
                unit_list.append(x['valueQuantity'][u'units'])
            else:
                unit_list.append('')
        value_list2 = [str(x) + y.encode('utf-8') for x, y in zip(value_list1, unit_list)]
        date_list2 = [date_pat.search(_['appliesDateTime']).group('date').encode('utf-8') for _ in ob_list]
        if data_type == 'vital':
            return matrix_list, date_list2, value_list2
        else:
            cmap = {}
            for idx, m in enumerate(matrix_list[::-1]):
                if m not in cmap:
                    cmap[m] = [[value_list1[idx]],
                                [date_list2[idx]]]
                else:
                    cmap[m][0].append(value_list1[idx])
                    cmap[m][1].append(date_list2[idx])

            return cmap
















































def my_view(request, offset, offset2):
    #return render_to_response('index.html', locals(), context_instance=RequestContext(request))
    
#     try:
#         print offset
#         print offset2
#     except ValueError:
#         raise Http404()
#     dt = datetime.datetime.now() + datetime.timedelta(hours=int(offset))
#     #assert False
#     html = "<html><body>It is now %s.</body></html>" %datetime.datetime.now()
#     return HttpResponse(html + offset + offset2 + str(dt))



    dictionary = {'Name': 'Saajan', 'Age': '23', 'Subjects': ["AI", "ML", "SOC"]}
    
    t = Template('index.html')
    c = Context({'dict': dictionary})
    
    #return render_to_response('index.html', locals(), context_instance=c)
    #return render(request, 'index.html', dictionary)
    return render(request, 'search_form.html', dictionary)
    
    
def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        publishers = Publisher.objects.filter(name__icontains=q)
        return render(request, 'search_results.html',
            {'books': publishers, 'query': q})
    else:
        if 'q' not in request.GET:
            error = False
        else:
            error=True
        return render(request, 'search_form.html', {'error': error})
    
    
    
# REST API    
    
@api_view(['GET', 'POST'])
def publisher_collection(request):
    if request.method == 'GET':
        posts = Publisher.objects.all()
        serializer = PublisherSerializer(posts, many=True)
        return HttpResponse(serializer.data)
    elif request.method == 'POST':
        data = {'text': request.DATA.get('the_post'), 'author': request.user.pk}
        serializer = PublisherSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def publisher_element(request, id):
    try:
        post = Publisher.objects.get(id=id)
    except Publisher.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PublisherSerializer(post)
        return Response(serializer.data)    



def dummy_my_view(request):
    
    final_dict = {}
    
    patients_list = appendtoDict( getPatients(50) )
    final_dict['patients_list'] = patients_list
    
    
    return render(request, 'Admin-master/index.html', final_dict)














####################DUMMY DATA

    