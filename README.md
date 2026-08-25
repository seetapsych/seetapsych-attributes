# SeetaPsych Attributes

> Face and body based psychology analysis

SeetaPsych Lib is a Python library for face- and body-based psychology analysis.
It provides a modular Pipeline/Runner runtime and an optional Streamlit WebUI.

This project is used to manage the specifications for various attribute outputs,
providing a unified standard so that different algorithm implementations can produce interchangeable and reusable module outputs.

## Catalog

- [face/detection](#facedetection) Obtain the face detection results, represented as rectangular bounding boxes.
- [face/landmarks](#facelandmarks) Get facial landmarks for basic alignment, including the centers of the left and right eyes, the nose tip, and the positions of the left and right mouth corners.
- [face/selection](#faceselection) Indicates the result of face selection. It will update the properties of face/detection and face/landmarks.
- [face/action_units](#faceaction_units) Indicate the confidence level of each Action Unit. Not all Action Units' results may be output.
- [face/expression](#faceexpression) Indicate the confidence level of each expression.

<a id="facedetection"></a>

## face/detection

### Properties

- <a id="properties/face_detection"></a>**`face_detection`** *(array, required)*
  - <a id="properties/face_detection/items"></a>**Items**: Refer to *[#/$defs/BBox](#%24defs/BBox)*.

### Definitions

- <a id="%24defs/BBox"></a>**`BBox`** *(object)*
  - <a id="%24defs/BBox/properties/xyxy"></a>**`xyxy`** *(array, required)*: Length must be equal to 4.
    - <a id="%24defs/BBox/properties/xyxy/items"></a>**Items** *(number)*
  - <a id="%24defs/BBox/properties/score"></a>**`score`** *(number, required)*

### Examples

  ```json
  {
      "face_detection": [
          {
              "score": 0.5,
              "xyxy": [
                  100,
                  200,
                  300,
                  400
              ]
          }
      ]
  }
  ```



<a id="facelandmarks"></a>

## face/landmarks

### Properties

- <a id="properties/face_landmarks"></a>**`face_landmarks`** *(array, required)*
  - <a id="properties/face_landmarks/items"></a>**Items**: Refer to *[#/$defs/Landmarks](#%24defs/Landmarks)*.

### Definitions

- <a id="%24defs/Landmarks"></a>**`Landmarks`** *(object)*
  - <a id="%24defs/Landmarks/properties/landmarks"></a>**`landmarks`** *(array, required)*: Length must be equal to 10.
    - <a id="%24defs/Landmarks/properties/landmarks/items"></a>**Items** *(number)*

### Examples

  ```json
  {
      "face_landmarks": [
          {
              "landmarks": [
                  100,
                  100,
                  200,
                  200,
                  300,
                  300,
                  400,
                  400,
                  500,
                  500
              ]
          }
      ]
  }
  ```



<a id="faceselection"></a>

## face/selection

### Properties

- <a id="properties/face_selection"></a>**`face_selection`** *(array, required)*
  - <a id="properties/face_selection/items"></a>**Items**: Refer to *[#/$defs/Selection](#%24defs/Selection)*.

### Definitions

- <a id="%24defs/Selection"></a>**`Selection`** *(object)*
  - <a id="%24defs/Selection/properties/pid"></a>**`pid`** *(integer, required)*: PID of selected face detection. It will automatically update starting from 1.

### Examples

  ```json
  {
      "face_detection": [
          {
              "score": 0.5,
              "xyxy": [
                  100,
                  200,
                  300,
                  400
              ]
          }
      ],
      "face_selection": {
          "pid": 1
      }
  }
  ```



<a id="faceaction_units"></a>

## face/action_units

### Properties

- <a id="properties/action_units"></a>**`action_units`** *(required)*: Refer to *[#/$defs/ActionUnits](#%24defs/ActionUnits)*.

### Definitions

- <a id="%24defs/ActionUnits"></a>**`ActionUnits`** *(object)*
  - <a id="%24defs/ActionUnits/properties/AU1"></a>**`AU1`** *(number)*: `[0, 1]`. Inner Brow Raiser. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU2"></a>**`AU2`** *(number)*: `[0, 1]`. Outer Brow Raiser. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU4"></a>**`AU4`** *(number)*: `[0, 1]`. Brow Lowerer. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU5"></a>**`AU5`** *(number)*: `[0, 1]`. Upper Lid Raiser. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU6"></a>**`AU6`** *(number)*: `[0, 1]`. Cheek Raiser. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU7"></a>**`AU7`** *(number)*: `[0, 1]`. Lid Tightener. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU9"></a>**`AU9`** *(number)*: `[0, 1]`. Nose Wrinkler. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU10"></a>**`AU10`** *(number)*: `[0, 1]`. Upper Lip Raiser. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU12"></a>**`AU12`** *(number)*: `[0, 1]`. Lip Corner Puller. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU15"></a>**`AU15`** *(number)*: `[0, 1]`. Lip Corner Depressor. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU17"></a>**`AU17`** *(number)*: `[0, 1]`. Chin Raiser. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU20"></a>**`AU20`** *(number)*: `[0, 1]`. Lip Stretcher. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU23"></a>**`AU23`** *(number)*: `[0, 1]`. Lip Tightener. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU24"></a>**`AU24`** *(number)*: `[0, 1]`. Lip Pressor. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU25"></a>**`AU25`** *(number)*: `[0, 1]`. Lips Part. Default: `null`.
  - <a id="%24defs/ActionUnits/properties/AU26"></a>**`AU26`** *(number)*: `[0, 1]`. Jaw Drop. Default: `null`.

### Examples

  ```json
  {
      "face_action_units": {
          "AU1": 0.5,
          "AU10": 0.5,
          "AU12": 0.5,
          "AU15": 0.5,
          "AU17": 0.5,
          "AU2": 0.5,
          "AU20": 0.5,
          "AU23": 0.5,
          "AU24": 0.5,
          "AU25": 0.5,
          "AU26": 0.5,
          "AU4": 0.5,
          "AU5": 0.5,
          "AU6": 0.5,
          "AU7": 0.5,
          "AU9": 0.5
      }
  }
  ```



<a id="faceexpression"></a>

## face/expression

### Properties

- <a id="properties/expression"></a>**`expression`** *(required)*: Refer to *[#/$defs/Expression](#%24defs/Expression)*.

### Definitions

- <a id="%24defs/Expression"></a>**`Expression`** *(object)*
  - <a id="%24defs/Expression/properties/neutral"></a>**`neutral`** *(number)*: Confidence in `[0, 1]`. Default: `null`.
  - <a id="%24defs/Expression/properties/anger"></a>**`anger`** *(number)*: Confidence in `[0, 1]`. Default: `null`.
  - <a id="%24defs/Expression/properties/disgust"></a>**`disgust`** *(number)*: Confidence in `[0, 1]`. Default: `null`.
  - <a id="%24defs/Expression/properties/fear"></a>**`fear`** *(number)*: Confidence in `[0, 1]`. Default: `null`.
  - <a id="%24defs/Expression/properties/happy"></a>**`happy`** *(number)*: Confidence in `[0, 1]`. Default: `null`.
  - <a id="%24defs/Expression/properties/sad"></a>**`sad`** *(number)*: Confidence in `[0, 1]`. Default: `null`.
  - <a id="%24defs/Expression/properties/surprise"></a>**`surprise`** *(number)*: Confidence in `[0, 1]`. Default: `null`.

### Examples

  ```json
  {
      "face_expression": {
          "anger": 0.01,
          "disgust": 0.01,
          "fear": 0.01,
          "happy": 0.94,
          "neutral": 0.01,
          "sad": 0.01,
          "surprise": 0.01
      }
  }
  ```
