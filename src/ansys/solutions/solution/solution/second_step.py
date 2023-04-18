# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the second step."""


from ansys.saf.glow.solution import StepModel


class SecondStep(StepModel):
    """Step definition of the second step."""

    id: str = "hey"
