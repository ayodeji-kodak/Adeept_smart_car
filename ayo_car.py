import RPi.GPIO as GPIO
import Adafruit_PCA9685 #import the library used to communicate with servo
import time
import threading
import curses

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)
#servo
pwm = Adafruit_PCA9685.PCA9685() #instantiate the objct used to control PWM
pwm.set_pwm_freq(50) #frequecy of pwm signal (servo specific)
#ultrasonic moodle
trig = 11 #trig pin
echo = 8 #echo pin
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(trig, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(echo, GPIO.IN)

#lights
def light_setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(5, GPIO.OUT)
	GPIO.setup(6, GPIO.OUT)
	GPIO.setup(13, GPIO.OUT)

#motor
Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 26
Motor_A_Pin2  = 21
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

Dir_forward   = 0
Dir_backward  = 1

left_forward  = 1
left_backward = 0

right_forward = 0
right_backward= 1

pwn_A = 0
pwm_B = 0

def motorStop(): #Motor stops
	GPIO.output(Motor_A_Pin1, GPIO.LOW)
	GPIO.output(Motor_A_Pin2, GPIO.LOW)
	GPIO.output(Motor_B_Pin1, GPIO.LOW)
	GPIO.output(Motor_B_Pin2, GPIO.LOW)
	GPIO.output(Motor_A_EN, GPIO.LOW)
	GPIO.output(Motor_B_EN, GPIO.LOW)


def setup(): #Motor initialization
	global pwm_A, pwm_B
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(Motor_A_EN, GPIO.OUT)
	GPIO.setup(Motor_B_EN, GPIO.OUT)
	GPIO.setup(Motor_A_Pin1, GPIO.OUT)
	GPIO.setup(Motor_A_Pin2, GPIO.OUT)
	GPIO.setup(Motor_B_Pin1, GPIO.OUT)
	GPIO.setup(Motor_B_Pin2, GPIO.OUT)

	motorStop()
	try:
		pwm_A = GPIO.PWM(Motor_A_EN, 1000)
		pwm_B = GPIO.PWM(Motor_B_EN, 1000)
	except:
		pass
def motor_left(status, direction, speed):#Motor 2 positive and negative rotation
	if status == 0: # stop
		GPIO.output(Motor_B_Pin1, GPIO.LOW)
		GPIO.output(Motor_B_Pin2, GPIO.LOW)
		GPIO.output(Motor_B_EN, GPIO.LOW)
	else:
		if direction == Dir_backward:
			GPIO.output(Motor_B_Pin1, GPIO.HIGH)
			GPIO.output(Motor_B_Pin2, GPIO.LOW)
			pwm_B.start(100)
			pwm_B.ChangeDutyCycle(speed)
		elif direction == Dir_forward:
			GPIO.output(Motor_B_Pin1, GPIO.LOW)
			GPIO.output(Motor_B_Pin2, GPIO.HIGH)
			pwm_B.start(0)
			pwm_B.ChangeDutyCycle(speed)


def motor_right(status, direction, speed):#Motor 1 positive and negative rotation
	if status == 0: # stop
		GPIO.output(Motor_A_Pin1, GPIO.LOW)
		GPIO.output(Motor_A_Pin2, GPIO.LOW)
		GPIO.output(Motor_A_EN, GPIO.LOW)
	else:
		if direction == Dir_forward:#
			GPIO.output(Motor_A_Pin1, GPIO.HIGH)
			GPIO.output(Motor_A_Pin2, GPIO.LOW)
			pwm_A.start(100)
			pwm_A.ChangeDutyCycle(speed)
		elif direction == Dir_backward:
			GPIO.output(Motor_A_Pin1, GPIO.LOW)
			GPIO.output(Motor_A_Pin2, GPIO.HIGH)
			pwm_A.start(0)
			pwm_A.ChangeDutyCycle(speed)
	return direction

def move(speed, direction, turn, radius=0.6):   # 0 < radius <= 1  
	#speed = 100
	if direction == 'forward':
		if turn == 'right':
			motor_left(0, left_backward, int(speed*radius))
			motor_right(1, right_forward, speed)
		elif turn == 'left':
			motor_left(1, left_forward, speed)
			motor_right(0, right_backward, int(speed*radius))
		else:
			motor_left(1, left_forward, speed)
			motor_right(1, right_forward, speed)
	elif direction == 'backward':
		if turn == 'right':
			motor_left(0, left_forward, int(speed*radius))
			motor_right(1, right_backward, speed)
		elif turn == 'left':
			motor_left(1, left_backward, speed)
			motor_right(0, right_forward, int(speed*radius))
		else:
			motor_left(1, left_backward, speed)
			motor_right(1, right_backward, speed)
	elif direction == 'no':
		if turn == 'right':
			motor_left(1, left_backward, speed)
			motor_right(1, right_forward, speed)
		elif turn == 'left':
			motor_left(1, left_forward, speed)
			motor_right(1, right_backward, speed)
		else:
			motorStop()
	else:
		pass

def destroy():
	motorStop()
	GPIO.cleanup()             # Release resource

def turn_left():
	pwm.set_pwm(0,0,400)
	time.sleep(1)
	#pwm.set_pwm(0,0,250)
	#time.sleep(1)


def turn_right():
	pwm.set_pwm(0,0,100)
	time.sleep(1)
	#pwm.set_pwm(0,0,250)
	#time.sleep(1)


def wheel_reset():
	pwm.set_pwm(0,0,250)
	time.sleep(1)

def look_left():
	pwm.set_pwm(1,0,450)
	time.sleep(1)
	#pwm.set_pwm(1,0,330)
	#time.sleep(1)


def look_right():
	pwm.set_pwm(1,0,200)
	time.sleep(1)
	#pwm.set_pwm(1,0,330)
	#time.sleep(1)

def look_up():
	pwm.set_pwm(2,0,450)
	time.sleep(1)
	pwm.set_pwm(2,0,350)
	time.sleep(1)

def look_down():
	pwm.set_pwm(2,0,280)
	time.sleep(1)
	pwm.set_pwm(2,0,350)
	time.sleep(1)

def head_reset():
	pwm.set_pwm(1,0,330)
	time.sleep(1)
	pwm.set_pwm(2,0,350)
	time.sleep(1)

def check_dist():       #Reading distance
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(echo, GPIO.IN)
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(trig, GPIO.LOW)
    while not GPIO.input(echo):
        pass
    t1 = time.time()
    while GPIO.input(echo):
        pass
    t2 = time.time()
    return round((t2-t1)*340/2,2)

def switch(port, status):
	'''
	port 1 = Headlight
	port 2 = left
	port 3 = right
	'''
	if port == 1:
		if status == 1:
			GPIO.output(5, GPIO.HIGH)
		elif status == 0:
			GPIO.output(5, GPIO.LOW)
		else:
			pass
	elif port == 2:
		if status == 1:
			GPIO.output(6, GPIO.HIGH)
		elif status == 0:
			GPIO.output(6, GPIO.LOW)
		else:
			pass
	elif port == 3:
		if status == 1:
			GPIO.output(13, GPIO.HIGH)
		elif status == 0:
			GPIO.output(13, GPIO.LOW)
		else:
			pass

	else:
		print('Wrong Command: Example--switch(3,1)->to switch on port3')

def indicate(side):
	if side == 'left':
		for x in range(4):
			switch(2,1)
			time.sleep(0.5)
			switch(2,0)
			time.sleep(0.5)
	elif side == 'right':
		for x in range(4):
			switch(3,1)
			time.sleep(0.5)
			switch(3,0)
			time.sleep(0.5)
def all_lights_on():
	switch(1,1)
	switch(2,1)
	switch(3,1)

def all_lights_off():
	switch(1,0)
	switch(2,0)
	switch(3,0)

def shake_body():
	turn_left()
	time.sleep(0.5)
	wheel_reset()
	time.sleep(0.5)
	turn_right()
	time_sleep(0.5)
	wheel_reset()
	time.sleep(0.5)
	look_left()
	time.sleep(0.5)
	head_reset()
	time.sleep(0.5)
	look_right()
	time.sleep(0.5)
	head_reset()
	time.sleep(0.5)
	look_up()
	time.sleep(0.5)
	look_down()
	time.sleep(0.5)
	move(speed_set, 'forward', 'no', 0.8)
	time.sleep(2)
	motorStop()
	move(speed_set, 'backward', 'no', 0.8)
	time.sleep(2)
	motorStop()

def test():
	all_lights_on()
	move(speed_set, 'forward', 'no', 0.5)


speed_set = 30
setup()
light_setup()
wheel_reset()
head_reset()



try:
	while True:
		char = screen.getch()
		if char == ord('q'):
			break
		elif char  == curses.KEY_UP:
			print("forward")
			wheel_reset()
			move(speed_set, 'forward', 'no', 10)
		elif char  == curses.KEY_DOWN:
			print("backward")
			wheel_reset()
			move(speed_set, 'backward', 'no', 10)
		elif char  == curses.KEY_LEFT:
			print("left")
			#indicate("left")
			left_indicator_thread = threading.Thread(target = indicate, args = ("left",))
			left_indicator_thread.start()
			turn_left()
		elif char  == curses.KEY_RIGHT:
			print("right")
			#indicate("right")
			right_indicator_thread = threading.Thread(target = indicate, args = ("right",))
			right_indicator_thread.start()
			turn_right()
		elif char == 10:
			print("stop")
			wheel_reset()
			motorStop()
finally:
	#Close down curses properly, inc turn echo back on!
	curses.nocbreak(); screen.keypad(0); curses.echo()
	curses.endwin()
