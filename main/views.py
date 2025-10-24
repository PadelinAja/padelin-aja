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

from main.models import Article, Events, Rating, Comment
from main.forms import ArticleForm

# =======================================
# ===           MAIN VIEWS             ===
# =======================================
def show_main(request):
    """Displays the main page with a combined list of articles, events (simplified)."""
    items = []

    content_type_article = ContentType.objects.get_for_model(Article)
    content_type_event = ContentType.objects.get_for_model(Events)

    articles = Article.objects.all().order_by('-published_date')
    events = Events.objects.all().order_by('-date')

    for a in articles:
        avg_rating = Rating.objects.filter(content_type=content_type_article, object_id=a.id).aggregate(avg=Avg('score'))['avg'] or 0
        items.append({
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

