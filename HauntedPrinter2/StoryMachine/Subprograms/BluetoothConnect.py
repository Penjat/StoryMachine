from bluezero import peripheral


class BluetoothConnect:

    def __init__(self, display_output, printer_output):
        self.display_output = display_output
        self.printer_output = printer_output
        self.is_advertizing = False
        self.menu_items = ["main menu", "start_advertizing"]
        self._current_selection = 0.0


    def write_callback(self, value, options):
        print("📩 Received from client:", value.decode(errors="ignore"))


    def start_advertizing(self):
        # Replace with your Pi’s Bluetooth adapter MAC (find with `hciconfig`)
        ADAPTER_ADDR = "DC:A6:32:3D:E3:00"

        periph = peripheral.Peripheral(adapter_addr=ADAPTER_ADDR, local_name="MyPi")

        # Add a service
        my_service = periph.add_service(srv_id=1, uuid="1234")

        # Add a writable characteristic
        my_service.add_characteristic(
            srv_id=1,
            chr_id=1,
            uuid="1235",
            value="",
            notifying=False,
            flags=["write"],
            write_callback=write_callback,
        )

        # Start advertising and running
        periph.publish()

    def update_display(self):
        self.display_output.on_next(self.selection)


# --------------- Input Methods -----------------

    def process_right_knob(self, event):
        if event == "up":
            self._current_selection += 0.5
        if event == "down":
            self._current_selection -= 0.5
        self.update_display()
    

    def process_left_knob(self, event):
        print(event)
        if self.selection == "reading":
            self.print_reading = (event == "down")
            
 
        self.update_display()

    def process_center_press(self, event):
        if event == "pressed":
            if self.selection == "main menu":
                self.printer_output.on_next(self.selection)
                return
            if self.selection == "start_advertizing":
                self.start_advertizing()
                
            else:
                print("did not recognize selection {self.selection}")