from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

import yaml

DistanceMode = Literal["sensor", "vision"]


@dataclass
class AudioConfig:
    input_device_index: Optional[int]
    output_voice: Optional[str]
    language: str


@dataclass
class VisionConfig:
    model_path: str
    camera_index: int
    confidence_threshold: float
    focal_length_px: float
    known_object_width_m: float


@dataclass
class OllamaConfig:
    base_url: str
    model: str
    temperature: float


@dataclass
class ArduinoConfig:
    port: str
    baudrate: int
    timeout_s: float


@dataclass
class RobotConfig:
    distance_mode: DistanceMode
    audio: AudioConfig
    vision: VisionConfig
    ollama: OllamaConfig
    arduino: ArduinoConfig


def load_config(path: Path) -> RobotConfig:
    data = yaml.safe_load(path.read_text())
    audio = AudioConfig(**data["audio"])
    vision = VisionConfig(**data["vision"])
    ollama = OllamaConfig(**data["ollama"])
    arduino = ArduinoConfig(**data["arduino"])
    return RobotConfig(
        distance_mode=data["distance_mode"],
        audio=audio,
        vision=vision,
        ollama=ollama,
        arduino=arduino,
    )
