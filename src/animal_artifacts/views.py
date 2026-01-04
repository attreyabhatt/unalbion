from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from .models import ArtifactItem, ArtifactPrice, ArtifactTier, ensure_artifact_catalog


def animal_artifacts_view(request):
    user = request.user

    if request.user.is_authenticated:
        ensure_artifact_catalog()

        if request.method == 'POST':
            updates = {}
            for key, value in request.POST.items():
                if key == 'csrfmiddlewaretoken' or not key.startswith("artifact_"):
                    continue

                parts = key.split("_", 2)
                if len(parts) != 3:
                    continue

                _, item_id, tier = parts
                if tier not in ArtifactTier.values:
                    continue

                try:
                    item_id = int(item_id)
                except ValueError:
                    continue

                updates[(item_id, tier)] = value.strip()

            item_ids = {item_id for item_id, _ in updates.keys()}
            items_by_id = ArtifactItem.objects.in_bulk(item_ids)

            existing_prices = ArtifactPrice.objects.filter(
                user=user,
                item_id__in=item_ids,
            )
            existing_by_key = {(p.item_id, p.tier): p for p in existing_prices}

            to_create = []
            to_update = []
            to_delete_keys = []

            for (item_id, tier), raw_value in updates.items():
                if item_id not in items_by_id:
                    continue

                if raw_value == "":
                    to_delete_keys.append((item_id, tier))
                    continue

                try:
                    price = int(raw_value)
                except ValueError:
                    continue

                existing = existing_by_key.get((item_id, tier))
                if existing:
                    if existing.price != price:
                        existing.price = price
                        to_update.append(existing)
                else:
                    to_create.append(
                        ArtifactPrice(user=user, item_id=item_id, tier=tier, price=price)
                    )

            with transaction.atomic():
                if to_create:
                    ArtifactPrice.objects.bulk_create(to_create)
                if to_update:
                    ArtifactPrice.objects.bulk_update(to_update, ["price"])
                if to_delete_keys:
                    delete_q = Q()
                    for item_id, tier in to_delete_keys:
                        delete_q |= Q(item_id=item_id, tier=tier)
                    ArtifactPrice.objects.filter(user=user).filter(delete_q).delete()

            return redirect('animal_artifacts')

        items = ArtifactItem.objects.all().order_by('name')
        prices = ArtifactPrice.objects.filter(user=user, item__in=items)

        prices_by_item = {}
        for price in prices:
            prices_by_item.setdefault(price.item_id, {})[price.tier] = price.price

        context = {
            'items': items,
            'artifact_tiers': [ArtifactTier.RUGGED, ArtifactTier.FINE, ArtifactTier.EXCELLENT],
            'prices_by_item': prices_by_item,
        }

        return render(request, 'animal_artifacts/animal_artifacts.html', context)
    else:
       return render(request, 'accounts/notloggedin.html')
