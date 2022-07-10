import tkinter as tk
from tkinter import ttk
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
    api_req_needed = math.ceil(num_candidates/50)
    list_responses = []

    for n in range(api_req_needed):
        string_id = ''
        
        for i in range(n*50, (n*50)+50):
            if i >= num_candidates:
                break
            else:
                string_id = string_id + str(candidateList[i].candid) + ','
        payload = {'candidate_ids': '%s' % string_id}
        r = requests.get(api_url + 'candidates', headers = headers, params = payload)
        parsed = json.loads(r.text)
        list_responses.extend(parsed)
    for i in range(num_candidates):
        for n in range(len(list_responses)):
            if candidateList[i].candid == list_responses[n]['id']:
                candidateList[i].name = list_responses[n]['first_name'] + ' ' + list_responses[n]['last_name']
                break

def table():
    
        root = tk.Tk()
        container = ttk.Frame(root)
        canvas = tk.Canvas(container)
        canvas.config(width=900, height=600)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

##        lbl = ttk.Label(scrollable_frame, text="Application Review", width= 17)
##        lbl.configure(background='white')
##        lbl.grid(column=0, row=0, padx=25, pady=(25, 45))

        lbl = ttk.Label(scrollable_frame, text="Screening")
        lbl.configure(background='white')
        lbl.grid(column=1, row=0, padx=25, pady=(25, 45))

        lbl = ttk.Label(scrollable_frame, text="Home Task")
        lbl.configure(background='white')
        lbl.grid(column=2, row=0, padx=25, pady=(25, 45))

        lbl = ttk.Label(scrollable_frame, text="Try Out")
        lbl.configure(background='white')
        lbl.grid(column=3, row=0, padx=25, pady=(25, 45))

        lbl = ttk.Label(scrollable_frame, text="Level 1")
        lbl.configure(background='white')
        lbl.grid(column=4, row=0, padx=25, pady=(25, 45))

        lbl = ttk.Label(scrollable_frame, text="Final Level")
        lbl.configure(background='white')
        lbl.grid(column=5, row=0, padx=25, pady=(25, 45))

        lbl = ttk.Label(scrollable_frame, text="Offer")
        lbl.configure(background='white')
        lbl.grid(column=6, row=0, padx=25, pady=(25, 45))

        for i in range(num_candidates):
##            if candidateList[i].applications == "Application Review":
##                lbl = ttk.Label(scrollable_frame, text=f"{candidateList[i].name}")
##                lbl.grid(column=0, row=i)
            if candidateList[i].applications == "Screening":
                lbl = ttk.Label(scrollable_frame, text=f"{candidateList[i].name}")
                lbl.grid(column=1, row=i+1)
            elif candidateList[i].applications == "Take Home Test":
                lbl = ttk.Label(scrollable_frame, text=f"{candidateList[i].name}")
                lbl.grid(column=2, row=i+1)
            elif candidateList[i].applications == "Try Out":
                lbl = ttk.Label(scrollable_frame, text=f"{candidateList[i].name}")
                lbl.grid(column=3, row=i+1)
            elif candidateList[i].applications == "Level 1":
                lbl = ttk.Label(scrollable_frame, text=f"{candidateList[i].name}")
                lbl.grid(column=4, row=i+1)
            elif candidateList[i].applications == "Final Level":
                lbl = ttk.Label(scrollable_frame, text=f"{candidateList[i].name}")
                lbl.grid(column=5, row=i+1)
            elif candidateList[i].applications == "Offer":
                lbl = ttk.Label(scrollable_frame, text=f"{candidateList[i].name}")
                lbl.grid(column=6, row=i+1)

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        root.mainloop()

get_eng_jobs()
get_ids()
get_candidates_name()
table()
