

import os, sys
from pathlib import Path
here = Path(__file__).parent
p = f'{here.parent}'
if p not in sys.path:
    sys.path.append(p)
from lymonet.apis import YOLO, LYMO
from dataclasses import dataclass, field
import hai


def run(args):
    # Create a new YOLO model from scratch
    # model_name = args.pop('model')
    kwargs = args.__dict__
    model_name_or_cfg = kwargs.pop('model')
    model_weights = kwargs.pop('weights', None)
    # LYMO.apply_improvements()
    model = LYMO(model_name_or_cfg)
    # model = YOLO(model_name_or_cfg)

    if model_weights:
        model = model.load(model_weights)
    
    # model = YOLO(model_name).load(model_weights)

    # results = model.train(**kwargs)

    # Evaluate the model's performance on the validation set
    results = model.val(data=args.data, split=args.split, batch=args.batch, imgsz=args.imgsz, 
                        conf=args.conf, half=args.half, device=args.device)  # results是validator.metrics
    print(results)

    # Perform object detection on an image using the model
    # results = model(f'{here}/lymonet/data/scripts/image.png')
    # print(results)

    # Export the model to ONNX format
    # success = model.export(format='onnx')

@dataclass
class Args:
    model: str =  '/home/tml/VSProjects/lymonet/lymonet/ultralytics/runs/classify/yolov8s_class10/weights/best.pt'
    mode: str = 'val'
    task: str = 'classify'
    val: bool = True
    # model: str =  f'{here}/lymonet/configs/yolov8s_1MHSA_CA.yaml'
    # model: str = "yolov8x.yaml"
    # weights: str = 'yolov8n.pt'
    # data: str = f'{here}/lymonet/configs/lymo_mixed2.yaml'
    data: str = "/data/tml/lymonet/lymo_yolo_square1"
    split: str = 'val'
    # epochs: int = 300
    batch: int = 32
    imgsz: int = 640
    workers: int = 16
    conf: float = 0.001  # confidence threshold
    device: str = '0'  # GPU id 
    half: bool = False  # use FP16 or NOT
    project: str = 'runs/val'
    name: str = 'lymonet'
    # merge_type: str = None
    
 
if __name__ == '__main__':
    args = hai.parse_args_into_dataclasses(Args)
    run(args)
