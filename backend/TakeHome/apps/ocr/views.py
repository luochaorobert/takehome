from PIL import Image
import pytesseract
from collections import Counter

from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse

from pure_pagination import Paginator, PageNotAnInteger

from TakeHome.settings import TESSERACT_CMD

from .models import ImageFile, RecognitionResult
from .forms import ImageForm


# 设置服务器端tesseract执行文件的路径
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


class IndexView(View):
    def get(self, request, *args, **kwargs):
        all_files = ImageFile.objects.all().order_by('-date_added')

        # 对已上传的图片记录进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        per_page = 5
        p = Paginator(all_files, per_page=per_page, request=request)
        paging_files = p.page(page)
        page_label = {
            "begin": per_page * (int(page) - 1) + 1,
            "end": per_page * (int(page) - 1) + len(paging_files.object_list),
            "total": p.count,
        }

        context = {
            "image_files": paging_files,
            "page_label": page_label,
        }
        return render(request, "index.html", context=context)

    def post(self, request, *args, **kwargs):
        image_form = ImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            if image.content_type != 'image/jpeg' and image.content_type != 'image/png':
                response = {
                    "message": "File format error.",
                }
            else:
                new_image_file = image_form.save()
                image_open = Image.open(image).convert('L')
                results = []
                limit = 1
                while limit < 2.01:
                    # 调整图像对比度以便更好进行识别
                    image_open = image_open.point(lambda x: x * limit)
                    # 使用pytesseract识别图片中的字符，返回字符串
                    result = pytesseract.image_to_string(image_open)
                    if result:
                        results.append(result)
                    limit += 0.05

                if results:
                    # 出现次数最多的结果作为最终结果
                    recognition_result, *_ = Counter(results).most_common(1)[0]
                else:
                    recognition_result = ""
                print(results)
                print(recognition_result)

                # 如果上传的是一张新图片，则将识别结果保存至数据库
                if new_image_file.pk:
                    new_recognition_results = []
                    for item in character_filter(recognition_result):
                        new_recognition_result = RecognitionResult(
                            image_file=new_image_file, letter=item)
                        new_recognition_results.append(new_recognition_result)
                    RecognitionResult.objects.bulk_create(new_recognition_results)

                response = {
                    "content": character_filter(recognition_result),
                }
        else:
            response = {
                "message": "failed.",
            }
        return JsonResponse(data=response, safe=False)


def character_filter(string):
    """将string字符串中的字母筛选出来，返回一个字母列表"""
    result = []
    for character in list(string):
        if character.isalpha():
            result.append(character)
    return result
