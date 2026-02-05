from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import cv2
from ultralytics import YOLO


@dataclass
class Detection:
    label: str
    confidence: float
    bbox: Tuple[int, int, int, int]
    distance_m: Optional[float]


class VisionDetector:
    def __init__(
        self,
        model_path: str,
        camera_index: int,
        confidence_threshold: float,
        focal_length_px: float,
        known_object_width_m: float,
    ) -> None:
        self._model = YOLO(model_path)
        self._camera = cv2.VideoCapture(camera_index)
        if not self._camera.isOpened():
            raise RuntimeError(f"Não foi possível abrir a câmera {camera_index}.")
        self._confidence_threshold = confidence_threshold
        self._focal_length_px = focal_length_px
        self._known_object_width_m = known_object_width_m

    def close(self) -> None:
        self._camera.release()

    def _estimate_distance(self, bbox_width_px: int) -> Optional[float]:
        if bbox_width_px <= 0:
            return None
        return (self._known_object_width_m * self._focal_length_px) / bbox_width_px

    def detect(self) -> List[Detection]:
        success, frame = self._camera.read()
        if not success:
            return []
        results = self._model.predict(frame, verbose=False)
        detections: List[Detection] = []
        for result in results:
            for box in result.boxes:
                confidence = float(box.conf.item())
                if confidence < self._confidence_threshold:
                    continue
                class_id = int(box.cls.item())
                names = self._model.names
                if isinstance(names, dict):
                    label = names.get(class_id, str(class_id))
                else:
                    label = names[class_id] if class_id < len(names) else str(class_id)
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                width_px = max(x2 - x1, 0)
                distance = self._estimate_distance(width_px)
                detections.append(
                    Detection(
                        label=label,
                        confidence=confidence,
                        bbox=(x1, y1, x2, y2),
                        distance_m=distance,
                    )
                )
        return detections
