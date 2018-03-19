from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, reverse
from .models import ICcard, Student, Staff, Course, Enrollment, AttendanceCheckingSession, StudentStatus
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def index(request):
    scanning = False
    if scanning:
        user_ic_card = '01120312CB180216'
        return HttpResponseRedirect(reverse(quick_dashboard, args=[user_ic_card]))
    return render_to_response('AttendanceCheck/index.html')


def dash_board(request):
    return render_to_response('AttendanceCheck/dashboard.html')


def quick_dashboard(request, user_ic_card):
    ic_card = ICcard.objects.get(card_id=user_ic_card)
    user = Staff.objects.get(ic_card=ic_card.id)
    user_name = user.name
    enrollment = Enrollment.objects.filter(staff=user.id)
    context = {
        'user_name': user_name,
        'enrollment': enrollment
    }
    return render(request, "AttendanceCheck/quick_attendance.html", context)


def test(request):
    return render(request, "AttendanceCheck/test.html")


def update_status(student_id, session_id):
    student = Student.objects.get(student_id=student_id)
    status = StudentStatus.objects.get(student=student, session=session_id)
    session = AttendanceCheckingSession.objects.get(id=session_id)
    check_in_time = datetime.now()
    # for testing: check_in_time = datetime(2018, 1, 23, 16, 20)
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


def begin_checking(request, enrollment_id):
    enrollment = Enrollment.objects.get(id=enrollment_id)

    if AttendanceCheckingSession.objects.filter(enrollment_id=enrollment_id).count():
        session = AttendanceCheckingSession.objects.get(enrollment_id=enrollment_id)
    else:
        session = AttendanceCheckingSession.objects.create(enrollment=enrollment, created_on=update_time(datetime.now()))

    session.init()
    studentstatus_list = StudentStatus.objects.filter(session=session).all()

    # for testing: update_status("1F10170118", session.id)

    total_student = studentstatus_list.count()
    ontime_count = 0
    for studentstatus in studentstatus_list:
        if studentstatus.status == 0:
            ontime_count += 1

    user = Staff.objects.get(enrollment=enrollment)
    course = Course.objects.get(enrollment=enrollment)
    context = {
        'total_student': total_student,
        'ontime_count': ontime_count,
        'session': session,
        'studentstatus_list': studentstatus_list,
        'user': user,
        'course': course
    }
    return render(request, "AttendanceCheck/check_attendance.html", context)


def history(request, enrollment_id):
    return render_to_response('AttendanceCheck/history_list.html')


def enrollment_update(request, enrollment_id):
    return HttpResponse("get a student status for a enrollment and edit it")


def enrollment_setting(request, enrollment_id):
    return render_to_response('AttendanceCheck/course_setting.html')
