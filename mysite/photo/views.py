from django.shortcuts import render

# Create your views here.
# Album listing 
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
#from settings import MEDIA_URL
from django.conf import settings
from photo.models import *
from string import join
from collections import defaultdict

def main(request):
    """Main listing."""
    albums = Album.objects.all()
    if not request.user.is_authenticated():
        albums = albums.filter(public=True)

    paginator = Paginator(albums, 10)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        albums = paginator.page(page)
    except (InvalidPage, EmptyPage):
        albums = paginator.page(paginator.num_pages)

    for album in albums.object_list:
        album.images = album.image_set.all()[:4]

    return render_to_response("photo/list.html", dict(albums=albums, user=request.user,
        media_url=settings.MEDIA_URL))


#def album(request, pk):
#    """Album listing."""
#    album = Album.objects.get(pk=pk)
#    if not album.public and not request.user.is_authenticated():
#        return HttpResponse("Error: you need to be logged in to view this album.")

#    images = album.image_set.all()
#    paginator = Paginator(images, 30)
#    try: page = int(request.GET.get("page", '1'))
#    except ValueError: page = 1

#    try:
#        images = paginator.page(page)
#    except (InvalidPage, EmptyPage):
#        images = paginator.page(paginator.num_pages)

#    return render_to_response("photo/album.html", dict(album=album, images=images, user=request.user,
#        media_url=settings.MEDIA_URL))


def album(request, pk, view="thumbnails"):
    """Album listing."""
    num_images = 30
    if view == "full": num_images = 10

    album = Album.objects.get(pk=pk)
    images = album.image_set.all()
    paginator = Paginator(images, num_images)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        images = paginator.page(page)
    except (InvalidPage, EmptyPage):
        images = paginator.page(paginator.num_pages)

#    return render_to_response("photo/album.html", dict(album=album, images=images,
#        user=request.user, view=view, media_url=settings.MEDIA_URL))
    
    # add list of tags as string and list of album objects to each image object
    for img in images.object_list:
        tags = [x[1] for x in img.tags.values_list()]
        img.tag_lst = join(tags, ', ')
        img.album_lst = [x[1] for x in img.albums.values_list()]

    d = dict(album=album, images=images, user=request.user, view=view, albums=Album.objects.all(),
        media_url=settings.MEDIA_URL)
    d.update(csrf(request))
    return render_to_response("photo/album.html", d)



def image(request, pk):
    """Image page."""
    img = Image.objects.get(pk=pk)
    return render_to_response("photo/image.html", dict(image=img, user=request.user,
         backurl=request.META["HTTP_REFERER"], media_url=settings.MEDIA_URL))

def update(request):
    """Update image title, rating, tags, albums."""
    p = request.POST
    images = defaultdict(dict)

    # create dictionary of properties for each image
    for k, v in p.items():
        if k.startswith("title") or k.startswith("rating") or k.startswith("tags"):
            k, pk = k.split('-')
            images[pk][k] = v
        elif k.startswith("album"):
            pk = k.split('-')[1]
            images[pk]["albums"] = p.getlist(k)

    # process properties, assign to image objects and save
    for k, d in images.items():
        image = Image.objects.get(pk=k)
        image.title = d["title"]
        image.rating = int(d["rating"])

        # tags - assign or create if a new tag!
        tags = d["tags"].split(', ')
        lst = []
        for t in tags:
            if t: lst.append(Tag.objects.get_or_create(tag=t)[0])
        image.tags = lst

        if "albums" in d:
            image.albums = d["albums"]
        image.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"], dict(media_url=settings.MEDIA_URL))
