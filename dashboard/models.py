from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import FileExtensionValidator
from django.db import models
from django.conf import settings
Role_CHOICES = [
    ("ADMIN", "Admin"),
    ("STAFF", "Staff"),
]


class ServiceType(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='services/icons/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name="services", default=1)  # default set to 1


    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="cart_items" 
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    service_name = models.CharField(max_length=255, blank=True) 
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"

    def save(self, *args, **kwargs):

        if not self.service_name:
            self.service_name = self.service.name
        if not self.service_price:
            self.service_price = self.service.price
        super(Cart, self).save(*args, **kwargs)

    def total_price(self):
        """Calculate the total price for this cart item (price * quantity)."""
        return self.quantity * self.service_price


class Pages(models.Model):
    pageName = models.CharField(max_length=50, null=True, blank=True)
    pageHeading = models.CharField(max_length=50, null=True, blank=True)
    pageDescription = models.TextField(null=True, blank=True)
    pageBanner = models.FileField(upload_to='services/icons/')
    pageTitle = models.CharField(max_length=50, null=True, blank=True)
    PageMetaDescription= models.CharField(max_length=50, null=True, blank=True)
    PageMetaKeywords = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.pageName

    @classmethod
    def add(cls, pagename, pageheading, pagedescptn, pagebaner, pagetitl, pagemetades, pagemetakey):
        res = cls(pageName=pagename, pageHeading=pageheading, pageDescription=pagedescptn, pageBanner=pagebaner, pageTitle=pagetitl,
                  PageMetaDescription=pagemetades, PageMetaKeywords=pagemetakey)

        res.save()
        print(res)
        return res

    @classmethod
    def update(cls, id,  pagename=None, pageheading=None, pagedescptn=None, pagebaner=None, pagetitl=None, pagemetades=None, pagemetakey=None):
        try:
            res = Pages.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

        if pagename is not None and pagename != res.pageName:
            res.pageName = pagename
        if pageheading is not None and pageheading != res.pageHeading:
            res.pageHeading = pageheading
        if pagedescptn is not None and pagedescptn != res.pageDescription:
            res.pageDescription = pagedescptn
        if pagebaner is not None and pagebaner != res.pageBanner:
            res.pageBanner = pagebaner
        if pagetitl is not None and pagetitl != res.pageTitle:
            res.pageTitle = pagetitl
        if pagemetades is not None and pagemetades != res.PageMetaDescription:
            res.PageMetaDescription = pagemetades
        if pagemetakey is not None and pagemetakey != res.PageMetaKeywords:
            res.PageMetaKeywords = pagemetakey

        res.save()

        print(res)
        return res


class Add_Section(models.Model):
    pageName = models.ForeignKey(Pages, on_delete=models.CASCADE, null=True, blank=True)
    sectionName = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.sectionName

    @classmethod
    def add(cls, pgeName, secName):
        page_instance = Pages.objects.get(id=pgeName)
        res = cls(pageName=page_instance, sectionName=secName)

        res.save()
        print(res)
        return res

    @classmethod
    def update(cls, id, pgeName=None, secName=None):
        try:
            res = Add_Section.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
        if pgeName is not None and pgeName != res.pageName:
            res.pageName = pgeName
        if secName is not None and secName != res.sectionName:
            res.sectionName = secName

        res.save()
        print(res)
        return res


class Content(models.Model):
    selectPage = models.ForeignKey(Pages, on_delete=models.CASCADE,  null=True, blank=True)
    selectSection = models.ForeignKey(Add_Section, on_delete=models.CASCADE,  null=True, blank=True)
    contentHeading = models.CharField(max_length=80, null=True, blank=True)
    contentDescription = models.TextField()
    contentImage = models.ImageField(upload_to='services/icons/')
    contentButton = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.selectPage)

    @classmethod
    def add(cls, selectpage, selectsec, contntheading, contntdes, contntImage, contntbut):
        selecPage = Pages.objects.get(id=selectpage)
        selecSec = Add_Section.objects.get(id=selectsec)
        res = cls(selectPage=selecPage, selectSection=selecSec, contentHeading=contntheading, contentDescription=contntdes,
                  contentImage=contntImage,
                  contentButton=contntbut)

        res.save()
        print(res)
        return res

    @classmethod
    def update(cls, id, selectpage=None, selectsec=None, contntheading=None, contntdes=None, contntImage=None,
               contntbut=None):

        try:
            res = Content.objects.get(id=id)
            selecPage = Pages.objects.get(id=selectpage)
            selecSec = Add_Section.objects.get(id=selectsec)
        except ObjectDoesNotExist:
            return None

        if selecPage is not None and selecPage != res.selectPage:
            res.selectPage = selecPage
        if selecSec is not None and selecSec != res.selectSection:
            res.selectSection = selecSec
        if contntheading is not None and contntheading != res.contentHeading:
            res.contentHeading = contntheading
        if contntdes is not None and contntdes != res.contentDescription:
            res.contentDescription = contntdes
        if contntImage is not None and contntImage != res.contentImage:
            res.contentImage = contntImage
        if contntbut is not None and contntbut != res.contentButton:
            res.contentButton = contntbut

        res.save()

        print(res)
        return res

class Sub_Content(models.Model):
    contentHeading = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='sub_contents',  null=True, blank=True)
    sub_contentHeading = models.CharField(max_length=255, null=True, blank=True)
    subContent = models.TextField()
    subContentImage = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    def __str__(self):
        return str(self.contentHeading)

    @classmethod
    def add(cls, cntntheading, sb_heding, sbcntnt, sbcontntImg):
        selecCntnt = Content.objects.get(id=cntntheading.id)
        res = cls(contentHeading=selecCntnt, sub_contentHeading=sb_heding, subContent=sbcntnt, subContentImage=sbcontntImg)
        res.save()

        print(res)
        return res

    @classmethod
    def update(cls, id, cntntheading=None, sb_heding=None, sbcntnt=None, sbcontntImg=None):
        try:
            res = Sub_Content.objects.get(id=id)
            cntntheading = Content.objects.get(id=cntntheading.id)
        except ObjectDoesNotExist:
            return None

        if cntntheading is not None and cntntheading != res.contentHeading:
            res.contentHeading = cntntheading
        if sb_heding is not None and sb_heding != res.sub_contentHeading:
            res.sub_contentHeading = sb_heding
        if sbcntnt is not None and sbcntnt != res.subContent:
            res.subContent = sbcntnt
        if sbcontntImg is not None and sbcontntImg != res.subContentImage:
            res.subContentImage = sbcontntImg

        res.save()

        print(res)
        return res