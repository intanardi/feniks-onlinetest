from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User


def convert_in_hours(time):
    per_hour = 60
    difference = time - per_hour
    if difference >= 0:
        hour = 0
        while per_hour <= time:
            calc = time - per_hour
            time = calc
            hour += 1
            if calc == 0:
                calc = "00"
        duration =str(hour)+":"+str(calc)
    else:
        duration = "00:"+str(time)


    return duration
def convert_in_minutes(time):
    time_split = time.split(":")
    var_hour = int(time_split[0])
    var_minute = int(time_split[1])
    fix_minutes = 0
    if var_hour!= 0:
        minutes = 60
        for i in range(1, var_hour):
            minutes +=60
        fix_minutes = var_minute+minutes

    duration_in_minutes = var_minute+fix_minutes
    return duration_in_minutes