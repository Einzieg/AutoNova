from ttkbootstrap import *

root = Window(themename='litera')
root.title("AutoNova")
root.iconbitmap("ico/auto.ico")
root.geometry("500x500")
root.resizable(False, False)

start_btn = Button(root, text='Start', bootstyle=(SUCCESS, OUTLINE), command=lambda: print('start'))
start_btn.pack(side=LEFT, padx=5, pady=5)

b6 = Button(root, text='Stop', bootstyle=(DANGER, OUTLINE), command=lambda: print('stop'))
b6.pack(side=LEFT, padx=5, pady=5)

root.mainloop()

start_btn.bind()
