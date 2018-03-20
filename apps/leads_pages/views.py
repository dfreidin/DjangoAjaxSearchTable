# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from datetime import timedelta, datetime
from .models import *
from math import ceil

# Create your views here.
def index(request):
    return render(request, "leads_pages/index.html")

def search(request):
    fn = request.GET.get("first_name", "")
    ln = request.GET.get("last_name", "")
    fd = request.GET.get("from", "")
    td = request.GET.get("to", "")
    pp = int(request.GET.get("per_page", 10))
    pn = int(request.GET.get("page", 1)) - 1
    sort = request.GET.get("sort", "first_name")
    leads = Lead.objects.filter(first_name__contains=fn, last_name__contains=ln)
    if fd != "":
        leads = leads.filter(created_at__gte=fd)
    if td != "":
        td = datetime.strptime(td, "%Y-%m-%d") + timedelta(days=1)
        leads = leads.filter(created_at__lte=td)
    leads = leads.order_by(sort)
    if pn*pp+pp-1 > len(leads):
        page = leads[pn*pp:]
    else:
        page = leads[pn*pp:(pn+1)*pp]
    num_pages = max(int(ceil(len(leads)/float(pp))), 1)
    table = render(request, "leads_pages/table.html", {"leads": page})
    page_list = render(request, "leads_pages/page_list.html", {"range": range(1, num_pages+1)})
    response = {"num_pages": num_pages, "pn": pn+1, "table": table.content, "page_list": page_list.content}
    # print response
    return JsonResponse(response)