"""
Intelligent Robotic Servicing System
Main Interface For the Robotic Arm Control Software
Author: Edwin Mwiti
Copyright: 2020
"""

# imports
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import Pmw
from time import time, sleep
from datetime import datetime
import os
import sys
import numericValidator
import tk_tools as tools
from pylive import live_plotter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import ArduinoConnection


class LoginForm(ttk.Frame):
    def __init__(self, parent):
        """Constructor"""
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        
        window_width = 470
        window_height = 150
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        x_position = int((screen_width/2) - (window_width/2))
        y_position = int((screen_height/2) - (window_height/2))
        
        self.parent.geometry("{}x{}+{}+{}".format(window_width, window_height, x_position, y_position))

        self.parent.title("IRSS|Login")
        self.parent.configure(background='gray40')
        
        self.widgeter()
    
    def widgeter(self, *args):
        """Create widgets for login window"""
        self.parent.bind("<Return>", self.verify_password_a)
        self.btnConf = {'font': ('verdana', 9), 'background': 'slategray', 'padx': '4', 'width': '8', 'pady': '4'}  # button configurations
        self.logo = Label(self.parent, text="IRSS", background='gray40', pady=10, font=('verdana', 13))
        
        self.password = Entry(self.parent, font=('verdana', 12), justify="center")
        self.password.configure(show="*")
        self.password.focus()
        self.filler = Label(self.parent, text="",background='gray40',  pady=10, font=('verdana', 13))
        self.login_btn = Button(self.parent, self.btnConf, text="Login", pady=5, relief=RIDGE,  command=self.verify_password)   # mouse click

        # place the widgets    
        self.logo.pack()
        self.password.pack()
        self.filler.pack()
        self.login_btn.pack()
            
    def verify_password(self, event=None):
        """Verify the password"""
        # get the password
        if self.password.get() != "r":
            messagebox.showerror('IRSS', 'Access Denied')
            self.password.focus()
        else:
            # proceed to the main window
            self.initialize_main_application()
            
    def verify_password_a(self, event):
        """Respond to enter key press"""
        self.verify_password()
    
    def initialize_main_application(self):
        """Show the main window if password correct"""
        self.parent.destroy()
        self.parent = Tk()
        self.main = Main(self.parent)
        self.parent.mainloop()
            
            
class Main:
    def __init__(self, parent):
        self.parent = parent
        
        # view fullscreen
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()   
        self.parent.geometry("{}x{}".format(screen_width, screen_height))
        self.parent.title("IRSS | Control Software")
        self.parent.state('zoomed')
        self.parent.configure(background='gray40')
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create Widgets for the main window"""

        # parent frame
        overall = Frame(self.parent, relief=RIDGE, background='gray40')
        overall.pack(side=LEFT, fill=BOTH)

        leftFrame = Frame(overall, relief=FLAT, background='gray40')
        leftFrame.pack(side=TOP, fill=Y)

        self.centerFrame = Frame(self.parent, relief=RIDGE, background='gray40')
        self.centerFrame.pack(side=LEFT, fill=Y)

        rightFrame = Frame(self.parent, relief=FLAT, background='gray30')
        rightFrame.pack(side=TOP, fill=Y)

        # Mode selection Frame
        self.mode = LabelFrame(leftFrame, text="Mode", font=('arial', 11, 'bold'))
        self.mode.configure(background='gray40')
        self.mode.pack(anchor=W)
        self.mode_var = IntVar()

        self.manual_mode =Radiobutton(self.mode,
                        text='Manual',
                        value=1,
                        variable=self.mode_var,
                        indicatoron=0, fg='red',
                        background='gray10',
                        font=('verdana', 11, 'bold'),
                        width=10,
                        command=self.check_current_mode,
                        selectcolor='lawngreen').pack(side=LEFT, padx=18, pady=5)

        self.intelligent_mode = Radiobutton(self.mode,
                        text='Intelligent',
                        value=2,
                        variable=self.mode_var,
                        indicatoron=0, fg='red',
                        background='gray10',
                        font=('verdana', 11, 'bold'),
                        width=10,
                        command=self.check_current_mode,
                        selectcolor='lawngreen').pack(side=LEFT, padx=18, pady=5)

        self.remote_mode = Radiobutton(self.mode,
                        text='Remote',
                        value=3,
                        variable=self.mode_var,
                        indicatoron=0, fg='red',
                        background='gray10',
                        font=('verdana', 11, 'bold'),
                        width=10,
                        command=self.check_current_mode,
                        selectcolor='lawngreen').pack(side=LEFT, padx=18, pady=5)
        
        # ==============================Pick coordinates frame================================================
        self.pick_group = LabelFrame(leftFrame, text="Pick Position", font=('arial',11, 'bold'))
        self.pick_group.configure(background='gray40')
        self.pick_group.pack(anchor=W)

        Label(self.pick_group, font=('verdana', 11), text="Enter coordinates of the desired position of gripper center", background='gray40').pack()

        # picking position coordinates entry frame
        pick_entry_frame = Frame(self.pick_group, relief=FLAT, background='gray40')
        pick_entry_frame.configure(background='gray40')

        x_coords = Frame(pick_entry_frame, relief=FLAT, background='gray40')
        x_coords.pack()
        x_label = Label(x_coords, text='x:                      ', font=('verdana', 11), background='gray40')
        self.x = numericValidator.NumericEntry(x_coords, font=('verdana', 11, 'bold'),background='gray70', width=10)
        x_label.pack(side=LEFT)
        self.x.pack(side=LEFT)

        y_coords = Frame(pick_entry_frame, relief=FLAT, background='gray40')
        y_coords.pack()
        y_label = Label(y_coords, text='y:                      ', font=('verdana', 11), background='gray40')
        self.y = numericValidator.NumericEntry(y_coords, font=('verdana', 11, 'bold'),background='gray70', width=10)
        y_label.pack(side=LEFT)
        self.y.pack(side=LEFT)

        z_coords = Frame(pick_entry_frame, relief=FLAT, background='gray40')
        z_coords.pack()
        z_label = Label(z_coords, text='z:                      ', font=('verdana', 11), background='gray40')
        self.z = numericValidator.NumericEntry(z_coords, font=('verdana', 11, 'bold'),background='gray70', width=10)
        z_label.pack(side=LEFT)
        self.z.pack(side=LEFT)

        # Inverse Kinematics computing button
        self.pick_ik = Button(pick_entry_frame, text="Compute IK", borderwidth=1, font=('verdana', 11, 'bold'), relief=SOLID, background='gray10', fg='orange')

        self.pick_ik.pack(pady=5)

        pick_entry_frame.pack()

        # pick position joint angles
        Label(self.pick_group,font=('verdana', 11), text="Joint Angles (deg)", background='gray40').pack(pady=5)
        joint_angles_frame = Frame(self.pick_group, relief=FLAT, background='gray40')

        shoulder_az = Frame(joint_angles_frame, relief=FLAT, background='gray40')
        shoulder_az.pack()
        Label(shoulder_az, text='Shoulder Azimuth:', font=('verdana', 11), background='gray40').pack(side=LEFT)
        self.shoulder_azimuth = numericValidator.NumericEntry(shoulder_az, width=10,  font=('verdana', 11, 'bold'),background='gray70',)
        self.shoulder_azimuth.pack(side=LEFT)

        shoulder_pivot = Frame(joint_angles_frame, relief=FLAT, background='gray40')
        shoulder_pivot.pack()
        Label(shoulder_pivot, text='Shoulder Pivot:     ', font=('verdana', 11), background='gray40').pack(side=LEFT)
        self.shoulder_pivot = numericValidator.NumericEntry(shoulder_pivot,width=10, font=('verdana', 11, 'bold'),background='gray70',)
        self.shoulder_pivot.pack(side=LEFT)

        elbow_p = Frame(joint_angles_frame, relief=FLAT, background='gray40')
        elbow_p.pack()
        Label(elbow_p, text='Elbow Pivot:         ', font=('verdana', 11), background='gray40').pack(side=LEFT)
        self.elbow_pivot = numericValidator.NumericEntry(elbow_p,width=10, font=('verdana', 11, 'bold'),background='gray70')
        self.elbow_pivot.pack(side=LEFT)

        wrist_p = Frame(joint_angles_frame, relief=FLAT, background='gray40')
        wrist_p.pack()
        Label(wrist_p, text='Wrist Pitch:          ', font=('verdana', 11), background='gray40').pack(side=LEFT)
        self.wrist_pivot = numericValidator.NumericEntry(wrist_p, width=10, font=('verdana', 11, 'bold'),background='gray70')
        self.wrist_pivot.pack(side=LEFT)

        joint_angles_frame.pack(side=TOP)

        # pick_x.component('entry').focus_set()
        # ===================================END================================================================

        # ===================================placing coordinates frame======================================
        self.place_group = LabelFrame(leftFrame, text='Place Position',font=('arial', 11, 'bold'), background='gray40')
        self.place_group.pack(anchor=W)

        Label(self.place_group, font=('verdana', 11), text="Enter coordinates of the desired position of gripper center", background='gray40').pack()

        # picking position coordinates entry frame
        place_entry_frame = Frame(self.place_group, relief=FLAT)

        place_x_coords = Frame(place_entry_frame, relief=FLAT, background='gray40')
        place_x_coords.pack()
        place_x_label = Label(place_x_coords, text='x:                      ', font=('verdana', 11), background='gray40')
        self.place_x = numericValidator.NumericEntry(place_x_coords, font=('verdana', 11, 'bold'),background='gray70', width=10)
        place_x_label.pack(side=LEFT)
        self.place_x.pack(side=LEFT)

        place_y_coords = Frame(place_entry_frame, relief=FLAT, background='gray40')
        place_y_coords.pack()
        place_y_label = Label(place_y_coords, text='y:                      ', font=('verdana', 11), background='gray40')
        self.place_y = numericValidator.NumericEntry(place_y_coords,font=('verdana', 11, 'bold'),background='gray70', width=10)
        place_y_label.pack(side=LEFT)
        self.place_y.pack(side=LEFT)

        place_z_coords = Frame(place_entry_frame, relief=FLAT, background='gray40')
        place_z_coords.pack()
        place_z_label = Label(place_z_coords, text='z:                      ', font=('verdana', 11), background='gray40')
        self.place_z = numericValidator.NumericEntry(place_z_coords, font=('verdana', 11, 'bold'),background='gray70', width=10)
        place_z_label.pack(side=LEFT)
        self.place_z.pack(side=LEFT)

        # Inverse Kinematics computing button
        self.place_ik = Button(self.place_group, text="Compute IK", borderwidth=1, font=('verdana', 11, 'bold'), relief=SOLID,
                         background='gray10', fg='orange')

        place_entry_frame.pack()

        self.place_ik.pack(pady=5)

        # pick position joint angles
        Label(self.place_group, font=('verdana', 11), text="Joint Angles (deg)", background='gray40').pack(pady=5)
        place_joint_angles = Frame(self.place_group, relief=FLAT, background='gray40')

        shoulder_az = Frame(place_joint_angles, relief=FLAT, background='gray40')
        shoulder_az.pack()
        Label(shoulder_az, text='Shoulder Azimuth:', font=('verdana', 11), background='gray40').pack(side=LEFT)
        self.shoulder_azimuth = numericValidator.NumericEntry(shoulder_az, width=10, font=('verdana', 11, 'bold'),background='gray70',)
        self.shoulder_azimuth.pack(side=LEFT)

        shoulder_pivot = Frame(place_joint_angles, relief=FLAT, background='gray40')
        shoulder_pivot.pack()
        Label(shoulder_pivot, text='Shoulder Pivot:     ', font=('verdana', 11), background='gray40').pack(side=LEFT)
        self.shoulder_pivot = numericValidator.NumericEntry(shoulder_pivot, width=10, font=('verdana', 11, 'bold'),background='gray70',)
        self.shoulder_pivot.pack(side=LEFT)

        elbow_p = Frame(place_joint_angles, relief=FLAT, background='gray40')
        elbow_p.pack()
        Label(elbow_p, text='Elbow Pivot:         ', font=('verdana', 11), background='gray40').pack(side=LEFT)
        self.elbow_pivot = numericValidator.NumericEntry(elbow_p, width=10, font=('verdana', 11, 'bold'),background='gray70',)
        self.elbow_pivot.pack(side=LEFT)

        wrist_p = Frame(place_joint_angles, relief=FLAT, background='gray40')
        wrist_p.pack()
        Label(wrist_p, text='Wrist Pitch:          ', font=('verdana', 11), background='gray40').pack(side=LEFT)
        self.wrist_pivot = numericValidator.NumericEntry(wrist_p, width=10, font=('verdana', 11, 'bold'),background='gray70',)
        self.wrist_pivot.pack(side=LEFT)

        place_joint_angles.pack(side=TOP)
        # ===================================END====================================================================

        # ===================================Operation Buttons======================================================
        operations = Frame(leftFrame, relief=FLAT, background='gray40')
        operations.pack(side=LEFT, anchor=W, fill=Y)

        #===============================OPERATION BUTTONS================================================

        # Load Button
        self.load_parameters = Button(operations, text='  UPLOAD  ', font=('lucida', 11, 'bold'), fg='red', width = 11, background='gray60', command=self.load_to_console)
        self.load_parameters.pack(padx=4,pady=10, side=LEFT)

        # run button
        self.btnRun = Button(operations, text='RUN ', font=('lucida', 11, 'bold'), fg='red', width = 10, background='gray60',command=self.run)
        self.btnRun.pack(padx=4,pady=10, side=LEFT)

        self.btnStop = Button(operations, text='STOP', font=('lucida', 11, 'bold'), fg='red', width=10, background='gray60',command=self.stop)
        self.btnStop.pack(padx=4,pady=10, side=LEFT)

        self.btnExit = Button(operations, text='EXIT', font=('lucida', 11, 'bold'), fg='red', width=10, background='gray60',command=self.exit)
        self.btnExit.pack(padx=4,pady=10, side=LEFT)
        # =================================END========================================================================

        # ==================================No of objects to be picked================================================

        parametersFrame = LabelFrame(self.centerFrame, background='gray40', text='Operation Parameters', font=('arial', 11, 'bold'))
        parametersFrame.pack(side=TOP)

        objects = Frame(parametersFrame, background='gray40')
        objectsLabel = Label(objects, text='No. of Objects:   ', font=('verdana', 11), background='gray40')
        self.objectsEntry = numericValidator.NumericEntry(objects, background='gray70', font=('verdana', 11, 'bold'), width=20)
        objectsLabel.pack(side=LEFT)
        self.objectsEntry.pack(side=LEFT, pady=4)

        objects.pack(side=TOP)

        servoFrame = Frame(parametersFrame, background='gray40')
        servoLabel = Label(servoFrame, text="Servo Speed:      ", font=('verdana', 11), background='gray40')
        # servoEntry = Entry(servoFrame, background='gray70', width=10)
        self.servoEntry = Pmw.Counter(servoFrame,
                                 entry_width=30,
                                 entryfield_value='12.5',
                                 datatype={'counter':'real', 'separator':'.'},
                                 entryfield_validate={'validator':'real', 'min':0.0, 'max':15.0, 'separator':'.'},
                                 increment=.2,

                                 )

        servoLabel.pack(side=LEFT)
        self.servoEntry.pack(side=LEFT, fill=Y, pady=4)
        servoFrame.pack(side=LEFT)

        # ==================================END======================================================================

        # status bar
        sbar = Frame(overall, relief=SUNKEN, background='gray40')
        self.statusbar = Label(sbar, text='Status:', bd=1, anchor=W, font=('consolas', 13, 'bold'))
        self.statusbar.configure(background='gray40', fg='lawngreen')
        self.cstat = Label(sbar, text='...', fg='lawngreen', background='gray40', font=('consolas', 13, 'bold'))

        self.statusbar.pack(anchor=W, side=LEFT)
        self.cstat.pack(anchor=W, side=LEFT)
        sbar.pack(fill=X)

        jaw_label = Label(self.centerFrame, text='Set Jaw width(mm)', font=('verdana', 10, 'bold'), background='gray40')
        jaw_label.pack(anchor=CENTER)

        # CREATE THE JAW WIDTH SLIDER
        self.slider_var = DoubleVar()
        self.scaler = Scale(self.centerFrame,
                            variable=self.slider_var,
                            orient=HORIZONTAL,
                            from_=0,
                            to=90,
                            tickinterval=0.2,
                            sliderlength=4,
                            relief=FLAT,
                            length=355,
                            fg='steelblue',
                            bg='gray40',
                            activebackground='brown',
                            font=('consolas', 11, 'bold')
                            )
        self.scaler.pack(anchor=CENTER)

        # ==================System info==============================================
        # Show the robot arm image
        simulator = LabelFrame(self.centerFrame, text='System Information', font=('arial', 11, 'bold'), height=700)
        simulator.pack(side=TOP, fill=Y, anchor=W)
        simulator.configure(background='gray40')

        # environment_parameters = LabelFrame(simulator, text='<<<Loaded Parameters:>', font=('consolas', 11))
        # environment_parameters.configure(background='gray40', fg='black')
        # environment_parameters.pack(side=TOP)

        tFrame = Frame(simulator, relief=FLAT)
        Label(tFrame, text='Modified: ', fg='black', background='gray40', font=('consolas', 11)).pack(side=LEFT)
        self.ctime = Label(tFrame, text='_', fg='black', background='gray40', font=('consolas', 11))
        self.ctime.pack(anchor=W)
        tFrame.pack(anchor=W)

        filler = Label(simulator, text='============================================', background='gray40',
                       fg='black')
        filler.pack()

        username = Frame(simulator, relief=FLAT)
        Label(username, text='Current User :', fg='black', background='gray40', font=('consolas', 11)).pack(side=LEFT)
        self.uname = Label(username, text='e5430', background='gray40', fg='black', font=('consolas', 11))
        self.uname.pack(anchor=W)
        username.pack(anchor=W)

        operatinSys = Frame(simulator, relief=FLAT)
        Label(operatinSys, text='OS :', fg='black', background='gray40', font=('consolas', 11)).pack(side=LEFT)
        self.operatingsys = Label(operatinSys, text='_', background='gray40', fg='black', font=('consolas', 11))
        self.operatingsys.pack(anchor=W)
        operatinSys.pack(anchor=W)

        controller = Frame(simulator, relief=FLAT)
        Label(controller, text='Microcontroller :', fg='black', background='gray40', font=('consolas', 11)).pack(
            side=LEFT)
        self.control = Label(controller, text='Arduino UNO ATMEGA328P', background='gray40', fg='black',
                             font=('consolas', 11))
        self.control.pack(anchor=W)
        controller.pack(anchor=W)

        configuration = Frame(simulator, relief=FLAT)
        Label(configuration, text='DoF :', fg='black', background='gray40', font=('consolas', 11)).pack(side=LEFT)
        self.config = Label(configuration, text='6', background='gray40', fg='black', font=('consolas', 11))
        self.config.pack(anchor=W)
        configuration.pack(anchor=W)

        run = Frame(simulator, relief=FLAT)
        Label(run, text='Run mode:', fg='black', background='gray40', font=('consolas', 11)).pack(side=LEFT)
        self.run_mode = Label(run, text='_', background='gray40', fg='black', font=('consolas', 11))
        self.run_mode.pack(anchor=W)
        run.pack(anchor=W)

        coords = Frame(simulator, relief=FLAT)
        Label(coords, text='Pick coordinates : ', fg='black', background='gray40', font=('consolas', 11)).pack(
            side=LEFT)
        self.pick_coords = Label(coords, text='_', background='gray40', fg='black', font=('consolas', 11))
        self.pick_coords.pack(anchor=W)
        coords.pack(anchor=W)

        pcoords = Frame(simulator, relief=FLAT)
        Label(pcoords, text='Place Coordinates : ', fg='black', background='gray40', font=('consolas', 11)).pack(
            side=LEFT)
        self.place_coords = Label(pcoords, text='_', background='gray40', fg='black', font=('consolas', 11))
        self.place_coords.pack(anchor=W)
        pcoords.pack(anchor=W)

        speed = Frame(simulator, relief=FLAT)
        Label(speed, text='Servo speed : ', fg='black', background='gray40', font=('consolas', 11)).pack(side=LEFT)
        self.servo_speed = Label(speed, text='_', background='gray40', fg='black', font=('consolas', 11))
        self.servo_speed.pack(anchor=W)
        speed.pack(anchor=W)

        objs = Frame(simulator, relief=FLAT)
        Label(objs, text='Objects : ', fg='black', background='gray40', font=('consolas', 11)).pack(side=LEFT)
        self.object = Label(objs, text='_', background='gray40', fg='black', font=('consolas', 11))
        self.object.pack(anchor=W)
        objs.pack(anchor=W)

        grip = Frame(simulator, relief=FLAT)
        Label(grip, text='Gripper width : ', fg='black', background='gray40', font=('consolas', 11)).pack(side=LEFT)
        self.gripper_width = Label(grip, text='_', background='gray40', fg='black', font=('consolas', 11))
        self.gripper_width.pack(anchor=W)
        grip.pack(anchor=W)

        # =====================END========================================================

        # Serial port
        self.centerLower = Frame(self.centerFrame, background='gray40')
        self.centerLower.pack(side=TOP)

        serialFrame = Frame(self.centerLower, background='gray40')
        serialFrame.pack(fill=X, side=TOP)

        serialLabel = Label(serialFrame, text='Serial Port:              ', background='gray40', font=('verdana', 11))
        serialLabel.pack(side=LEFT, anchor=W, fill=X)
        self.ports=['COM13', 'COM17']
        self.serialport = ttk.Combobox(serialFrame, font=('courier', 11),
                                       values=['COM13', 'COM17'])

        self.serialport.pack(side=LEFT)
        self.serialport.current(0)

        self.connect_status = Frame(self.centerLower, background='gray40')
        self.connect_status.pack(side=BOTTOM)
        self.connectLabel = Label(self.connect_status, text='', background='gray40', font=('verdana', 10, 'bold'))
        self.connectLabel.pack(anchor=CENTER)

        # =====================ANALOG GAUGES================================================

        # subdividing the right frame
        rightupper = LabelFrame(rightFrame, bg='gray40', text='Monitors', font=('verdana', 10, 'bold'))
        rightupper.pack()

        self.inputVoltage = tools.Gauge(rightupper,
                                        width=180,
                                        height=150,
                                        min_value=0.0, max_value=5,
                                        label='Volts-In',
                                        unit='V',
                                        bg='gray40',
                                        yellow=100,
                                        red=100,
                                        red_low=80)
        self.inputVoltage.set_value(4.5)
        self.inputVoltage.grid(row=0, column=0)

        self.motorOne = tools.Gauge(rightupper,
                                    width=180,
                                    height=150,
                                        min_value=0.0, max_value=5,
                                        label='M1',
                                        unit='mW',
                                        bg='gray40',
                                    red_low=70,
                                    yellow=100)
        self.motorOne.set_value(4)
        self.motorOne.grid(row=0, column=1)

        self.motorTwo = tools.Gauge(rightupper,
                                    width=180,
                                    height=150,
                                        min_value=0.0, max_value=5,
                                        label='M2',
                                        unit='mW',
                                        bg='gray40',
                                    red_low=70,
                                    yellow=100)
        self.motorTwo.set_value(4.5)
        self.motorTwo.grid(row=0, column=2)

        self.motorThree = tools.Gauge(rightupper,
                                      width=180,
                                      height=150,
                                        min_value=0.0, max_value=5,
                                        label='M3',
                                        unit='mW',
                                        bg='gray40',
                                    red_low=70,
                                    yellow=100)
        self.motorThree.set_value(4.5)
        self.motorThree.grid(row=1, column=0)

        self.motorFour = tools.Gauge(rightupper,
                                     width=180,
                                     height=150,
                                        min_value=0.0, max_value=5,
                                        label='M4',
                                        unit='mW',
                                        bg='gray40',
                                    red_low=70,
                                    yellow=100)
        self.motorFour.set_value(3)
        self.motorFour.grid(row=1, column=1)
        #
        self.motorFive = tools.Gauge(rightupper,
                                     width=180,
                                     height=150,
                                        min_value=0.0, max_value=5,
                                        label='M5',
                                        unit='mw',
                                        bg='gray40',
                                    red_low=70,
                                    yellow=100)
        self.motorFive.set_value(4.5)
        self.motorFive.grid(row=1, column=2)
        #
        self.gripperMotor = tools.Gauge(rightupper,
                                        width=180,
                                        height=150,
                                        min_value=0.0, max_value=5,
                                        label='Gmotor',
                                        unit='mW',
                                        bg='gray40',
                                    red_low=70,
                                    yellow=100)
        self.gripperMotor.set_value(4.5)
        self.gripperMotor.grid(row=2, column=0)

        self.gripperForce = tools.Gauge(rightupper,
                                        width=180,
                                        height=150,
                                        min_value=0.0, max_value=5,
                                        label='GrForce',
                                        unit='mN',
                                        bg='gray40',
                                    red_low=70,
                                    yellow=100)
        self.gripperForce.set_value(4.5)
        self.gripperForce.grid(row=2, column=1)

        self.proximitySensor = tools.Gauge(rightupper,
                                           width=180,
                                           height=150,
                                        min_value=0.0, max_value=5,
                                        label='Contact',
                                        unit='mm',
                                        bg='gray40',
                                           yellow=100,
                                           red=100)
        self.proximitySensor.set_value(4.5)
        self.proximitySensor.grid(row=2, column=2)
        # ===============================END================================================

        # ============================GRIPPER FORCE GRAPH====================================
        rightLower = LabelFrame(rightFrame, bg='gray40', text='Gripper Force', font=('verdana', 10, 'bold'))
        rightLower.pack(fill=X)

        figure = Figure(figsize=(4.5, 2.5), dpi=100)
        figure.tight_layout(h_pad=5)

        subplot = figure.add_subplot(111)
        # subplot.set_xlabel('Time(s)')
        subplot.set_ylabel('Force(N)')
        subplot.plot([1,2,3,4,5,6,7,8], [5,6,7,5,6,1,2,3], color='orange')


        graphcanvas = FigureCanvasTkAgg(figure, rightLower)
        graphcanvas.draw()
        graphcanvas.get_tk_widget().pack(fill=X)

        # =================================END===============================================



    def check_current_mode(self):
        """call respective functions for the selected robot operation mode"""

        # update status bar

        print(self.mode_var.get())

    def console_mode(self):
        """Display the current mode of operation"""
        rmode = self.mode_var.get()

        mode = 'ERROR'
        if rmode == 1:
            mode = 'Manual...'
        elif rmode == 2:
            mode = 'Intelligent...'
        elif rmode == 3:
            mode = 'Remote...'

        return mode

    def load_to_console(self):
        """Console display configurations"""

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_time = str(current_time+'...')
        self.ctime.config(text=current_time)

        user = os.getlogin()
        self.uname.config(text=user+'...')

        opsys = sys.platform
        self.operatingsys.config(text=opsys+'...')

        all_coordinates = self.get_all_coordinates()

        # get the operation coordinates
        self.get_all_coordinates()
        self.pick_coords.config(text=all_coordinates[0])
        self.place_coords.config(text=all_coordinates[1])

        self.servo_speed.config(text=str(self.get_servo_speed())+'...')

        self.object.config(text=str(self.get_no_of_objects())+'...')

        self.run_mode.config(text=str(self.console_mode())+'...')

        # create connection with the Arduino board
        self.connect_status = ArduinoConnection.create_arduino_connection(self.get_port())

        # check the connection status
        if self.connect_status is True:
            self.conn_status = 'Connection successful'
            # create label to display the status
            self.connectLabel.config(text=self.conn_status, fg='green')
        else:
            self.conn_status = 'Connection failed. Please try again.'
            self.connectLabel.config(text=self.conn_status, fg='red')


    def get_port(self):
        """Fetch the serial port chosen"""
        return self.serialport.get()


    def get_all_coordinates(self):
        """Get all coordinates => Pick and place
        (pick), (place)
        (x, y, z), (x, y, z)
        """
        return [(self.x.get(),self.y.get(),self.z.get()),  (self.place_x.get(), self.place_y.get(), self.place_z.get())]

    def get_servo_speed(self):
        s = self.servoEntry.getvalue()
        return s

    def get_no_of_objects(self):
        o = self.objectsEntry.get()
        return o

    def run(self):
        """Run the arm"""

        #update status bar
        self.cstat.config(text='RUNNING...')

    def stop(self):
        pass

    def exit(self):
        pass

if __name__ == "__main__":
    root = Tk()
    Pmw.initialise()
    LoginForm(root)
    root.mainloop()
