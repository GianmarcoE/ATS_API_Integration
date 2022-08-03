import tkinter as tk
from tkinter import ttk
import requests, base64, json, math
from datetime import datetime, timedelta
import threading

today = datetime.now()
today = today.isoformat()
today = today.partition("T")[0]
today = datetime.strptime(today, "%Y-%m-%d")

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

stages = ["Screening", "Take Home Test", "Try Out", "Level 1", "Final Level", "Offer"]
candidateList = []
job_ids = []
eng_people = ["All", "Ruta", "Alex", "Edita", "Gianmarco", "Luiza", "Irene"]
other = ["All", "Rugilė", "Giedrė", "Raimonda", "Agnija", "Justina", "Jekaterina"]
joinedpeople = eng_people + other
var = []
departments = ['4002211101', '4002214101', '4010068101', '4010103101', '4002212101',
               '4002216101', '4002217101', '4002210101', '4004137101', '4002221101',
               '4002209101', '4003517101', '4007388101', '4003524101', '4003522101',
               '4003521101', '4003520101', '4003519101', '4003518101', '4010423101',
               '4007781101', '4008991101', '4003523101', '4010069101', '4002208101',
               '4002219101', '4002213101', '4008086101', '4007682101', '4007681101',
               '4007680101', '4007679101', '4007678101']

class Candidate(object):
    """__init__() functions as the class constructor"""
    def __init__(self, candid=None, name=None, applications=None, role=None, last_activity=None, recruiter=None):
        self.candid = candid
        self.name = name
        self.applications = applications
        self.role = role
        self.last_activity = last_activity
        self.recruiter = recruiter

#gets all open jobs in engineering department
def get_jobs(st_thread, end_thread):
    for n in range(st_thread, end_thread):
        payload = {'per_page': '100', 'status': 'open', 'department_id': '%s' %departments[n]}
        r = requests.get(api_url + 'jobs', headers = headers, params = payload)
        parsed = json.loads(r.text)

        for i in range(len(parsed)):
            job_ids.append(parsed[i]['id'])

#finds ids, role and application status of the candidates in those jobs found above
def get_ids(st_thread, end_thread):
    for n in range(st_thread, end_thread):
        payload = {'status': 'active', 'per_page': '500', 'created_after': '%s' % my_date, 'job_id': '%s' %job_ids[n]}

        r = requests.get(api_url + 'applications', headers = headers, params = payload)
        parsed = json.loads(r.text)
        
        candidate_count = len(parsed)
        for i in range(candidate_count):
            try:
                if parsed[i]['current_stage']['name'] == "Application Review":
                    pass
                else:
                    candidateList.append(Candidate(parsed[i]['candidate_id']))
                    candidateList[-1].candid = parsed[i]['candidate_id']
                    candidateList[-1].role = parsed[i]['jobs'][0]['name'].replace('Software', '')
                    candidateList[-1].applications = parsed[i]['current_stage']['name']
            except:
                pass

##    global num_candidates
##    num_candidates = len(candidateList)

#matches the id with candidate's name and surname
def get_candidates_name(st_thread, end_thread):
    
    list_responses = []

    for n in range(st_thread, end_thread):
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
                try:
                    candidateList[i].name = list_responses[n]['first_name'] + ' ' + list_responses[n]['last_name']
                except:
                    candidateList[i].name = "No Name"
                candidateList[i].last_activity = list_responses[n]['last_activity']
                candidateList[i].last_activity = candidateList[i].last_activity.partition("T")[0]
                candidateList[i].last_activity = datetime.strptime(candidateList[i].last_activity, "%Y-%m-%d")
                candidateList[i].last_activity = abs((today - candidateList[i].last_activity).days)
                try:
                    candidateList[i].recruiter = list_responses[n]['recruiter']['first_name']
                except:
                    candidateList[i].recruiter = "None"
                break
            
def table():
    root = tk.Tk()
    root.title('Engineering Talent Pipeline by Gian')
    container = ttk.Frame(root)
    root.minsize(1125, 625)
    space = '                       '
    lbl = ttk.Label(root, text=f'{space}{space}{space} Screening{space}  Home Task{space}   Try Out{space}         Level 1{space}      Final Level{space}     Offer')
    lbl.pack(fill='x')
    canvas = tk.Canvas(container)
    canvas.config(width=1100, height=600)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    global scrollable_frame
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    sepa = ttk.Separator(scrollable_frame, orient="horizontal")
    sepa.grid(row=0, column= 0, pady=(0, 15), sticky='EW', columnspan=7)

    scrollable_frame.columnconfigure(6, minsize=140)

    for i in range(6):
        if i == 0:
            sepa = ttk.Separator(scrollable_frame, orient="vertical")
            sepa.grid(row=0, column= i, padx=(202, 0), sticky='NS', rowspan=num_candidates+1)
        else:
            sepa = ttk.Separator(scrollable_frame, orient="vertical")
            sepa.grid(row=0, column= i, padx=(152, 0), sticky='NS', rowspan=num_candidates+1)

    for x in range(len(var)):
        if var[x].get() == 1:
            if x == 0:
                for i in range(num_candidates):
                    if candidateList[i].recruiter not in eng_people:
                        pass
                    else:
                        print_line(i)
            elif x == len(eng_people):
                for i in range(num_candidates):
                    if candidateList[i].recruiter not in other:
                        pass
                    else:
                        print_line(i)
            else:
                for i in range(num_candidates):
                    if candidateList[i].recruiter == joinedpeople[x]:
                        print_line(i)
                break

    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

def print_line(i):
    for p in range(len(stages)):
        if candidateList[i].applications == stages[p]:
            lbl = ttk.Label(scrollable_frame, text=f"{candidateList[i].name}")
            lbl.grid(column=p+1, row=i+1, pady=(0, 25))
            if candidateList[i].last_activity > 14:
                lbl.config(foreground='red')
            compact_role(i)
            break
        
def compact_role(i):
    lbl = ttk.Label(scrollable_frame, text=f"{candidateList[i].role.replace('Engineer', '')}")
    lbl.grid(column=0, row=i+1, pady=(0, 25))
    sepa = ttk.Separator(scrollable_frame, orient="horizontal")
    sepa.grid(row=i+1, column= 0, pady=(12, 0), sticky='EW', columnspan=7)

def first_table():
    root = tk.Tk()
    root.title('Engineering Talent Pipeline by Gian')
    
    lbl = ttk.Label(root, text="Select Stream")
    lbl.grid(row=0, column=0, columnspan=3, pady=10)

    lbl = ttk.Label(root, text ="Engineering")
    lbl.grid(row=1, column=0, padx=20, pady=(10,15))
    lbl = ttk.Label(root, text ="Commercial")
    lbl.grid(row=1, column=2, padx=20, pady=(10, 15))

    sepa = ttk.Separator(root, orient="vertical")
    sepa.grid(row=1, column=1, sticky='NS', rowspan=8)

    for i in range(len(eng_people)):
        variab = tk.IntVar()
        var.append(variab)
        names = tk.Checkbutton (root, text=f'{eng_people[i]}', variable=var[i])
        names.grid(row=2+i, column=0, pady=5, padx=20, sticky='W')

    for i in range(len(other)):
        variab = tk.IntVar()
        var.append(variab)
        names = tk.Checkbutton (root, text=f'{other[i]}', variable=var[i+len(eng_people)])
        names.grid(row=2+i, column=2, pady=5, padx=20, sticky='W')        

    button = ttk.Button(root, text ="GO", command=table)
    button.grid(row=9, column=0, columnspan=3, pady=25)

def thread_pro():
    for _ in ([x, y, z, w]):
        _.start()

    for _ in ([x, y, z, w]):
        _.join()

x = threading.Thread(target=get_jobs, args=(0, 8,))
y = threading.Thread(target=get_jobs, args=(8, 16,))
z = threading.Thread(target=get_jobs, args=(16, 24,))
w = threading.Thread(target=get_jobs, args=(24, 32,))

thread_pro()

quanto = len(job_ids)
x = threading.Thread(target=get_ids, args=(0, int(quanto/4),))
y = threading.Thread(target=get_ids, args=(int(quanto/4), int(quanto/2),))
z = threading.Thread(target=get_ids, args=(int(quanto/2), int((quanto/4)*3),))
w = threading.Thread(target=get_ids, args=(int((quanto/4)*3), quanto,))

thread_pro()

num_candidates = len(candidateList)
api_req_needed = math.ceil(num_candidates/50)

x = threading.Thread(target=get_candidates_name, args=(0, int(api_req_needed/4),))
y = threading.Thread(target=get_candidates_name, args=(int(api_req_needed/4), int(api_req_needed/2),))
z = threading.Thread(target=get_candidates_name, args=(int(api_req_needed/2), int((api_req_needed/4)*3),))
w = threading.Thread(target=get_candidates_name, args=(int((api_req_needed/4)*3), api_req_needed,))

thread_pro()

first_table()
#get_jobs()
#get_ids()
#get_candidates_name()
