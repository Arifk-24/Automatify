import audioRecognize
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, messagebox, simpledialog
import speech_recognition
from PIL import Image,ImageTk
from email.mime.text import MIMEText
import ocr_api
import pyperclip
import translate
import smtplib
import os

def savefile(event=None):
    file = filedialog.asksaveasfile(initialfile='Untitled.txt',
                                defaultextension=".txt",
                                filetypes=[("All Files", "*.*"),
                                           ("Text Documents", "*.txt")])
    if file is not None:
        file.write(textbox.get(1.0, "end"))
        file.close()


def openfile(event=None):
    clear_window()
    file = filedialog.askopenfile(defaultextension=".txt",
                              filetypes=[("All Files", "*.*"),
                                         ("Text Documents", "*.txt")])
    if file is not None:
        textbox.insert(1.0, file.read())
        file.close()

def recognize_speech():
    try :
        audioRecognize.listen_using_microphone()
        text = audioRecognize.recognize_audio()
        textbox.insert(tk.END,text+"\n")
        # textbox.insert(tk.END,result+"\n")
    except speech_recognition.RequestError:
        messagebox.showerror("","Please Check Your connection")

def recognize_audio():
    audioRecognize.listen_from_audiofile()
    text= audioRecognize.recognize_audio()
    textbox.insert(tk.END,text+"\n")

def recognize_text_from_images():
    text = ocr_api.captureFromPhone()
    textbox.insert(tk.END,text+"\n")

def copy_to_clipboard():
    pyperclip.copy(textbox.get(1.0, "end"))

def translate_to_other_language():
    tran = tk.Toplevel()
    tran.title("Expert Potato")
    tran.config(bg="white")
    tran.geometry("700x540")
    tran.minsize(700,540)
    def copy_tran_textbox_to_clipboard():
        pyperclip.copy(tran_textbox.get(1.0, "end"))

    def send_mail_in_hindi():
        sender_email = os.environ.get("sender_email")  # accessing the sender email from environment variable
        sender_pass = os.environ.get("sender_pass")  # accessing the sender password from environment variable


        reciever_mail = simpledialog.askstring("input", "Enter e-mail address")

        subject = simpledialog.askstring("input", "Subject of mail")

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # It will encript the connection using tls (Transport Layer Security)
            server.login(sender_email, sender_pass)
            msg = MIMEText(f"Subject:{subject}\n\n{result}", "plain", 'utf-8').as_string()
            server.sendmail(sender_email, reciever_mail, msg)
            print("Mail sent successfully.")


    copy_icon = ImageTk.PhotoImage(Image.open("icons/copy.png"), master=tran)
    copy = tk.Button(tran,borderwidth=0,command=copy_tran_textbox_to_clipboard, image=copy_icon)
    copy.place(x=0,y=0)

    mail_button =tk.Button(tran, command=send_mail_in_hindi,image=mail_icon, text= "mail")
    mail_button.place(x=40,y=0)

    text_box_font = tkFont.Font(size=18)
    tran_textbox = tk.Text(tran,font=text_box_font)
    tran_textbox.place(x=0, y=40, relheight=1, relwidth=1)

    text = textbox.get(1.0,"end")
    tobj = translate.Translator(to_lang = 'hi')
     # It will create object of the class Translator present in translate module
    result = tobj.translate(text)
     # It will translate the given text to given language
    tran_textbox.insert(tk.END,result)

    print("Translation : ",result)

    tran.mainloop()


def mail_recognized_text():

    sender_email = os.environ.get("sender_email")# accessing the sender email from environment variable
    sender_pass = os.environ.get("sender_pass")# accessing the sender password from environment variable


    reciever_mail= simpledialog.askstring("input","Enter e-mail address")

    subject = simpledialog.askstring("input","Subject of mail")

    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.starttls() # It will encript the connection using tls (Transport Layer Security)
        server.login(sender_email,sender_pass)

        text = textbox.get(1.0,"end")
        msg = f"Subject:{subject}\n\n{text}"
        server.sendmail(sender_email, reciever_mail , msg)
        print("Mail sent successfully.")


def clear_window():
    textbox.delete(1.0,"end")



root = tk.Tk()
root.title("Expert Potato")
root.config(bg="white")
root.geometry("700x540")
root.minsize(700,540)


microphone_icon = ImageTk.PhotoImage(Image.open("icons/mic.png"), master=root)
recognize_from_speech = tk.Button(root,borderwidth=0, command=recognize_speech, image=microphone_icon)
recognize_from_speech.place(x=0, y=0)


camera_icon = ImageTk.PhotoImage(Image.open("icons/camera.png"), master=root)
recognize_from_speech = tk.Button(root,borderwidth=0,command=recognize_text_from_images, image=camera_icon)
recognize_from_speech.place(x=80,y=0)


copy_icon = ImageTk.PhotoImage(Image.open("icons/copy.png"), master=root)
copy_to_clipboard = tk.Button(root,borderwidth=0,command=copy_to_clipboard, image=copy_icon)
copy_to_clipboard.place(x=200,y=0)


translate_icon= ImageTk.PhotoImage(Image.open("icons/translate.png"), master=root)
translate_to_other_language = tk.Button(root,borderwidth=0,command=translate_to_other_language, image=translate_icon)
translate_to_other_language.place(x=120,y=0)

audio_file_icon= ImageTk.PhotoImage(Image.open("icons/audio_file.png"), master=root)
audio_button = tk.Button(root, command=recognize_audio,image=audio_file_icon, text="file")
audio_button.place(x=40, y=0)

mail_icon= ImageTk.PhotoImage(Image.open("icons/email.png"), master=root)
mail_button= tk.Button(root, command=mail_recognized_text,image=mail_icon, text= "mail")
mail_button.place(x=160,y=0)




text_box_font = tkFont.Font(size=18)
textbox = tk.Text(root,font=text_box_font)
textbox.place(x=0, y=40, relheight=1, relwidth=1)



menu = tk.Menu(root)
root.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New',command=clear_window)
filemenu.add_command(label='Open...',command=openfile)
filemenu.add_command(label='save', command=savefile)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=exit)

root.bind('<Command-s>', savefile)
root.bind('<Command-o>', openfile)

root.mainloop()
