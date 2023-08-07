# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

MONITORING_TABS = [
    {
        "label": "Project Summary",
        "tab_id": "project_summary_tab",
        "is_root": True,
        "is_system": False,
        "is_actor": False,
    },
    {"label": "Summary", "tab_id": "summary_tab", "is_root": False, "is_system": True, "is_actor": True},
    {"label": "Result Files", "tab_id": "result_files_tab", "is_root": True, "is_system": False, "is_actor": False},
    {"label": "Scenery", "tab_id": "scenery_tab", "is_root": True, "is_system": False, "is_actor": False},
    {"label": "Design Table", "tab_id": "design_table_tab", "is_root": True, "is_system": True, "is_actor": False},
    {"label": "Visualization", "tab_id": "visualization_tab", "is_root": True, "is_system": True, "is_actor": False},
    {"label": "Status Overview", "tab_id": "status_overview_tab", "is_root": True, "is_system": True, "is_actor": True},
]

PROJECT_STATES = {
    "NOT STARTED": {
        "alert": "optiSLang project not started.",
        "color": "warning"
    },
    "IDLE": {
        "alert": "optiSLang project is pending.",
        "color": "warning"
    },
    "PROCESSING": {
        "alert": "optiSLang project in progress.",
        "color": "primary"
    },
    "PAUSED": {
        "alert": "optiSLang project paused.",
        "color": "warning"
    },
    "PAUSE_REQUESTED": {
        "alert": "optiSLang project requested to pause.",
        "color": "warning"
    },
    "STOPPED": {
        "alert": "optiSLang project stopped.",
        "color": "warning"
    },
    "STOP_REQUESTED": {
        "alert": "optiSLang project requetsed to stop.",
        "color": "warning"
    },
    "GENTLY_STOPPED": {
        "alert": "optiSLang project gently stopped.",
        "color": "warning"
    },
    "GENTLE_STOP_REQUESTED": {
        "alert": "optiSLang project requested to gently stop.",
        "color": "warning"
    },
    "FINISHED": {
        "alert": "optiSLang project completed successfully.",
        "color": "success"
    },
}
