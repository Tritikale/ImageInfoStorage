from django.shortcuts import render
from django.core.files.images import ImageFile
from PIL import Image, ImageDraw
from tempfile import TemporaryFile
from .forms import UserInfo
from .models import Page
import random
import string


def create_image(text_str, file):
    tmp = Image.new(mode="RGB", size=(1, 1))
    tmp_draw = ImageDraw.Draw(tmp)
    width, height = tmp_draw.textsize(text_str)
    img = Image.new('RGB', (width + 10, height + 10), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((5,5), text_str, fill=(0, 0, 0))
    img.save(file, 'png')


def create_password():
    length = 10
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    all = lower + upper + num + symbols
    temp = random.sample(all, length)
    password = "".join(temp)
    return password


def create_image_name():
    length = 5
    lower = string.ascii_lowercase
    num = string.digits
    all = lower + num
    temp = random.sample(all, length)
    image_name = "".join(temp)
    return image_name


def index(request):
    if request.method == 'POST':
        form = UserInfo(request.POST)
        if form.is_valid():
            with TemporaryFile(mode='w+b') as file:
                create_image(form.data['text_info'], file)
                Page.objects.create(image=ImageFile(file, name=create_image_name()+".png"), password=create_password())
    else:
        form = UserInfo()
    return render(request, 'main/index.html', {'form': form})
