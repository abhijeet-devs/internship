import tkinter as tk
import random

def generateOTP():
    return random.randint(100000, 999999)
   
def verifyOTP():
    user_input = otp_entry.get().strip()
    try:
        user_otp = int(user_input)
        if user_otp == otp:
            result_label.config(text="OTP verification successful!", fg="green")
        else:
            result_label.config(text="OTP verification failed. Please try again.", fg="red")
    except ValueError:
        result_label.config(text="Invalid OTP format. Please enter a 6-digit number.", fg="red")

root = tk.Tk()
root.title("OTP Verification")
root.geometry("400x200")  

otp = generateOTP()

otp_label = tk.Label(root, text=f"Enter OTP sent to you: {otp}")
otp_label.pack(pady=10)

otp_entry = tk.Entry(root, width=10)
otp_entry.pack()

verify_button = tk.Button(root, text="Verify OTP", command=verifyOTP)
verify_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
