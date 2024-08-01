from math import sqrt, pow
import numpy as np
import tkinter as tk
import tkinter.filedialog 
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


class StormSurge:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Storm Surge ")
        self.filename = "untitled"
        #self.root.protocol("WM_DELETE_WINDOW", self.telos)
        icon_path = "icon.png"
        if os.path.exists(icon_path):
           img = ImageTk.PhotoImage(Image.open(icon_path))
           self.root.iconphoto(False, img)
        self.canvas = None
        self.Setwidgets()
        self.setMenus()     
        self.root.protocol("WM_DELETE_WINDOW", self.telos)
        self.root.mainloop()
        
    def Setwidgets(self):
        
        
        i=0
        temp = tk.Label(self.root, text="Calculation of  Water Surface Elevation due to Wind Shear", bg="white", font=("Arial",12))
        temp.grid(row=i, column=0, columnspan=2, sticky="we")
        
        i+= 1
        temp = tk.Label(self.root, text="Depth at the limit of the continental shelf (m):", bg="lightblue") 
        temp.grid(row=i, column=0, sticky="e")
        self.entHo = tk.Entry(self.root, width=35)
        self.entHo.grid(row=i, column=1, sticky="we")
        
        i+= 1
        temp = tk.Label(self.root, text="Length of the continental shelf (m):", bg="lightblue") 
        temp.grid(row=i, column=0, sticky="e")
        self.entl = tk.Entry(self.root, width=35)
        self.entl.grid(row=i, column=1, sticky="we")
        
        i+= 1
        temp = tk.Label(self.root, text="Distance of the limit of the continental shelf from the coast (m):", bg="lightblue") 
        temp.grid(row=i, column=0, sticky="e")
        self.entx = tk.Entry(self.root, width=35)
        self.entx.grid(row=i, column=1, sticky="we")

        i+= 1
        temp = tk.Label(self.root, text="Wind velocity 10m above sea level (m/s):", bg="lightblue")
        temp.grid(row=i, column=0, sticky="e")
        self.entvel = tk.Entry(self.root, width=35)
        self.entvel.grid(row=i, column=1, sticky="we")
        
        i+= 1
        temp = tk.Label(self.root, text="Wind denisty (kg/m^3):", bg="lightblue") 
        temp.grid(row=i, column=0, sticky="e")
        self.entden = tk.Entry(self.root, width=35)
        self.entden.grid(row=i, column=1, sticky="we")
        
        i+= 1 
        temp = tk.Label(self.root, text="Drag coefficient (Cd):", bg="lightblue") 
        temp.grid(row=i, column=0, sticky="e")
        self.entdrag = tk.Entry(self.root, width=35)
        self.entdrag.grid(row=i, column=1, sticky="we")
        
        i+= 1 
        temp = tk.Label(self.root, text="Calibrating coefficient (n):", bg="lightblue") 
        temp.grid(row=i, column=0, sticky="e")
        self.entcal = tk.Entry(self.root, width=35)
        self.entcal.grid(row=i, column=1, sticky="we")
                            
        i+= 1
        temp = tk.Label(self.root, text="Wind Shear(N/m^2) :", bg="lightblue") 
        temp.grid(row=i, column=0, sticky="e")
        self.entwind = tk.Entry(self.root, width=35, state="readonly")
        self.entwind.grid(row=i, column=1, sticky="we")
        
        
        i+= 1
        temp = tk.Label(self.root, text="Depth of the continental shelf(m):", bg="lightblue") 
        temp.grid(row=i, column=0, sticky="e")
        self.entdepth = tk.Entry(self.root, width=35, state="readonly")
        self.entdepth.grid(row=i, column=1, sticky="we")
        
        i+= 1
        temp = tk.Label(self.root, text="Elevation of Water Surface(cm):", bg="lightblue") 
        temp.grid(row=i, column=0, sticky="e")
        self.entelev = tk.Entry(self.root, width=35, state="readonly")
        self.entelev.grid(row=i, column=1, sticky="we")
        
        
        i+=1
        self.frame = tk.Frame(self.root, height=200, background="lightgrey")
        self.frame.grid(row=i, column=0, columnspan=3, sticky="we")
                          
        self.root.configure(bg='lightblue')               
        self.root.columnconfigure(1, weight=1)    
              
                          
                          
                          
    def calcWindshear(self):
        
        vals = []
        for index in self.entvel, self.entdrag, self.entden:
            t = index.get().replace(",",".")
            try: 
               temp = float(t)
            except ValueError:
                temp = None
            if temp is None or temp <=0:
                tk.messagebox.showinfo("Error", "Not a positive number", parent=self.root, icon=tk.messagebox.ERROR)#
                index.focus_set()
                return None  
            else:
                vals.append(temp)  
        tempwind = pow(vals[0],2)*vals[1]*vals[2]
        self.entwind.config(state=tk.NORMAL) #allow the widget to me modified
        self.entwind.delete(0, tk.END) #deletes any exisitng text in the widget
        self.entwind.insert(0, "{:.5f}".format(tempwind)) #inser the value in the widget
        return tempwind
        
    def calcDepth(self): 
        
        vals = []
        for index in self.entl, self.entHo, self.entx:
            t = index.get().replace(",",".")
            try: 
               temp = float(t)
            except ValueError:
                temp = None
            if temp is None or temp <=0: 
                tk.messagebox.showinfo("Error", "Not a positive number", parent=self.root, icon=tk.messagebox.ERROR)#
                index.focus_set()
                return None
            else:
                 vals.append(temp)  
        tempdepth = vals[1]*(1-vals[2]/vals[0])
        self.entdepth.config(state=tk.NORMAL) #allow the widget to me modified
        self.entdepth.delete(0, tk.END) #deletes any exisitng text in the widget
        self.entdepth.insert(0, "{:.3f}".format(tempdepth)) #inser the value in the widget
        return tempdepth
        
            
    def bisecroot(self,f, a, b, eps):
        iterations = 0
        maxiter = 100  # maximum number of iterations
        while iterations <= maxiter:
            x = (a + b) / 2
            if abs(b - a) / 2 <= eps:
                return x
            elif f(a) * f(x) < 0:
                b = x
            else:
                a = x
                iterations += 1
        return None         


    
    def calcelevation(self):
        
        twx = self.calcWindshear()
        h = self.calcDepth()
        vals = []
        for index in self.entx, self.entcal:
            t = index.get().replace(",",".")
            try: 
               temp = float(t)
            except ValueError:
                temp = None
            if temp is None or temp <=0: 
                tk.messagebox.showinfo("Error", "Not a positive number", parent=self.root, icon=tk.messagebox.ERROR)
                index.focus_set()
                return None
            else:
                vals.append(temp)
        
        f = lambda x : (-h + sqrt(h**2 + (2 * twx * vals[1] * vals[0]) / (9.81 * 1025)) - x)
        eps = 10**-6
        temp = self.bisecroot(f, 0, h, eps)
        elevation = temp * (10^3)
        if elevation  is None:
            tk.messagebox.showinfo("Error", "Check data provided", parent = self.root, icon = tk.messagebox.ERROR)
        else:    
            self.entelev.config(state=tk.NORMAL) #allow the widget to me modified
            self.entelev.delete(0, tk.END) #deletes any exisitng text in the widget
            self.entelev.insert(0, "{:.5f}".format(elevation)) #inser the value in the widget
            return elevation
        
    def about(self):
        tk.messagebox.showinfo("", "This is a GUI that calculates water elevation due to Wind Shear using Dean and Dalrymple 1991 formula,  developed by George Hadjidemosthenous.", parent=self.root, icon=tk.messagebox.INFO)
    

    def getVals(self):
        
        vals = []
        for index in self.entHo,self.entl, self.entx, self.entvel, self.entden, self.entdrag, self.entcal:
            t = index.get().replace(",",".")
            try: 
               temp = float(t)
            except ValueError:
                temp = None
            if temp is None or temp <=0:
                return None               
            else:
                vals.append(temp) 
        return vals
    
      
    def plot(self):
    
        vals = self.getVals()
        speed = vals[3]
        h = self.calcDepth()
        yaxis = []
        xaxis = []
        Cd = vals[5]
        density = vals[4]
        eps = 10**-6
        for speed in np.arange(speed * 0.5, speed * 1.5, speed / 20):
            twx = (speed**2 * density * Cd)
            f = lambda x : (-h + sqrt(h**2 + (2 * twx * vals[2] * vals[6]) / (9.81 * 1025)) - x)
            temp = self.bisecroot(f, 0, h, eps)
            yaxis.append(temp * (10^3))
       
        xaxis = np.linspace(speed * 0.5, speed * 1.5, 20)   
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(xaxis, yaxis, label='Surface Elevation')
        ax.set_xlabel('Wind Speed (m/s)')
        ax.set_ylabel('Surface Elevation (mm)')
        ax.set_title('Correlation between Wind Speed and Surface Elevation')
        ax.legend()
        ax.grid(True)
        
        
       
        
        
        if self.canvas is not None:  # Clear previous canvas if exists
               self.canvas.get_tk_widget().destroy()
               
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
   
    
   
    def write(self, filename):
        
        vals = self.getVals() #gather all the data in the list Vals
        for index in self.entwind, self.entdepth, self.entelev:
           t = index.get().replace(",",".")
           try: 
              temp = float(t)
           except ValueError:
               temp = None
           if temp is None:
               vals.append("")
           else:
               vals.append(temp)
            
        
        with open(filename,'w') as fw:
            
            fw.write("Data: \n")
            fw.write("Depth at the limit of the continental shelf:  {:.2f} #m\n".format(vals[0]))
            fw.write("Length of the continental shelf:  {:.2f} #m\n".format(vals[1]))
            fw.write("Distance of the limit of the continental shelf from the coast: {:.2f}#m\n".format(vals[2]))
            fw.write("Wind velocity 10m above sea level:  {:.3f} #m/s\n".format(vals[3])) 
            fw.write("Wind density:  {:.1f} #kg/m^3\n".format(vals[4]))
            fw.write("Drag coefficient:  {:.5f}\n".format(vals[5]))
            fw.write("Calibrating coefficient:  {:.1f}\n".format(vals[6]))
            fw.write("\n")
            fw.write("Results:\n")
            fw.write("Wind Shear:  {:.5f} #N/m^2\n".format(vals[7]))
            fw.write("Depth of the continental shelf:  {:.3f} #m\n".format(vals[8]))
            fw.write("Elevation of Water Surface:  {:.5f} #cm".format(vals[9]))
            
        
    
    def saveas(self):
        
       fw = tk.filedialog.asksaveasfile(parent=self.root, defaultextension=".hyd", title="Open file for save") #opens file dialog for the user to choose on which file the data will be saved
       if fw is None: return #user cancelled save
      
       
       self.fw = fw
       vals = self.getVals()
       
       if vals is None: 
           tk.messagebox.showinfo("Error", "No data has been given", parent=self.root, icon=tk.messagebox.ERROR)
           return
       else:
           self.filename = fw.name
           self.write(self.filename)
        
    
    def save(self):
        
        try:  #checks if the data is already saved as
             self.fw 
        except AttributeError:
            self.fw = None
            
        if self.fw is None:
                     tk.messagebox.showinfo("Error", "Please use the funciton save as to select a file first", parent=self.root, icon=tk.messagebox.ERROR)
                     self.saveas()
        else:
                if self.getVals() is None:
                    tk.messagebox.showinfo("Error", "No data has been given", parent=self.root, icon=tk.messagebox.ERROR)
                    return
                else: 
                    self.write(self.filename)
        
        
    def telos(self):
        
        try:    
             self.fw
        except AttributeError: self.fw = None
        
        vals = self.getVals()
        if vals is None:
            self.root.destroy()
        
        elif self.fw == None and vals!=None:
            self.r = tk.messagebox.askokcancel("Data is not saved","ok to abandon changes?", default="cancel", parent=self.root)
            if self.r == True: #user selected ok
                del  self.entHo,self.entl, self.entx, self.entvel, self.entden, self.entdrag, self.entcal, self.entwind, self.entdepth, self.entelev 
                self.root.destroy()
        else:
            del self.entHo,self.entl, self.entx, self.entvel, self.entden, self.entdrag, self.entcal, self.entwind, self.entdepth, self.entelev 
            self.root.destroy()

    
  
    def setMenus(self):
        
        menuBar = tk.Menu(self.root, activebackground="green")
        self.root.config(menu=menuBar)
        
        menu1= tk.Menu(menuBar, activebackground="green", tearoff=False)
        menuBar.add_cascade(label = "File", menu = menu1, foreground="blue")
        menu1.add_command(label = "Save as", command = self.saveas, foreground="blue")
        menu1.add_separator()
        menu1.add_command(label="Save", command = self.save, foreground = "blue")
        
        menu2 = tk.Menu(menuBar, activebackground="green", tearoff=False)
        menuBar.add_cascade(label = "Compute", menu = menu2, foreground="blue")
        menu2.add_command(label="Calculate Wind-Shear", command=self.calcWindshear, foreground="blue")
        menu2.add_separator()   
        menu2.add_command(label="Calculate Continental Shelf Depth", command=self.calcDepth, foreground="blue")
        menu2.add_separator()
        menu2.add_command(label = "Calculate Water Surface Elevation", command=self.calcelevation, foreground="blue")
        menu2.add_separator()
        menu2.add_command(label= "Plot", command=self.plot, foreground="blue")
        
        menuBar.add_command(label="About", command = self.about, foreground="blue")
        menuBar.add_command(label ="Exit", command = self.telos, foreground="blue")

        
                          
if __name__ == "__main__":
    surge = StormSurge()                          
        
