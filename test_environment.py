import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib

print("FinTrack Environment Check")

print("NumPy Version:", np.__version__)
print("Pandas Version:", pd.__version__)
print("Matplotlib Version:", matplotlib.__version__)

root = tk.Tk()
root.title("FinTrack Environment Test")
root.geometry("400x200")

label = tk.Label(
    root,
    text="FinTrack Environment Ready!",
    font=("Arial", 16, "bold")
)

label.pack(pady=60)

root.mainloop()