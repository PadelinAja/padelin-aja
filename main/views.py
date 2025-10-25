# =======================================
# ===           IMPORTS               ===
# =======================================
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.template.loader import render_to_string
<<<<<<< HEAD
=======
from django.contrib.auth.models import User
>>>>>>> origin/main
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Avg, Q
from django.contrib.contenttypes.models import ContentType

<<<<<<< HEAD
from main.models import Article, Events, Rating, Comment
from main.forms import ArticleForm
=======
from main.forms import VenueForm, ArticleForm, EventForm

from main.models import Venue, Article, Events, Rating


from django.utils import timezone
>>>>>>> origin/main

# =======================================
# ===           MAIN VIEWS             ===
# =======================================
def show_main(request):
<<<<<<< HEAD
    """Displays the main page with a combined list of articles, events (simplified)."""
    items = []

    content_type_article = ContentType.objects.get_for_model(Article)
    content_type_event = ContentType.objects.get_for_model(Events)

    articles = Article.objects.all().order_by('-published_date')
=======
    items = []
    top_venues = []
    
    content_type_article = ContentType.objects.get_for_model(Article)
    content_type_venue = ContentType.objects.get_for_model(Venue)
    content_type_event = ContentType.objects.get_for_model(Events)

    articles = Article.objects.all().order_by('-published_date')
    venues = Venue.objects.all()
>>>>>>> origin/main
    events = Events.objects.all().order_by('-date')

    for a in articles:
        avg_rating = Rating.objects.filter(content_type=content_type_article, object_id=a.id).aggregate(avg=Avg('score'))['avg'] or 0
        items.append({
<<<<<<< HEAD
            'id': a.id, 'type': 'article', 'title': a.title, 'content': a.content,
            'created_at': a.published_date, 'user': a.user, 'detail_url_name': 'main:show_article',
            'avg_rating': round(avg_rating, 1),
        })

    for e in events:
        items.append({
            'id': e.id, 'type': 'event', 'name': e.name, 'description': e.description,
            'date': e.date, 'user': e.user, 'detail_url_name': 'main:show_event',
        })

    items.sort(key=lambda x: x.get('created_at', x.get('date', timezone.now())), reverse=True)

    return render(request, "main.html", {'items': items, 'user': request.user, 'active_page': 'home'})

# =======================================
# ===        ARTICLE VIEWS            ===
# =======================================
def article_list_view(request):
    """Displays the list of articles."""
    articles = Article.objects.all().order_by('-published_date')
    return render(request, 'article_page.html', {'articles': articles, 'active_page': 'blogs'})

def show_article(request, id):
    """Displays an article detail page with rating and comments."""
    article = get_object_or_404(Article, id=id)
    content_type = ContentType.objects.get_for_model(Article)

    avg_rating = Rating.objects.filter(content_type=content_type, object_id=article.id).aggregate(avg=Avg('score'))['avg'] or 0
    comments = Comment.objects.filter(content_type=content_type, object_id=article.id).order_by('-created_at')

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_object = article
            comment.save()
            return redirect('main:show_article', id=article.id)
    else:
        form = ArticleForm()

    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(content_type=content_type, object_id=article.id, user=request.user).score
        except Rating.DoesNotExist:
            pass

    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'avg_rating': round(avg_rating, 1),
        'user_rating': user_rating,
    }
    return render(request, "article_detail.html", context)

def ajax_article_form(request):
    """Handles AJAX GET (fetch form) and POST (submit form) for articles."""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    else:
        form = ArticleForm()
        try:
            html = render_to_string('partials/article_form.html', {'form': form}, request=request)
            return JsonResponse({'html': html})
        except Exception:
            return JsonResponse({'error': 'Could not load form template.'}, status=500)

# =======================================
# ===           EVENT VIEWS           ===
# =======================================
def ajax_event_detail(request, id):
    """Handles AJAX GET request for event details."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request type'}, status=400)
    try:
        event = get_object_or_404(Events, id=id)
        html = render_to_string('partials/event_detail_snippet.html', {'event': event, 'user': request.user})
        return JsonResponse({'html': html})
    except Http404:
        return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception:
        return JsonResponse({'error': 'Failed to load details'}, status=500)

# =======================================
# ===        GENERAL AJAX & CRUD      ===
# =======================================
@login_required
@require_POST
def ajax_delete(request, type, id):
    """Handles AJAX DELETE requests for articles, venues, and events."""
    model_map = {'article': Article, 'event': Events}
    model = model_map.get(type)
    if not model:
        return JsonResponse({'success': False, 'errors': 'Invalid type.'}, status=400)
    obj = get_object_or_404(model, pk=id)
    if hasattr(obj, 'user') and obj.user != request.user:
        return JsonResponse({'success': False, 'errors': 'Permission denied.'}, status=403)
    try:
        obj.delete()
        return JsonResponse({'success': True})
    except Exception:
        return JsonResponse({'success': False, 'errors': 'Could not delete item.'}, status=500)

=======
            'id': a.id, 'type': 'article', 'title': a.title, 'content': a.content, 'category': a.category,
            'created_at': a.published_date, 'thumbnail': getattr(a, 'image_url', None), 'user': a.user,
            'detail_url_name': 'main:show_article',
            'avg_rating': round(avg_rating, 1),
        })
        
    for v in venues:
        avg_rating = Rating.objects.filter(content_type=content_type_venue, object_id=v.id).aggregate(avg=Avg('score'))['avg'] or 0
        
        venue_dict = {
            'id': v.id, 'type': 'venue', 'name': v.name, 'city': v.city, 'address': v.address,
            'contact': v.contact, 'website': v.website,
            'thumbnail': getattr(v, 'image_url', None), 'user': v.user,
            'detail_url_name': 'main:show_venue',
            'avg_rating': round(avg_rating, 1),
            'price_range': getattr(v, 'price_range', None),
            'facilities': getattr(v, 'facilities', None),
        }
        
        top_venues.append(venue_dict)
        items.append(venue_dict)

    for e in events:
        avg_rating = Rating.objects.filter(content_type=content_type_event, object_id=e.id).aggregate(avg=Avg('score'))['avg'] or 0
        items.append({
            'id': e.id, 'type': 'event', 'name': e.name, 'description': e.description,
            'date': e.date, 'venue': e.venue,
            'thumbnail': getattr(e, 'image_url', None), 'user': e.user,
            'detail_url_name': 'main:show_event',
            'avg_rating': round(avg_rating, 1),
        })

    items.sort(key=lambda x: x.get('created_at', x.get('date', timezone.now())), reverse=True)

    context = {
        'items': items,
        'top_venues': top_venues,
        'user': request.user,
        'active_page': 'home',
    }
    return render(request, "main.html", context)

@login_required
def create_venue(request):
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.user = request.user
            venue.save()
            return redirect('main:show_venues')
    else:
        form = VenueForm()
    context = {'form': form, 'active_page': 'venues'}
    return render(request, "create_venue.html", context)

def show_venues(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    price = request.GET.get('price', '')

    venue_list = Venue.objects.all()
    if query:
        venue_list = venue_list.filter(name__icontains=query)
    if location:
        venue_list = venue_list.filter(Q(city__icontains=location) | Q(address__icontains=location))
    if price:
        venue_list = venue_list.filter(price_range__icontains=price)

    items = []
    
    content_type_venue = ContentType.objects.get_for_model(Venue)
    
    for v in venue_list:
        avg_rating = Rating.objects.filter(content_type=content_type_venue, object_id=v.id).aggregate(avg=Avg('score'))['avg'] or 0
        items.append({
            'id': v.id, 
            'type': 'venue', 
            'name': v.name, 
            'city': v.city, 
            'address': v.address,
            'thumbnail': getattr(v, 'image_url', None), 
            'user': v.user,
            'avg_rating': round(avg_rating, 1),
            'detail_url_name': 'main:show_venue', 
            'price_range': getattr(v, 'price_range', None), 
        })

    context = {
        'items': items, 'user': request.user, 'active_page': 'venues',
        'search_query': query, 
        'search_location': location, 
        'search_price': price,
    }
    return render(request, "venues.html", context)

def show_venue(request, id):
    venue = get_object_or_404(Venue, pk=id)
    content_type_venue = ContentType.objects.get_for_model(Venue)

    avg_rating = Rating.objects.filter(
        content_type=content_type_venue, object_id=venue.id
    ).aggregate(avg=Avg('score'))['avg'] or 0

    reviews = Rating.objects.filter(
        content_type=content_type_venue, object_id=venue.id
    ).order_by('-created_at')

    context = {
        'venue': venue,
        'avg_rating': round(avg_rating, 1),
        'active_page': 'venues',
        'reviews': reviews
    }
    return render(request, "venue_detail.html", context)

def ajax_venue_form(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            if request.user.is_authenticated:
                 venue.user = request.user
            venue.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    else:
        form = VenueForm()
        try:
            html = render_to_string('partials/venue_form.html', {'form': form}, request=request)
            return JsonResponse({'html': html})
        except Exception as e:
            print(f"Error rendering venue form: {e}")
            return JsonResponse({'error': 'Could not load form template.'}, status=500)

@login_required
@require_POST
def ajax_delete(request, type, id):
    model_map = {'article': Article, 'venue': Venue, 'event': Events}
    model = model_map.get(type)
    if not model: return JsonResponse({'success': False, 'errors': 'Invalid type.'}, status=400)

    obj = get_object_or_404(model, pk=id)
    if hasattr(obj, 'user') and obj.user != request.user:
        return JsonResponse({'success': False, 'errors': 'Permission denied.'}, status=403)

    try:
        obj.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        print(f"Error deleting {type} {id}: {e}")
        return JsonResponse({'success': False, 'errors': 'Could not delete item.'}, status=500)

@login_required
def ajax_edit(request, type, id):
    model_map = {'article': Article, 'venue': Venue, 'event': Events}
    form_map = {'article': ArticleForm, 'venue': VenueForm, 'event': EventForm}
    model = model_map.get(type)
    form_class = form_map.get(type)
    if not model or not form_class: return JsonResponse({'success': False, 'errors': 'Invalid type.'}, status=400)

    obj = get_object_or_404(model, pk=id)
    if hasattr(obj, 'user') and obj.user != request.user:
        return JsonResponse({'success': False, 'errors': 'Permission denied.'}, status=403)

    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    else:
        context = {
            'form': form_class(instance=obj),
            'form_action_url': f"/ajax_edit/{type}/{id}/"
        }
        partial_template_name = f'partials/{type}_form.html'
        try:
            html = render_to_string(partial_template_name, context, request=request)
            return JsonResponse({'html': html})
        except Exception as e:
            print(f"Error rendering edit form ({partial_template_name}): {e}")
            return JsonResponse({'error': f'Could not load edit form template ({partial_template_name}).'}, status=500)

def ajax_cards(request):
    type_filter = request.GET.get('type', 'all')
    items = []

    items.sort(key=lambda x: x.get('created_at', x.get('date', timezone.now())), reverse=True)
    try:
        html = "".join([ render_to_string('card.html', {'item': item, 'user': request.user}, request=request) for item in items ])
        return HttpResponse(html)
    except Exception as e:
         print(f"Error rendering ajax_cards: {e}")
         return HttpResponse("Error loading cards.", status=500)
>>>>>>> origin/main
