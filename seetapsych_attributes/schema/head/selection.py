# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "Report",
]


class HeadSelection(BaseModel):
    count: int = Field(..., description="Number of selected head detections.")
    selected_indices: list[int] = Field(
        ...,
        description=("Indices of selected detections in the original head_detection list, before sorting."),
    )


class Report(BaseModel):
    head_selection: HeadSelection

    model_config = ConfigDict(
        title="head/selection",
        json_schema_extra={
            "description": ("Top-N head selection result (count + original indices), reordering head_detection."),
            "examples": [
                {
                    "head_selection": {
                        "count": 1,
                        "selected_indices": [0],
                    },
                    "head_detection": [
                        {
                            "xyxy": [100, 200, 300, 400],
                            "score": 0.85,
                        }
                    ],
                }
            ],
        },
    )
