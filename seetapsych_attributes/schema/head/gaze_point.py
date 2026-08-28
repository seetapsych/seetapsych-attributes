# -*- coding: utf-8 -*-

from typing import Annotated, Any

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class HeadGazePoint(BaseModel):
    head_location_xyxy: Annotated[list[int], Field(min_length=4, max_length=4)]
    gaze_point_px: Annotated[list[float], Field(min_length=2, max_length=2)]
    heatmap: list[list[float]] = Field(..., description="2D heatmap array of gaze likelihood over the scene.")


class Report(BaseModel):
    head_gaze_point: list[HeadGazePoint]

    model_config = ConfigDict(
        title="head/gaze_point",
        json_schema_extra={
            "x-brief": "Predict per-head 2D gaze target point on scene image using CoSI transformer model with heatmap.",
            "examples": [{
                "head_gaze_point": [
                    {
                        "head_location_xyxy": [100, 200, 300, 400],
                        "gaze_point_px": [640.0, 360.0],
                        "heatmap": [[0.1, 0.2], [0.3, 0.4]],
                    }
                ]
            }]
        }
    )
