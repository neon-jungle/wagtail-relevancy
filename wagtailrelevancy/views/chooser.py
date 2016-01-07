from django.shortcuts import render
from wagtail.wagtailusers.forms import GroupForm, GroupPagePermissionFormSet


def edit(request):
    group = get_object_or_404(Group, id=group_id)
    if request.method == "POST":
        pass
    else:
        form = GroupForm(instance=group)
        formset = GroupPagePermissionFormSet(instance=group)
    return render(request, 'wagtailrelevancy/edit.html', {
        'request': request,
        'form': form,
        'formset': formset,
    })
