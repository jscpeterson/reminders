from django.http import HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext


def test_exception(request):
    raise Exception("Test exception raised from error/ URL")


def handler403(request, exception):
    response = render_to_response("403.html")
    response.status_code = 403
    return HttpResponseForbidden(response)


def handler404(request, exception):
    response = render_to_response("404.html")
    response.status_code = 404
    return HttpResponseNotFound(response)


def handler500(request):
    response = render_to_response("500.html")
    response.status_code = 500
    return HttpResponseServerError(response)
