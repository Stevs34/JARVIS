import cv2
import mediapipe as mp
import threading
import time
import os
from datetime import datetime

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_detection
mp_pose = mp.solutions.pose

# State
vision_active = False
camera = None
current_frame = None
person_present = False
gesture_callback = None
presence_callback = None

# Gesture names
GESTURES = {
    "thumbs_up": "THUMBS_UP",
    "thumbs_down": "THUMBS_DOWN",
    "open_hand": "OPEN_HAND",
    "fist": "FIST",
    "peace": "PEACE"
}

def start_camera():
    """Start the webcam"""
    global camera, vision_active
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Could not open webcam")
        return False
    vision_active = True
    print("Camera started")
    return True

def stop_camera():
    """Stop the webcam"""
    global camera, vision_active
    vision_active = False
    if camera:
        camera.release()
    cv2.destroyAllWindows()

def detect_gesture(hand_landmarks):
    """Detect hand gesture from landmarks"""
    landmarks = hand_landmarks.landmark

    # Get finger tip and base positions
    thumb_tip = landmarks[4]
    thumb_base = landmarks[2]
    index_tip = landmarks[8]
    index_base = landmarks[5]
    middle_tip = landmarks[12]
    middle_base = landmarks[9]
    ring_tip = landmarks[16]
    ring_base = landmarks[13]
    pinky_tip = landmarks[20]
    pinky_base = landmarks[17]

    # Check which fingers are up
    thumb_up = thumb_tip.x < thumb_base.x
    index_up = index_tip.y < index_base.y
    middle_up = middle_tip.y < middle_base.y
    ring_up = ring_tip.y < ring_base.y
    pinky_up = pinky_tip.y < pinky_base.y

    fingers_up = [index_up, middle_up, ring_up, pinky_up]
    count_up = sum(fingers_up)

    # Identify gesture
    if thumb_up and count_up == 0:
        return "THUMBS_UP"
    elif not thumb_up and count_up == 0:
        return "FIST"
    elif count_up == 4:
        return "OPEN_HAND"
    elif index_up and middle_up and not ring_up and not pinky_up:
        return "PEACE"
    elif not thumb_up and count_up == 0:
        return "THUMBS_DOWN"
    return None

def vision_loop(speak_func):
    """Main vision processing loop"""
    global current_frame, person_present

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7
    )

    face_detection = mp_face.FaceDetection(
        min_detection_confidence=0.7
    )

    last_gesture = None
    last_gesture_time = 0
    last_presence_state = False
    presence_start_time = None
    GESTURE_COOLDOWN = 2.0
    PRESENCE_CONFIRM_TIME = 2.0

    while vision_active:
        ret, frame = camera.read()
        if not ret:
            continue

        current_frame = frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Face detection — is someone in the room?
        face_results = face_detection.process(rgb_frame)
        face_detected = face_results.detections is not None and len(face_results.detections) > 0

        # Confirm presence for a few seconds before triggering
        if face_detected:
            if presence_start_time is None:
                presence_start_time = time.time()
            elif time.time() - presence_start_time > PRESENCE_CONFIRM_TIME:
                person_present = True
        else:
            presence_start_time = None
            person_present = False

        # Trigger presence callback when state changes
        if person_present != last_presence_state:
            last_presence_state = person_present
            if presence_callback:
                presence_callback(person_present)

        # Hand gesture detection
        hand_results = hands.process(rgb_frame)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                gesture = detect_gesture(hand_landmarks)
                now = time.time()
                if gesture and gesture != last_gesture and (now - last_gesture_time) > GESTURE_COOLDOWN:
                    last_gesture = gesture
                    last_gesture_time = now
                    print(f"Gesture detected: {gesture}")
                    if gesture_callback:
                        gesture_callback(gesture)

        time.sleep(0.05)

    hands.close()
    face_detection.close()

def start_vision(speak_func, on_gesture=None, on_presence=None):
    """Start vision in background thread"""
    global gesture_callback, presence_callback
    gesture_callback = on_gesture
    presence_callback = on_presence

    if start_camera():
        thread = threading.Thread(
            target=vision_loop,
            args=(speak_func,),
            daemon=True
        )
        thread.start()
        print("Vision module started")
        return True
    return False

def take_snapshot():
    """Take a photo and save it"""
    global current_frame
    if current_frame is not None:
        filename = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(filename, current_frame)
        return filename
    return None

def is_person_present():
    """Check if someone is in front of the camera"""
    return person_present