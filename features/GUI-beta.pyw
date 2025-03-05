import tkinter as tk


m = tk.Tk()
m.title('SummarAIze ------ [BETA]')

# Create a label widget
label = tk.Label(m, text='SummarAIze')
m.geometry('400x300')
m.resizable(False, False)
label.pack()

if __name__ == '__main__':
    m.mainloop()