import tkinter as tk
from query_main import Query

root = tk.Tk()
root.title('SER 531 Team 6 - Q.A.L.D.')


def returnEntry(arg=None):
    """Gets the result from Entry and return it to the Label"""
    q = Query()
    result = myEntry.get()
    parsed_result = q.parse(result)
    resultLabel.config(text=parsed_result)
    myEntry.delete(0, tk.END)


# Initialization
T = tk.Text(root, height=3, width=70)
T.pack()
T.insert(tk.END, "This is your bilingual assistant FACX, please ask me a question\n我是你的双语虚拟助手FACX")
T1 = tk.Text(root, height=3, width=70)
T1.pack()
T1.insert(tk.END,
          "If you don't know questions, please type 'template'\n输入问答查看问题模板/type 'mix' to see bilingual template")

# Create the Entry widget
myEntry = tk.Entry(root, font=('Calibri', 18), bd=5, bg='white', width=50)
myEntry.focus()
myEntry.bind("<Return>", returnEntry)
myEntry.pack()

# Create the Enter button
enterEntry = tk.Button(root, text="Enter", command=returnEntry)
enterEntry.pack(fill=tk.X)

# Create and empty Label to put the result in
resultLabel = tk.Label(root, text="", width=50, wraplength=600)
resultLabel.pack(fill=tk.X)
root.geometry("+450+400")
root.mainloop()
