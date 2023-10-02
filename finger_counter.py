
import time
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

class FingerCounter():
   def __init__(self):
      self.result = mp.tasks.vision.HandLandmarkerResult
      self.landmarker = mp.tasks.vision.HandLandmarker
      self.model_path = "model/hand_landmarker.task"
      self.createLandmarker()
   
   def createLandmarker(self):
 
      def update_result(result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
         self.result = result


      options = mp.tasks.vision.HandLandmarkerOptions( 
         base_options = mp.tasks.BaseOptions(model_asset_path=self.model_path),
         running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM, 
         num_hands = 2,
         min_hand_detection_confidence = 0.3, 
         min_hand_presence_confidence = 0.3,
         min_tracking_confidence = 0.3,
         result_callback=update_result)
      
      self.landmarker = self.landmarker.create_from_options(options)
   
   def detect_async(self, frame):
      mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
      self.landmarker.detect_async(image = mp_image, timestamp_ms = int(time.time() * 1000))

   def close(self):
      self.landmarker.close()

def draw_landmarks_on_image(rgb_image, detection_result: mp.tasks.vision.HandLandmarkerResult):
      try:
         if detection_result.hand_landmarks == []:
            return rgb_image
         else:
            hand_landmarks_list = detection_result.hand_landmarks
            handedness_list = detection_result.handedness
            annotated_image = np.copy(rgb_image)


            for idx in range(len(hand_landmarks_list)):
               hand_landmarks = hand_landmarks_list[idx]


               hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
               hand_landmarks_proto.landmark.extend([
                  landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks])
               mp.solutions.drawing_utils.draw_landmarks(
                  annotated_image,
                  hand_landmarks_proto,
                  mp.solutions.hands.HAND_CONNECTIONS,
                  mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                  mp.solutions.drawing_styles.get_default_hand_connections_style())

            return annotated_image
      except:
         return rgb_image

def count_fingers_raised(rgb_image, detection_result: mp.tasks.vision.HandLandmarkerResult):
      # https://developers.google.com/mediapipe/solutions/vision/hand_landmarker 
      try:
         hand_landmarks_list = detection_result.hand_landmarks
         numRaised = 0

         for idx in range(len(hand_landmarks_list)):

            hand_landmarks = hand_landmarks_list[idx]
            for i in range(8,21,4):
               tip_y = hand_landmarks[i].y
               dip_y = hand_landmarks[i-1].y
               pip_y = hand_landmarks[i-2].y
               mcp_y = hand_landmarks[i-3].y
               if tip_y < min(dip_y,pip_y,mcp_y):
                  numRaised += 1

            # thumb
            tip_x = hand_landmarks[4].x
            dip_x = hand_landmarks[3].x
            pip_x = hand_landmarks[2].x
            mcp_x = hand_landmarks[1].x
            palm_x = hand_landmarks[0].x
            if mcp_x > palm_x:
               if tip_x > max(dip_x,pip_x,mcp_x):
                  numRaised += 1
            else:
               if tip_x < min(dip_x,pip_x,mcp_x):
                  numRaised += 1

         annotated_image = np.copy(rgb_image)
         height, width, _ = annotated_image.shape
         text_x = int(hand_landmarks[0].x * width) - 100
         text_y = int(hand_landmarks[0].y * height) + 50
         cv2.putText(img = annotated_image, text = str(numRaised) + " Fingers Raised", 
                           org = (text_x, text_y), fontFace = cv2.FONT_HERSHEY_COMPLEX,
                           fontScale = 1, color = (0,0,255), thickness = 2, lineType = cv2.LINE_4)
         return (annotated_image, numRaised)
      except:
         return (rgb_image, 0)
