import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def get_hash(filepath):
    """Calculates SHA-512 of the selected file."""
    sha512 = hashlib.sha512()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(4096):
                sha512.update(chunk)
        return sha512.hexdigest()
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file: {e}")
        return None

# Simple dictionary 'database'
stored_hashes = {}

def update_hash_display(text_content):
    """Updates the scrollable text box with the new hash."""
    hash_display.config(state=tk.NORMAL) # Unlock for editing
    hash_display.delete(1.0, tk.END)    # Clear old text
    hash_display.insert(tk.INSERT, text_content)
    hash_display.config(state=tk.DISABLED) # Lock back to read-only

def upload_and_register():
    path = filedialog.askopenfilename()
    if path:
        file_hash = get_hash(path)
        if file_hash:
            stored_hashes[path] = file_hash
            update_hash_display(f"REGISTERED HASH:\n{file_hash}")
            messagebox.showinfo("Success", "Original Image HASH Registered!")

def upload_and_verify():
    path = filedialog.askopenfilename()
    if path:
        if path not in stored_hashes:
            messagebox.showerror("Error", "This image was never registered!")
            return
        
        current_hash = get_hash(path)
        if current_hash:
            update_hash_display(f"CURRENT HASH:\n{current_hash}")
            
            if current_hash == stored_hashes[path]:
                messagebox.showinfo("Result", "🛡️ AUTHENTIC\nNo tampering detected.")
            else:
                messagebox.showwarning("Result", "⚠️ TAMPERED!\nThe hash does not match the original.")

# --- Setup the UI Window ---
root = tk.Tk()
root.title("SHA-512 Image Integrity Shield")
root.geometry("500x450")
root.configure(padx=20, pady=20)

# Header
tk.Label(root, text="Image Tamper Detection System", font=("Arial", 16, "bold")).pack(pady=10)
tk.Label(root, text="Using Cryptographic SHA-512", font=("Arial", 10, "italic")).pack()

# Buttons
tk.Button(root, text="1. Select & Register Original", command=upload_and_register, 
          width=35, bg="#e1f5fe", font=("Arial", 10)).pack(pady=10)

tk.Button(root, text="2. Select & Verify Image", command=upload_and_verify, 
          width=35, bg="#ffebee", font=("Arial", 10)).pack(pady=5)

# Scrollable Hash Display
tk.Label(root, text="Full SHA-512 Digest:", font=("Arial", 10, "bold")).pack(pady=(20, 5))
hash_display = scrolledtext.ScrolledText(root, width=50, height=6, font=("Courier", 10))
hash_display.pack()
hash_display.insert(tk.INSERT, "No image processed yet...")
hash_display.config(state=tk.DISABLED) # Make it read-only initially

root.mainloop()