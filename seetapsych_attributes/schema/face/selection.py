# -*- coding: utf-8 -*-


from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "Report",
]


class Selection(BaseModel):
    pid: int = Field(
        ...,
        description="PID of selected face detection (1-based).",
    )


class Report(BaseModel):
    face_selection: Selection

    model_config = ConfigDict(
        title="face/selection",
        json_schema_extra={
            "description": (
                "Selected face PID. Selected face order is reflected in face/detection and face/landmarks."
            ),
            "examples": [
                {
                    "face_selection": {"pid": 1},
                    "face_detection": [{"xyxy": [100, 200, 300, 400], "score": 0.5}],
                }
            ],
        },
    )
