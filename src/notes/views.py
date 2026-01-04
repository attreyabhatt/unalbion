from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note

@login_required
def create_note(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        Note.objects.create(user=request.user, title=title, content=content)
        return redirect("note_list")
    return render(request, "notes/note_form.html")

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notes/note_list.html", {"notes": notes})
