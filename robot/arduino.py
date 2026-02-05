from dataclasses import dataclass
from typing import Optional

import serial


@dataclass
class CommandResult:
    ok: bool
    response: str


class ArduinoController:
    def __init__(self, port: str, baudrate: int, timeout_s: float) -> None:
        self._serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout_s)

    def close(self) -> None:
        self._serial.close()

    def send(self, command: str) -> CommandResult:
        payload = f"{command.strip()}\n".encode("utf-8")
        self._serial.write(payload)
        response = self._serial.readline().decode("utf-8").strip()
        return CommandResult(ok=response.startswith("OK"), response=response)

    def lift(self) -> CommandResult:
        return self.send("LIFT")

    def move_arm(self, angle: int) -> CommandResult:
        return self.send(f"ARM:{angle}")

    def grab(self) -> CommandResult:
        return self.send("GRAB")

    def release(self) -> CommandResult:
        return self.send("RELEASE")

    def walk(self, direction: str, steps: int) -> CommandResult:
        return self.send(f"WALK:{direction}:{steps}")

    def rotate(self, direction: str, degrees: int) -> CommandResult:
        return self.send(f"ROTATE:{direction}:{degrees}")

    def read_distance(self) -> Optional[float]:
        result = self.send("DIST")
        if not result.ok:
            return None
        try:
            return float(result.response.split(":")[-1])
        except ValueError:
            return None
