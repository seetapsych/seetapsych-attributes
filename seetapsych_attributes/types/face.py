# -*- coding: utf-8 -*-

from typing import TypedDict

__all__ = [
    "BBox",
    "FaceDetection",
    "Landmarks",
    "FaceLandmarks",
    "Selection",
    "FaceSelection",
    "ActionUnits",
    "FaceActionUnits",
    "Expression",
    "FaceExpression",
    "DenseLandmarks",
    "FaceDenseLandmarks",
    "MeshLandmarks",
    "FaceMesh",
    "GazePoint",
    "GazeData",
    "GazeScreen",
    "FaceGazeScreen",
    "HeartRate",
    "FaceHeartRate",
    "DimensionalAffect",
    "FaceDimensionalAffect",
]


class BBox(TypedDict):
    """Rectangular face detection result with confidence score."""

    # [x1, y1, x2, y2] -- pixel-coordinate bounding box
    xyxy: list[float]
    # detection confidence in [0, 1]
    score: float


# List of all detected faces (bounding boxes).
FaceDetection = list[BBox]


class Landmarks(TypedDict):
    """Basic 5-point facial landmarks used for rough alignment."""

    # 5-point interleaved [x,y]: L-eye, R-eye, nose, L-mouth, R-mouth
    landmarks: list[float]


# List of basic 5-point landmarks per detected face.
FaceLandmarks = list[Landmarks]


class Selection(TypedDict):
    """Result of face selection, referencing a single picked detection."""

    # selected face PID, auto-incremented starting from 1
    pid: int


# Alias: face-level selection output.
FaceSelection = Selection


class ActionUnits(TypedDict, total=False):
    """Facial Action Unit activations (FACS). All fields optional."""

    # [0,1] -- Inner Brow Raiser
    AU1: float
    # [0,1] -- Outer Brow Raiser
    AU2: float
    # [0,1] -- Brow Lowerer
    AU4: float
    # [0,1] -- Upper Lid Raiser
    AU5: float
    # [0,1] -- Cheek Raiser
    AU6: float
    # [0,1] -- Lid Tightener
    AU7: float
    # [0,1] -- Nose Wrinkler
    AU9: float
    # [0,1] -- Upper Lip Raiser
    AU10: float
    # [0,1] -- Lip Corner Puller
    AU12: float
    # [0,1] -- Lip Corner Depressor
    AU15: float
    # [0,1] -- Chin Raiser
    AU17: float
    # [0,1] -- Lip Stretcher
    AU20: float
    # [0,1] -- Lip Tightener
    AU23: float
    # [0,1] -- Lip Pressor
    AU24: float
    # [0,1] -- Lips Part
    AU25: float
    # [0,1] -- Jaw Drop
    AU26: float


# Per-face list of Action Unit confidence results.
FaceActionUnits = list[ActionUnits]


class Expression(TypedDict, total=False):
    """Discrete 7-class expression confidence scores. All fields optional."""

    # confidence in [0, 1]
    neutral: float
    # confidence in [0, 1]
    anger: float
    # confidence in [0, 1]
    disgust: float
    # confidence in [0, 1]
    fear: float
    # confidence in [0, 1]
    happy: float
    # confidence in [0, 1]
    sad: float
    # confidence in [0, 1]
    surprise: float


# Per-face list of discrete expression results.
FaceExpression = list[Expression]


class DenseLandmarks(TypedDict):
    """280-point dense facial landmarks for detailed alignment."""

    # 280-point interleaved [x,y], 560 floats total
    landmarks: list[float]


# Per-face list of dense landmark results.
FaceDenseLandmarks = list[DenseLandmarks]


class MeshLandmarks(TypedDict):
    """468-point 3D face mesh in normalized coordinates."""

    # 468 pts x [x,y,z] = 1404 normalized floats
    normalized_3d_landmarks: list[float]


# Per-face list of 3D mesh landmark results.
FaceMesh = list[MeshLandmarks]


class GazePoint(TypedDict):
    """Point-of-gaze coordinates for two eyes in either screen-pixel or camera-millimeter space."""

    # gaze-screen-px [x,y] or gaze-camera-mm [x,y(,z)]; 2D/3D depending on algorithm; empty if unavailable
    left_eye: list[float]
    # screen-px [x,y] or camera-mm [x,y(,z)]; 2D/3D depending on algorithm; empty if unavailable
    right_eye: list[float]


class GazeData(TypedDict):
    """Gaze estimation result for a single face."""

    # whether gaze estimation succeeded for this face
    success: bool
    # per-eye point-of-gaze in screen-space pixels; origin at left top corner of the screen
    gaze_screen_px: GazePoint
    # per-eye point-of-gaze in camera-space millimeters; origin at camera optical center;
    # 2D on image plane or 3D in camera space depending on algorithm
    gaze_camera_mm: GazePoint


class GazeScreen(TypedDict):
    """Wrapper for per-face gaze data in face/gaze_screen schema."""

    # per-face gaze estimation payload
    gaze: GazeData


# List of per-face gaze screen results.
FaceGazeScreen = list[GazeScreen]


class HeartRate(TypedDict, total=False):
    """Heart rate estimation in BPM.

    Fields are optional until enough video frames have been buffered.
    """

    # estimated FPS of the incoming stream
    fps: float
    # seconds until buffer is fully populated; 0.0 means HR is ready
    wait_seconds: float
    # estimated BPM; present only when estimation is ready
    hr_bpm: float


# Alias: face-level heart-rate output.
FaceHeartRate = HeartRate


class DimensionalAffect(TypedDict):
    """Continuous valence/arousal coordinates in Russell's affect space."""

    # valence axis: positive = pleasant, negative = unpleasant
    valence: float
    # arousal axis: positive = activated, negative = calm
    arousal: float


# Per-face list of continuous valence/arousal results.
FaceDimensionalAffect = list[DimensionalAffect]
