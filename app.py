import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import json
import os
class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hotel Management System")
        self.geometry("900x700")

        self.rooms = {}
        self.reservations = {}

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_rooms = self.tabview.add("Manage Rooms")
        self.tab_reservations = self.tabview.add("Make Reservation")
        self.tab_history = self.tabview.add("Reservation History")

        self.setup_rooms_tab()
        self.setup_reservations_tab()
        self.setup_history_tab()

        self.load_data() 

    def save_data(self):
        data = {
            "rooms": self.rooms,
            "reservations": self.reservations
        }
        with open("hotel_data.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists("hotel_data.json"):
            with open("hotel_data.json", "r") as f:
                data = json.load(f)
            self.rooms = data.get("rooms", {})
            self.reservations = data.get("reservations", {})
            self.update_room_list()
            self.update_room_comboboxes()
        else:
            self.rooms = {}
            self.reservations = {}

    def setup_rooms_tab(self):
        frame = ctk.CTkFrame(self.tab_rooms)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Room Number:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.room_number = ctk.CTkEntry(frame)
        self.room_number.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Room Type:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.room_type = ctk.CTkComboBox(frame, values=["Single", "Double", "Suite"])
        self.room_type.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Capacity:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.capacity = ctk.CTkEntry(frame)
        self.capacity.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Price per Night (DZD):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.price = ctk.CTkEntry(frame)
        self.price.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkButton(frame, text="Add Room", command=self.add_room).grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        self.room_list = ctk.CTkTextbox(frame, height=200, state="disabled")
        self.room_list.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(5, weight=1)

    def setup_reservations_tab(self):
        frame = ctk.CTkFrame(self.tab_reservations)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Room Number:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.res_room_number = ctk.CTkComboBox(frame, values=list(self.rooms.keys()))
        self.res_room_number.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Check-in Date:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.check_in = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.check_in.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Check-out Date:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.check_out = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.check_out.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Guest Name:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.guest_name = ctk.CTkEntry(frame)
        self.guest_name.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Guest Email:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.guest_email = ctk.CTkEntry(frame)
        self.guest_email.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Guest Phone:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.guest_phone = ctk.CTkEntry(frame)
        self.guest_phone.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkButton(frame, text="Make Reservation", command=self.make_reservation).grid(row=6, column=0, columnspan=2, padx=5, pady=10)

        self.reservation_info = ctk.CTkTextbox(frame, height=100, state="disabled")
        self.reservation_info.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(7, weight=1)

    def setup_history_tab(self):
        frame = ctk.CTkFrame(self.tab_history)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        search_frame = ctk.CTkFrame(frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ctk.CTkLabel(search_frame, text="Search by:").pack(side=tk.LEFT, padx=5)
        self.search_option = ctk.CTkComboBox(search_frame, values=["Room Number", "Guest Name", "Date"])
        self.search_option.pack(side=tk.LEFT, padx=5)
        self.search_option.set("Room Number")

        self.search_entry = ctk.CTkEntry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        ctk.CTkButton(search_frame, text="Search", command=self.search_reservations).pack(side=tk.LEFT, padx=5)

        self.history_text = ctk.CTkTextbox(frame, height=400, state="disabled")
        self.history_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    def add_room(self):
        room_number = self.room_number.get()
        room_type = self.room_type.get()
        capacity = self.capacity.get()
        price = self.price.get()

        if room_number and room_type and capacity and price:
            self.rooms[room_number] = {
                "type": room_type,
                "capacity": capacity,
                "price": float(price)
            }
            self.update_room_list()
            self.clear_room_inputs()
            self.update_room_comboboxes()
            self.save_data()  # Sauvegarde des données
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def update_room_list(self):
        self.room_list.configure(state="normal")
        self.room_list.delete("1.0", tk.END)
        for room, details in self.rooms.items():
            self.room_list.insert(tk.END, f"Room {room}: {details['type']}, Capacity: {details['capacity']}, Price: {details['price']:.2f} DZD\n")
        self.room_list.configure(state="disabled")

    def clear_room_inputs(self):
        self.room_number.delete(0, tk.END)
        self.room_type.set("")
        self.capacity.delete(0, tk.END)
        self.price.delete(0, tk.END)

    def update_room_comboboxes(self):
        room_numbers = list(self.rooms.keys())
        self.res_room_number.configure(values=room_numbers)
        if room_numbers:
            self.res_room_number.set(room_numbers[0])
        else:
            self.res_room_number.set("")

    def make_reservation(self):
        room_number = self.res_room_number.get()
        check_in = self.check_in.get_date().strftime("%Y-%m-%d")
        check_out = self.check_out.get_date().strftime("%Y-%m-%d")
        guest_name = self.guest_name.get()
        guest_email = self.guest_email.get()
        guest_phone = self.guest_phone.get()

        if room_number and check_in and check_out and guest_name and guest_email and guest_phone:
            if self.is_room_available(room_number, check_in, check_out):
                total_price = self.calculate_total_price(room_number, check_in, check_out)
                reservation = {
                    "room": room_number,
                    "check_in": check_in,
                    "check_out": check_out,
                    "guest_name": guest_name,
                    "guest_email": guest_email,
                    "guest_phone": guest_phone,
                    "total_price": total_price
                }
                if room_number not in self.reservations:
                    self.reservations[room_number] = []

                self.reservations[room_number].append(reservation)
                self.show_reservation_info(reservation)
                self.clear_reservation_inputs()
                self.save_data()
            else:
                messagebox.showerror("Error", "Room is not available for the selected dates")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def is_room_available(self, room_number, check_in, check_out):
        if room_number not in self.reservations:
            return True
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        for reservation in self.reservations[room_number]:
            res_check_in = datetime.strptime(reservation["check_in"], "%Y-%m-%d")
            res_check_out = datetime.strptime(reservation["check_out"], "%Y-%m-%d")
            if (check_in_date >= res_check_in and check_in_date < res_check_out) or \
               (check_out_date > res_check_in and check_out_date <= res_check_out) or \
               (check_in_date <= res_check_in and check_out_date >= res_check_out):
                return False
        return True

    def calculate_total_price(self, room_number, check_in, check_out):
        room_price = self.rooms[room_number]["price"]
        days = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
        return room_price * days

    def show_reservation_info(self, reservation):
        self.reservation_info.configure(state="normal")
        self.reservation_info.delete("1.0", tk.END)
        self.reservation_info.insert(tk.END, f"Reservation made for Room {reservation['room']}\n")
        self.reservation_info.insert(tk.END, f"Check-in: {reservation['check_in']}, Check-out: {reservation['check_out']}\n")
        self.reservation_info.insert(tk.END, f"Total Price: {reservation['total_price']:.2f} DZD")
        self.reservation_info.configure(state="disabled")

    def clear_reservation_inputs(self):
        self.res_room_number.set("")
        self.check_in.set_date(datetime.now())
        self.check_out.set_date(datetime.now() + timedelta(days=1))
        self.guest_name.delete(0, tk.END)
        self.guest_email.delete(0, tk.END)
        self.guest_phone.delete(0, tk.END)

    def search_reservations(self):
        search_option = self.search_option.get()
        search_value = self.search_entry.get()

        self.history_text.configure(state="normal")
        self.history_text.delete("1.0", tk.END)

        if search_option == "Room Number":
            if search_value in self.reservations:
                self.display_room_history(search_value)
            else:
                self.history_text.insert(tk.END, "No reservations found for this room.")
        elif search_option == "Guest Name":
            found = False
            for room, reservations in self.reservations.items():
                for reservation in reservations:
                    if search_value.lower() in reservation['guest_name'].lower():
                        self.display_reservation(reservation)
                        found = True
            if not found:
                self.history_text.insert(tk.END, "No reservations found for this guest name.")
        elif search_option == "Date":
            found = False
            for room, reservations in self.reservations.items():
                for reservation in reservations:
                    if search_value in reservation['check_in'] or search_value in reservation['check_out']:
                        self.display_reservation(reservation)
                        found = True
            if not found:
                self.history_text.insert(tk.END, "No reservations found for this date.")

        self.history_text.configure(state="disabled")

    def display_room_history(self, room_number):
        for reservation in self.reservations[room_number]:
            self.display_reservation(reservation)

    def display_reservation(self, reservation):
        self.history_text.insert(tk.END, f"Room: {reservation['room']}\n")
        self.history_text.insert(tk.END, f"Guest: {reservation['guest_name']}\n")
        self.history_text.insert(tk.END, f"Check-in: {reservation['check_in']}, Check-out: {reservation['check_out']}\n")
        self.history_text.insert(tk.END, f"Total Price: {reservation['total_price']:.2f} DZD\n")
        self.history_text.insert(tk.END, "-" * 30 + "\n")

    def on_closing(self):
        self.save_data()
        self.destroy()
if __name__ == "__main__":
    app = HotelApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()