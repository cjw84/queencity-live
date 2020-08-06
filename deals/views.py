from .models import Company, Deal, Funding, Industry
from .forms import DealForm, CompanyForm
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd


def deals_home(request):
    colors1 = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c',
               '#fabebe',
               '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075',
               '#808080',
               '#ffffff', '#000000']
    data1 = dict()
    labels1 = list()
    data2 = dict()
    labels2 = list()
    deals = list(Deal.objects.all().values())
    latitude = list()
    longitude = list()
    funding = list()
    funding_str = list()
    name = list()
    for deal in deals:
        industry = Industry.objects.all().filter(
            id=Company.objects.all().filter(id=deal['company_id']).values()[0]['industry_id']).values()[0]['title']
        if industry in data1:
            data1[industry] = data1[industry] + deal['funding_amount']
        else:
            data1[industry] = deal['funding_amount']
            labels1.append(industry)
        date = str(deal['date'])
        if date in data2:
            data2[date] = data2[date] + deal['funding_amount']
        else:
            data2[date] = deal['funding_amount']
            labels2.append(date)
        name.append(Company.objects.all().filter(id=deal['company_id']).values()[0]['name'])
        funding.append(deal['funding_amount'])
        funding_str.append('$' + str(deal['funding_amount']))
        latitude.append(Company.objects.all().filter(id=deal['company_id']).values()[0]['location'].split(',')[0])
        longitude.append(Company.objects.all().filter(id=deal['company_id']).values()[0]['location'].split(',')[1])
    labels2 = sorted(labels2)
    data2_list = list()
    for label in labels2:
        data2_list.append(data2[label])
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(lon=longitude, lat=latitude,
                                marker=dict(color=funding, colorbar=dict(titleside='right'),
                                            colorbar_title='Funding Raised (MM)', ),
                                hovertemplate='Company: ' + pd.Series(name) + '<br>' + 'Funding:' + pd.Series(
                                    funding_str) + '<extra></extra>'))
    plt = plot(fig, output_type='div')
    context = {
        'data1': list(data1.values()),
        'labels1': labels1,
        'colors1': colors1,
        'data2': data2_list,
        'labels2': labels2,
        'plt': plt,
    }
    return render(request, 'deals/deal-home.html', context)


def create_deal(request):
    form = DealForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('deals-home'))
    context = {
        'form': form,
    }
    return render(request, 'deals/create-deal.html', context)


def create_company(request):
    form = CompanyForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('deals-home'))
    context = {
        'form': form,
    }
    return render(request, 'deals/create-company.html', context)


def search(request, type, specifier):
    if type == 'query':
        queryset = Deal.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(company__name__icontains=query) | Q(company__overview__icontains=query) | Q(
                    company__industry__title__icontains=query)).distinct()
    if type == 'industry':
        queryset = Deal.objects.all().filter(company__industry__title=specifier)
    if type == 'company':
        queryset = Deal.objects.all().filter(company__name=specifier)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    paginator = Paginator(queryset, 4)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
    }
    return render(request, 'deals/deal-home.html', context)