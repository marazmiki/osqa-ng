# coding: utf-8

from django.utils.timezone import now
import datetime


def one_day_from_now():
    return now() + datetime.timedelta(days=1)
