import tkinter as tk

def add_image():
    text.image_create(tk.END, image = img) # Example 1
    text.window_create(tk.END, window = tk.Label(text, image = img)) # Example 2
    print(text.get("1.0", tk.END))

root = tk.Tk()

text = tk.Text(root)
text.pack(padx = 20, pady = 20)

tk.Button(root, text = "Insert", command = add_image).pack()

img = tk.PhotoImage(file = "link.png")

root.mainloop()