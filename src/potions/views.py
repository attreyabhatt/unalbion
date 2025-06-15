from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Field
from .models import PotionInput


@login_required
def potion_input_view(request):
    input_instance, _ = PotionInput.objects.get_or_create(user=request.user)

    if request.method == "POST":
        for key, value in request.POST.items():
            if hasattr(input_instance, key) and value:
                setattr(input_instance, key, int(value))
        input_instance.save()
        return redirect("potion_input_view")

    editable_fields = [
        field.name for field in input_instance._meta.get_fields()
        if isinstance(field, Field) and field.editable and field.name not in ("id", "user")
    ]

    context = {
        "input_instance": input_instance,
        "editable_fields": editable_fields,
    }
    return render(request, "potions/profit_calculator.html", context)
