from django.contrib import admin
from .models import PrivateRoom, PrivateMessage as message
from django.core.cache import cache
from django.core.paginator import Paginator
# Register your models here.
class CachingPaginator(Paginator):
    def _get_count(self):
       if not hasattr(self, "_count"):
            self._count = None
       if self._count is None:
              try:
                     key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                     self._count = cache.get(key, -1)
                     if self._count == -1:
                            self._count = super().count
                            cache.set(key, self._count, 3600)
              except:
                   self._count = len(self.object_list)
       return self._count
    
    count = property(_get_count)


class ChatAdmin(admin.ModelAdmin):
    list_filter = ['id', 'sender', 'receiver']
    list_display = ['id', 'message_body', 'sender', 'receiver', 'date_time', 'seen', 'is_delete']
    search_fields = ['id', 'message_body', 'sender__username', 'receiver__username']
    readonly_fields = ['id', 'message_body', 'sender', 'receiver', 'date_time', 'seen', 'is_delete']
    show_full_result_count = False
    paginator = CachingPaginator
    class Meta:
        model = message

class PrivateRoomAdmin(admin.ModelAdmin):
    list_filter = ['id', 'user1', 'user2']
    list_display = ['id', 'user1', 'user2']
    search_fields = ['user1', 'user2']
    readonly_fields = ['id', 'user1', 'user2']
    class Meta:
        model = PrivateRoom


admin.site.register(message ,ChatAdmin)
admin.site.register(PrivateRoom, PrivateRoomAdmin)


       
            
