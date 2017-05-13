# template for "Stopwatch: The Game"

# define global variables
import simplegui


attemp = 0
win = 0
count = 0
display = '0:00.0'

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format():
    global count, display
    tenth = count % 10
    second = ((count - tenth) / 10) % 60 
    minute = count // 600      
    if second < 10:
        display = str(minute) + ':' + '0' + str(second) + '.' + str(tenth)
    else:
        display = str(minute) + ':' +  str(second) + '.' + str(tenth)
    return display
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()    
    
def stop():
    global attemp, win
    timer.stop()
    attemp += 1
    if count % 50 == 0:
        win += 1
        

def reset():
    global count, attemp, win
    count = 0
    attemp = 0
    win = 0
    timer.stop()
    

# define event handler for timer with 0.1 sec interval
def timer():
    global count
    count += 1
    
    

# define draw handler
def draw(canvas):
    canvas.draw_text(format(), [65, 100], 36, 'white')
    canvas.draw_text(str(win) + '/' + str(attemp), [160, 30], 28, 'green')
    
# create frame 
frame = simplegui.create_frame('Stopwatch: The Game', 200, 200)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, timer)
frame.add_button('Start', start, 100)
frame.add_button('Stop', stop, 100)
frame.add_button('Reset', reset, 100)

# start frame
frame.start()

# Please remember to review the grading rubric
