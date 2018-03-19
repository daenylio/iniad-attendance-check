from django.shortcuts import render
from datetime import datetime
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from AttendanceCheck.models import Student, StudentStatus, AttendanceCheckingSession, ICcard
import subprocess

@csrf_exempt
def index(request):
    if request.POST.get('type') == 'login':
        return JsonResponse({"ic": get_ID().upper()})
    elif request.POST.get('type') == 'check':
        session = request.POST.get('session')
        iccard = ICcard.objects.get(card_id=get_ID().upper())
        user = Student.objects.get(ic_card=iccard.id)
        user_id = user.id
        update_status(user_id, session)
        return JsonResponse({"status": 1})


def update_status(studentid, session_id):
    #student = Student.objects.get(student_id=studentid)
    status = StudentStatus.objects.get(student_id=studentid, session_id=session_id)
    session = AttendanceCheckingSession.objects.get(id=session_id)
    check_in_time = datetime.now()
    check_in_time = datetime(2018, 1, 23, 16, 20)
    time_limit = session.created_on
    time_limit = datetime(time_limit.year, time_limit.month, time_limit.day, time_limit.hour, time_limit.minute) # convert to offset-aware datetime
    if check_in_time <= time_limit:
        status.status = 0 # ontime
    elif check_in_time.minute <= time_limit.minute + 20:
        status.status = 1 # late
    else:
        status.status = 2 # absent
    status.save()
    print(check_in_time, time_limit)
    print(status)
    return


def update_time(time):
    if time <= datetime(time.year, time.month, time.day, 9, 0):
        return datetime(time.year, time.month, time.day, 9, 0)
    elif time <= datetime(time.year, time.month, time.day, 10, 40):
        return  datetime(time.year, time.month, time.day, 10, 40)
    elif time <= datetime(time.year, time.month, time.day, 13, 0):
        return  datetime(time.year, time.month, time.day, 13, 0)
    elif time <= datetime(time.year, time.month, time.day, 14, 45):
        return  datetime(time.year, time.month, time.day, 14, 45)
    elif time <= datetime(time.year, time.month, time.day, 16, 30):
        return  datetime(time.year, time.month, time.day, 16, 30)
    elif time <= datetime(time.year, time.month, time.day, 18, 15):
        return  datetime(time.year, time.month, time.day, 18, 15)
    else:
        return  datetime(1996, 2, 29, 0, 0)



def nfc_raw():
    """Receive raw input from PN532 chip."""
    try:
        lines = subprocess.check_output("/usr/bin/nfc-poll", stderr=open('/dev/null', 'w'))
        print(lines)

        return lines
    # NFC-poll times out on 30s by default, so restart
    except subprocess.CalledProcessError:
        read_nfc()


def read_nfc():
    """Each individual read is returned."""
    lines = nfc_raw()
    buffer = []
    type = 0
    if lines is None:
        read_nfc()
    else:
        for line in lines.splitlines():
            line_content = line.split()
            # two types of cards, deepending on size of ID
            # UID for NFCID1
            # ID for NFCID2
            if line_content[0] == 'ID':
                buffer.append(line_content)
                type = 8
            elif line_content[0] == 'UID':
                buffer.append(line_content)
                type = 4
            else:
                pass
        str = buffer[0]
        if type == 8:
            id_str = str[2] + str[3] + str[4] + str[5] + str[6] + str[7] + str[8] + str[9]
        elif type == 4:
            id_str = id_str = str[2] + str[3] + str[4] + str[5]

        return id_str


def get_ID():
    """Export read ID."""
    return read_nfc()
