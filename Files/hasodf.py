paul = Snake(0,0, "N")
x = 20
def lab():
	global x
	while x > 0:
		paul.turn_right()
		if paul.can_move():
			paul.move()
		else:
			paul.turn_right()
			paul.turn_right()
		x = x-1
lab()


print("hi")















