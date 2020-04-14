from django.db import models

# Create your models here.
class Users(models.Model):
    userid = models.AutoField(primary_key=True)
    username=models.CharField(max_length=20, verbose_name='用户名')
    password=models.CharField(max_length=20, verbose_name='密码')
    birth=models.DateField(verbose_name='生日')
    sex=models.CharField(max_length=6,verbose_name='性别',choices=(('男','男'),('女','女')),default='男')
    mnum = models.IntegerField(verbose_name='消息数', default=0)
    head=models.CharField(max_length=40, verbose_name='头像',default='nohead.png')
    newmessage=models.TextField(verbose_name='新信息',default='{"like":[],"comment":[],"follow":[]}')
    def __str__(self):
        return str(self.userid)
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
class Pets(models.Model):
    petid= models.AutoField(primary_key=True)
    petprice=models.FloatField(verbose_name='宠物价格',default=0)
    pett=models.CharField(max_length=6,verbose_name='状态',choices=(('已出售','已出售'),('未出售','未出售')),default='未出售')
    petname=models.CharField(max_length=20, verbose_name='宠物名')
    petsex=models.CharField(max_length=6,verbose_name='性别',choices=(('公','公'),('母','母')),default='公')
    petbirth=models.DateField(verbose_name='宠物生日')
    speci=models.CharField(verbose_name='物种',choices=(('狗','狗'),('猫','猫'),('其他','其他')),max_length=10,default="狗")
    vnum=models.IntegerField(verbose_name='访问人数',default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    def __str__(self):
        return str(self.petid)

    class Meta:
        verbose_name = '宠物'
        verbose_name_plural = verbose_name
class Goods(models.Model):
    goodsid=models.AutoField(primary_key=True)
    goodname=models.CharField(max_length=20, verbose_name='商品名')
    goodprice=models.FloatField(verbose_name='商品单价',default=0)
    goodnum=models.IntegerField(verbose_name='商品存货数',default=0)
    goodtext=models.TextField(verbose_name='商品详情')
    goodtype=models.CharField(verbose_name='商品类型',choices=(('宠物食品','宠物食品'),('宠物玩具','宠物玩具'),('清洁用品','清洁用品'),('药品','药品'),('宠物衣物','宠物衣物')),max_length=10,default="宠物食品")

    def __str__(self):
        return str(self.goodsid)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
class Developments(models.Model):
    dmentid= models.AutoField(primary_key=True)
    user=models.ForeignKey(Users,verbose_name='用户',on_delete=models.CASCADE)
    username=models.CharField(max_length=20, verbose_name='用户名')
    likenum = models.IntegerField(verbose_name='点赞数', default=0)
    dmenttext = models.TextField(verbose_name='动态详情')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    create_date = models.DateField(verbose_name='创建日期', auto_now_add=True)
    def __str__(self):
        return str(self.dmentid)

    class Meta:
        verbose_name = '动态'
        verbose_name_plural = verbose_name
class WhosCar(models.Model):
    user = models.ForeignKey(Users, verbose_name='用户',on_delete=models.CASCADE)
    carname=models.CharField(max_length=20, verbose_name='购物车表名')
    useradress = models.CharField(verbose_name='收货地址', max_length=35)
    phone = models.CharField(verbose_name='收货电话', max_length=11)
    def __str__(self):
        return self.carname
    class Meta:
        verbose_name = '谁的车'
        verbose_name_plural = verbose_name
class Likes(models.Model):
    dmentid = models.ForeignKey(Developments,verbose_name='动态',on_delete=models.CASCADE)
    userid = models.ForeignKey(Users,verbose_name='用户',on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='时间',auto_now_add=True)
    def __str__(self):
        return str(self.dmentid)

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name
class Orders(models.Model):
    oderid=models.CharField(max_length=30,verbose_name='订单号')
    oderitem=models.TextField(verbose_name='订单详情')
    time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    userid = models.ForeignKey(Users,verbose_name='用户',on_delete=models.CASCADE)
    useradress=models.CharField(verbose_name='收货地址',max_length=35)
    phone = models.CharField(verbose_name='收货电话',max_length=11)
    totalprice=models.FloatField(verbose_name='总价',default=0)
    type=models.CharField(max_length=6, verbose_name='种类', choices=(('商品', '商品'), ('宠物', '宠物')), default='商品')
    oders = models.CharField(max_length=6, verbose_name='状态', choices=(('未发货', '未发货'), ('已发货', '已发货')), default='未发货')
    def __str__(self):
        return self.oderid

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
class Follow(models.Model):
    usertof = models.ForeignKey(Users,verbose_name='关注用户',on_delete=models.CASCADE)
    usergetfid=models.CharField(max_length=20, verbose_name='被关注用户id')


    def __str__(self):
        return str(self.usertof)

    class Meta:
        verbose_name = '关注'
        verbose_name_plural = verbose_name
class Comment(models.Model):
    cid= models.AutoField(primary_key=True)
    user=models.ForeignKey(Users,verbose_name='用户',on_delete=models.CASCADE)
    dment=models.ForeignKey(Developments,verbose_name='动态',on_delete=models.CASCADE)
    ctext = models.TextField(verbose_name='评论详情')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return str(self.cid)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
