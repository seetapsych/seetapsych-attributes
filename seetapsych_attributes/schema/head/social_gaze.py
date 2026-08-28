# -*- coding: utf-8 -*-

from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class SocialGazePerson(BaseModel):
    head_location_xyxy: Annotated[list[int], Field(min_length=4, max_length=4)]
    gaze_point_px: Annotated[list[float], Field(min_length=2, max_length=2)]
    heatmap: list[list[float]] = Field(..., description="2D heatmap array of gaze likelihood.")
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
            "x-brief": "Infer social gaze relations (looking-at, mutual, avert) between pairs of people via CoSI dyadic model.",
            "examples": [{
                "head_social_gaze": {
                    "success": True,
                    "principal": {
                        "head_location_xyxy": [100, 200, 300, 400],
                        "gaze_point_px": [800.0, 300.0],
                        "heatmap": [[0.1, 0.2], [0.3, 0.4]],
                        "social_gaze_id": 0,
                        "social_gaze_label": "looking-at",
                    },
                    "associate": {
                        "head_location_xyxy": [600, 200, 800, 400],
                        "gaze_point_px": [200.0, 300.0],
                        "heatmap": [[0.2, 0.1], [0.4, 0.3]],
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
