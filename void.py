import dearpygui.dearpygui as dpg
import sys
import subprocess
import threading
import cv2 as cv

# Made by Theo Kershaw

def log(text):
    with open("phone.log", "a") as f:
        f.write(f"{text}\n")
    print(text)

class Void:
    def __init__(self):
        pass

    def satellite(self):
        log("[INF] Opening satellite tracker")
        try:
            output = subprocess.getoutput("gpredict")
            log(f"[INF] Output: {output}")
        except Exception as e:
            log(f"[ERR] Problem with satellite tracker: {e}: {output}")

    def telescope(self):
        log("[INF] Opening Stellarium")
        try:
            output = subprocess.getoutput("sudo /Applications/Stellarium.app/Contents/MacOs/stellarium")
            log(f"[INF] Output: {output}")
        except Exception as e:
            log(f"[ERR] Problem with Stellarium: {e}: {output}")
    
    def system_htop(self):
        log("[INF] Opening HTOP")
        try:
            output = subprocess.getoutput("sudo xterm htop")
            log(f"[INF] Output: {output}")
        except Exception as e:
            log(f"[ERR] Problem with HTOP: {e}: {output}")

    def press(self, sender):
        label = dpg.get_item_label(sender)
        current = dpg.get_value("display")

        if label == "C":
            dpg.set_value("display", "")
        elif label == "=":
            try:
                dpg.set_value("display", str(eval(current)))
            except:
                dpg.set_value("display", "Error")
        else:
            dpg.set_value("display", current + label)
        
    def calculator(self):
        log("[INF] Opening calculator")
        if dpg.does_item_exist("calc_window"):  
            dpg.focus_item("calc_window")     
            return    
        try:
            with dpg.window(label="Calculator", width=100, height=150, tag="calc_window", on_close=lambda s: dpg.delete_item(s)):
                dpg.add_input_text(tag="display", readonly=True, width=-1)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="1", callback=self.press)
                    dpg.add_button(label="2", callback=self.press)
                    dpg.add_button(label="3", callback=self.press)
                    dpg.add_button(label="+", callback=self.press)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="4", callback=self.press)
                    dpg.add_button(label="5", callback=self.press)
                    dpg.add_button(label="6", callback=self.press)
                    dpg.add_button(label="-", callback=self.press)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="7", callback=self.press)
                    dpg.add_button(label="8", callback=self.press)
                    dpg.add_button(label="9", callback=self.press)
                    dpg.add_button(label="*", callback=self.press)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="C", callback=self.press)
                    dpg.add_button(label="0", callback=self.press)
                    dpg.add_button(label="=", callback=self.press)
                    dpg.add_button(label="/", callback=self.press)
        except Exception as e:
            log(f"[ERR] Problem with calculator: {e}")

    def credit(self):
        log("[INF] MADE BY THEO KERSHAW")
        if dpg.does_item_exist("cred_window"):  
            dpg.focus_item("cred_window")     
            return    
        with dpg.window(label="Credits", width=100, height=150, tag="cred_window", on_close=lambda s: dpg.delete_item(s)):
                    dpg.add_button(label="Theo Kerhaw")

if __name__ == "__main__":
    void = Void()

    dpg.create_context()
    dpg.create_viewport(title="Void", width=800, height=480)

    with dpg.window(label="Void", width=300, height=120):
        dpg.add_button(label="Satellites", callback=lambda: threading.Thread(target=void.satellite, daemon=True).start())
        dpg.add_button(label="Virtual Telescope", callback=lambda: threading.Thread(target=void.telescope, daemon=True).start())
        dpg.add_button(label="System Processes", callback=lambda: threading.Thread(target=void.system_htop, daemon=True).start())
        dpg.add_button(label="Calculator", callback=lambda: threading.Thread(target=void.calculator, daemon=True).start())
        dpg.add_button(label="Credits", callback=lambda: threading.Thread(target=void.credit, daemon=True).start())

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
