from django.shortcuts import render
from animal_artifacts.models import AnimalArtifact,AnimalArtifactItem


def home_view(request, *args, **kwargs):
    context = {
        'title': 'UnAlbion Home',
        'description': 'Welcome to UnAlbion, your go-to place for all things Albion Online.',
        'keywords': 'Albion Online, MMORPG, gaming, community',
    }
    return render(request, 'home.html', context)

def animal_artifact_view(request, *args, **kwargs):

    if request.method == "POST":
        
        # print(request.POST.get('5'))
        context={}
        
        return render(request, 'animal_artifacts/animal_artifacts.html', context)


    all_animal_artifacts = AnimalArtifact.objects.all().values()
    # print(all_animal_artifacts)

    rugged_artifact = AnimalArtifactItem.objects.filter(artifact_tier_id=1).values()
    fine_artifact = AnimalArtifactItem.objects.filter(artifact_tier_id=2).values()
    excellent_artifact = AnimalArtifactItem.objects.filter(artifact_tier_id=3).values()

    
    # print(rugged_artifact[6]['name'], rugged_artifact[6]['market_price'])
    
    context = {
        'artifact_zipped_list': zip(rugged_artifact, fine_artifact, excellent_artifact),
        
    }
    return render(request, 'animal_artifacts/animal_artifacts.html', context)

    