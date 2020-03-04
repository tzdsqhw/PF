from django.contrib import admin
from .models import *
# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ['userid','username','password','birth','sex','head']
    list_editable = ['username','password','birth','sex','head']
class PetsAdmin(admin.ModelAdmin):
    list_display = ['petid','petname','petsex','petbirth','speci']
    list_editable = ['petname','petsex','petbirth','speci']
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['goodsid','goodname','goodnum','goodtext','goodtype','goodprice']
    list_editable = ['goodname','goodnum','goodtext','goodtype','goodprice']
class DevelopAdmin(admin.ModelAdmin):
    list_display = ['user','username','dmentid','dmenttext','create_time','create_date','likenum']
    list_editable = ['username','dmenttext','likenum']
class WhocarAdmin(admin.ModelAdmin):
    list_display = ['user','carname','useradress','phone']
    list_editable = ['carname','useradress','phone']
class LikeAdmin(admin.ModelAdmin):
    list_display = ['userid', 'dmentid','time']
class OderAdmin(admin.ModelAdmin):
    list_display = ['oderid','oderitem','time','userid','totalprice','useradress','phone','oders']
    list_editable = ['oderitem','useradress','phone','oders']
admin.site.register(Users,UsersAdmin)
admin.site.register(Pets,PetsAdmin)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(Developments,DevelopAdmin)
admin.site.register(WhosCar,WhocarAdmin)
admin.site.register(Likes,LikeAdmin)
admin.site.register(Orders,OderAdmin)
