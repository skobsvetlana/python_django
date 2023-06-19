from django.http import HttpRequest
from time import time

from django.shortcuts import render


def set_useraent_on_request_middleware(get_response):
    print("initial call")

    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        reaponse = get_response(request)
        print("after get response")

        return reaponse

    return middleware


class Restrict_num_requests_middleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_requests_time = {}

    def __call__(self, request: HttpRequest):
        context = {
            "time_delay": 10
        }
        ip_address = request.META["REMOTE_ADDR"]
        print(ip_address)
        last_request_time = self.last_requests_time.get(ip_address)
        print("last_request_time", last_request_time)
        request_time = time()

        if last_request_time and round(request_time - last_request_time) < context["time_delay"]:
            print("time_diff", round(request_time - last_request_time))
            context["time_diff"] = round(context["time_delay"] - (round(time() - last_request_time)))

            return render(request, "requestdataapp/error-time_request.html", context=context)
        else:
            self.set_request_time(request_time, ip_address)
            response = self.get_response(request)

            return response

    def set_request_time(self, request_time, ip_address):
        self.last_requests_time[ip_address] = request_time




class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exeptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("requests_count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses_count", self.responses_count)

        return response

    def process_exeption(self, request: HttpRequest, exception: Exception):
        self.exeptions_count += 1
        print("got", self.exeptions_count, "exceptions so far")
