# =======================================
# ===           IMPORTS               ===
# =======================================
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Avg, Q
from django.contrib.contenttypes.models import ContentType

# Models & Forms
from main.models import Venue, Article, Events, Rating, Comment
from main.forms import VenueForm, ArticleForm, EventForm

from main.forms import VenueForm, ArticleForm, EventForm, ProfileForm

from main.models import Venue, Article, Events, Rating, UserProfile

from django.utils import timezone



# =======================================
# ===           MAIN VIEWS             ===
# =======================================
def show_main(request):
    """
    Home page: show mixed feed of Articles, Venues (top) and Events.
    """
    items = []
    top_venues = []

    ct_article = ContentType.objects.get_for_model(Article)
    ct_venue = ContentType.objects.get_for_model(Venue)
    ct_event = ContentType.objects.get_for_model(Events)

    articles = Article.objects.all().order_by('-published_date')
    venues = Venue.objects.all()
    events = Events.objects.all().order_by('-date')

    # Articles
    for a in articles:
        avg_rating = Rating.objects.filter(
            content_type=ct_article, object_id=a.id
        ).aggregate(avg=Avg('score'))['avg'] or 0
        items.append({
            'id': a.id,
            'type': 'article',
            'title': a.title,
            'content': a.content,
            'category': a.category,
            'created_at': a.published_date,
            'thumbnail': getattr(a, 'image_url', None),
            'user': a.user,
            'detail_url_name': 'main:show_article',
            'avg_rating': round(avg_rating, 1),
        })

    # Venues
    for v in venues:
        avg_rating = Rating.objects.filter(
            content_type=ct_venue, object_id=v.id
        ).aggregate(avg=Avg('score'))['avg'] or 0

        venue_dict = {
            'id': v.id,
            'type': 'venue',
            'name': v.name,
            'city': v.city,
            'address': v.address,
            'contact': v.contact,
            'website': v.website,
            'thumbnail': getattr(v, 'image_url', None),
            'user': v.user,
            'detail_url_name': 'main:show_venue',
            'avg_rating': round(avg_rating, 1),
            'price_range': getattr(v, 'price_range', None),
            'facilities': getattr(v, 'facilities', None),
        }
        top_venues.append(venue_dict)
        items.append(venue_dict)

    # Events
    for e in events:
        avg_rating = Rating.objects.filter(
            content_type=ct_event, object_id=e.id
        ).aggregate(avg=Avg('score'))['avg'] or 0

        items.append({
            'id': e.id,
            'type': 'event',
            'name': e.name,
            'description': e.description,
            'date': e.date,
            'venue': e.venue,
            'thumbnail': getattr(e, 'image_url', None),
            'user': e.user,
            'detail_url_name': 'main:show_event',  # make sure your URL exists if you link this
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


# =======================================
# ===            VENUES               ===
# =======================================
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
    """
    Displays a list of venues with search filters.
    Query params: q (name), location (city/address), price (price_range contains)
    """
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
    ct_venue = ContentType.objects.get_for_model(Venue)

    for v in venue_list:
        avg_rating = Rating.objects.filter(
            content_type=ct_venue, object_id=v.id
        ).aggregate(avg=Avg('score'))['avg'] or 0
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
        'items': items,
        'user': request.user,
        'active_page': 'venues',
        'search_query': query,
        'search_location': location,
        'search_price': price,
    }
    return render(request, "venues.html", context)


def show_venue(request, id):
    """
    Venue detail page including ratings list and average.
    """
    venue = get_object_or_404(Venue, pk=id)
    ct_venue = ContentType.objects.get_for_model(Venue)

    avg_rating = Rating.objects.filter(
        content_type=ct_venue, object_id=venue.id
    ).aggregate(avg=Avg('score'))['avg'] or 0

    reviews = Rating.objects.filter(
        content_type=ct_venue, object_id=venue.id
    ).order_by('-created_at')

    context = {
        'venue': venue,
        'avg_rating': round(avg_rating, 1),
        'active_page': 'venues',
        'reviews': reviews
    }
    return render(request, "venue_detail.html", context)


def ajax_venue_form(request):
    """
    AJAX: return venue form (GET) or create venue (POST).
    """
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


# =======================================
# ===            ARTICLES             ===
# =======================================
def article_list_view(request):
    """
    List of articles (if you prefer `article_list`, wire that in urls instead).
    """
    articles = Article.objects.all().order_by('-published_date')
    return render(request, 'article_page.html', {'articles': articles, 'active_page': 'blogs'})


def show_article(request, id):
    """
    Article detail with ratings and comments list.
    (Comment creation requires a CommentForm—left out to avoid coupling.)
    """
    article = get_object_or_404(Article, id=id)
    ct_article = ContentType.objects.get_for_model(Article)

    avg_rating = Rating.objects.filter(
        content_type=ct_article, object_id=article.id
    ).aggregate(avg=Avg('score'))['avg'] or 0

    comments = Comment.objects.filter(
        content_type=ct_article, object_id=article.id
    ).order_by('-created_at')

    context = {
        'article': article,
        'comments': comments,
        'avg_rating': round(avg_rating, 1),
    }
    return render(request, "article_detail.html", context)


def ajax_article_form(request):
    """
    AJAX: return article form (GET) or create article (POST).
    """
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            if request.user.is_authenticated:
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
# ===             EVENTS              ===
# =======================================
def ajax_event_detail(request, id):
    """
    AJAX: return event detail snippet.
    """
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
    """
    Delete an object by type (article/venue/event) via AJAX.
    """
    model_map = {'article': Article, 'venue': Venue, 'event': Events}
    model = model_map.get(type)
    if not model:
        return JsonResponse({'success': False, 'errors': 'Invalid type.'}, status=400)

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
    """
    Edit an object by type (article/venue/event) via AJAX.
    """
    model_map = {'article': Article, 'venue': Venue, 'event': Events}
    form_map = {'article': ArticleForm, 'venue': VenueForm, 'event': EventForm}
    model = model_map.get(type)
    form_class = form_map.get(type)
    if not model or not form_class:
        return JsonResponse({'success': False, 'errors': 'Invalid type.'}, status=400)

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
    """
    Render cards (HTML snippets) filtered by ?type=all|article|venue|event
    """
    type_filter = request.GET.get('type', 'all')
    items = []

    ct_article = ContentType.objects.get_for_model(Article)
    ct_venue = ContentType.objects.get_for_model(Venue)
    ct_event = ContentType.objects.get_for_model(Events)

    if type_filter in ('all', 'article'):
        for a in Article.objects.all().order_by('-published_date'):
            avg_rating = Rating.objects.filter(content_type=ct_article, object_id=a.id)\
                                       .aggregate(avg=Avg('score'))['avg'] or 0
            items.append({
                'id': a.id, 'type': 'article', 'title': a.title, 'content': a.content,
                'created_at': a.published_date, 'thumbnail': getattr(a, 'image_url', None),
                'user': a.user, 'detail_url_name': 'main:show_article', 'avg_rating': round(avg_rating, 1),
            })

    if type_filter in ('all', 'venue'):
        for v in Venue.objects.all():
            avg_rating = Rating.objects.filter(content_type=ct_venue, object_id=v.id)\
                                       .aggregate(avg=Avg('score'))['avg'] or 0
            items.append({
                'id': v.id, 'type': 'venue', 'name': v.name, 'city': v.city, 'address': v.address,
                'thumbnail': getattr(v, 'image_url', None), 'user': v.user,
                'detail_url_name': 'main:show_venue', 'avg_rating': round(avg_rating, 1),
                'created_at': timezone.now(),  # to allow sorting with mixed lists
            })

    if type_filter in ('all', 'event'):
        for e in Events.objects.all().order_by('-date'):
            avg_rating = Rating.objects.filter(content_type=ct_event, object_id=e.id)\
                                       .aggregate(avg=Avg('score'))['avg'] or 0
            items.append({
                'id': e.id, 'type': 'event', 'name': e.name, 'description': e.description,
                'date': e.date, 'thumbnail': getattr(e, 'image_url', None),
                'user': e.user, 'detail_url_name': 'main:show_event', 'avg_rating': round(avg_rating, 1),
                'created_at': e.date,
            })

    items.sort(key=lambda x: x.get('created_at', x.get('date', timezone.now())), reverse=True)

    try:
        html = "".join([
            render_to_string('card.html', {'item': item, 'user': request.user}, request=request)
            for item in items
        ])
        return HttpResponse(html)
    except Exception as e:
        print(f"Error rendering ajax_cards: {e}")
        return HttpResponse("Error loading cards.", status=500)


# =======================================
# ===            RATING API           ===
# =======================================
def rate_item(request):
    """
    POST endpoint to rate an Article / Venue / Event.
    - Logged-in users: stored with user.
    - Anonymous users: must provide `name` (stored in Rating.anonymous_name).
    Body params: type [article|venue|event], id (UUID), score (1..5), comment (optional), name (required if anon).
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    item_type = request.POST.get('type')
    item_id = request.POST.get('id')
    score_str = request.POST.get('score')
    comment_text = request.POST.get('comment', '')
    anonymous_name = request.POST.get('name', '').strip()

    if not score_str:
        return JsonResponse({'error': 'Score is required.'}, status=400)

    # Parse score
    try:
        score = int(score_str)
        if not (1 <= score <= 5):
            raise ValueError("Score out of range")
    except ValueError:
        return JsonResponse({'error': 'Invalid score value.'}, status=400)

    # Resolve model
    model_map = {'event': Events, 'venue': Venue, 'article': Article}
    model = model_map.get(item_type)
    if not model:
        return JsonResponse({'error': 'Invalid type'}, status=400)

    # Validate object exists
    if not model.objects.filter(pk=item_id).exists():
        return JsonResponse({'error': 'Item not found.'}, status=404)

    content_type = ContentType.objects.get_for_model(model)

    # If anonymous, require a display name
    if not request.user.is_authenticated and not anonymous_name:
        return JsonResponse({'error': 'Your name is required for anonymous reviews.'}, status=400)

    try:
        Rating.objects.create(
            user=request.user if request.user.is_authenticated else None,
            anonymous_name=None if request.user.is_authenticated else anonymous_name,
            content_type=content_type,
            object_id=item_id,
            score=score,
            comment=comment_text
        )

        avg = Rating.objects.filter(
            content_type=content_type, object_id=item_id
        ).aggregate(avg=Avg('score'))['avg'] or 0

        return JsonResponse({'message': 'Rating saved!', 'average': round(avg, 1)})
    except Exception as e:
        print(f"Error saving rating: {e}")
        return JsonResponse({'error': 'Could not save rating.'}, status=500)
        try:
            Rating.objects.create(
                user=None,
                anonymous_name=anonymous_name,
                content_type=content_type, 
                object_id=item_id,
                score=score,
                comment=comment_text
            )
            
            avg = Rating.objects.filter(
                content_type=content_type, object_id=item_id
            ).aggregate(avg=Avg('score'))['avg'] or 0
            return JsonResponse({'message': 'Rating saved!', 'average': round(avg, 1)})
        
        except Exception as e:
            print(f"Error saving rating: {e}")
            return JsonResponse({'error': 'Could not save rating.'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("main:edit_profile")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
        "active_page": "profile",  
    }
    return render(request, "profile_form.html", context)

@login_required
def profile_json(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    return JsonResponse({
        "username": request.user.username,
        "email": request.user.email,
        "phone_number": profile.phone_number,
        "hobbies": profile.hobbies,
        "competence": profile.competence,
        "profile_picture": profile.profile_picture.url if profile.profile_picture else None,
    })

@csrf_exempt
@login_required
def edit_profile_json(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "errors": "POST required."}, status=405)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    profile.phone_number = request.POST.get("phone_number", profile.phone_number)
    profile.hobbies = request.POST.get("hobbies", profile.hobbies)
    profile.competence = request.POST.get("competence", profile.competence)

    if "profile_picture" in request.FILES:
        profile.profile_picture = request.FILES["profile_picture"]

    profile.save()

    return JsonResponse({"success": True})

@csrf_exempt
def logout_json(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "errors": "POST required."}, status=405)

    logout(request)
    return JsonResponse({"success": True})
