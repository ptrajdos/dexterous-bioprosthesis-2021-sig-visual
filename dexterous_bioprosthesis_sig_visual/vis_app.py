import multiprocessing
import os
import tkinter as tk
from tkinter import END, ttk, Button, messagebox

from matplotlib.figure import Figure
import numpy as np
from dexterous_bioprosthesis_2021_raw_datasets.raw_signals.raw_signal import RawSignal
from dexterous_bioprosthesis_2021_raw_datasets.raw_signals.raw_signals import RawSignals
from dexterous_bioprosthesis_2021_raw_datasets.raw_signals.raw_signals_io import read_signals_from_dirs
from tkinter import filedialog
from tkinter import messagebox

from scipy import signal
import joblib
from joblib import Parallel
joblib.parallel.DEFAULT_N_JOBS=None

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from dexterous_bioprosthesis_sig_visual import settings
from functools import wraps


class RawSignalVisualizer(tk.Frame):
    def __init__(self, parent,n_jobs = None, *args, **kwargs):
        tk.Frame.__init__(self, parent,  *args, **kwargs, height=300)
        self.parent = parent
        self.n_jobs = n_jobs

        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        try:
            self.parent.attributes('-zoomed', True)
        except tk.TclError:
            self.parent.state('zoomed')

        self.parent.title('Podgląd danych')
        self.zoom_val = 1

        self.bind_keys()
        self._create_menubar()
        self.init_listbox_signals()
        self.init_listbox_channels_frame()
        self.plot_frame_init()

    def _create_menubar(self):
        self.menubar = tk.Menu(self.parent)

        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(label="Open Directory", command=self.open_directory)

        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Help", command=self.open_help_window)

        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)



        self.parent.config(menu=self.menubar)
    
    def open_help_window(self):
        help_window = tk.Toplevel(self.parent)
        help_window.title("Help")
        help_window.geometry("800x600")
        
        help_text = """
        Otwieranie zbioru: File -> Open Directory
        Skróty klawiaturowe:
        <Up>: Następny obiekt
        <Down>: Poprzedni obiekt
        <Left>: Następny kanał
        <Right>: Poprzedni kanał
        """

        help_label = tk.Label(help_window, text=help_text)
        help_label.pack(pady=20, padx=20)

        ok_button = ttk.Button(help_window, text="OK", command=help_window.destroy)
        ok_button.pack(pady=10)

    def open_directory(self):
        dir_path = filedialog.askdirectory(title="Open Directory")
        if dir_path:
            self._load_from_directory(dir_path)

    def _load_from_directory(self, path, subset='accepted'):
        
        raw_set = read_signals_from_dirs(path, n_jobs=self.n_jobs, parallel_options={'backend':'multiprocessing'})[subset]
        self._data_init(raw_set)

    def _data_init(self, raw_signals:RawSignals):
        self.set_data(raw_signals=raw_signals)
        self.reload_listbox_signals()
        self.reload_listbox_channels()
        self.plot_selected_signal()


    def set_data(self, raw_signals:RawSignals):
        self.raw_signals = raw_signals
        self.selected_signal:RawSignal= raw_signals[0]
        self.selected_channel = self.selected_signal.signal[:,0]

        

    def make_raw_signals_list_representation(self, raw_signals:RawSignals):

        return [ "{}: {}".format(i, raw_signal.object_class) for i, raw_signal in enumerate(raw_signals)]

    def bind_keys(self):
        self.parent.bind('<Escape>', self.on_closing)
        self.parent.bind('<Down>', self.next_object)
        self.parent.bind('<Up>', self.prev_object)
        self.parent.bind('<Right>', self.next_channel)
        self.parent.bind('<Left>', self.prev_channel)

    def init_listbox_signals(self):
        self.frame_listbox = tk.Frame(self.parent,pady=1, padx=1)
        self.listbox_objects_var  = tk.Variable(value=[])
        self.listbox_objects = tk.Listbox(
                    self.frame_listbox,
                    listvariable= self.listbox_objects_var,
                    width=20,
                    selectmode=tk.SINGLE,
                    font = ("Consolas", 10))

        self.listbox_objects.pack(side="left", fill="both")
        self.listbox_objects.configure(exportselection=False)

        
        scrollbar = ttk.Scrollbar(
            self.frame_listbox,
            orient=tk.VERTICAL,
            command=self.listbox_objects.yview
        )

        self.listbox_objects['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side="right", expand=True, fill="both")
        self.listbox_objects.bind('<<ListboxSelect>>', self.object_selected)

        self.listbox_objects.selection_clear(0, tk.END)
        self.listbox_objects.selection_set(0)
        self.listbox_objects.see(0)
        self.listbox_objects.activate(0)
        self.listbox_objects.selection_anchor(0)

        self.frame_listbox.pack(side="left", fill="both")
        

    def reload_listbox_signals(self):
        
        self.listbox_objects_var.set(self.make_raw_signals_list_representation(self.raw_signals))

        self.listbox_objects.selection_clear(0, tk.END)
        self.listbox_objects.selection_set(0)
        self.listbox_objects.see(0)
        self.listbox_objects.activate(0)
        self.listbox_objects.selection_anchor(0)  
       
            

    def object_selected(self, event):

        try: 

            selected_objects_idxs = self.listbox_objects.curselection()
            selected_object_idx = int( selected_objects_idxs[0])

            self.selected_signal = self.raw_signals[selected_object_idx]
            self.selected_channel = self.selected_signal.signal[:,0]


            self.listbox_channels.selection_clear(0, tk.END)
            self.listbox_channels.selection_set(0)
            self.listbox_channels.see(0)
            self.listbox_channels.activate(0)
            self.listbox_channels.selection_anchor(0)

            self.plot_selected_signal()
        except IndexError as id:
            pass
        except Exception as e:
            raise e



    def reload_listbox_channels(self):
        self.listbox_channels_variable.set([str(ch_name) for ch_name in self.selected_signal.channel_names ])

        self.listbox_channels.selection_clear(0, tk.END)
        self.listbox_channels.selection_set(0)
        self.listbox_channels.see(0)
        self.listbox_channels.activate(0)
        self.listbox_channels.selection_anchor(0)


    def init_listbox_channels_frame(self):
        
        frame_listbox = tk.Frame(self.parent,pady=1, padx=1)
        self.listbox_channels_variable = tk.Variable(value=[])

        self.listbox_channels = tk.Listbox(
                    frame_listbox,
                    listvariable=self.listbox_channels_variable,
                    width=10,
                    selectmode=tk.SINGLE,
                    font = ("Consolas", 10))

        self.listbox_channels.pack(side="left", fill="both")
        self.listbox_channels.configure(exportselection=False)

        scrollbar = ttk.Scrollbar(
            frame_listbox,
            orient=tk.VERTICAL,
            command=self.listbox_channels.yview
        )

        self.listbox_channels['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side="right", expand=True, fill="both")
        self.listbox_channels.bind('<<ListboxSelect>>', self.channel_selected)

        self.listbox_channels.selection_clear(0, tk.END)
        self.listbox_channels.selection_set(0)
        self.listbox_channels.see(0)
        self.listbox_channels.activate(0)
        self.listbox_channels.selection_anchor(0)
        

        frame_listbox.pack(side="left", fill="both")

    def channel_selected(self,event):

        try: 

            selected_channel_idxs = self.listbox_channels.curselection()
            if len(selected_channel_idxs)  == 1:
                selected_channel_idx = int( selected_channel_idxs[0])

                self.selected_channel = self.selected_signal.signal[:,selected_channel_idx]
                
                self.plot_selected_signal()
                return

        except IndexError as id:
            pass
        except Exception as e:
            raise e

    def plot_selected_signal(self):

        obj_idx = self.listbox_objects.curselection()[0]
        obj_class = self.selected_signal.object_class
        channel_idx = self.listbox_channels.curselection()[0]
        self.canvas.figure.suptitle("Idx: {}, Class: {}, Channel: {}".format(obj_idx, obj_class, channel_idx))

        ax0 =  self.canvas.figure.axes[0]
        ax0.clear()
        ax0.set_xlabel('Sample number')
        ax0.set_ylabel('Amplitude')
        ax0.set_title('Signal')
        ax0.plot(self.selected_channel)

        ax1 =  self.canvas.figure.axes[1]
        ax1.clear()

        f, t, Sxx = signal.spectrogram(self.selected_channel,self.raw_signals.sample_rate)
        # cwt_sig = signal.cwt(self.selected_channel, wavelet=signal.ricker, widths=np.arange(1,3001))
        # cwt_sig_flip = np.flip(cwt_sig)
        ax1.pcolormesh(t, f, Sxx, shading='gouraud',cmap='viridis')
        # ax1.imshow(cwt_sig_flip)
        ax1.set_title('Spectrogram')
        ax1.set_ylabel('Frequency [Hz]')
        ax1.set_xlabel('Time [sec]')

        ax2 =  self.canvas.figure.axes[2]
        ax2.clear()

        ax2.magnitude_spectrum(self.selected_channel, Fs=self.raw_signals.sample_rate, scale='dB', color='C1')

        self.canvas.draw()



    def plot_frame_init(self):
        frame_listbox = tk.Frame(self.parent,pady=1, padx=1)

        self.figure = Figure(figsize = (20, 10))
        self.figure.add_subplot(1,3,1)
        self.figure.add_subplot(1,3,2)
        self.figure.add_subplot(1,3,3)
        

        self.canvas = FigureCanvasTkAgg(self.figure, master=frame_listbox)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(self.canvas, root)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        frame_listbox.pack(side="left", fill="both")


    def on_closing(self, event=None):
        self.parent.destroy()

    def next_object(self, event):
        n_objects = len(self.raw_signals)

        curr_idx = self.listbox_objects.curselection()[0]
        next_idx = curr_idx

        if curr_idx < n_objects-1:
            next_idx +=1
        else:
            next_idx=0
            
        self.listbox_objects.select_clear(0,tk.END)
        self.listbox_objects.selection_set(next_idx)
        self.listbox_objects.see(next_idx)
        self.listbox_objects.activate(next_idx)
        self.listbox_objects.select_anchor(next_idx)

        self.selected_signal = self.raw_signals[next_idx]


        channel_idx = self.listbox_channels.curselection()[0]
        self.selected_channel = self.selected_signal.signal[:,channel_idx]
        self.plot_selected_signal()

 
    def prev_object(self, event):
        n_objects = len(self.raw_signals)

        curr_idx = self.listbox_objects.curselection()[0]
        next_idx = curr_idx

        if curr_idx > 0:
            next_idx -=1
        else:
            next_idx= n_objects -1
            
        self.listbox_objects.select_clear(0,tk.END)
        self.listbox_objects.selection_set(next_idx)
        self.listbox_objects.see(next_idx)
        self.listbox_objects.activate(next_idx)
        self.listbox_objects.select_anchor(next_idx)

        self.selected_signal = self.raw_signals[next_idx]

        channel_idx = self.listbox_channels.curselection()[0]
        self.selected_channel = self.selected_signal.signal[:,channel_idx]
        self.plot_selected_signal()
 
    def next_channel(self, event):

        n_channels = self.selected_signal.signal.shape[1]
        curr_idx = self.listbox_channels.curselection()[0]
        next_idx = curr_idx

        if curr_idx < n_channels -1:
            next_idx += 1
        else:
            next_idx = 0

        self.listbox_channels.select_clear(0,tk.END)
        self.listbox_channels.selection_set(next_idx)
        self.listbox_channels.see(next_idx)
        self.listbox_channels.activate(next_idx)
        self.listbox_channels.select_anchor(next_idx)

        self.selected_channel = self.selected_signal.signal[:,next_idx]
        self.plot_selected_signal()
 
    def prev_channel(self, event):
        n_channels = self.selected_signal.signal.shape[1]
        curr_idx = self.listbox_channels.curselection()[0]
        next_idx = curr_idx

        if curr_idx > 0:
            next_idx -= 1
        else:
            next_idx = n_channels - 1

        self.listbox_channels.select_clear(0,tk.END)
        self.listbox_channels.selection_set(next_idx)
        self.listbox_channels.see(next_idx)
        self.listbox_channels.activate(next_idx)
        self.listbox_channels.select_anchor(next_idx)

        self.selected_channel = self.selected_signal.signal[:,next_idx]
        self.plot_selected_signal()
 


if __name__ == "__main__":
    multiprocessing.freeze_support()

    root = tk.Tk()
    RawSignalVisualizer(root, n_jobs=-1).pack(side="top", fill="both", expand=True)
    root.mainloop()
    
