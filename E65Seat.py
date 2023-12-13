import can
import threading
import time
import tkinter as tk
import random

bus = can.interface.Bus(channel='com11', bustype='seeedstudio', bitrate=100000)

# button booleans
headrest_up = False
headrest_down = False

back_support_center_extend = False
back_support_center_retract = False

back_support_lower_extend = False
back_support_lower_retract = False

leg_bolster_in = False
leg_bolster_out = False

side_bolster_in = False
side_bolster_out = False

backrest_forward = False
backrest_backward = False

backrest_fold_forward = False
backrest_fold_backward = False

seat_up = False
seat_down = False

seat_tilt_up = False
seat_tilt_down = False

seat_forward = False
seat_backward = False

heat = False
vent = False
active = False

#seat status
heat_status = 0
vent_status = 0
active_status = 0



def parseSeatStatus(message):
    global heat_status
    global vent_status
    global massage_status
    heat_status = (message.data[0] & 0b00110000) >> 4
    vent_status = message.data[1] & 0b00000011
    active_status = (message.data[0] & 0xF) == 1
    print(f"Heat: {heat_status}")
    print(f"Vent: {vent_status}")
    print(f"Active: {active_status}")
    print(f"Raw: {bin(message.data[0])} {bin(message.data[1])} {bin(message.data[2])}")



#create and start a thread that sends three different can messages (0x130, 0x232, 0x14b) on the bus
def send_can_messages():
    counter = 0x00
    while True:
        delay = 0.01
        
        #Ignition
        bus.send(can.Message(arbitration_id=0x130, data=[0x45, 0xfe, 0xfc, 0xff, counter&0xff], is_extended_id=False))
        time.sleep(delay)
        
        
        #0x1E7 (Seat Heat/Vent)
        if heat:
            bus.send(can.Message(arbitration_id=0x1e7, data=[1, 0xff], is_extended_id=False))
        elif vent:
            bus.send(can.Message(arbitration_id=0x1e7, data=[4, 0xff], is_extended_id=False))
        else:
            bus.send(can.Message(arbitration_id=0x1e7, data=[0, 0xff], is_extended_id=False))
        time.sleep(delay)

        #0xDA (Seat Move)
        
        if seat_forward:
            bus.send(can.Message(arbitration_id=0xda, data=[1, 0, 0, 0xff], is_extended_id=False))
        elif seat_backward:
            bus.send(can.Message(arbitration_id=0xda, data=[2, 0, 0, 0xff], is_extended_id=False))
            
        elif seat_up:
            bus.send(can.Message(arbitration_id=0xda, data=[4, 0, 0, 0xff], is_extended_id=False))
        elif seat_down:
            bus.send(can.Message(arbitration_id=0xda, data=[8, 0, 0, 0xff], is_extended_id=False))
            
        elif backrest_forward:
            bus.send(can.Message(arbitration_id=0xda, data=[16, 0, 0, 0xff], is_extended_id=False))
        elif backrest_backward:
            bus.send(can.Message(arbitration_id=0xda, data=[32, 0, 0, 0xff], is_extended_id=False))
            
        elif seat_tilt_up:
            bus.send(can.Message(arbitration_id=0xda, data=[64, 0, 0, 0xff], is_extended_id=False))
        elif seat_tilt_down:
            bus.send(can.Message(arbitration_id=0xda, data=[128, 0, 0, 0xff], is_extended_id=False))
            
        elif side_bolster_in:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 1, 0, 0xff], is_extended_id=False))
        elif side_bolster_out:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 2, 0, 0xff], is_extended_id=False))
            
        elif leg_bolster_in:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 32, 0, 0xff], is_extended_id=False))
        elif leg_bolster_out:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 16, 0, 0xff], is_extended_id=False))
            
        elif backrest_fold_forward:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 64, 0, 0xff], is_extended_id=False))
        elif backrest_fold_backward:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 128, 0, 0xff], is_extended_id=False))
            
        elif headrest_up:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 0, 1, 0xff], is_extended_id=False))
        elif headrest_down:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 0, 2, 0xff], is_extended_id=False))
            
        elif back_support_center_extend:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 0, 4, 0xff], is_extended_id=False))
        elif back_support_center_retract:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 0, 8, 0xff], is_extended_id=False))
            
        elif back_support_lower_extend:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 0, 16, 0xff], is_extended_id=False))
        elif back_support_lower_retract:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 0, 32, 0xff], is_extended_id=False))
            
        else:
            bus.send(can.Message(arbitration_id=0xda, data=[0, 0, 0, 0xff], is_extended_id=False))
        time.sleep(delay)

        if active:
            bus.send(can.Message(arbitration_id=0x1eb, data=[1, 0xff], is_extended_id=False))
        else:
            bus.send(can.Message(arbitration_id=0x1eb, data=[0, 0xff], is_extended_id=False))
        time.sleep(delay)

        bus.send(can.Message(arbitration_id=0x1f3, data=[0xf0, 0xff], is_extended_id=False))
        time.sleep(delay)

        bus.send(can.Message(arbitration_id=0x580, data=[0x04, 0x11, 0x04, 0x01, 0x05, 0xFF, 0, 0xf0], is_extended_id=False))
        time.sleep(delay)

        bus.send(can.Message(arbitration_id=0x1dc, data=[random.randint(0,1),0xff,0xff,0xff,0xff,0xff,0xff,0xff], is_extended_id=False))
        time.sleep(delay)


def toggle_var(var):
    globals()[var] = not globals()[var]

#create another thread that reads messages from the bus and calls parseSeatStatus(message) if the message id is 0x15b
def receive_can_messages():
    while True:
        try:
            message = bus.recv()
        except:
            print("ow")
        #print(message)
        if message.arbitration_id == 0x232:
            if message.data[0] != 255:
                parseSeatStatus(message)
            else:
                print("Malformed seat stsus message recved")

def create_tkinter_window():
    root = tk.Tk()
    root.title("Seat Control")

    button_seat_forward = tk.Button(root, text="Forward")
    button_seat_forward.bind('<ButtonPress-1>', lambda event: toggle_var("seat_forward"))
    button_seat_forward.bind('<ButtonRelease-1>', lambda event: toggle_var("seat_forward"))
    button_seat_back = tk.Button(root, text="Backward")
    button_seat_back.bind('<ButtonPress-1>', lambda event: toggle_var("seat_backward"))
    button_seat_back.bind('<ButtonRelease-1>', lambda event: toggle_var("seat_backward"))

    button_seat_tilt_up = tk.Button(root, text="Tilt Up")
    button_seat_tilt_up.bind('<ButtonPress-1>', lambda event: toggle_var("seat_tilt_up"))
    button_seat_tilt_up.bind('<ButtonRelease-1>', lambda event: toggle_var("seat_tilt_up"))
    button_seat_tilt_down = tk.Button(root, text="Tilt Down")
    button_seat_tilt_down.bind('<ButtonPress-1>', lambda event: toggle_var("seat_tilt_down"))
    button_seat_tilt_down.bind('<ButtonRelease-1>', lambda event: toggle_var("seat_tilt_down"))
    
    button_seat_up = tk.Button(root, text="Up")
    button_seat_up.bind('<ButtonPress-1>', lambda event: toggle_var("seat_up"))
    button_seat_up.bind('<ButtonRelease-1>', lambda event: toggle_var("seat_up"))
    button_seat_down = tk.Button(root, text="Down")
    button_seat_down.bind('<ButtonPress-1>', lambda event: toggle_var("seat_down"))
    button_seat_down.bind('<ButtonRelease-1>', lambda event: toggle_var("seat_down"))
    
    button_backrest_forward = tk.Button(root, text="Backrest Forward")
    button_backrest_forward.bind('<ButtonPress-1>', lambda event: toggle_var("backrest_forward"))
    button_backrest_forward.bind('<ButtonRelease-1>', lambda event: toggle_var("backrest_forward"))
    button_backrest_backward = tk.Button(root, text="Backrest Backward")
    button_backrest_backward.bind('<ButtonPress-1>', lambda event: toggle_var("backrest_backward"))
    button_backrest_backward.bind('<ButtonRelease-1>', lambda event: toggle_var("backrest_backward"))
    
    # Add buttons for headrest control
    button_headrest_up = tk.Button(root, text="Headrest Up")
    button_headrest_up.bind('<ButtonPress-1>', lambda event: toggle_var("headrest_up"))
    button_headrest_up.bind('<ButtonRelease-1>', lambda event: toggle_var("headrest_up"))

    button_headrest_down = tk.Button(root, text="Headrest Down")
    button_headrest_down.bind('<ButtonPress-1>', lambda event: toggle_var("headrest_down"))
    button_headrest_down.bind('<ButtonRelease-1>', lambda event: toggle_var("headrest_down"))

    # Add buttons for center support control
    button_center_support_extend = tk.Button(root, text="Lumbar Up")
    button_center_support_extend.bind('<ButtonPress-1>', lambda event: toggle_var("back_support_center_extend"))
    button_center_support_extend.bind('<ButtonRelease-1>', lambda event: toggle_var("back_support_center_extend"))

    button_center_support_retract = tk.Button(root, text="Lumbar Down")
    button_center_support_retract.bind('<ButtonPress-1>', lambda event: toggle_var("back_support_center_retract"))
    button_center_support_retract.bind('<ButtonRelease-1>', lambda event: toggle_var("back_support_center_retract"))

    # Add buttons for lower support control
    button_lower_support_extend = tk.Button(root, text="Lumbar Forward")
    button_lower_support_extend.bind('<ButtonPress-1>', lambda event: toggle_var("back_support_lower_extend"))
    button_lower_support_extend.bind('<ButtonRelease-1>', lambda event: toggle_var("back_support_lower_extend"))

    button_lower_support_retract = tk.Button(root, text="Lumbar Back")
    button_lower_support_retract.bind('<ButtonPress-1>', lambda event: toggle_var("back_support_lower_retract"))
    button_lower_support_retract.bind('<ButtonRelease-1>', lambda event: toggle_var("back_support_lower_retract"))

    # Add buttons for backrest fold control
    button_backrest_fold_forward = tk.Button(root, text="Backrest Fold Forward")
    button_backrest_fold_forward.bind('<ButtonPress-1>', lambda event: toggle_var("backrest_fold_forward"))
    button_backrest_fold_forward.bind('<ButtonRelease-1>', lambda event: toggle_var("backrest_fold_forward"))

    button_backrest_fold_backward = tk.Button(root, text="Backrest Fold Backward")
    button_backrest_fold_backward.bind('<ButtonPress-1>', lambda event: toggle_var("backrest_fold_backward"))
    button_backrest_fold_backward.bind('<ButtonRelease-1>', lambda event: toggle_var("backrest_fold_backward"))

    # Add buttons for leg bolster control
    button_leg_bolster_in = tk.Button(root, text="Leg Bolster In")
    button_leg_bolster_in.bind('<ButtonPress-1>', lambda event: toggle_var("leg_bolster_in"))
    button_leg_bolster_in.bind('<ButtonRelease-1>', lambda event: toggle_var("leg_bolster_in"))

    button_leg_bolster_out = tk.Button(root, text="Leg Bolster Out")
    button_leg_bolster_out.bind('<ButtonPress-1>', lambda event: toggle_var("leg_bolster_out"))
    button_leg_bolster_out.bind('<ButtonRelease-1>', lambda event: toggle_var("leg_bolster_out"))

    # Add buttons for side bolster control
    button_side_bolster_in = tk.Button(root, text="Side Bolster In")
    button_side_bolster_in.bind('<ButtonPress-1>', lambda event: toggle_var("side_bolster_in"))
    button_side_bolster_in.bind('<ButtonRelease-1>', lambda event: toggle_var("side_bolster_in"))

    button_side_bolster_out = tk.Button(root, text="Side Bolster Out")
    button_side_bolster_out.bind('<ButtonPress-1>', lambda event: toggle_var("side_bolster_out"))
    button_side_bolster_out.bind('<ButtonRelease-1>', lambda event: toggle_var("side_bolster_out"))

    
    heat_button = tk.Button(root, text="Heat")
    heat_button.bind('<ButtonPress-1>', lambda event: toggle_var("heat"))
    heat_button.bind('<ButtonRelease-1>', lambda event: toggle_var("heat"))

    vent_button = tk.Button(root, text="Vent")
    vent_button.bind('<ButtonPress-1>', lambda event: toggle_var("vent"))
    vent_button.bind('<ButtonRelease-1>', lambda event: toggle_var("vent"))

    active_button = tk.Button(root, text="Active Seat")
    active_button.bind('<ButtonPress-1>', lambda event: toggle_var("active"))
    active_button.bind('<ButtonRelease-1>', lambda event: toggle_var("active"))

    button_seat_forward.pack()
    button_seat_back.pack()
    button_seat_tilt_up.pack()
    button_seat_tilt_down.pack()
    button_seat_up.pack()
    button_seat_down.pack()
    button_backrest_forward.pack()
    button_backrest_backward.pack()
    button_headrest_up.pack()
    button_headrest_down.pack()
    button_center_support_extend.pack()
    button_center_support_retract.pack()
    button_lower_support_extend.pack()
    button_lower_support_retract.pack()
    button_backrest_fold_forward.pack()
    button_backrest_fold_backward.pack()
    button_leg_bolster_in.pack()
    button_leg_bolster_out.pack()
    button_side_bolster_in.pack()
    button_side_bolster_out.pack()
    heat_button.pack()
    vent_button.pack()
    active_button.pack()

    root.mainloop()

# Start threads for sending and receiving CAN messages
send_thread = threading.Thread(target=send_can_messages)
receive_thread = threading.Thread(target=receive_can_messages)
control_thread = threading.Thread(target=create_tkinter_window)

send_thread.start()
receive_thread.start()
control_thread.start()

send_thread.join()
receive_thread.join()
control_thread.join()
