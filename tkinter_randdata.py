import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from PIL import Image, ImageTk

class ContinuousPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Continuous Random Data Generation and Plotting")
        self.root.geometry("1920x1080")

        # Load the logo (optional)
        try:
            self.logo_image = Image.open("lbl_logo.ico")
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.root.iconphoto(False, self.logo_photo)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load logo: {e}")

        self.data1 = [{'x': [], 'y': []}, {'x': [], 'y': []}]
        self.data2 = {'x': [], 'y': []}

        # Plot 1 Frame with scrollbar
        self.frame1_container = ttk.Frame(self.root)
        self.frame1_container.pack(fill=tk.BOTH, expand=True)
        self.frame1_canvas = tk.Canvas(self.frame1_container)
        self.frame1_scrollbar = ttk.Scrollbar(self.frame1_container, orient="horizontal")
        self.frame1_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.frame1_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frame1_canvas.configure(xscrollcommand=self.frame1_scrollbar.set)

        self.frame1 = ttk.Frame(self.frame1_canvas)
        self.frame1_canvas.create_window((0, 0), window=self.frame1, anchor="nw")
        self.frame1.bind("<Configure>", lambda e: self.frame1_canvas.configure(scrollregion=self.frame1_canvas.bbox("all")))

        self.fig1, self.ax1 = plt.subplots(figsize=(10, 4))
        self.lines1 = [
            self.ax1.plot([], [], 'r-', label='Line 1')[0],
            self.ax1.plot([], [], 'b-', label='Line 2')[0]
        ]
        self.ax1.set_xlim(0, 100)
        self.ax1.set_title('Plot 1 (Two Lines)')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Amplitude')
        self.ax1.grid(True)
        self.ax1.legend(loc='upper right')
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.frame1)
        self.canvas1_widget = self.canvas1.get_tk_widget()
        self.canvas1_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas1.mpl_connect('scroll_event', lambda event: self.on_scroll(event, self.ax1, reverse=True))

        self.frame1_scrollbar.config(command=lambda *args: self.scroll_from_scrollbar(self.ax1, *args))

        # Plot 2 Frame with scrollbar
        self.frame2_container = ttk.Frame(self.root)
        self.frame2_container.pack(fill=tk.BOTH, expand=True)
        self.frame2_canvas = tk.Canvas(self.frame2_container)
        self.frame2_scrollbar = ttk.Scrollbar(self.frame2_container, orient="horizontal")
        self.frame2_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.frame2_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frame2_canvas.configure(xscrollcommand=self.frame2_scrollbar.set)

        self.frame2 = ttk.Frame(self.frame2_canvas)
        self.frame2_canvas.create_window((0, 0), window=self.frame2, anchor="nw")
        self.frame2.bind("<Configure>", lambda e: self.frame2_canvas.configure(scrollregion=self.frame2_canvas.bbox("all")))

        self.fig2, self.ax2 = plt.subplots(figsize=(10, 4))
        self.line2 = self.ax2.plot([], [], 'g-', label='Line 3')[0]
        self.ax2.set_xlim(0, 100)
        self.ax2.set_title('Plot 2 (One Line)')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Amplitude')
        self.ax2.grid(True)
        self.ax2.legend(loc='upper right')
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.frame2)
        self.canvas2_widget = self.canvas2.get_tk_widget()
        self.canvas2_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas2.mpl_connect('scroll_event', lambda event: self.on_scroll(event, self.ax2, reverse=True))

        self.frame2_scrollbar.config(command=lambda *args: self.scroll_from_scrollbar(self.ax2, *args))

        # Hover annotations
        self.hover_annotations = [
            self.ax1.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points"),
            self.ax2.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points")
        ]
        for ann in self.hover_annotations:
            ann.set_visible(False)
        self.canvas1.mpl_connect('motion_notify_event', lambda event: self.on_motion(event, self.ax1, 0))
        self.canvas2.mpl_connect('motion_notify_event', lambda event: self.on_motion(event, self.ax2, 1))

        # Control buttons
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.start_button = ttk.Button(self.control_frame, text="Start", command=self.start_plotting)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(self.control_frame, text="Pause", command=self.stop_plotting)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.save_button = ttk.Button(self.control_frame, text="Save Data", command=self.save_data)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = ttk.Button(self.control_frame, text="Exit", command=self.exit_program)
        self.exit_button.pack(side=tk.RIGHT, padx=10)

        self.is_plotting = False
        self.data_saved = False

    def start_plotting(self):
        if not self.is_plotting:
            self.is_plotting = True
            self.update_plots()

    def stop_plotting(self):
        self.is_plotting = False

    def update_plots(self):
        if self.is_plotting:
            for i in range(2):
                new_x = len(self.data1[i]['x'])
                new_y = np.random.normal(0, 0.5)
                self.data1[i]['x'].append(new_x)
                self.data1[i]['y'].append(new_y)
                self.lines1[i].set_data(self.data1[i]['x'], self.data1[i]['y'])

            new_x1 = len(self.data1[0]['x']) - 1
            if new_x1 > 99:
                self.ax1.set_xlim(new_x1 - 99, new_x1)

            self.ax1.relim()
            self.ax1.autoscale_view(scalex=False, scaley=True)

            new_x2 = len(self.data2['x'])
            new_y2 = np.random.normal(0, 0.5)
            self.data2['x'].append(new_x2)
            self.data2['y'].append(new_y2)
            self.line2.set_data(self.data2['x'], self.data2['y'])

            if new_x2 > 99:
                self.ax2.set_xlim(new_x2 - 99, new_x2)

            self.ax2.relim()
            self.ax2.autoscale_view(scalex=False, scaley=True)

            max_scroll1 = max(self.data1[0]['x'] + self.data1[1]['x'], default=100)
            max_scroll2 = max(self.data2['x'], default=100)

            self.frame1_scrollbar.set(0.0, 100 / max(max_scroll1, 100))
            self.frame2_scrollbar.set(0.0, 100 / max(max_scroll2, 100))

            self.canvas1.draw()
            self.canvas2.draw()
            self.root.after(100, self.update_plots)

    def scroll_from_scrollbar(self, ax, *args):
        try:
            view_start = float(args[0])
        except:
            return
        data_x = self.data1[0]['x'] + self.data1[1]['x'] if ax == self.ax1 else self.data2['x']
        max_x = max(data_x, default=100)
        plot_width = 100
        new_min = view_start * max_x
        new_max = new_min + plot_width
        if new_max > max_x:
            new_max = max_x
            new_min = max(0, new_max - plot_width)
        ax.set_xlim(new_min, new_max)
        ax.figure.canvas.draw_idle()

    def on_scroll(self, event, ax, reverse=False):
        x_min, x_max = ax.get_xlim()
        range_x = x_max - x_min
        step = range_x * 0.1
        max_x = 0
        if ax == self.ax1:
            max_x = max(self.data1[0]['x'] + self.data1[1]['x'], default=100)
        elif ax == self.ax2:
            max_x = max(self.data2['x'], default=100)

        if (event.button == 'up' and not reverse) or (event.button == 'down' and reverse):
            new_x_max = min(max_x, x_max + step)
            new_x_min = max(0, new_x_max - range_x)
        elif (event.button == 'down' and not reverse) or (event.button == 'up' and reverse):
            new_x_min = max(0, x_min - step)
            new_x_max = new_x_min + range_x

        ax.set_xlim(new_x_min, new_x_max)
        ax.figure.canvas.draw_idle()

    def save_data(self):
        max_len = max(len(self.data1[0]['x']), len(self.data1[1]['x']))
        x_values = self.data1[0]['x'] + [np.nan] * (max_len - len(self.data1[0]['x']))
        y1 = self.data1[0]['y'] + [np.nan] * (max_len - len(self.data1[0]['y']))
        y2 = self.data1[1]['y'] + [np.nan] * (max_len - len(self.data1[1]['y']))

        df = pd.DataFrame({
            'X': x_values,
            'Line1_Y': y1,
            'Line2_Y': y2
        })

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                                                 title="Save Data")
        if file_path:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Plot1_XY_Values', index=False)
            messagebox.showinfo("Save Data", f"X and Y values from Plot 1 saved successfully to {file_path}")
            self.data_saved = True

    def exit_program(self):
        if not self.data_saved:
            confirm = messagebox.askyesnocancel("Confirm Exit", "You have unsaved data. Do you want to save it before exiting?")
            if confirm is None:
                return
            elif confirm:
                self.save_data()
                if not self.data_saved:
                    return
        if self.is_plotting:
            self.stop_plotting()
        self.root.destroy()

    def on_motion(self, event, ax, index):
        if event.inaxes == ax:
            cont, _ = ax.contains(event)
            if cont:
                x, y = event.xdata, event.ydata
                self.hover_annotations[index].xy = (x, y)
                self.hover_annotations[index].set_text(f"x: {x:.2f}\ny: {y:.2f}")
                self.hover_annotations[index].set_visible(True)
            else:
                self.hover_annotations[index].set_visible(False)
        else:
            self.hover_annotations[index].set_visible(False)
        if index == 0:
            self.canvas1.draw()
        else:
            self.canvas2.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContinuousPlotApp(root)
    root.mainloop()