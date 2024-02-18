import cv2
import numpy as np

def process_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detection to find edges in the image
    edges = cv2.Canny(blurred, 50, 150)

    # Use HoughLinesP to detect lines in the image
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=10)

    return lines

def follow_line(lines, left_motor_pwm, right_motor_pwm):
    if lines is not None:
        dotted_lines = []
        solid_lines = []

        # Categorize lines into dotted and solid based on slope
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')
            if 0.5 < abs(slope) < 2.0:
                if slope > 0:
                    dotted_lines.append(line)
                else:
                    solid_lines.append(line)

        # Calculate average positions of dotted and solid lines
        dotted_center_x = np.mean([np.mean(line[:, [0, 2]]) for line in dotted_lines])
        solid_center_x = np.mean([np.mean(line[:, [0, 2]]) for line in solid_lines])

        # Calculate the center between dotted and solid lines
        target_center_x = (dotted_center_x + solid_center_x) / 2

        # Implement your control logic here based on the target_center_x
        current_center_x = (lines[0][0][0] + lines[0][0][2]) / 2
        center_difference = target_center_x - current_center_x

        # Adjust motor speeds based on the center difference
        if center_difference < -10:
            print("Turn left")
            left_motor_pwm.ChangeDutyCycle(50)
            right_motor_pwm.ChangeDutyCycle(100)
        elif center_difference > 10:
            print("Turn right")
            left_motor_pwm.ChangeDutyCycle(100)
            right_motor_pwm.ChangeDutyCycle(50)
        else:
            print("Go straight")
            left_motor_pwm.ChangeDutyCycle(100)
            right_motor_pwm.ChangeDutyCycle(100)
