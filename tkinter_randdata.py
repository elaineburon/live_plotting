# 2025 06 22 21:21 

# - Fix Excel file to have all the y-val saved into a single sheet
# - Center the plots in their frames
# - Icon function not working

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import messagebox, filedialog
import pandas as pd
from PIL import Image, ImageTk
import os

class ContinuousPlotApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Continuous Plot")
        self.root.geometry("1920x1080")
        self.root.resizable(width=True, height=True)

        try:
            self.root.iconbitmap("lbl_logo.ico")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load logo: {e}")

        self.file_path = None
        self.data1 = [{'x': [], 'y': []}, {'x': [], 'y': []}]
        self.data2 = {'x': [], 'y': []}

        self.follow_var1 = ctk.BooleanVar(value=True)
        self.follow_var2 = ctk.BooleanVar(value=True)

        # Container for plots and controls
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(2, weight=0)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Left side - Plots
        self.plots_frame = ctk.CTkFrame(self.main_frame, width=150, border_width=1, border_color="red")
        self.plots_frame.grid(row=0, column=0, sticky="nsew")

        # Plot 1
        self.plot1_container = ctk.CTkFrame(self.plots_frame)
        self.plot1_container.pack(padx=10, pady=10, fill="x")
        self.plot1_container.grid_columnconfigure(0, weight=1)
        self.plot1_container.grid_columnconfigure(1, weight=0)

        self.canvas1_container = ctk.CTkFrame(self.plot1_container)
        self.canvas1_container.grid(row=0, column=0, sticky="nsew")

        self.fig1, self.ax1 = plt.subplots(figsize=(10, 4.5))
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
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.canvas1_container)
        self.canvas1_widget = self.canvas1.get_tk_widget()
        self.canvas1_widget.pack(pady=10)
        self.canvas1.mpl_connect('scroll_event', lambda event: self.on_scroll(event, self.ax1, self.data1))
        self.canvas1_widget.bind('<B1-Motion>', lambda event: self.drag_scroll(event, self.ax1, self.data1))

        # Controls for Plot 1 (aligned vertically center right)
        self.plot1_controls = ctk.CTkFrame(self.plot1_container)
        self.plot1_controls.grid(row=0, column=1, sticky="ns", padx=200, pady=200)
        self.plot1_controls.grid_rowconfigure(0, weight=1)
        self.plot1_controls.grid_rowconfigure(1, weight=1)
        self.jump1_button = ctk.CTkButton(self.plot1_controls, text="Jump to Current 1", command=self.jump_to_current1)
        self.jump1_button.grid(row=0, column=0, pady=(115, 5))
        self.follow_check1 = ctk.CTkCheckBox(self.plot1_controls, text="Disable Auto-Follow 1", variable=self.follow_var1, onvalue=False, offvalue=True)
        self.follow_check1.grid(row=0, column=0, pady=(185, 5))

        # Plot 2
        self.plot2_container = ctk.CTkFrame(self.plots_frame)
        self.plot2_container.pack(padx=10, pady=10, fill="x")
        self.plot2_container.grid_columnconfigure(0, weight=1)
        self.plot2_container.grid_columnconfigure(1, weight=0)

        self.canvas2_container = ctk.CTkFrame(self.plot2_container)
        self.canvas2_container.grid(row=1, column=0, sticky="nsew")

        self.fig2, self.ax2 = plt.subplots(figsize=(10, 4.5))
        self.line2 = self.ax2.plot([], [], 'g-', label='Line 3')[0]
        self.ax2.set_xlim(0, 100)
        self.ax2.set_title('Plot 2 (One Line)')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Amplitude')
        self.ax2.grid(True)
        self.ax2.legend(loc='upper right')
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.canvas2_container)
        self.canvas2_widget = self.canvas2.get_tk_widget()
        self.canvas2_widget.pack(pady=10)
        self.canvas2.mpl_connect('scroll_event', lambda event: self.on_scroll(event, self.ax2, [self.data2]))
        self.canvas2_widget.bind('<B1-Motion>', lambda event: self.drag_scroll(event, self.ax2, [self.data2]))

        # Controls for Plot 2 (aligned vertically center right)
        self.plot2_controls = ctk.CTkFrame(self.plot2_container, width=150, border_width=1, border_color="red")
        self.plot2_controls.grid(row=1, column=1, sticky="ns", padx=200)
        self.plot2_controls.grid_rowconfigure(0, weight=1)
        self.plot2_controls.grid_rowconfigure(1, weight=1)
        self.jump2_button = ctk.CTkButton(self.plot2_controls, text="Jump to Current 2", command=self.jump_to_current2)
        self.jump2_button.grid(row=0, column=0, pady=(115, 5))
        self.follow_check2 = ctk.CTkCheckBox(self.plot2_controls, text="Disable Auto-Follow 2", variable=self.follow_var2, onvalue=False, offvalue=True)
        self.follow_check2.grid(row=0, column=0, pady=(185, 5))

        # Main control buttons on the far right
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.grid(row=0, column=2, sticky="ns", padx=10, pady=10)
        self.start_button = ctk.CTkButton(self.control_frame, text="Start", command=self.start_plotting)
        self.start_button.pack(pady=5, fill="x")
        self.stop_button = ctk.CTkButton(self.control_frame, text="Pause", command=self.stop_plotting)
        self.stop_button.pack(pady=5, fill="x")
        self.save_button = ctk.CTkButton(self.control_frame, text="Save Data", command=self.save_data)
        self.save_button.pack(pady=5, fill="x")
        self.exit_button = ctk.CTkButton(self.control_frame, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=5, fill="x")

        self.hover_annotations = [
            self.ax1.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points"),
            self.ax2.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points")
        ]
        for ann in self.hover_annotations:
            ann.set_visible(False)
        self.canvas1.mpl_connect('motion_notify_event', lambda event: self.on_motion(event, self.ax1, 0))
        self.canvas2.mpl_connect('motion_notify_event', lambda event: self.on_motion(event, self.ax2, 1))

        self.is_plotting = False
        self.data_saved = False

    def on_scroll(self, event, ax, data):
        if ax == self.ax1:
            self.follow_var1.set(False)
        elif ax == self.ax2:
            self.follow_var2.set(False)
        x_min, x_max = ax.get_xlim()
        step = (x_max - x_min) * 0.1
        direction = -1 if event.button == 'up' else 1
        max_x = max([max(d['x']) if d['x'] else 0 for d in data])
        new_min = min(max(0, x_min + direction * step), max_x - (x_max - x_min))
        new_max = new_min + (x_max - x_min)
        ax.set_xlim(new_min, new_max)
        ax.figure.canvas.draw_idle()

    def drag_scroll(self, event, ax, data):
        if ax == self.ax1:
            self.follow_var1.set(False)
        elif ax == self.ax2:
            self.follow_var2.set(False)
        if event.x != 0:
            x_min, x_max = ax.get_xlim()
            dx = -(event.x - getattr(self, 'last_drag_x', event.x)) * 0.1
            new_min = max(0, x_min + dx)
            max_x = max([max(d['x']) if d['x'] else 0 for d in data])
            plot_width = x_max - x_min
            new_min = min(new_min, max_x - plot_width)
            ax.set_xlim(new_min, new_min + plot_width)
            ax.figure.canvas.draw_idle()
            self.last_drag_x = event.x

    def on_motion(self, event, ax, index):
        if event.inaxes == ax and event.xdata and event.ydata:
            self.hover_annotations[index].xy = (event.xdata, event.ydata)
            self.hover_annotations[index].set_text(f"x: {event.xdata:.2f}\ny: {event.ydata:.2f}")
            self.hover_annotations[index].set_visible(True)
        else:
            self.hover_annotations[index].set_visible(False)
        ax.figure.canvas.draw_idle()

    def start_plotting(self):
        if not self.file_path:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Choose file to save data"
            )
            if not file_path:
                messagebox.showwarning("No File", "No file selected. Aborting start.")
                return
            self.file_path = file_path
            filename = os.path.basename(file_path)
            self.root.title(f"Continuous Plot - {filename}")

        if not self.is_plotting:
            self.is_plotting = True
            self.follow_var1.set(True)
            self.follow_var2.set(True)
            self.update_plots()

    def stop_plotting(self):
        self.is_plotting = False

    def jump_to_current1(self):
        self.follow_var1.set(True)

    def jump_to_current2(self):
        self.follow_var2.set(True)

    def update_plots(self):
        if self.is_plotting:
            for i in range(2):
                new_x1 = len(self.data1[i]['x'])
                new_y1 = np.random.normal(0, 0.5)
                self.data1[i]['x'].append(new_x1)
                self.data1[i]['y'].append(new_y1)
                self.lines1[i].set_data(self.data1[i]['x'], self.data1[i]['y'])

            self.ax1.relim()
            self.ax1.autoscale_view()
            if self.follow_var1.get():
                x_max = len(self.data1[0]['x'])
                self.ax1.set_xlim(max(0, x_max - 100), x_max)
            self.canvas1.draw()

            new_x2 = len(self.data2['x'])
            new_y2 = np.random.normal(0, 0.5)
            self.data2['x'].append(new_x2)
            self.data2['y'].append(new_y2)
            self.line2.set_data(self.data2['x'], self.data2['y'])

            self.ax2.relim()
            self.ax2.autoscale_view()
            if self.follow_var2.get():
                x_max = len(self.data2['x'])
                self.ax2.set_xlim(max(0, x_max - 100), x_max)
            self.canvas2.draw()

            self.root.after(100, self.update_plots)

    def save_data(self):
        df1_1 = pd.DataFrame(self.data1[0])
        df1_2 = pd.DataFrame(self.data1[1])
        df2 = pd.DataFrame(self.data2)

        file_path = self.file_path
        if file_path:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df1_1.to_excel(writer, sheet_name='Plot1_Line1', index=False)
                df1_2.to_excel(writer, sheet_name='Plot1_Line2', index=False)
                df2.to_excel(writer, sheet_name='Plot2_Line1', index=False)
            messagebox.showinfo("Save Data", f"Data saved to {file_path}")
            self.data_saved = True

    def exit_program(self):
        if not self.data_saved:
            confirm = messagebox.askyesnocancel("Exit", "Save data before exiting?")
            if confirm is None:
                return
            elif confirm:
                self.save_data()
                if not self.data_saved:
                    return
        self.root.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    app = ContinuousPlotApp(root)
    root.mainloop()