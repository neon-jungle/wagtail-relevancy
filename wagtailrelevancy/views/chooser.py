from django.shortcuts import render

from ..forms import ReminderFormSet


def edit(request):
    if request.method == "POST":
        formset = ReminderFormSet(request.POST, instance=request.user)
        if formset.is_valid():
            formset.save()
    else:
        formset = ReminderFormSet(instance=request.user)
    return render(request, 'wagtailrelevancy/edit.html', {
        'request': request,
        'formset': formset,
    })
