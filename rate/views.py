from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Professor, Field


def home(request):
    fields = Field.objects.all()
    context = {'fields': fields}

    if not fields:
        messages.info(request, 'as empty as my pocket.')

    return render(request, 'rate/home.html', context=context)


def all(request, slug):
    field_name, field_area = Field.name_and_area_by(slug)
    professors = Professor.objects.filter(
            field__name=field_name,
            field__area=field_area,
            ).order_by(
                'score'
            )

    context = {'professors': professors, 'slug': slug}

    if not professors:
        messages.info(request, 'as empty as my pocket.')

    return render(request, 'rate/all.html', context=context)


def first(request, slug):
    if request.session.get('voted', False):
        messages.info(request, 'قبلا رای داده که :((')
        return redirect('home')

    field_name, field_area = Field.name_and_area_by(slug)
    try:
        professor = Professor.objects.filter(
                created_date__lt=timezone.now(),
                field__name=field_name,
                field__area=field_area,
                )[0]
    except IndexError:
        return redirect('all', slug=slug)

    request.session['voted'] = True
    uuid = professor.uuid
    return redirect('show', slug=slug, uuid=uuid)


def show(request, slug, uuid):
    field_name, field_area = Field.name_and_area_by(slug)
    professor = get_object_or_404(
            Professor,
            uuid=uuid,
            field__name=field_name,
            field__area=field_area,
            )
    context = {'professor': professor, 'slug': slug}
    return render(request, 'rate/show.html', context=context)


def next(request, slug, uuid):
    field_name, field_area = Field.name_and_area_by(slug)
    professor = get_object_or_404(
            Professor,
            uuid=uuid,
            )
    try:
        next_professor = Professor.objects.filter(
                created_date__gt=professor.created_date,
                field__name=field_name,
                field__area=field_area,
                )[0]
    except IndexError:
        return redirect('all', slug=slug)

    next_uuid = next_professor.uuid
    return redirect('show', slug=slug, uuid=next_uuid)


def upvote(request, slug, uuid):
    if request.method == "POST":
        professor = get_object_or_404(Professor, uuid=uuid)
        professor.score += 1
        professor.save()
    return redirect('next', slug=slug, uuid=uuid)


def downvote(request, slug, uuid):
    if request.method == "POST":
        professor = get_object_or_404(Professor, uuid=uuid)
        professor.score -= 1
        professor.save()
    return redirect('next', slug=slug, uuid=uuid)
