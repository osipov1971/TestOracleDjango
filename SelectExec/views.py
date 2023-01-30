# from collections import OrderedDict
import cx_Oracle
from django.db import connection
# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED


# Create your views here.

def dictdetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class SelectListView(APIView):
    template_name = ''

    def get(self, request):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM mz.v_subgroup_shop WHERE code_shop >= %s', [request.data['code_shop']])
        res = dictdetchall(cursor)
        return Response(res, status=HTTP_200_OK)

    def put(self, request):
        cursor = connection.cursor()
        cursor.callproc('mz.SPR$_EXTERNAL_DEVICE.LogDiscountCard',
                        [request.data['code_shop'], request.data['code_shop'], 'I', request.data['description']])
        connection.commit()
        return Response({"code": request.data['code_shop']}, status=HTTP_201_CREATED)

    def post(self, request):
        cursor = connection.cursor()
        rout = cursor.var(cx_Oracle.NUMBER).var  # это для выходного параметра в процедуре
        code_shop = cursor.callfunc('mz.SumPaySupplyWithRet', int, [request.data['code_shop'], rout])
        connection.commit()
        return Response({"code": code_shop, "out": rout.getvalue()})
