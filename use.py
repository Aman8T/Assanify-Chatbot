def exit():
    print('1')
    
from threading import Timer
input_time=2
t = Timer(input_time, exit)
t.start()
prompt = "You have %d seconds type 'Y'or 'N'\n" % input_time
user_input = input(prompt)

print('s')