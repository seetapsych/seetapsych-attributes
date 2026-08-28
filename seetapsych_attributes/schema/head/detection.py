# -*- coding: utf-8 -*-

from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class HeadBBox(BaseModel):
    xyxy: Annotated[list[int], Field(min_length=4, max_length=4)]
    score: float


class Report(BaseModel):
    head_detection: list[HeadBBox]

    model_config = ConfigDict(
        title="head/detection",
        json_schema_extra={
            "x-brief": "YOLO-based multi-person head detection with configurable confidence and NMS thresholds.",
            "examples": [{
                "head_detection": [
                    {
                        "xyxy": [100, 200, 300, 400],
                        "score": 0.85,
                    }
                ]
            }]
        }
    )
