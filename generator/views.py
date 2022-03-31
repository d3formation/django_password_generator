from django.shortcuts import render
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from pathlib import Path
import mimetypes
import os
import random


def downloadfile(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'psw_list.txt'
    filepath = base_dir + '/Files/' + filename
    thefile = filepath
    filename = os.path.basename(thefile)
    response = StreamingHttpResponse(FileWrapper(open(thefile, 'r', encoding='utf-8')),
                                     content_type=mimetypes.guess_type(thefile[0]))
    response['Content-Length'] = Path(thefile).stat().st_size - len(open(thefile, 'r', encoding='utf-8').readlines())
    response['Content-Disposition'] = "Attachment;filename=%s" % filename
    return response


def home(request):
    return render(request, 'generator/home.html')


def password(request):
    characters = list('abcdefghijklmnopqrstuvwxyz')

    if request.GET.get('+uppercase'):
        characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    if request.GET.get('+special'):
        characters.extend(list('!"№;%:?*()@#$^&'))
    if request.GET.get('+numbers'):
        characters.extend(list('0123456789'))

    length = int(request.GET.get('length', 12))

    thepassword = ''

    for x in range(length):
        thepassword += random.choice(characters)

    return render(request, 'generator/password.html', {'password': thepassword})


def about(request):
    return render(request, 'generator/about_page.html')


def download(request):
    user_input = request.GET.get('quantity', 100)
    try:
        filenum = int(user_input)
        if 0 < filenum <= 10_000:

            characters = list('abcdefghijklmnopqrstuvwxyz')

            if request.GET.get('uppercase'):
                characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
            if request.GET.get('special'):
                characters.extend(list('!"№;%:?*()@#$^&'))
            if request.GET.get('numbers'):
                characters.extend(list('0123456789'))

            length = int(request.GET.get('length', 12))

            totalpass = []
            for _ in range(filenum):
                thepassword = ''
                for x in range(length):
                    thepassword += random.choice(characters)
                if thepassword not in totalpass:
                    totalpass.append(thepassword)
                else:
                    while thepassword in totalpass:
                        thepassword = ''
                        for x in range(length):
                            thepassword += random.choice(characters)
                    totalpass.append(thepassword)

            with open('Files/psw_list.txt', 'w', encoding='utf-8') as file:
                for line in totalpass:
                    file.write(line + '\n')

            return render(request, 'generator/downloadlink.html', {'totalpsw': totalpass})
        else:
            return render(request, 'generator/comeback.html')
    except ValueError:
        return render(request, 'generator/comeback.html')
