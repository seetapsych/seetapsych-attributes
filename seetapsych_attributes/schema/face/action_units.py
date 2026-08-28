# -*- coding: utf-8 -*-

from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class ActionUnits(BaseModel):
    AU1: float = Field(None, description="`[0, 1]`. Inner Brow Raiser.")
    AU2: float = Field(None, description="`[0, 1]`. Outer Brow Raiser.")
    AU4: float = Field(None, description="`[0, 1]`. Brow Lowerer.")
    AU5: float = Field(None, description="`[0, 1]`. Upper Lid Raiser.")
    AU6: float = Field(None, description="`[0, 1]`. Cheek Raiser.")
    AU7: float = Field(None, description="`[0, 1]`. Lid Tightener.")
    AU9: float = Field(None, description="`[0, 1]`. Nose Wrinkler.")
    AU10: float = Field(None, description="`[0, 1]`. Upper Lip Raiser.")
    AU12: float = Field(None, description="`[0, 1]`. Lip Corner Puller.")
    AU15: float = Field(None, description="`[0, 1]`. Lip Corner Depressor.")
    AU17: float = Field(None, description="`[0, 1]`. Chin Raiser.")
    AU20: float = Field(None, description="`[0, 1]`. Lip Stretcher.")
    AU23: float = Field(None, description="`[0, 1]`. Lip Tightener.")
    AU24: float = Field(None, description="`[0, 1]`. Lip Pressor.")
    AU25: float = Field(None, description="`[0, 1]`. Lips Part.")
    AU26: float = Field(None, description="`[0, 1]`. Jaw Drop.")


class Report(BaseModel):
    face_action_units: list[ActionUnits]

    model_config = ConfigDict(
        title="face/action_units",
        json_schema_extra={
            "x-brief": "Indicate the confidence level of each Action Unit. "
                       "Not all Action Units' results may be output.",
            "examples": [{
                "face_action_units": [
                    {
                        "AU1": 0.5,
                        "AU2": 0.5,
                        "AU4": 0.5,
                        "AU5": 0.5,
                        "AU6": 0.5,
                        "AU7": 0.5,
                        "AU9": 0.5,
                        "AU10": 0.5,
                        "AU12": 0.5,
                        "AU15": 0.5,
                        "AU17": 0.5,
                        "AU20": 0.5,
                        "AU23": 0.5,
                        "AU24": 0.5,
                        "AU25": 0.5,
                        "AU26": 0.5,
                    },
                ],
            }]
        }
    )
