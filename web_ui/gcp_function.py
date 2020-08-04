import json
import urllib.request
from fastai.vision import *
from io import BytesIO
import logging


def handler(request):
    try:
        incoming = request.files['file'].read()
        bytes = BytesIO(incoming)
        image = open_image(bytes)

        defaults.device = torch.device('cpu')
        model_path = "https://github.com/jkennedy559/course-v3/blob/master/assignments%20/data/towers/export.pkl?raw=true"
        urllib.request.urlretrieve(model_path, '/tmp/model.pkl')
        path = Path('/tmp')
        learner = load_learner(path, 'model.pkl')

        pred_class, pred_idx, outputs = learner.predict(image)
        message = json.dumps({
            "predictions": sorted(
            zip(learner.data.classes, map(float, outputs)),
            key=lambda p: p[1],
            reverse=True)
             })
    except Exception as e:
        message = 'Failure'
        logging.critical(str(e))
    return message