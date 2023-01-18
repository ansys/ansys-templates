# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the first step."""


from ansys.saf.glow.solution import StepModel


class FirstStep(StepModel):
    """Step definition of the first step."""

    id: str = "hey"
