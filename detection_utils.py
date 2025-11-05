from PIL import Image, ImageDraw
import random
import numpy as np

try:
    from ultralytics import YOLO as YOLO_Model
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

YOLO = False   # set True when you want to use the trained YOLO model
MODEL_PATH = "runs/detect/train/weights/best.pt"  # path to your model weights
DUMMY_ITEMS = ["CocaCola", "Pepsi", "Sprite", "Kinley", "ThumbsUp", "MountainDew"]

def run_yolo_inference(image: Image.Image):
    """
    Runs YOLO inference if enabled, else runs dummy detection.
    Returns:
      annotated_image (PIL.Image)
      counts (dict: item_name → count)
      boxes (list of tuples: (label, (x1, y1, x2, y2)))
    """
    if not YOLO or not YOLO_AVAILABLE:
        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)
        w, h = image.size
        counts = {}
        boxes = []

        for i, label in enumerate(DUMMY_ITEMS[:random.randint(3, 5)]):
            x1 = random.randint(0, int(w * 0.7))
            y1 = random.randint(0, int(h * 0.7))
            x2 = x1 + random.randint(int(w * 0.1), int(w * 0.2))
            y2 = y1 + random.randint(int(h * 0.1), int(h * 0.2))

            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            draw.text((x1 + 5, y1 + 5), label, fill="white")
            count = random.randint(10, 20)
            counts[label] = count
            boxes.append((label, (x1, y1, x2, y2)))

        return annotated, counts, boxes

    else:
        if not MODEL_PATH:
            raise FileNotFoundError("❌ MODEL_PATH not set for YOLO mode")

        global _YOLO_MODEL
        if '_YOLO_MODEL' not in globals():
            _YOLO_MODEL = YOLO_Model(MODEL_PATH)

        # Convert PIL → numpy
        img_np = np.array(image.convert("RGB"))

        # Run inference
        results = _YOLO_MODEL.predict(img_np, imgsz=640, conf=0.4, verbose=False)
        res = results[0]

        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)
        counts = {}
        boxes = []

        names = res.names if hasattr(res, "names") else {}

        for box in res.boxes:
            xyxy = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = map(int, xyxy)
            cls = int(box.cls.cpu().numpy())
            label = names.get(cls, f"class_{cls}")
            conf = float(box.conf.cpu().numpy())

            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            draw.text((x1 + 5, y1 + 5), f"{label} ({conf:.2f})", fill="white")

            counts[label] = counts.get(label, 0) + 1
            boxes.append((label, (x1, y1, x2, y2)))

        return annotated, counts, boxes
