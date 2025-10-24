from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg
from django.contrib.contenttypes.models import ContentType
from main.models import Venue, Rating


def show_venues(request):
    """Displays a list of venues with search filters."""
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
    """Displays the detail page for a single venue."""
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




def rate_item(request):
    """Handles POST request to rate an item (article, venue, or event)."""
    
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
