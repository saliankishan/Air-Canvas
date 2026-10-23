def fingers_up(hand):
    fingers = []
    fingers.append(hand.landmark[4].x < hand.landmark[3].x)     # thumb
    fingers.append(hand.landmark[8].y < hand.landmark[6].y)     # index
    fingers.append(hand.landmark[12].y < hand.landmark[10].y)   # middle
    fingers.append(hand.landmark[16].y < hand.landmark[14].y)   # ring
    fingers.append(hand.landmark[20].y < hand.landmark[18].y)   # pinky
    return fingers
