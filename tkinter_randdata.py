import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

class ContinuousPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Continuous Random Data Generation and Plotting")

        # Set the window size
        self.root.geometry("1200x1000")  # Width x Height

        # Load the logo
        try:
            self.logo_image = Image.open("lbl_logo.ico")  # Replace with your logo file path
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load logo: {e}")
            self.logo_photo = None

        # Set logo 
        try:
            self.logo_image = Image.open('lbl_logo.ico')  # File has to be in the same path 
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load logo: {e}")
            self.logo_photo = None

        # Display the logo
        if self.logo_photo:
            self.root.iconphoto(False, self.logo_photo)

        # Initialize plots with a smaller figsize
        self.fig, self.axes = plt.subplots(nrows=2, ncols=1, figsize=(6, 8))
        self.lines1 = [self.axes[0].plot([], [], 'r-')[0], self.axes[0].plot([], [], 'b-')[0]]  # Two lines for the first plot
        self.line2 = self.axes[1].plot([], [], 'g-')[0]  # One line for the second plot

        # Set initial limits and titles for each plot
        for ax, title in zip(self.axes, ['Plot 1 (Two Lines)', 'Plot 2 (One Line)']):
            ax.set_xlim(0, 100)
            ax.set_title(title)
            ax.set_xlabel('Time')
            ax.set_ylabel('Amplitude')
            ax.grid(True)  # Enable grid

        # Initialize data arrays for each plot
        self.data1 = [{'x': [], 'y': []}, {'x': [], 'y': []}]  # Data for two lines in the first plot
        self.data2 = {'x': [], 'y': []}  # Data for one line in the second plot

        # Embed plots in Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create annotations for displaying x and y values on hover
        self.hover_annotations = [ax.annotate("", xy=(0, 0), xytext=(20, 20),
                                             textcoords="offset points"
                                             )
                                for ax in self.axes]
        for ann in self.hover_annotations:
            ann.set_visible(False)

        # Connect mouse motion event to the callback function
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

        # Create control buttons using ttk
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.start_button = ttk.Button(self.control_frame, text="Start", command=self.start_plotting)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = ttk.Button(self.control_frame, text="Pause", command=self.stop_plotting)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.save_button = ttk.Button(self.control_frame, text="Save Data", command=self.save_data)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.exit_button = ttk.Button(self.control_frame, text="Exit", command=self.exit_program)
        self.exit_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Flag to control plotting
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
            # Update the first plot with two lines of random data
            for i in range(2):
                # Generate new data point
                new_x1 = len(self.data1[i]['x'])
                new_y1 = np.random.normal(0, 0.5)  # Random data point with larger variance to allow negative values

                # Append new data point to the lists
                self.data1[i]['x'].append(new_x1)
                self.data1[i]['y'].append(new_y1)

                # Update the plot data
                self.lines1[i].set_data(self.data1[i]['x'], self.data1[i]['y'])

                # Adjust the x-axis limit if necessary
                if new_x1 > 99:
                    self.axes[0].set_xlim(new_x1 - 99, new_x1)

            # Auto-adjust y-axis for the first plot
            self.axes[0].relim()
            self.axes[0].autoscale_view()

            # Update the second plot with one line of random data
            new_x2 = len(self.data2['x'])
            new_y2 = np.random.normal(0, 0.5)  # Random data point with larger variance to allow negative values

            # Append new data point to the lists
            self.data2['x'].append(new_x2)
            self.data2['y'].append(new_y2)

            # Update the plot data
            self.line2.set_data(self.data2['x'], self.data2['y'])

            # Adjust the x-axis limit if necessary
            if new_x2 > 99:
                self.axes[1].set_xlim(new_x2 - 99, new_x2)

            # Auto-adjust y-axis for the second plot
            self.axes[1].relim()
            self.axes[1].autoscale_view()

            # Redraw the canvas
            self.canvas.draw()

            # Schedule the next update
            self.root.after(100, self.update_plots)  # Update every 100 ms

    def save_data(self):
        # Combine data into a DataFrame
        df1_1 = pd.DataFrame(self.data1[0])
        df1_2 = pd.DataFrame(self.data1[1])
        df2 = pd.DataFrame(self.data2)

        # Ask for file name and location
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                               filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                                               title="Save Data")
        if file_path:
            # Save to Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df1_1.to_excel(writer, sheet_name='Plot1_Line1', index=False)
                df1_2.to_excel(writer, sheet_name='Plot1_Line2', index=False)
                df2.to_excel(writer, sheet_name='Plot2_Line1', index=False)

            messagebox.showinfo("Save Data", f"Data saved successfully to {file_path}")
            self.data_saved = True

    def exit_program(self):
        if not self.data_saved:
            confirm = messagebox.askyesnocancel("Confirm Exit", "You have unsaved data. Do you want to save it before exiting?")
            if confirm is None:
                return  # User clicked Cancel
            elif confirm:
                self.save_data()
                if not self.data_saved:
                    return  # User canceled the save operation

        if self.is_plotting:
            self.stop_plotting()
        self.root.destroy()

    def on_motion(self, event):
        for i, ax in enumerate(self.axes):
            if event.inaxes == ax:
                cont, ind = ax.contains(event)
                if cont:
                    x, y = event.xdata, event.ydata
                    self.hover_annotations[i].xy = (x, y)
                    self.hover_annotations[i].set_text(f"x: {x:.2f}\ny: {y:.2f}")
                    self.hover_annotations[i].set_visible(True)
                    # Adjust annotation position to avoid going off-screen
                    if y < 0:
                        self.hover_annotations[i].set_verticalalignment('top')
                    else:
                        self.hover_annotations[i].set_verticalalignment('bottom')
                else:
                    self.hover_annotations[i].set_visible(False)
            else:
                self.hover_annotations[i].set_visible(False)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = ContinuousPlotApp(root)
    root.mainloop()