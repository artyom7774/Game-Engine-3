class AngleVector:
    def __init__(self, angle: int, power: int, decreaseSpeed: int = 0) -> None:
        self.angle = angle
        self.power = power

        self.decreaseSpeed = decreaseSpeed

    def __str__(self) -> str:
        return f"AngleVector(power = {self.power} angle = {self.angle})"

    def __repr__(self) -> str:
        return f"AngleVector (power = {self.power} angle = {self.angle})"

    def rotate(self, angle: int) -> None:
        self.angle = (self.angle + angle) % 360

    def update(self) -> None:
        self.power -= self.decreaseSpeed
