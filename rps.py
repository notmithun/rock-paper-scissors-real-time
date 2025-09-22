try:
    import cv2
    import mediapipe as mp
    import random

    class CameraError(Exception):
        pass

    print("Imports complete!")

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    print("Mediapipe setup completed!")

    ROCK = "Rock"
    PAPER = "Paper"
    SCISSORS = "Scissors"
    UNKNOWN = "Unknown"
    WAITING = "Waiting..."
    DRAW = "Draw"

    print("Created function: `detect_hand`")
    def detect_hand(frame):
        """Detects what the hand is.
        Example:
        If the index finger and the middle finger are open then, the hand is scissors

        Args:
            frame: Frame to detect the hand

        Returns:
            str: either "Rock", "Paper", "Scissors" or "Unknown" (which is used if hand doesn't match the Rock, Paper or Scissors)\nIF no hand is detected then its None
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            landmarks = result.multi_hand_landmarks[0]

            finger_tips = [8, 12, 16, 20]
            finger_open = sum(
                1 for tip in finger_tips
                if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y
            )

            if finger_open == 0:
                return ROCK
            elif finger_open == 2:
                return SCISSORS
            elif finger_open == 4:
                return PAPER
            else:
                return UNKNOWN
        return None

    def decide_winner(p: str, c: str):
        """Checks who the winner is according to the values given in the arugements

        Args:
            p (str): Player's choice
            c (str): Computer's choice
        """
        if p in [None, UNKNOWN]:
            print("didnt choose one")
            return WAITING
        if p == c:
            print(DRAW)
            return DRAW
        if (p == ROCK and c == SCISSORS) or \
        (p == SCISSORS and c == PAPER) or \
        (p == PAPER and c == ROCK):
            return "Player"
        return "Computer"


    cap = cv2.VideoCapture(0)
    if not cap.isOpened:
        raise CameraError("Unable to access the camera!")
    cpu_move = WAITING
    winner = WAITING

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            raise CameraError("Failed to read camera")
        
        player_move = detect_hand(frame=frame)
        
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for lm in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
        
        cv2.putText(frame, f"Your Move: {player_move}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"CPU Move: {cpu_move}", (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        cv2.putText(frame, f"Winner: {winner}", (30, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 255), 2)

        cv2.putText(frame, "Press SPACE = play, ESC = quit", (30, 450),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (180, 180, 180), 2)
        
        cv2.imshow("Rock, Paper, Scissors but Real-Time", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == 32:
            cpu_move = random.choice([ROCK, PAPER, SCISSORS])
            winner = decide_winner(player_move, cpu_move)

    cap.release()
    cv2.destroyAllWindows()
    exit(0)
except KeyboardInterrupt:
    print("User halted!")
    exit(1)