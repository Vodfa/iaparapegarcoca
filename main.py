import argparse
from pathlib import Path

from robot.arduino import ArduinoController
from robot.audio import AudioConfig, AudioInterface
from robot.config import load_config
from robot.controller import RobotController
from robot.ollama_client import OllamaClient
from robot.vision import VisionDetector


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Robô local com Ollama, YOLO e Arduino")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Caminho para o YAML de configuração",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    arduino = ArduinoController(
        port=config.arduino.port,
        baudrate=config.arduino.baudrate,
        timeout_s=config.arduino.timeout_s,
    )
    vision = VisionDetector(
        model_path=config.vision.model_path,
        camera_index=config.vision.camera_index,
        confidence_threshold=config.vision.confidence_threshold,
        focal_length_px=config.vision.focal_length_px,
        known_object_width_m=config.vision.known_object_width_m,
    )
    audio = AudioInterface(
        AudioConfig(
            input_device_index=config.audio.input_device_index,
            output_voice=config.audio.output_voice,
            language=config.audio.language,
        )
    )
    ollama = OllamaClient(
        base_url=config.ollama.base_url,
        model=config.ollama.model,
        temperature=config.ollama.temperature,
    )

    controller = RobotController(
        arduino=arduino,
        vision=vision,
        audio=audio,
        ollama=ollama,
        distance_mode=config.distance_mode,
    )

    try:
        while True:
            controller.run_once()
    except KeyboardInterrupt:
        pass
    finally:
        controller.close()


if __name__ == "__main__":
    main()
