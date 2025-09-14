import customtkinter as ctk
import math, itertools

# ---------------- Main App ----------------
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("RGB Gaming Calculator")
app.geometry("420x650")
app.resizable(False, False)

# ---------------- Entry ----------------
entry = ctk.CTkEntry(app, width=380, height=70,
                    font=("Consolas", 26),
                    justify="right",
                    corner_radius=20)
entry.pack(pady=20)

# ---------------- Global Vars ----------------
button_widgets = []
rgb_colors = ["#FF007F","#7D00FF","#00CFFF","#00FF7F","#FFD300","#FF5E00"]
color_cycle = itertools.cycle(rgb_colors)
history_data = []   # store calculations
pages = {}
current_page = None

# ---------------- Functions ----------------
def click(button_text):
    if button_text == "=":
        try:
            result = str(eval(entry.get()))
            expr = entry.get()
            entry.delete(0, "end")
            entry.insert("end", result)
            # save history
            history_data.append(f"{expr} = {result}")
            update_history()
        except:
            entry.delete(0, "end")
            entry.insert("end", "Error")
    elif button_text == "C":
        entry.delete(0, "end")
    else:
        entry.insert("end", button_text)

# history updater
def update_history():
    history_box.configure(state="normal")
    history_box.delete("1.0","end")
    for line in history_data[-15:][::-1]:
        history_box.insert("end", line+"\n")
    history_box.configure(state="disabled")

def clear_history():
    history_data.clear()
    update_history()

# show page with slide animation
def show_page(page_name):
    global current_page
    if current_page:
        pages[current_page].pack_forget()
    pages[page_name].pack(pady=10)
    current_page = page_name

# ---------------- RGB Text Effect ----------------
def rgb_text_effect():
    for btn in button_widgets:
        btn.configure(text_color=next(color_cycle))
    app.after(400, rgb_text_effect)

# ---------------- Basic Frame ----------------
frame_basic = ctk.CTkFrame(app, corner_radius=20)

buttons_basic = [
    ("7","8","9","/"),
    ("4","5","6","*"),
    ("1","2","3","-"),
    ("0",".","=","+")
]

for r, row in enumerate(buttons_basic):
    for c, b in enumerate(row):
        btn = ctk.CTkButton(frame_basic, text=b,
                            width=80, height=65,
                            font=("Consolas",20,"bold"),
                            fg_color="#222", hover_color="#333",
                            corner_radius=18,
                            command=lambda x=b: click(x))
        btn.grid(row=r, column=c, padx=8, pady=8)
        button_widgets.append(btn)

# ---------------- Scientific Frame ----------------
frame_sci = ctk.CTkFrame(app, corner_radius=20)

sci_buttons = [
    ("sin","cos","tan","log"),
    ("sqrt","pi","e","**"),
    ("(",")","%","//")
]

for r, row in enumerate(sci_buttons):
    for c, b in enumerate(row):
        btn = ctk.CTkButton(frame_sci, text=b,
                            width=90, height=65,
                            font=("Consolas",18,"bold"),
                            fg_color="#222", hover_color="#333",
                            corner_radius=18,
                            command=lambda x=b: click(f"math.{x}(") if x in ["sin","cos","tan","log","sqrt"]
                                     else click(f"math.{x}") if x in ["pi","e"]
                                     else click(x))
        btn.grid(row=r, column=c, padx=8, pady=8)
        button_widgets.append(btn)

# ---------------- History Frame ----------------
frame_history = ctk.CTkFrame(app, corner_radius=20)

history_box = ctk.CTkTextbox(frame_history, width=380, height=300,
                            font=("Consolas",18),
                            corner_radius=15,
                            fg_color="#111")
history_box.pack(pady=20)
history_box.configure(state="disabled")

clear_btn_history = ctk.CTkButton(frame_history, text="Clear History",
                                  width=200, height=45,
                                  font=("Consolas",18,"bold"),
                                  fg_color="red", hover_color="#800000",
                                  corner_radius=15,
                                  command=clear_history)
clear_btn_history.pack(pady=10)

# ---------------- Page Switch Buttons ----------------
switch_frame = ctk.CTkFrame(app, fg_color="transparent")
switch_frame.pack(pady=10)

btn_basic = ctk.CTkButton(switch_frame, text="Basic",
                          width=110, height=40,
                          font=("Consolas",16,"bold"),
                          command=lambda: show_page("basic"))
btn_basic.grid(row=0, column=0, padx=8)

btn_sci = ctk.CTkButton(switch_frame, text="Scientific",
                        width=110, height=40,
                        font=("Consolas",16,"bold"),
                        command=lambda: show_page("sci"))
btn_sci.grid(row=0, column=1, padx=8)

btn_hist = ctk.CTkButton(switch_frame, text="History",
                         width=110, height=40,
                         font=("Consolas",16,"bold"),
                         command=lambda: show_page("history"))
btn_hist.grid(row=0, column=2, padx=8)

# ---------------- Clear Button ----------------
clear_btn = ctk.CTkButton(app, text="C",
                          width=380, height=60,
                          font=("Consolas",22,"bold"),
                          fg_color="red", hover_color="#800000",
                          corner_radius=20,
                          command=lambda: click("C"))
clear_btn.pack(pady=10)

# ---------------- Store Pages ----------------
pages = {"basic": frame_basic, "sci": frame_sci, "history": frame_history}

# ---------------- Start RGB Effect ----------------
rgb_text_effect()

# ---------------- Start with Basic ----------------
show_page("basic")

# ---------------- Run ----------------
app.mainloop()
