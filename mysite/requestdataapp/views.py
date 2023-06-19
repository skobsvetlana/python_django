from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

import os

def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdataapp/request_querry_params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:

    return render(request, "requestdataapp/user-bio-form.html")


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    context = {
        "message": "Ошибка. Размер файла не должен быть больше 1 Мб.",
    }

    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]
        context["filename"] = myfile.name
        context["filesize"] = myfile.size / 1000

        if myfile.size / 1000 > 1:
            print("file size = ", myfile.size / 1000, "Mb")
        else:
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print("saved file", filename)

    return render(request, "requestdataapp/file-upload.html", context=context)


