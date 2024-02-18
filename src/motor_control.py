import Jetson.GPIO as GPIO

def init_motors():
    # GPIO pins for motor control
    LEFT_MOTOR_PWM_PIN = 18  # Replace with your actual GPIO pin
    RIGHT_MOTOR_PWM_PIN = 13  # Replace with your actual GPIO pin

    # Motor initialization
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LEFT_MOTOR_PWM_PIN, GPIO.OUT)
    GPIO.setup(RIGHT_MOTOR_PWM_PIN, GPIO.OUT)
    left_motor_pwm = GPIO.PWM(LEFT_MOTOR_PWM_PIN, 1000)
    right_motor_pwm = GPIO.PWM(RIGHT_MOTOR_PWM_PIN, 1000)
    left_motor_pwm.start(0)
    right_motor_pwm.start(0)

    return left_motor_pwm, right_motor_pwm

def control_motors(left_motor_pwm, right_motor_pwm, cleanup=False):
    # Stop the motors
    left_motor_pwm.stop()
    right_motor_pwm.stop()

    # Cleanup GPIO if needed
    if cleanup:
        GPIO.cleanup()
