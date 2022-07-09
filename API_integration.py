import requests, base64, json, math
from datetime import datetime, timedelta

my_date = datetime.now()
my_date = my_date - timedelta(days=90)
my_date = my_date.isoformat()

#authentication
api_key = "1234567890"
api_url = "https://harvest.greenhouse.io/v1/"
password = ""

userpass = api_key + ':' + password
encoded_u = base64.b64encode(userpass.encode()).decode()
headers = {"Authorization" : "Basic %s" % encoded_u}

candidateList = []
job_ids = []

class Candidate(object):
    """__init__() functions as the class constructor"""
    def __init__(self, candid=None, name=None, applications=None, role=None):
        self.candid = candid
        self.name = name
        self.applications = applications
        self.role = role

#gets all open jobs in engineering department
def get_eng_jobs():
    payload = {'per_page': '100', 'status': 'open', 'department_id': '4002211101'}
    r = requests.get(api_url + 'jobs', headers = headers, params = payload)
    parsed = json.loads(r.text)

    for i in range(len(parsed)):
        job_ids.append(parsed[i]['id'])

#finds ids, role and application status of the candidates in those jobs found above
def get_ids():
    for n in range(len(job_ids)):
        payload = {'status': 'active', 'per_page': '100', 'created_after': '%s' % my_date, 'job_id': '%s' %job_ids[n]}

        r = requests.get(api_url + 'applications', headers = headers, params = payload)
        parsed = json.loads(r.text)
        
        candidate_count = len(parsed)
        for i in range(candidate_count):
            candidateList.append(Candidate(parsed[i]['candidate_id']))
            candidateList[-1].candid = parsed[i]['candidate_id']
            candidateList[-1].role = parsed[i]['jobs'][0]['name']
            candidateList[-1].applications = parsed[i]['current_stage']['name']

    global num_candidates
    num_candidates = len(candidateList)

#matches the id with candidate's name and surname
def get_candidates_name():
    api_req_needed = math.ceil(len(candidateList)/50)

    for n in range(api_req_needed):
        string_id = ''
        
        for i in range(n*50, (n*50)+50):
            if i > num_candidates:
                break
            else:
                string_id = string_id + str(candidateList[i].candid) + ','
        payload = {'candidate_ids': '%s' % string_id}
        r = requests.get(api_url + 'candidates', headers = headers, params = payload)
        parsed = json.loads(r.text)
        for i in range(len(parsed)):
            candidateList[(n*50) + i].name = parsed[i]['first_name'] + ' ' + parsed[i]['last_name']

def output():
    for i in range(num_candidates):
        print(candidateList[i].name)
        print(candidateList[i].candid)
        print(candidateList[i].role)
        print(candidateList[i].applications)
        print()

get_eng_jobs()
get_ids()
get_candidates_name()
output()
