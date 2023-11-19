from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Film
from .forms import MoveForm

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'blog/room_list.html', {'rooms': rooms})

def room_detail(request, id_room):
    room = get_object_or_404(Room, id_room=id_room)
    return render(request, 'blog/room_detail.html', {'Room': room})

def film_list(request):
    films = Film.objects.all().order_by('titre')
    return render(request, 'blog/film_list.html', {'films': films})

def film_detail(request, id_film):
    film_object = get_object_or_404(Film, id_film=id_film)
    salle = film_object.salle
    form = MoveForm(instance=film_object)
    message = ''  

    if request.method == 'POST':
        form = MoveForm(request.POST, instance=film_object)
        if form.is_valid():
            new_salle = form.cleaned_data['salle']

            if new_salle != salle:
                if new_salle.id_room == 'Salle de stockage des films non diffusés':
                    associated_films_count = Film.objects.filter(salle=new_salle).count()
                    if associated_films_count >= 10:
                        message = 'La salle est indisponible'
                    else:
                        update_salle_disponibilite(salle)
                        update_salle_disponibilite(new_salle)
                        message = 'La salle a été mise à jour'
                        film_object.salle = new_salle
                        
                        film_object.etat = 'Non diffusé aujourd\'hui' if new_salle.id_room == 'Salle de stockage des films non diffusés' else 'Diffusé aujourd\'hui'

                        film_object.save()
                        return redirect('film_detail', id_film=id_film)
                else:
                    associated_films_count = Film.objects.filter(salle=new_salle).count()
                    if associated_films_count > 0:
                        message = 'La salle est indisponible'
                    else:
                        update_salle_disponibilite(salle)
                        update_salle_disponibilite(new_salle)
                        message = 'La salle a été mise à jour'
                        film_object.salle = new_salle
                        
                        film_object.etat = 'Non diffusé aujourd\'hui' if new_salle.id_room == 'Salle de stockage des films non diffusés' else 'Diffusé aujourd\'hui'

                        film_object.save()
                        return redirect('film_detail', id_film=id_film)
            else:
                message = "Cette salle est déjà affectée à ce film."

    return render(request, 'blog/film_detail.html', {
        'Film': film_object,
        'salle': salle,
        'form': form,
        'message': message,
    })

def update_salle_disponibilite(salle):
    if salle.id_room == 'Salle de stockage des films non diffusés':
        associated_films_count = Film.objects.filter(salle=salle).count()
        if associated_films_count >= 10:
            salle.disponibilite = 'occupée'
        else:
            salle.disponibilite = 'dispo'
    else:
        associated_films_count = Film.objects.filter(salle=salle).count()
        if associated_films_count == 0:
            salle.disponibilite = 'dispo'
        else:
            salle.disponibilite = 'occupée'
    salle.save()

def home(request):
    return render(request, 'blog/home.html', {})
