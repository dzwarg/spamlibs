from django.shortcuts import render
from .models import Email

def index(request):
    """
    Generate the front page of spamlibs. This shows the 10 most recent spam
    email messages, and allows users to seed and view them.

    :param HttpRequest request: A web request.
    :rtype: An HttpResponse object.
    """
    limit = 10

    recent_spams = Email.objects.order_by('-date')[:limit]
    viewed_spams = Email.objects.order_by('-views')[:limit]
    popular_spams = Email.objects.order_by('-rating')[:limit]

    count = Email.objects.count()

    ctx = {
        'recent_spams': recent_spams,
        'viewed_spams': viewed_spams,
        'popular_spams': popular_spams,
        'more': count > limit
    }

    return render(request, 'index.html', ctx)