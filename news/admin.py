from django.contrib import admin
from .models import News
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



class NewsAdmin(admin.ModelAdmin):
    list_filter = ['id', 'author', 'title']
    list_display = ['id', 'author', 'title']
    search_fields = ['id', 'news_id', 'author']
    readonly_fields = ['id', 'news_id', 'author']
    show_full_result_count = False
    paginator = CachingPaginator
    class Meta:
        model = News
admin.site.register(News , NewsAdmin)