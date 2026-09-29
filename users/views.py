from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hesabınız başarıyla oluşturuldu, {username}!')
            return redirect('home')
        else:
            # Şifre uyuşmazlığı vs. gibi hataları ekrana mesaj olarak gönderir ve aynı sayfada tutar
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect(request.META.get('HTTP_REFERER', 'home'))

    return redirect('home')