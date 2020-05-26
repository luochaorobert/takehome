import os
import hashlib

from django.db import models


def upload_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.name, ext)
    return os.path.join("upload_image", filename)


class ImageFile(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="文件名称")
    image = models.ImageField(upload_to=upload_image_path, verbose_name="上传图像")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "上传图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        content = self.image.file.read()
        md5 = hashlib.md5(content).hexdigest()
        # 如果数据库中已有重复项，则放弃保存
        if ImageFile.objects.filter(name=md5):
            return "image already exists"
        self.name = md5
        super().save(*args, **kwargs)


class RecognitionResult(models.Model):
    image_file = models.ForeignKey(ImageFile, on_delete=models.CASCADE,
                                   verbose_name="图片文件")
    letter = models.CharField(max_length=1, verbose_name="识别字母")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "识别结果"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.letter
