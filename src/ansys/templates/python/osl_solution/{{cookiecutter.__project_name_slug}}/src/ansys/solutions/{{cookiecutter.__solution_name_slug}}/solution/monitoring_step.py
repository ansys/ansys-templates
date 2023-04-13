# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the monitoring step."""


from ansys.saf.glow.solution import StepModel


class MonitoringStep(StepModel):
    """Step definition of the monitoring step."""

    id: str = "hey"
