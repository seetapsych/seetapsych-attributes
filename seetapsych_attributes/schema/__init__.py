# -*- coding: utf-8 -*-


from pydantic import BaseModel

from . import face

schema: dict[str, type[BaseModel]] = {
    'face/detection': face.detection.Report,
    'face/landmarks': face.landmarks.Report,
    'face/selection': face.selection.Report,
    'face/action_units': face.action_units.Report,
    'face/expression': face.expression.Report,
}
