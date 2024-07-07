import tkinter as tk
from tkinter import messagebox
import datetime
import winsound  # Windows-specific for beep sound
import os  # For Unix-like systems
import threading
import time

class AlarmClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Alarm Clock")
        
        self.alarm_hour = tk.StringVar()
        self.alarm_minute = tk.StringVar()
        
        self.alarm_set = False
        
        self.create_widgets()
        
        # Start the thread for alarm checking
        self.alarm_thread = threading.Thread(target=self.check_alarm_thread, daemon=True)
        self.alarm_thread.start()
    
    def create_widgets(self):
        # Labels and Entry fields for Alarm Time
        tk.Label(self.root, text="Enter Alarm Time (24-hour format):", font=("Helvetica", 14)).pack(pady=10)
        
        # Hour Entry field
        tk.Label(self.root, text="Hour:", font=("Helvetica", 12)).pack(pady=5)
        tk.Entry(self.root, textvariable=self.alarm_hour, width=10).pack(pady=5)
        
        # Minutes Entry field
        tk.Label(self.root, text="Minutes:", font=("Helvetica", 12)).pack(pady=5)
        tk.Entry(self.root, textvariable=self.alarm_minute, width=10).pack(pady=5)
        
        # Set Alarm Button
        tk.Button(self.root, text="Set Alarm", command=self.set_alarm).pack(pady=10)
        
        # Quit Button
        tk.Button(self.root, text="Quit", command=self.quit_app).pack(pady=10)
    
    def set_alarm(self):
        # Validate input
        try:
            hour = int(self.alarm_hour.get())
            minute = int(self.alarm_minute.get())
            
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError("Invalid hour or minute value")
            
            self.alarm_set = True
            messagebox.showinfo("Alarm", f"Alarm set for {hour:02}:{minute:02}")
        except ValueError:
            messagebox.showwarning("Alarm", "Please enter valid values for hour (0-23) and minute (0-59).")
    
    def check_alarm_thread(self):
        while True:
            if self.alarm_set:
                try:
                    current_time = datetime.datetime.now().strftime("%H:%M")
                    alarm_time = self.get_alarm_time()
                    
                    if current_time == alarm_time:
                        self.trigger_alarm()
                except Exception as e:
                    print(f"Error in alarm checking: {e}")
            
            time.sleep(1)  # Check every second
    
    def get_alarm_time(self):
        # Get current hour and minute
        hour = int(self.alarm_hour.get())
        minute = int(self.alarm_minute.get())
        
        return f"{hour:02}:{minute:02}"
    
    def trigger_alarm(self):
        messagebox.showinfo("Alarm", "Wake up!")
        self.play_alarm_sound()
        self.alarm_set = False  # Reset alarm after triggering
    
    def play_alarm_sound(self):
        if os.name == 'nt':  # Check if it's a Windows system
            winsound.Beep(1000, 1000)  # Beep at 1000 Hz for 1 second
        else:
            print("\a")  # Beep on Unix-like systems
    
    def quit_app(self):
        self.root.destroy()

def main():
    root = tk.Tk()
    app = AlarmClockApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
