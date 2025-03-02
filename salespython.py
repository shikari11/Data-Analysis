import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

class SalesPerformanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Performance Analysis")

        # Create a button to load the CSV file
        self.load_button = tk.Button(root, text="Load Sales Data", command=self.load_data)
        self.load_button.pack()

        # Create buttons for different graphs
        self.total_sales_button = tk.Button(root, text="Show Total Sales by Product", command=self.show_total_sales)
        self.total_sales_button.pack()

        self.sales_by_time_button = tk.Button(root, text="Show Sales by Time", command=self.show_sales_by_time)
        self.sales_by_time_button.pack()

        # Create a canvas for the plots
        self.figure, self.ax = plt.subplots(figsize=(10, 5))  # Adjusted to a single plot
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Initialize dataframe
        self.df = None

    def load_data(self):
        # Load CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df['Sales'] = pd.to_numeric(self.df['Sales'])

    def show_total_sales(self):
        if self.df is not None:
            self.figure.clear()
            self.ax = self.figure.add_subplot(111)
            
            # Total sales by product
            sales_by_product = self.df.groupby('Product')['Sales'].sum()
            sales_by_product.plot(kind='bar', ax=self.ax)
            self.ax.set_title('Total Sales by Product')
            self.ax.set_xlabel('Product')
            self.ax.set_ylabel('Total Sales')
            self.canvas.draw()

    def show_sales_by_time(self):
        if self.df is not None:
            self.figure.clear()
            self.ax = self.figure.add_subplot(111)
            
            # Sales by time
            self.df_sorted = self.df.sort_values('Date')
            for product in self.df['Product'].unique():
                product_data = self.df_sorted[self.df_sorted['Product'] == product]
                self.ax.plot(product_data['Date'], product_data['Sales'], label=product)
            
            self.ax.set_title('Sales Over Time')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Sales')
            self.ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            self.ax.xaxis.set_major_locator(mdates.MonthLocator())
            self.ax.legend()
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesPerformanceApp(root)
    root.mainloop()
