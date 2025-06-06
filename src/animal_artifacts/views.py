from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import AnimalArtifactItem, ArtifactType

@login_required
def animal_artifacts_view(request):
    user = request.user

    if request.method == 'POST':
        for code_name, value in request.POST.items():
            if code_name == 'csrfmiddlewaretoken':
                continue

            try:
                item = AnimalArtifactItem.objects.get(code_name=code_name, artifact__user=user)
                if value.strip() != "":
                    item.market_price = int(value)
                else:
                    item.market_price = None
                item.save()
            except AnimalArtifactItem.DoesNotExist:
                continue

        return redirect('animal_artifacts')

    items = AnimalArtifactItem.objects.filter(artifact__user=user).select_related('artifact').order_by('id')

    grouped = {}
    for item in items:
        name = item.name
        tier = item.artifact.artifact_type
        if name not in grouped:
            grouped[name] = {}
        grouped[name][tier] = item

    context = {
        'grouped_items': grouped,
        'artifact_types': [ArtifactType.RUGGED, ArtifactType.FINE, ArtifactType.EXCELLENT],
    }

    return render(request, 'animal_artifacts/animal_artifacts.html', context)
