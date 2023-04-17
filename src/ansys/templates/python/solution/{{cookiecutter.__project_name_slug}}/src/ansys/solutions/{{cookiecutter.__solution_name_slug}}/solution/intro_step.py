# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the introduction step."""


from ansys.saf.glow.solution import StepModel


class IntroStep(StepModel):
    """Step definition of the introduction step."""

    id: str = "hey"
