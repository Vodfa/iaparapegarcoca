from dataclasses import dataclass
from typing import List, Optional

from robot.arduino import ArduinoController
from robot.audio import AudioInterface
from robot.ollama_client import Message, OllamaClient
from robot.vision import Detection, VisionDetector


@dataclass
class RobotState:
    last_detections: List[Detection]
    last_distance_m: Optional[float]


class RobotController:
    def __init__(
        self,
        arduino: ArduinoController,
        vision: VisionDetector,
        audio: AudioInterface,
        ollama: OllamaClient,
        distance_mode: str,
    ) -> None:
        self._arduino = arduino
        self._vision = vision
        self._audio = audio
        self._ollama = ollama
        self._distance_mode = distance_mode
        self._state = RobotState(last_detections=[], last_distance_m=None)

    def close(self) -> None:
        self._vision.close()
        self._arduino.close()

    def update_perception(self) -> RobotState:
        detections = self._vision.detect()
        distance = None
        if self._distance_mode == "sensor":
            distance = self._arduino.read_distance()
        elif detections:
            distance = detections[0].distance_m
        self._state = RobotState(last_detections=detections, last_distance_m=distance)
        return self._state

    def handle_command(self, command: str) -> str:
        normalized = command.lower()
        if "levantar" in normalized:
            result = self._arduino.lift()
            return f"Comando lift: {result.response}"
        if "braco" in normalized or "braço" in normalized:
            result = self._arduino.move_arm(90)
            return f"Comando braço: {result.response}"
        if "pegar" in normalized:
            result = self._arduino.grab()
            return f"Comando pegar: {result.response}"
        if "soltar" in normalized:
            result = self._arduino.release()
            return f"Comando soltar: {result.response}"
        if "andar" in normalized:
            result = self._arduino.walk("forward", 3)
            return f"Comando andar: {result.response}"
        if "girar" in normalized:
            result = self._arduino.rotate("left", 45)
            return f"Comando girar: {result.response}"
        return "Comando não reconhecido."

    def chat(self, user_text: str) -> str:
        context = []
        if self._state.last_detections:
            labels = ", ".join(d.label for d in self._state.last_detections[:5])
            context.append(f"Objetos detectados: {labels}.")
        if self._state.last_distance_m is not None:
            context.append(f"Distância estimada: {self._state.last_distance_m:.2f} m.")
        system_prompt = (
            "Você é o cérebro de um robô doméstico com visão, locomoção e braço. "
            "Responda em português e seja direto ao orientar o usuário."
        )
        messages = [Message(role="system", content=system_prompt)]
        if context:
            messages.append(Message(role="system", content=" ".join(context)))
        messages.append(Message(role="user", content=user_text))
        return self._ollama.chat(messages)

    def run_once(self) -> None:
        self.update_perception()
        user_text = self._audio.listen()
        if not user_text:
            return
        response = self.chat(user_text)
        action_feedback = self.handle_command(user_text)
        self._audio.speak(f"{response} {action_feedback}")
