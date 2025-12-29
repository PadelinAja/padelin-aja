from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Avg, Q
from django.contrib.contenttypes.models import ContentType
from main.forms import VenueForm, ArticleForm, EventForm
from main.models import Venue, Article, Events, Rating
from django.utils import timezone
import json



def show_main(request):
    items = []
    top_venues = []
    
    content_type_article = ContentType.objects.get_for_model(Article)
    content_type_venue = ContentType.objects.get_for_model(Venue)
    content_type_event = ContentType.objects.get_for_model(Events)

    articles = Article.objects.all().order_by('-published_date')
    venues = Venue.objects.all()
    events = Events.objects.all().order_by('-date')

    for a in articles:
        avg_rating = Rating.objects.filter(content_type=content_type_article, object_id=a.id).aggregate(avg=Avg('score'))['avg'] or 0
        items.append({
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

@csrf_exempt
def create_venue_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # 1. User Logic (Pick Admin if anonymous)
            user = request.user
            if not user.is_authenticated:
                user = User.objects.filter(is_superuser=True).first()
            if not user:
                return JsonResponse({"status": "error", "message": "No admin user found"}, status=500)

            # 2. Create Venue with DEFAULTS for everything
            # This prevents "NOT NULL constraint failed" errors
            new_venue = Venue.objects.create(
                user=user,
                name=data.get("name", "Untitled Venue"),
                city=data.get("city", "Jakarta"),
                address=data.get("address", "No Address"),
                contact=data.get("contact", "000-000-000"),
                price_range=data.get("price_range", "100k-200k"),
                
                # OPTIONAL FIELDS (We give them empty strings if missing)
                website=data.get("website", ""),
                facilities=data.get("facilities", "Standard Courts"),
                image_url=data.get("image_url", "https://example.com/default.jpg"),
                
                # These might exist in your model, so we default them too
                image_url_2="", 
                image_url_3="", 
                image_url_4="", 
                image_url_5="" 
            )
            
            new_venue.save()
            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            # Print the REAL error to your terminal so you can see it
            print(f"========== ERROR ==========")
            print(e) 
            print("===========================")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error"}, status=401)

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


@csrf_exempt
def create_blog_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # 1. User fallback: use admin if anonymous
            user = request.user
            if not user.is_authenticated:
                user = User.objects.filter(is_superuser=True).first()
            if not user:
                return JsonResponse({"status": "error", "message": "No admin user found"}, status=500)

            # 2. Create Article with safe defaults to avoid missing fields
            new_article = Article.objects.create(
                user=user,
                title=data.get("title", "Untitled Article"),
                content=data.get("content", ""),
                category=data.get("category", Article.CategoryChoices.TIPS.value),
                image_url=data.get("image_url", "https://example.com/default.jpg"),
            )

            new_article.save()
            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            print(f"========== ARTICLE ERROR ==========")
            print(e)
            print("===================================")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error"}, status=401)

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

def show_venues_json(request):
    venues = Venue.objects.all()
    
    data = []
    for v in venues:
        item = {
            "id": str(v.id),
            "name": v.name,
            "city": v.city,
            "address": v.address,
            "price_range": getattr(v, 'price_range', 'N/A'),
            "image_url": getattr(v, 'image_url', '') 
        }
        data.append(item)
    
    # 3. Return JSON response
    return JsonResponse(data, safe=False)

@login_required
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

def article_list(request):
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    articles = Article.objects.all().order_by('-published_date')

    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    if category_filter:
        articles = articles.filter(category=category_filter)

    context = {
        'articles': articles,
        'search_query': search_query,
        'category_filter': category_filter,
        'active_page': 'blogs'
    }
    
    return render(request, 'article_page.html', context)

@login_required
def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('main:article_list')
    else:
        form = ArticleForm()
    context = {'form': form, 'active_page': 'blogs'}
    return render(request, "create_article.html", context)

def show_article(request, id):
    article = get_object_or_404(Article, pk=id)
    avg_rating = Rating.objects.filter(
        content_type=ContentType.objects.get_for_model(Article), object_id=article.id
    ).aggregate(avg=Avg('score'))['avg'] or 0
    context = {'article': article, 'avg_rating': round(avg_rating, 1), 'active_page': 'blogs'}
    return render(request, "article_detail.html", context)

@login_required
def ajax_article_form(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            if request.user.is_authenticated:
                article.user = request.user
            article.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    else: 
        form = ArticleForm()
        try:
            html = render_to_string('partials/article_form.html', {'form': form}, request=request)
            return JsonResponse({'html': html})
        except Exception as e:
            print(f"Error rendering article form template: {e}")
            return JsonResponse({'error': 'Could not load form template.'}, status=500)

def event_page(request):
    queryset = Events.objects.all().order_by('-date')
    search_query = request.GET.get('q', '')
    city_filter = request.GET.get('city', '')
    price_filter = request.GET.get('price', '')
    if search_query:
        queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    if city_filter:
        queryset = queryset.filter(venue__city__iexact=city_filter)
    if price_filter:
        if price_filter == '<100k': queryset = queryset.filter(price__lt=100000)
        elif price_filter == '100k-200k': queryset = queryset.filter(price__gte=100000, price__lte=200000)
        elif price_filter == '>200k': queryset = queryset.filter(price__gt=200000)
    context = {
        'events': queryset, 'active_page': 'events',
        'search_query': search_query, 'city_filter': city_filter, 'price_filter': price_filter,
    }
    return render(request, 'event_page.html', context)

@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('main:event_page')
    else:
        form = EventForm()
    context = {'form': form, 'active_page': 'events'}
    return render(request, "create_event.html", context)

@csrf_exempt
def create_event_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # 1. User Fallback Logic (Crucial Fix)
            user = request.user
            if not user.is_authenticated:
                user = User.objects.filter(is_superuser=True).first()
            if not user:
                 return JsonResponse({"status": "error", "message": "No admin user found"}, status=500)

            # 2. Get the Venue
            venue_id = data.get("venue_id")
            if not venue_id:
                return JsonResponse({"status": "error", "message": "Venue ID is required"}, status=400)
                
            venue = Venue.objects.get(id=venue_id)

            # 3. Create the Event
            new_event = Events.objects.create(
                user=user,  # <--- Now uses the fallback user
                name=data["name"],
                date=data["date"], # Django handles ISO strings automatically
                price=int(data["price"]),
                venue=venue,
                image_url=data.get("image_url", ""),
                # description removed as per your earlier request
            )

            return JsonResponse({"status": "success"}, status=200)
            
        except Venue.DoesNotExist:
             return JsonResponse({"status": "error", "message": "Venue not found"}, status=404)
        except Exception as e:
            # Print the real error to your terminal
            print(f"========== EVENT ERROR ==========")
            print(e)
            print("=================================")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    return JsonResponse({"status": "error"}, status=401)

def show_event(request, id):
    event = get_object_or_404(Events, pk=id)
    avg_rating = Rating.objects.filter(
        content_type=ContentType.objects.get_for_model(Events), object_id=event.id
    ).aggregate(avg=Avg('score'))['avg'] or 0
    context = {'event': event, 'avg_rating': round(avg_rating, 1), 'active_page': 'events'}
    return render(request, "event_detail.html", context)

def show_events_json(request):
    events = Events.objects.all().order_by('date')
    
    data = []
    for e in events:
        try:
            data.append({
                "id": str(e.id),
                "name": e.name,
                "date": e.date.isoformat() if e.date else None,
                "price": e.price,
                "type": getattr(e, 'type', 'Fun Match'),
                "image_url": getattr(e, 'image_url', ''),
                
                "venue": {
                    "name": e.venue.name if e.venue.name else "Unknown Venue",
                    "city": e.venue.city.strip() if e.venue.city else "Unknown City", # .strip() removes accidental spaces
                    "address": e.venue.address if e.venue.address else "-"
                }
            })
        except Exception as err:
            print(f"Skipping broken event: {err}")
            
    return JsonResponse(data, safe=False)

@login_required
def ajax_event_form(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            if request.user.is_authenticated:
                event.user = request.user
            event.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    else:
        form = EventForm()
        try:
            html = render_to_string('partials/event_form.html', {'form': form}, request=request)
            return JsonResponse({'html': html})
        except Exception as e:
            print(f"Error rendering event form: {e}")
            return JsonResponse({'error': 'Could not load form template.'}, status=500)

def ajax_event_detail(request, id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if not is_ajax:
        return JsonResponse({'error': 'Invalid request type'}, status=400)

    try:
        event = get_object_or_404(Events, id=id)
        html = render_to_string(
            'partials/event_detail_snippet.html',
            {'event': event, 'user': request.user}
        )
        return JsonResponse({'html': html})
    except Http404:
         return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        print(f"Error in ajax_event_detail: {e}")
        return JsonResponse({'error': 'Failed to load details'}, status=500)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not all([username, email, password]):
            return JsonResponse({'success': False, 'errors': 'All fields required.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'errors': 'Username already exists.'}, status=400)
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error during registration: {e}")
            return JsonResponse({'success': False, 'errors': 'Could not create user.'}, status=500)
    return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': 'Invalid credentials.'}, status=400)
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('main:show_main')

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


def about_view(request):
    context = {'active_page': 'about'}
    return render(request, "about.html", context)

def rate_item(request):
    if request.user.is_authenticated:
        return JsonResponse({'error': 'Logged-in users cannot submit reviews.'}, status=403)
        
    if request.method == 'POST':
        item_type = request.POST.get('type')
        item_id = request.POST.get('id')
        score_str = request.POST.get('score')
        comment_text = request.POST.get('comment', '')
        anonymous_name = request.POST.get('name', '')

        if not score_str: return JsonResponse({'error': 'Score is required.'}, status=400)
        if not anonymous_name: return JsonResponse({'error': 'Your name is required.'}, status=400)

        try:
            score = int(score_str)
            if not (1 <= score <= 5): raise ValueError("Score out of range")
        except ValueError:
            return JsonResponse({'error': 'Invalid score value.'}, status=400)

        model_map = {'event': Events, 'venue': Venue, 'article': Article}
        if item_type not in model_map: return JsonResponse({'error': 'Invalid type'}, status=400)
        model = model_map[item_type]
        content_type = ContentType.objects.get_for_model(model)

        if not model.objects.filter(pk=item_id).exists():
            return JsonResponse({'error': 'Item not found.'}, status=404)

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