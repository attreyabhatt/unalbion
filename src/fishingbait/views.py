from django.shortcuts import render
from .models import FishingBaitData
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def fishing_profit_view(request):
    if not request.user.is_authenticated:
        return render(request, "accounts/notloggedin.html")
    else:
        if request.method == "POST":
            worm = request.POST.get("worm_price")
            t1 = request.POST.get("t1_price") or None
            t3 = request.POST.get("t3_price") or None
            t5 = request.POST.get("t5_price") or None

            # Required field check
            if not worm or not worm.isdigit():
                return render(request, "profit.html", {
                    "error": "Worm price is required and must be a number.",
                    "worm": worm,
                    "t1": t1,
                    "t3": t3,
                    "t5": t5,
                })

            worm = int(worm)

            def parse_or_none(val):
                return int(val) if val and val.isdigit() else None

            FishingBaitData.objects.update_or_create(
                user=request.user,
                defaults={
                    "worm_price": worm,
                    "t1_price": parse_or_none(t1),
                    "t3_price": parse_or_none(t3),
                    "t5_price": parse_or_none(t5),
                },
            )
            return redirect("fishing_bait")

        # Load existing data
        existing_data = FishingBaitData.objects.filter(user=request.user).first() if request.user.is_authenticated else None

        context = {
            "worm": existing_data.worm_price if existing_data else '',
            "t1": existing_data.t1_price if existing_data else '',
            "t3": existing_data.t3_price if existing_data else '',
            "t5": existing_data.t5_price if existing_data else '',
        }

        return render(request, "fishingbait/profit.html", context)


