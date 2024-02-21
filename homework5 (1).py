# Homework 5. Plot three charts for Open price, Adj Close price and Volume data

# Open AnacondaPrompt in Windows 10
# Open Terminal in MacBook and enter 'conda activate'
# In either case, enter 'pip install yfinance'
# After that, enter 'python -m idlelib' to use Python IDLE

import yfinance as yf
import tkinter as tk
import matplotlib.figure as fig
import matplotlib.backends.backend_tkagg as bac

def PlotChart():
    # Read the ticker from your window
    # +++ Your Code Below +++
    my_ticker = my_ticker_entry.get()
    print(my_ticker)
    # +++ Your Code Above +++

    # You need to download stock price for 'ticker' from 2023-01-01 to 2023-05-31'
    # yfinance package will provides data of 'Open', 'High', 'Low', 'Close', 'Adj Close' and 'Volume'.
    # But you only need 'Open', 'Adj Close' and 'Volume' data
    # +++ Your Code Below +++
    my_data = yf.download(my_ticker,'2023-01-01','2023-12-31')
    open_data = my_data['Open']
    adjclose_data = my_data['Adj Close']
    volume_data = my_data['Volume']
    # +++ Your Code Above +++

    # create three figures: 1st figure contains the plot of 'Open' prices, 2nd figure has the plot of 'Adj Close' prices, and 3rd figure has the plot of 'Volumn'
    # +++ Your Code Below +++ 
    myfigOpen = fig.Figure(figsize = (4, 3))
    myfigClose = fig.Figure(figsize = (4, 3))
    myfigVolume= fig.Figure(figsize = (4, 3))

    # +++ Your Code Above +++ 

    # add three subplots
    # +++ Your Code Below +++ 
    myfigOpen = myfigOpen.add_subplot()
    myfigClose = myfigClose.add_subplot()
    myfigVolume = myfigVolume.add_subplot()
    # +++ Your Code Above +++ 
  
    # plot three graphs
    # +++ Your Code Below +++ 
    myfigOpen.plot(open_data, color='red', label= "Open")  
    myfigOpen.legend(loc='upper right') 
    myfigClose.plot(adjclose_data, color='blue', label='Adj Close')   
    myfigClose.legend(loc='upper right')   
    myfigVolume.plot(volume_data, color='blue', label='Volume')   
    myfigVolume.legend(loc='upper right') 
    # +++ Your Code Above +++ 
 
    # create three Tkinter canvas
    # +++ Your Code Below +++ 
    mycanvas1 = bac.FigureCanvasTkAgg(myfigOpen, master = mywindow)
    mycanvas1.draw()
    mycanvas2 = bac.FigureCanvasTkAgg(myfigClose, master = mywindow)
    mycanvas2.draw()
    mycanvas3 = bac.FigureCanvasTkAgg(myfigVolume, master = mywindow)
    mycanvas3.draw()
    # +++ Your Code Above +++ 
    
    # place the canvas on the Tkinter window at (x=1, y=70), (x=370, y=70) and (x=740, y=70) respectively.
    # +++ Your Code Below +++ 
    mycanvas1.get_tk_widget().place(x=1, y=70)
    mycanvas2.get_tk_widget().place(x=370, y=70)
    mycanvas3.get_tk_widget().place(x=740, y=70)
    # +++ Your Code Above +++ 
    
def QuitNow():
    mywindow.destroy()


# create a main window
mywindow = tk.Tk()
mywindow.geometry('1100x400')
mywindow.title('Plotting in Tkinter')

tk.Label(mywindow, text = 'Ticker').pack(side=tk.TOP)
my_ticker_entry = tk.StringVar(mywindow)
# create a text entry box and store the ticker in "my_ticker_entry"
# +++ Your Code Below +++ 
tk.Entry(mywindow, textvariable = my_ticker_entry).pack(side=tk.TOP)

# +++ Your Code Above +++ 

# create a push-button named "Plot Chart" and it will call a function "PlotChart()"
# create another push-button named "Quit Now" and it will call a function "QuitNow()"
# +++ Your Code Below +++ 
tk.Button(master=mywindow, text="Plot My Chart", command = PlotChart).pack(side=tk.TOP)
tk.Button(master=mywindow, text="Quit Now", command= QuitNow).pack(side=tk.BOTTOM)

# +++ Your Code Above +++ 


mywindow.mainloop()
