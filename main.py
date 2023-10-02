import time
import cv2
import finger_counter as rfp
from question_generator import QuestionGenerator

def main():
    cap = cv2.VideoCapture(0)
    hand_landmarker = rfp.FingerCounter()
    question_generator = QuestionGenerator()
    num1, num2, correct_answer = question_generator.generate_question()
    numRaised = 0

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        hand_landmarker.detect_async(frame)
        frame = rfp.draw_landmarks_on_image(frame,hand_landmarker.result)
        frame, numRaised = rfp.count_fingers_raised(frame,hand_landmarker.result)
        question = "What should be in the missing number _ x {} = {}?".format(num2,correct_answer)
        frame = cv2.putText(img = frame, text = question, 
                           org = (10, 50), fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                           fontScale = 0.6, color = (0,0,255), thickness = 2, lineType = cv2.LINE_AA)
        if(numRaised == num1):
            frame = cv2.putText(img = frame, text = "Correct!", 
                           org = (10, 100), fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                           fontScale = 0.6, color = (0,255,0), thickness = 2, lineType = cv2.LINE_AA)
            
            
                 
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) == ord('q'):
            break
   

    rfp.hand_landmarker.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()