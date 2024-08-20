from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Quote
from django.db.models import Count
from django.core.paginator import Paginator


def quotes_list(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'quotes/quotes_list.html', {'page_obj': page_obj})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'quotes/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'quotes/login.html', {'form': form})


def quotes_by_tag(request, tag):
    quotes = Quote.objects.filter(tags__icontains=tag)
    return render(request, 'quotes/quotes_by_tag.html', {'quotes': quotes, 'tag': tag})


def top_tags(request):
    tags = Quote.objects.values('tags').annotate(tag_count=Count('tags')).order_by('-tag_count')[:10]
    return render(request, 'quotes/top_tags.html', {'tags': tags})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def add_author(request):
    if request.method == 'POST':
        name = request.POST['name']
        bio = request.POST['bio']
        Author.objects.create(name=name, bio=bio)
        return redirect('home')
    return render(request, 'quotes/add_author.html')


@login_required
def add_quote(request):
    if request.method == 'POST':
        author = Author.objects.get(id=request.POST['author_id'])
        text = request.POST['text']
        tags = request.POST['tags']
        Quote.objects.create(author=author, text=text, tags=tags, added_by=request.user)
        return redirect('home')
    authors = Author.objects.all()
    return render(request, 'quotes/add_quote.html', {'authors': authors})
