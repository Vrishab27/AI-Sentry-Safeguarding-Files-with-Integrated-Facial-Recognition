#gui_1.py
import tkinter as tk
from tkinter import filedialog, Listbox, messagebox
import logic_1 as frl

def lock_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        frl.add_or_train_face(file_path)
        file_list.insert(tk.END, file_path)
        print(f"Locked file: {file_path}")

def unlock_file():
    selected = file_list.curselection()
    if selected:
        file_path = file_list.get(selected[0])
        if frl.unlock_file_folder(file_path):
            messagebox.showinfo("Success", "File unlocked successfully.")
        else:
            messagebox.showerror("Error", "Face not recognized.")

root = tk.Tk()
root.title("Face Recognition File Unlocker")

lock_btn = tk.Button(root, text="Lock File", command=lock_file)
lock_btn.pack(pady=5)

unlock_btn = tk.Button(root, text="Unlock File", command=unlock_file)
unlock_btn.pack(pady=5)

file_list = Listbox(root)
file_list.pack(pady=15, fill=tk.BOTH, expand=True)

root.mainloop()
