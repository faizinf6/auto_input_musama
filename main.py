import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import threading
import requests
import pyautogui
import time
import json


class AutoInputApp:
    def __init__(self, root):
        self.root = root
        self.data = None  # Initialize data storage
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Auto Input App")

        # Date Selector with dd-mm-yyyy format
        self.date_label = ttk.Label(self.root, text="Select Date:")
        self.date_label.grid(column=0, row=0, padx=10, pady=10)

        self.date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2,
                                    date_pattern='dd-mm-yyyy')
        self.date_entry.grid(column=1, row=0, padx=10, pady=10)

        # Event Selector
        self.event_label = ttk.Label(self.root, text="Select Event:")
        self.event_label.grid(column=0, row=1, padx=10, pady=10)

        self.event_name = tk.StringVar()
        events = ["Jamaah Subuh", "Jamaah Dzuhur", "Jamaah Ashar", "Jamaah Maghrib", "Jamaah Isya", "Ngaji Pagi",
                  "Ngaji Abah","Ngaji Malam"]
        columns = 4  # Number of columns you want to split the buttons into
        rows_per_column = len(events) // columns + (len(events) % columns > 0)

        for idx, event in enumerate(events):
            column_idx = idx // rows_per_column
            row_idx = idx % rows_per_column + 2  # Starting row for radio buttons
            ttk.Radiobutton(self.root, text=event, variable=self.event_name, value=event).grid(column=column_idx,
                                                                                               row=row_idx, padx=10,
                                                                                               pady=2)

        # Status Label for displaying messages
        self.status_label = ttk.Label(self.root, text="Status: Ready")
        self.status_label.grid(column=0, row=5, columnspan=3, sticky=tk.W, padx=10, pady=5)

        # Get Data Button
        self.get_data_button = ttk.Button(self.root, text="Get Data", command=self.fetch_data)
        self.get_data_button.grid(column=0, row=6, padx=10, pady=10)

        # Start Button
        self.start_button = ttk.Button(self.root, text="Start", command=self.start_execution, state='disabled')
        self.start_button.grid(column=1, row=6, padx=10, pady=10)

        # Stop Button
        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_execution, state='disabled')
        self.stop_button.grid(column=2, row=6, padx=10, pady=10)

    def fetch_data(self):
        event_date = self.date_entry.get_date().strftime("%Y_%m_%d")
        event_name = self.event_name.get().replace(" ", "%20")

        try:
            response = requests.get(f"http://103.127.98.123/musama/merge?event_name={event_name}&event_date={event_date}")
            self.data = response.json()
            self.update_status("Data fetched successfully. You can start now.")
            self.start_button['state'] = 'normal'
            self.stop_button['state'] = 'normal'
            print(self.data)
            # for item in self.data:
            #     rfid_value = item['rfid']
            #     # Do something with the rfid_value (e.g., print it)
            #     print(rfid_value)
        except requests.exceptions.RequestException as e:
            self.update_status(f"Failed to fetch data: {e}")
            self.data = None
            self.start_button['state'] = 'disabled'
            self.stop_button['state'] = 'disabled'

    def start_execution(self):
        if self.data is not None:
            self.update_status("menunggu 10 detik  untuk user menyiapkan kursor")
            time.sleep(10)
            threading.Thread(target=self.execute_data).start()
        else:
            self.update_status("No data to start. Please get data first.")

    def execute_data(self):
        for item in self.data:
            rfid_str = str(item['nis'])
            pyautogui.write(rfid_str)
            pyautogui.press('enter')
            self.update_status(f"menulis {rfid_str}")
            time.sleep(1)
            self.update_status(f"..")
            time.sleep(1)
            self.update_status(f"....")
            time.sleep(1)
            self.update_status(f"........")
            time.sleep(1)
            self.update_status(f"Mengambil data lagi...")
            if self.data is None:  # Check if stop was pressed during execution
                break

        self.stop_execution()
        self.update_status("Completed.")

    def stop_execution(self):
        self.data = None  # Clear data from memory
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'disabled'
        self.update_status("Stopped and data cleared. Fetch new data to start.")

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoInputApp(root)
    root.mainloop()
