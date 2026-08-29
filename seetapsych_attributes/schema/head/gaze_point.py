# -*- coding: utf-8 -*-

from typing import Annotated, Any

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class HeadGazePoint(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    head_location_xyxy: Annotated[list[int], Field(min_length=4, max_length=4)]
    gaze_point_px: Annotated[list[float], Field(min_length=2, max_length=2)]
    heatmap: Any = Field(
        ...,
        description=(
            "2D gaze likelihood heatmap over the scene. "
            "Runtime type: numpy.ndarray of float32, "
            "shape [image_height, image_width], values in [0, 1] probability range. "
            "Serialize with .tolist() to 2D nested number array for JSON transport."
        ),
        json_schema_extra={
            "type": "array",
            "items": {"type": "array", "items": {"type": "number"}},
            "example_description": (
                "numpy.ndarray(shape=[H, W], dtype=float32) — "
                "use .tolist() to serialize to nested list for JSON transport."
            ),
        },
    )


class Report(BaseModel):
    head_gaze_point: list[HeadGazePoint]

    model_config = ConfigDict(
        title="head/gaze_point",
        json_schema_extra={
            "description": "Per-head 2D scene gaze target point with associated likelihood heatmap.",
            "examples": [{
                "head_gaze_point": [
                    {
                        "head_location_xyxy": [100, 200, 300, 400],
                        "gaze_point_px": [640.0, 360.0],
                        "heatmap": "numpy.ndarray(shape=[H, W], dtype=float32) — 2D [0,1] gaze likelihood heatmap",
                    }
                ]
            }]
        }
    )
