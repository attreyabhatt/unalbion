from django.shortcuts import render
from animal_artifacts.models import AnimalArtifact,AnimalArtifactItem
from django.http import JsonResponse

def home_view(request, *args, **kwargs):
    context = {
        'title': 'UnAlbion Home',
        'description': 'Welcome to UnAlbion, your go-to place for all things Albion Online.',
        'keywords': 'Albion Online, MMORPG, gaming, community',
    }
    return render(request, 'home.html', context)

def animal_artifact_view(request, *args, **kwargs):

    if request.method == "POST":

        codenamelist = [
        't3shadow', 't5shadow', 't7shadow',
        't3root', 't5root', 't7root',
        't3spirit', 't5spirit', 't7spirit',
        't3werewolf', 't5werewolf', 't7werewolf',
        't3imp', 't5imp', 't7imp',
        't3runestone', 't5runestone', 't7runestone',
        't3dawn', 't5dawn', 't7dawn',
        ]

        for current_code_name in codenamelist:
            if request.POST.get(current_code_name):
                AnimalArtifactItem.objects.filter(code_name=current_code_name).update(market_price=request.POST.get(current_code_name))
            else:
                AnimalArtifactItem.objects.filter(code_name=current_code_name).update(market_price=None)

        

    all_animal_artifacts = AnimalArtifact.objects.all().values()
    # print(all_animal_artifacts)

    rugged_artifact = AnimalArtifactItem.objects.filter(artifact_tier_id=1).order_by('id').values()
    fine_artifact = AnimalArtifactItem.objects.filter(artifact_tier_id=2).order_by('id').values()
    excellent_artifact = AnimalArtifactItem.objects.filter(artifact_tier_id=3).order_by('id').values()
    
    context = {
        'artifact_zipped_list': zip(rugged_artifact, fine_artifact, excellent_artifact),
    }
                
    return render(request, 'animal_artifacts/animal_artifacts.html', context)

    