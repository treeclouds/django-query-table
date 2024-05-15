from django.shortcuts import render, redirect
from django.db import connections, OperationalError
from .models import SQLQuery
from .forms import SQLQueryForm, DatabaseForm
from .tables import SQLResultsTable
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse
from django.conf import settings
import django_tables2 as tables

def index(request):
    if request.method == 'POST':
        query_form = SQLQueryForm(request.POST)
        db_form = DatabaseForm(request.POST)
        if query_form.is_valid() and db_form.is_valid():
            request.session['db_params'] = db_form.cleaned_data
            query_form.save()
            return redirect('execute_query')
    else:
        query_form = SQLQueryForm()
        db_form = DatabaseForm()
    return render(request, 'queryapp/index.html', {'query_form': query_form, 'db_form': db_form})

def execute_query(request):
    query = SQLQuery.objects.latest('created_at')
    db_params = request.session.get('db_params')

    if not db_params:
        return redirect('index')

    db_alias = 'dynamic_db'
    databases = {
        db_alias: {
            'ENGINE': db_params['engine'],
            'NAME': db_params['dbname'],
            'USER': db_params['user'],
            'PASSWORD': db_params['password'],
            'HOST': db_params['host'],
            'PORT': db_params['port'],
            'OPTIONS': {},  # Add additional options if needed
            'TIME_ZONE': settings.TIME_ZONE,  # Ensure TIME_ZONE is set
            'CONN_MAX_AGE': settings.CONN_MAX_AGE,  # Connection persistence
            'CONN_HEALTH_CHECKS': settings.CONN_HEALTH_CHECKS,  # Health checks
            'AUTOCOMMIT': True,  # Ensure autocommit is set to True
            'ATOMIC_REQUESTS': True,  # Ensure atomic requests are set to True
        }
    }

    connections.databases.update(databases)

    try:
        with connections[db_alias].cursor() as cursor:
            cursor.execute(query.query)
            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()

        filter_value = request.GET.get('filter')
        if filter_value:
            results = [row for row in results if filter_value in str(row)]

        data = [dict(zip(columns, row)) for row in results]
        table = SQLResultsTable(data, extra_columns=[(col, tables.Column()) for col in columns])
        print(data)
        tables.RequestConfig(request, paginate={'per_page': 10}).configure(table)

        return render(request, 'queryapp/results.html', {
            'query': query,
            'table': table,
        })
    except OperationalError as e:
        return render(request, 'queryapp/error.html', {'error': str(e)})

def download_data(request):
    query = SQLQuery.objects.latest('created_at')
    db_params = request.session.get('db_params')

    if not db_params:
        return redirect('index')

    db_alias = 'dynamic_db'
    databases = {
        db_alias: {
            'ENGINE': db_params['engine'],
            'NAME': db_params['dbname'],
            'USER': db_params['user'],
            'PASSWORD': db_params['password'],
            'HOST': db_params['host'],
            'PORT': db_params['port'],
            'OPTIONS': {},  # Add additional options if needed
            'TIME_ZONE': settings.TIME_ZONE,  # Ensure TIME_ZONE is set
            'CONN_MAX_AGE': settings.CONN_MAX_AGE,  # Connection persistence
            'CONN_HEALTH_CHECKS': settings.CONN_HEALTH_CHECKS,  # Health checks
            'AUTOCOMMIT': True,  # Ensure autocommit is set to True
            'ATOMIC_REQUESTS': True,  # Ensure atomic requests are set to True
        }
    }

    connections.databases.update(databases)

    try:
        with connections[db_alias].cursor() as cursor:
            cursor.execute(query.query)
            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        writer = csv.writer(response)
        writer.writerow(columns)
        for row in results:
            writer.writerow(row)

        return response
    except OperationalError as e:
        return render(request, 'queryapp/error.html', {'error': str(e)})