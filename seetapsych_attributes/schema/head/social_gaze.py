# -*- coding: utf-8 -*-

from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class SocialGazePerson(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    head_location_xyxy: Annotated[list[int], Field(min_length=4, max_length=4)]
    gaze_point_px: Annotated[list[float], Field(min_length=2, max_length=2)]
    heatmap: Any = Field(
        ...,
        description=(
            "2D gaze likelihood heatmap. "
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
    social_gaze_id: int = Field(..., description="Integer ID of the social gaze relation class.")
    social_gaze_label: str = Field(..., description="Human-readable label of the social gaze relation (e.g. looking-at, mutual, avert).")


class HeadSocialGaze(BaseModel):
    principal: Optional[SocialGazePerson] = Field(None, description="Left-side / primary person in dyadic interaction.")
    associate: Optional[SocialGazePerson] = Field(None, description="Right-side / secondary person in dyadic interaction.")
    success: bool = Field(True, description="Whether at least two heads were detected for social gaze inference.")


class Report(BaseModel):
    head_social_gaze: HeadSocialGaze

    model_config = ConfigDict(
        title="head/social_gaze",
        json_schema_extra={
            "description": "Dyadic social gaze relations (looking-at, mutual, avert) between two detected people.",
            "examples": [{
                "head_social_gaze": {
                    "success": True,
                    "principal": {
                        "head_location_xyxy": [100, 200, 300, 400],
                        "gaze_point_px": [800.0, 300.0],
                        "heatmap": "numpy.ndarray(shape=[H, W], dtype=float32) — 2D [0,1] gaze likelihood heatmap",
                        "social_gaze_id": 0,
                        "social_gaze_label": "looking-at",
                    },
                    "associate": {
                        "head_location_xyxy": [600, 200, 800, 400],
                        "gaze_point_px": [200.0, 300.0],
                        "heatmap": "numpy.ndarray(shape=[H, W], dtype=float32) — 2D [0,1] gaze likelihood heatmap",
                        "social_gaze_id": 0,
                        "social_gaze_label": "looking-at",
                    },
                }
            }, {
                "head_social_gaze": {
                    "success": False,
                }
            }]
        }
    )
