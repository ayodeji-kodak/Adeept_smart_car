import Adafruit_PCA9685 # Import the library used to communicate with PCA9685
import time
import RPi.GPIO as GPIO
import random

#servo
pwm = Adafruit_PCA9685.PCA9685() # Instantiate the object used to control the PWM
pwm.set_pwm_freq(50) # Set the frequency of the PWM signal

#ultrasonic_module
Tr = 11 # The pin number of the input end of the ultrasonic module
Ec = 8 # Pin number of the output end of the ultrasonic module

GPIO.setmode(GPIO.BCM)
GPIO.setup(Tr, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(Ec, GPIO.IN)

def checkdist():
	GPIO.output(Tr, GPIO.HIGH) # Set the input terminal of the module to high level and send out an initial sound wave.
	time.sleep(0.000015)
	GPIO.output(Tr, GPIO.LOW)
	while not GPIO.input(Ec): # When the module no longer receives the initial sound wave ①
		pass
	t1 = time.time() # Write down the time when the initial sound wave was emitted.
	while GPIO.input(Ec): # When the module receives the return sound wave.
		pass
	t2 = time.time() # Write down the time when the return sound wave was captured.
	return round((t2-t1)*340/2,2) # Calculate the distance.

def look_right():
	pwm.set_pwm(1, 0, 270)
def look_left():
	pwm.set_pwm(1, 0, 400)
def look_down():
	pwm.set_pwm(2, 0, 210)
def look_up():
	pwm.set_pwm(2, 0, 300)
def central():
	pwm.set_pwm(1, 0, 340)
	pwm.set_pwm(2, 0, 250)

'''
for i in range(10)
	print(checkdist())
	time.sleep(1)
'''

# Function to generate a random number from 0 to 3, avoiding consecutive repeats
def random_without_repeats(prev_num=None):
    choices = list(range(4))  # Numbers from 0 to 3
    if prev_num is not None:
        choices.remove(prev_num)  # Remove the previously selected number
    return random.choice(choices)

# Example usage
previous_number = None

while True:
	distance = checkdist()

	if (distance > 0.2):
		central()

	elif (distance < 0.2):
		location = random.randint(0,3)
		#Generate 10 random numbers without consecutive repeats
		'''
		for _ in range(200):
			random_number = random_without_repeats(previous_number)
			print(random_number)
			previous_number = random_number
			location = random_number
		'''
		if (location == 0):
			look_up()
			distance = checkdist()
			#if (distance > 0.2):
				#break
		elif (location ==  1):
			look_down()
			distance = checkdist()
			#if (distance > 0.2):
				#break

		elif (location == 2):
			look_right()
			distance = checkdist()
			#if (distance > 0.2):
				#break
		elif (location == 3):
			look_left()
			distance = checkdist()
			#if (distance > 0.2):
				#break
	time.sleep(0.5)
