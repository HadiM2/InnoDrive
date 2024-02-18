import cv2
from motor_control import init_motors, control_motors
from image_processing import process_image, follow_line

# Initialize motors
left_motor_pwm, right_motor_pwm = init_motors()

# Main loop for processing images from the CSI camera on Jetson Nano
cap = cv2.VideoCapture(0)  # 0 represents the default camera (CSI camera)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Process the current frame to extract line information
    lines = process_image(frame)

    # Follow the line based on the extracted information and control the motors
    follow_line(lines, left_motor_pwm, right_motor_pwm)

    # Display the processed frame
    cv2.imshow('Duckiebot', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object, stop the motors, and close all windows
cap.release()
control_motors(left_motor_pwm, right_motor_pwm, cleanup=True)
cv2.destroyAllWindows()
