from django.contrib import admin
from photo.models import *

#3rd party file uploader app 
from multiupload.admin import MultiUploadAdmin

class AlbumInline(admin.TabularInline):
    # inlining with many-to-many relationships
    model = Album.pics.through

class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]

class ImageAdmin(admin.ModelAdmin):
    inlines = [ AlbumInline, ]
    list_display = ["__unicode__", "title", "user", "albums_", 
                    "rating", "size", "tags_", "thumbnail_", "created"]
    list_filter = ["tags", "user"]

    def save_model(self, request, obj, form, change):
        if not obj.user: obj.user = request.user
        obj.save()


class AlbumAdmin(MultiUploadAdmin):
    """ Allow upload multiple photos inside an album 
    using multiuploader app. Album is a container 
    for the files to be uploaded
    """
    search_fields = ["title"]
    # default value of all parameters:
    #change_form_template = 'multiupload/change_form.html'
    #change_list_template = 'multiupload/change_list.html'
    #multiupload_template = 'multiupload/upload.html'
    # if true, enable multiupload on list screen
    # generaly used when the model is the uploaded element
    multiupload_list = False
    # if true enable multiupload on edit screen
    # generaly used when the model is a container for uploaded files
    # eg: gallery
    # can upload files direct inside a gallery.
    multiupload_form = True
    # max allowed filesize for uploads in bytes
    multiupload_maxfilesize = 3 * 2 ** 20 # 3 Mb
    # min allowed filesize for uploads in bytes
    multiupload_minfilesize = 0
    # tuple with mimetype accepted
    multiupload_acceptedformats = ( "image/jpeg",
                                    "image/pjpeg",
                                    "image/png",)

    def process_uploaded_file(self, uploaded, object, request):
        """
        This method will be called for every file uploaded.
        Parameters:
            :uploaded: instance of uploaded file
            :object: instance of object if in form_multiupload else None
            :kwargs: request.POST received with file
        Return:
            It MUST return at least a dict with:
            {
                'url': 'url to download the file',
                'thumbnail_url': 'some url for an image_thumbnail or icon',
                'id': 'id of instance created in this method',
                'name': 'the name of created file',
            }
        """
        title = request.POST.get('title', '') or uploaded.name
        temp = Image(image=uploaded, title=title)
        temp.save()
        object.pics.add(temp)
        object.save()
        return {
            'url': temp.thumbnail_(),
            'thumbnail_url': temp.thumbnail_(),
            'id': temp.id,
            'name': temp.title
        }

    def delete_file(self, pk, request):
        """
        Function to delete a file.
        """
        obj = get_object_or_404(self.queryset(request), pk=pk)
        obj.delete()
        

admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)

