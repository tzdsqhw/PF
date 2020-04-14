from django.contrib import admin
from .models import *
# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ['userid','username','password','birth','sex','head','mnum','newmessage']
    list_editable = ['username','password','birth','sex','head','newmessage']
class PetsAdmin(admin.ModelAdmin):
    list_display = ['petid','petname','petsex','petbirth','speci','petprice','pett']
    list_editable = ['petname','petsex','petbirth','speci','petprice','pett']
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
    list_display = ['oderid','oderitem','time','userid','totalprice','useradress','phone','oders','type']
    list_editable = ['oderitem','useradress','phone','oders','type']
class FollowAdmin(admin.ModelAdmin):
    list_display = ['usertof','usergetfid']
class CommentAdmin(admin.ModelAdmin):
    list_display = ['cid','dment','user','ctext','create_time']
    list_editable = ['dment','user','ctext']
admin.site.register(Users,UsersAdmin)
admin.site.register(Pets,PetsAdmin)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(Developments,DevelopAdmin)
admin.site.register(WhosCar,WhocarAdmin)
admin.site.register(Likes,LikeAdmin)
admin.site.register(Orders,OderAdmin)
admin.site.register(Follow,FollowAdmin)
admin.site.register(Comment,CommentAdmin)