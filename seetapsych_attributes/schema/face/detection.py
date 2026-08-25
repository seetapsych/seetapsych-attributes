# -*- coding: utf-8 -*-

from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class BBox(BaseModel):
    xyxy: Annotated[list[float], Field(min_length=4, max_length=4)]
    score: float


class Report(BaseModel):
    face_detection: list[BBox]

    model_config = ConfigDict(
        title="face/detection",
        json_schema_extra={
            "x-brief": "Obtain the face detection results, represented as rectangular bounding boxes.",
            "examples": [{
                "face_detection": [
                    {
                        "xyxy": [100, 200, 300, 400],
                        "score": 0.5
                    }
                ]
            }]
        }
    )
