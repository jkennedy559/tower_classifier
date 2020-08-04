from django.shortcuts import render
import requests
from .forms import FileForm
from base64 import b64encode

GCP_URL = 'https://us-central1-lucid-sonar-280416.cloudfunctions.net/towers'
tower_dict = {'cn_tower': 'CN Tower',
              'skytree': 'Skytree',
              'space_needle': 'Space Needle'}


def home(request):
    """
    Return form on HTTP GET, if HTTP POST retrieve image from form
    for classification by GCP function and display predictions
    """
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            image_bytes = request.FILES['image'].read()

            files = {'file': ('tower.jpg', image_bytes,
                     'application/octet-stream')}
            response = requests.post(GCP_URL, files=files)
            dict_ = response.json()
            prediction = dict_['predictions'][0]
            tower, certainty = tower_dict[prediction[0]], prediction[1] * 100

            encoded = b64encode(image_bytes).decode()
            mime = 'image/jpeg;'
            context = {"image": "data:%sbase64,%s" % (mime, encoded),
                       'tower': tower,
                       'certainty': certainty}

            return render(request, 'web_ui/home.html', context)
    else:
        form = FileForm()
    return render(request, 'web_ui/home.html', {'form': form})


