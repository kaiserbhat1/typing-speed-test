import random
from tkinter import Tk, Frame, Label, Button, Text, END,StringVar,OptionMenu
from speed_engine import Speed

NUMBER_OF_WORDS = 35

class Window:
    def __init__(self):
        self.root = Tk()
        self.root.title("Typing Speed Test")
        self.root.geometry("900x700")
        self.root.resizable(False,False)

        self.upper_frame = Frame(self.root, bg="#8174A0", width=900, height=200)
        self.upper_frame.place(x=0, y=0)
        self.score_frame = Frame(self.upper_frame,bg="#A888B5",width=200,height=150,highlightthickness=1)
        self.score_frame.place(x=650,y=25)

        self.user_name_label = Label(self.score_frame,bg="#A888B5",text="Username : Nil",font=("",12),fg="#1B1833")
        self.high_wpm_label = Label(self.score_frame, bg="#A888B5",text="Highest WPM : Nil",font=("",12),fg="#1B1833")
        self.accuracy_label = Label(self.score_frame,bg="#A888B5", text="Accuracy : Nil",font=("",12),fg="#1B1833")
        self.correct_words_label = Label(self.score_frame,bg="#A888B5", text="Correct Words : Nil",font=("",12),fg="#1B1833")
        self.user_name_label.place(x=15,y=20)
        self.high_wpm_label.place(x=15,y=50)
        self.accuracy_label.place(x=15,y=80)
        self.correct_words_label.place(x=15,y=110)

        self.mid_frame = Frame(self.root, bg="#8174A0", width=900, height=200, padx=20, pady=10)
        self.mid_frame.place(x=0, y=200)
        self.bottom_frame = Frame(self.root, bg="#8174A0", width=900, height=300, padx=20)
        self.bottom_frame.place(x=0, y=400)

        self.cpm_label = Label(self.upper_frame, text="Corrected CPM: 0",font=("",14),bg="#8174A0",fg="#1B1833")
        self.cpm_label.place(x=50, y=50)
        self.wpm_label = Label(self.upper_frame, text="Corrected WPM: 0.0",font=("",14),bg="#8174A0",fg="#1B1833")
        self.wpm_label.place(x=50, y=100)
        self.time_label = Label(self.upper_frame, text="Time left : 0:0:0s",font=("",14),bg="#8174A0",fg="#1B1833")
        self.time_label.place(x=50, y=150)

        self.start_btn = Button(self.bottom_frame,text="start",bg="#FFD2A0",width=10,font=("",12))
        self.start_btn.place(x=60,y=235)
        self.read_area_label = Label(self.upper_frame,text="Passage",font=("",15),bg="#8174A0")
        self.read_area_label.place(x=425,y=170)
        self.read_area = Text(self.mid_frame, height=5, width=55, font=("", 20), padx=10, pady=5,wrap="word")
        self.read_area.place(x=10, y=0)
        self.text_area = Text(self.bottom_frame, height=1, width=25, font=("", 20), padx=10, pady=3, relief="raised",borderwidth=5,wrap="word")
        self.text_area.place(x=210, y=225)
        self.user_read_area = Text(self.bottom_frame, height=5, width=55, font=("", 20), padx=10, pady=3, relief="raised",borderwidth=2,wrap="word")
        self.user_read_area.place(x=10, y=25)
        self.time_out = True
        self.name_label= Label(self.bottom_frame,text="Please Enter Your Name Below! then Press the 'START' button to Start!",font=("",12),bg="#8174A0",fg="pink")
        self.name_label.place(x=210,y=200)
        self.option_label = Label(self.bottom_frame,text="Set Time",bg="#8174A0")
        self.option_label.place(x=750,y=210)
        self.username_var = StringVar(self.root,"Guest")
        self.mode_var = StringVar(self.root,"1 Min")
        self.mode = OptionMenu(self.bottom_frame,self.mode_var,*["1 Min","3 Min","5 Min",])
        self.mode.place(x=750,y=230)
        self.mainloop = self.root.mainloop

    @staticmethod
    def disable_widget(widget):
        widget.config(state="disabled")

    def get_user_typed(self, condition=None):
        word = self.text_area.get(1.0, END)
        if condition:
            self.text_area.delete(1.0,END)
        return word
    def timer(self, seconds: int,set_score):
        if self.time_out:
            sec = seconds % 60
            min = seconds // 60 % 60
            hour = seconds // 3600
            if sec <10:
                sec = f"0{sec}"
            if min <10:
                min = f"0{min}"
            if hour <10:
                hour = f"0{hour}"
            if seconds >=0:
                self.time_label.config(text=f"Time: {hour}:{min}:{sec}s")
                seconds -= 1
                self.root.after(1000,self.timer,seconds,set_score)

            else:
                self.time_out=False
                self.start_btn.config(state="normal",text="Restart",bg="#FFD2A0",borderwidth=1,command=restart)
                self.block()
                set_score()
                return
        else:
            self.start_btn.config(state="normal", text="Restart", bg="#FFD2A0", borderwidth=1, command=restart)
            self.block()
            set_score()
            return
    def block(self):
        self.text_area.delete(1.0,END)
        self.text_area.insert(1.0,"Time is Over!")
        self.text_area.config(bg="pink",state="disabled")
        self.user_read_area.config(bg="pink",state="disabled")

    def clear_all(self):
        self.start_btn.config(state="disabled",text="",bg="#8174A0",borderwidth=0)
        self.text_area.config(state="normal",bg="white")
        self.text_area.delete(1.0, END)
        self.user_read_area.config(bg="white")
        self.time_out=True
    def tag_word(self,index,color):

        if color == "red":
            self.read_area.tag_add("highlight",f"1.{index}",f"1.{index + 1}")
            self.read_area.tag_config("highlight",foreground=color)
        elif color == "next":
            self.read_area.tag_add("current", f"1.{index}", f"1.{index+1}")
            self.read_area.tag_config("current", underline=True, underlinefg="black")
        elif color =="orange":
            self.read_area.tag_add("underline", f"1.{index}", f"1.{index+1}")
            self.read_area.tag_config("underline",underline=True,underlinefg="orange")
        elif color =="blue":
            self.read_area.tag_add("cap", f"1.{index}", f"1.{index+1}")
            self.read_area.tag_config("cap",underline=True,underlinefg="black",foreground="blue")
        elif color =="grey":
            self.read_area.tag_add("forgot", f"1.{index}", f"1.{index+1}")
            self.read_area.tag_config("forgot", foreground="grey")
        else:
            self.read_area.tag_add("colored", f"1.{index}", f"1.{index + 1}")
            self.read_area.tag_config("colored", foreground=color)


app = Window()
file = Speed()
file.total_words = NUMBER_OF_WORDS
def update_display():
        app.read_area.config(state="normal")
        app.read_area.delete(1.0, END)
        for word in file.display_word:
            app.read_area.insert(END, f"{word}")
        app.read_area.config(state="disabled")

        app.user_read_area.config(state="normal")
        app.user_read_area.delete(1.0, END)
        for word in file.display_word_user:
            app.user_read_area.insert(END, f"{word}")
        app.user_read_area.config(state="disabled")

def restart():
    file.clear_all_values()
    app.clear_all()
    initialize()

def compare(event=None):

    file.temp_text = ""
    app.cpm_label.config(text=f"Corrected CPM: {file.wpm}")
    app.wpm_label.config(text=f"Corrected WPM: {file.round_wpm()}")
    if event.char ==" " and app.time_out:
        if len(file.user_text.split()) + 1 == NUMBER_OF_WORDS:
            app.time_out = False
        type_text = app.get_user_typed(condition=True)
        file.user_text += type_text
        user_word_list = file.set_text(file.user_text.split())
        file.display_word_user =user_word_list
        update_display()
        file.check_user_typed(file.user_text, app.tag_word)

    else:
        if app.time_out:
            type_text = app.get_user_typed(condition=False)
            file.temp_text+= file.user_text
            file.temp_text+=type_text
            update_display()
            file.check_user_typed(file.temp_text, app.tag_word)



def get_file():
    words = file.read_csv("words.csv")
    sentence = random.sample(words, NUMBER_OF_WORDS)
    return sentence
def set_score_board():
    file.record(app.username_var.get())
    result = Speed.get_score()
    if result:
        app.user_name_label.config(text=f"Username : {result[0]}")
        app.high_wpm_label.config(text=f"Highest WPM : {result[1]}")
        app.accuracy_label.config(text=f"Accuracy : {result[2]}%")
        app.correct_words_label.config(text=f"Correct Words : {result[3]}")
    return
def get_username():
    name = app.get_user_typed(condition=True).split()
    if name:
        app.username_var.set(name[0])
    else:
        app.username_var.set("Guest")
    return

def initialize():
    time = app.mode_var.get()
    if time == "1 Min":
        time = 60
    elif time == "3 Min":
        time = 180
    elif time == "5 Min":
        time = 300
    file.time = time//60
    app.name_label.config(text="Enter the Text Below!")
    file.display_word = file.set_text(get_file())
    update_display()
    app.timer(time, set_score_board)

def start_test():
   get_username()
   app.text_area.bind("<KeyRelease>", compare)
   initialize()
   app.start_btn.config(state="disabled",borderwidth=0,text="",bg="#8174A0")

app.start_btn.config(command=start_test)
update_display()
set_score_board()

app.mainloop()

