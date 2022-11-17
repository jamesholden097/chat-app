import os
import tkinter
import customtkinter
import tkinter.filedialog
from tkinter.font import Font

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
chat_history = []

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter complex_example.py")
        self.geometry("1280x720")
        self.resizable(0, 0)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        self.buttons = {}

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame_left = customtkinter.CTkFrame(master=self)
        self.frame_left.grid(row=0, column=0, rowspan=2 ,sticky="ns", padx=5, pady=5)


        self.frame_right_top = customtkinter.CTkFrame(master=self, padx=5, pady=5)
        self.frame_right_top.grid(row=0, column=1, sticky="nsew")
        self.frame_right_top.grid_columnconfigure(0, weight=1)
        self.frame_right_top.grid_rowconfigure(2, weight=1)

        self.frame_right_bottom = customtkinter.CTkFrame(master=self)
        self.frame_right_bottom.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.frame_right_bottom.grid_columnconfigure(1, weight=1)
        self.frame_right_bottom.grid_columnconfigure(5, weight=0)
        self.sent = True
        self.num_text = 0
        self.font = Font()
        self.create_widgets()

    def create_widgets(self):
        self.left_label = customtkinter.CTkLabel(master=self.frame_left, text="left",text_font=("Roboto Medium", -16))  
        self.left_label.grid(row=1, column=0, pady=10, padx=10)
        self.create_button(self.frame_left, 'button1', 0, 0)
        self.top_label = customtkinter.CTkLabel(master=self.frame_right_top, text="Name of Contact",text_font=("Roboto Medium", -16))  
        self.top_label.grid(row=0, column=0, rowspan=2, columnspan=5,sticky="ew")
        
        self.text_canvas = tkinter.Canvas(master=self.frame_right_top, bd = 0 ,bg="gray12", highlightthickness=1, highlightbackground="black")
        self.text_canvas.grid(row=2, column=0,  sticky="nsew")
        
        self.canvas_scrollbar = customtkinter.CTkScrollbar(self.frame_right_top,command=self.text_canvas.yview)
        self.canvas_scrollbar.grid(row=2, column=6, rowspan=5,sticky="ns")
        self.text_canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.text_canvas.bind('<Configure>', self.reset_scroll_region)
        
        self.canvas_frame = customtkinter.CTkFrame(master=self.text_canvas, fg_color='gray12')
        
        self.text_canvas.update()
        self.text_canvas.create_window((0, 0), window=self.canvas_frame, anchor='nw', width=self.text_canvas.winfo_width())
        
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(2, weight=1)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        '''
        for i in range(self.num_text):
            if i % 2 == 0:
                received_text = customtkinter.CTkLabel(master=self.canvas_frame, text=f' label{i} \n' * i ,fg_color='#3B8ED0',corner_radius=10, justify=tkinter.LEFT)
                received_text.grid(row=i, column=0, columnspan=2, padx=(10, 10), pady=(10, 10),sticky="nsew")
            else:
                sent_text = customtkinter.CTkLabel(master=self.canvas_frame, text=f'    label{i} ',fg_color='#3B8ED0', corner_radius=10 , justify=tkinter.RIGHT)
                sent_text.grid(row=i, column=1, columnspan=2, padx=(10, 10), pady=(10, 10),sticky="nsew")
        '''

        self.message_entry = customtkinter.CTkEntry(master=self.frame_right_bottom)
        self.message_entry.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=(5, 5), pady=(5, 5))
        self.message_entry.entry.bind("<Return>", self.entry_callback)
        self.buttons['+'] = customtkinter.CTkButton(master=self.frame_right_bottom, text='+', command=lambda text='+': self.button_callback('+'), width=25, height=25)
        self.buttons['+'].grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nws")
        self.buttons['send'] = customtkinter.CTkButton(master=self.frame_right_bottom, text='send', command=lambda text='send': self.button_callback('send'), width=40, height=25)
        self.buttons['send'].grid(row=0, column=5, padx=(5, 5), pady=(5, 5), sticky="nsew")


    def create_button(self, frame, text, row, column, rowspan=1, columnspan=1, sticky="nsew"):
        self.buttons[text] = customtkinter.CTkButton(master=frame, text=text, command=lambda text=text: self.button_callback(text))
        self.buttons[text].grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=(5, 5), pady=(5, 5), sticky=sticky)

    def button_callback(self,button_id):
        # print(f"{button_id} Button pressed")
        if button_id == 'send':
            self.update_message_widget()
        if button_id == '+':
            self.filetypes = (("All files", "*.*"), )
            self.filename = tkinter.filedialog.askopenfilename(title='Celect File to Send', initialdir=os.getcwd(), filetypes=self.filetypes)
            self. update_message_widget(self.filename)

        if button_id == 'button1':
            self.top_label.configure(text=f"Name of contact : {self.num_text}")

    def entry_callback(self, event=None):
        self.update_message_widget()

    def update_message_widget(self, message=None):
        if not message:
            message = f"{self.num_text} : {self.message_entry.get()}" 
        w, h = tkinter.font.Font().measure(message) + 15, tkinter.font.Font(font='TkDefaultFont').metrics('linespace')  + 15
        # print(self.font.measure(message), self.font.metrics(message))
        if not self.sent:
            received_text = customtkinter.CTkLabel(master=self.canvas_frame, text=message, width=w, height=h, corner_radius=h / 2, fg_color='#3B8ED0', justify=tkinter.LEFT)
            received_text.grid(row=self.num_text, column=0, columnspan=2, padx=(10, 10), pady=(10, 10),sticky="nsw")
        else:
            sent_text = customtkinter.CTkLabel(master=self.canvas_frame, text=message, width=w, height=h, corner_radius=h / 2, fg_color='#3B8ED0', justify=tkinter.RIGHT)
            sent_text.grid(row=self.num_text, column=1, columnspan=2, padx=(10, 10), pady=(10, 10),sticky="nse")

        chat_history.append([self.sent, str(self.num_text), self.num_text])
        self.message_entry.delete(0, tkinter.END)
        self.sent = not self.sent
        self.num_text += 1
        self.reset_scroll_region()
        self.text_canvas.yview_moveto('1.0')

    def reset_scroll_region(self, event=0):
        self.text_canvas.configure(scrollregion=self.text_canvas.bbox("all"))
    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()