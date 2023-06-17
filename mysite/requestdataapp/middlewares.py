from django.http import HttpRequest


def set_useraent_on_request_middleware(get_response):
    print("initial call")
    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        reaponse = get_response(request)
        print("after get response")

        return reaponse

    return middleware


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