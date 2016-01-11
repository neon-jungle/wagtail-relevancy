from django.shortcuts import redirect, render

from ..models import Reminder


def review(request, pk):
    reminder = Reminder.objects.get(pk=pk)

    if request.method == "POST":
        reminder.page_reviewed = True
        reminder.save()
        return redirect('wagtailadmin_home')

    return render(request, 'wagtailrelevancy/review.html', {
        'request': request,
        'reminder': reminder,
    })
