# -*- coding: utf-8 -*-

from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class Selection(BaseModel):
    pid: int = Field(
        ...,
        description="PID of selected face detection. It will automatically update starting from 1.",
    )


class Report(BaseModel):
    face_selection: list[Selection]

    model_config = ConfigDict(
        title="face/selection",
        json_schema_extra={
            "x-brief": "Indicates the result of face selection. "
                       "It will update the properties of face/detection and face/landmarks.",
            "examples": [{
                "face_selection": {
                    "pid": 1
                },
                "face_detection": [
                    {
                        "xyxy": [100, 200, 300, 400],
                        "score": 0.5
                    }
                ]
            }]
        }
    )
