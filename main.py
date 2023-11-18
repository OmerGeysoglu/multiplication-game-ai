import time
import cv2
import finger_counter as rfp
from question_generator import QuestionGenerator

def main():
    cap = cv2.VideoCapture(0)
    hand_landmarker = rfp.FingerCounter()
    question_generator = QuestionGenerator()
    numRaised = 0
    question = question_generator.generate_question()
    frame_counter_next_question = 0
    isCorrectlyAnswered = False
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.blur(frame, (4,4))
        hand_landmarker.detect_async(frame)
        frame = rfp.draw_landmarks_on_image(frame,hand_landmarker.result)
        frame, numRaised = rfp.count_fingers_raised(frame,hand_landmarker.result)
        
        frame = cv2.putText(img = frame, text = question, 
                           org = (10, 50), fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                           fontScale = 0.6, color = (0,0,255), thickness = 2, lineType = cv2.LINE_AA)
        isAnswerCorrect = question_generator.checkAnswer(numRaised)
        if(isAnswerCorrect):
            frame = cv2.putText(img = frame, text = "Correct!", 
                           org = (10, 100), fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                           fontScale = 0.6, color = (0,255,0), thickness = 2, lineType = cv2.LINE_AA)
            isCorrectlyAnswered = True
        if(isCorrectlyAnswered):
            frame_counter_next_question += 1
            if(frame_counter_next_question > 40):
                frame_counter_next_question = 0
                isCorrectlyAnswered = False
                question = question_generator.generate_question()
            
            
                 
        cv2.imshow('Multiplication Game',frame)
        if cv2.waitKey(1) == ord('q'):
            break
   

    rfp.hand_landmarker.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()