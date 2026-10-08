from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout, login

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # Kullanıcıyı doğrudan giriş yapmış olarak başlat
            login(request, user)
            messages.success(request, f'Hoş geldin, {username}! Hesabın başarıyla oluşturuldu.')
            return redirect('home')
        else:
            # Şifre uyuşmazlığı, zayıf şifre gibi hataları ekrana gönder
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect(request.META.get('HTTP_REFERER', 'home'))
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Başarıyla çıkış yapıldı.")
    return redirect('home')
