import os

from .gui.main_window import GUI


os.system("rm -r pictures")
os.mkdir("pictures")
with open("pictures/index.txt", mode="w") as index_file:
    index_file.write("0")
GUI().mainloop()
