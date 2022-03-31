from django.shortcuts import render
import random


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
            return render(request, 'generator/downloadlink.html', {'totalpsw': totalpass})
        else:
            return render(request, 'generator/comeback.html')
    except ValueError:
        return render(request, 'generator/comeback.html')
