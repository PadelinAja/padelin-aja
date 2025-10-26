from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden

from main.models import Venue, Article, Events
from main.forms import VenueForm, ArticleForm, EventForm


def is_site_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='SiteAdmin').exists())


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and (user.is_superuser or user.groups.filter(name='SiteAdmin').exists()):
            login(request, user)
            return redirect('/admin/')
        else:
            return render(request, 'admin/login.html', {'error': 'Invalid credentials or not an admin.'})
    return render(request, 'admin/login.html')


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_logout(request):
    logout(request)
    return redirect('/admin/login/')


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_dashboard(request):
    counts = {
        'venues': Venue.objects.count(),
        'articles': Article.objects.count(),
        'events': Events.objects.count(),
    }
    return render(request, 'admin/dashboard.html', {'counts': counts})


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_venues_list(request):
    venues = Venue.objects.all().order_by('name')
    return render(request, 'admin/venues_list.html', {'venues': venues})


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_create_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            # store admin user as creator
            venue.user = request.user
            venue.save()
            return redirect('/admin/venues/')
    else:
        form = VenueForm()
    return render(request, 'admin/venue_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_edit_venue(request, id):
    venue = get_object_or_404(Venue, pk=id)
    if request.method == 'POST':
        form = VenueForm(request.POST, instance=venue)
        if form.is_valid():
            form.save()
            return redirect('/admin/venues/')
    else:
        form = VenueForm(instance=venue)
    return render(request, 'admin/venue_form.html', {'form': form, 'action': 'Edit'})


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_delete_venue(request, id):
    venue = get_object_or_404(Venue, pk=id)
    if request.method == 'POST':
        venue.delete()
    return redirect('/admin/venues/')
    return render(request, 'admin/confirm_delete.html', {'obj': venue, 'type': 'venue'})


# Articles
@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_articles_list(request):
    articles = Article.objects.all().order_by('-published_date')
    return render(request, 'admin/articles_list.html', {'articles': articles})


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('/admin/articles/')
    else:
        form = ArticleForm()
    return render(request, 'admin/article_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_edit_article(request, id):
    article = get_object_or_404(Article, pk=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('/admin/articles/')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'admin/article_form.html', {'form': form, 'action': 'Edit'})


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_delete_article(request, id):
    article = get_object_or_404(Article, pk=id)
    if request.method == 'POST':
        article.delete()
    return redirect('/admin/articles/')
    return render(request, 'admin/confirm_delete.html', {'obj': article, 'type': 'article'})


# Events
@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_events_list(request):
    events = Events.objects.all().order_by('-date')
    return render(request, 'admin/events_list.html', {'events': events})


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('/admin/events/')
    else:
        form = EventForm()
    return render(request, 'admin/event_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_edit_event(request, id):
    event = get_object_or_404(Events, pk=id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('/admin/events/')
    else:
        form = EventForm(instance=event)
    return render(request, 'admin/event_form.html', {'form': form, 'action': 'Edit'})


@login_required
@user_passes_test(is_site_admin, login_url='/admin/login/')
def admin_delete_event(request, id):
    event = get_object_or_404(Events, pk=id)
    if request.method == 'POST':
        event.delete()
    return redirect('/admin/events/')
    return render(request, 'admin/confirm_delete.html', {'obj': event, 'type': 'event'})
