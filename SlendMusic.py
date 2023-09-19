import glob
from datetime import datetime
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import time
import webbrowser
from mutagen.mp3 import MP3
from pygame import mixer
import keyboard
import codecs
import gspread
import http.client

try:
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET","/ip")
    ip = conn.getresponse().read()

    gc = gspread.service_account_from_dict({
      "type": "service_account",
      "project_id": "slend-music",
      "private_key_id": "YOUR PRIVATE KEY ID",
      "private_key": "-----BEGIN PRIVATE KEY-----\n"
        "YOUR PRIVATE KEY"
                     "--END PRIVATE KEY-----\n",
      "client_email": "YOUR EMAIL",
      "client_id": "YOUR ID",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "YOUR URL"})
    sh = gc.open_by_key("SPREADSHEETS KEY")
    ws = sh.worksheet("INFO")
    listed = sh.worksheet("Analytics")
except:
    pass

mixer.init()

count = 0
files = []
duration = []
lyrics = []
lyr = 0
val = 0
z=0

if open("config.txt", "r").read() == '':
    win3 = tk.Tk()
    win3.title("Registation")
    win3.geometry('300x300')
    win3.minsize(200,200)
    win3.maxsize(200,200)
    win3.resizable(0, 0)
    def save():
        print(ws.get('R2:R1000'))
        if user.get() in ws.get('R2:R1000')[0]:
            print(True)
            check_id = ws.get('R2:R1000')[0].index(user.get())
            print(check_id)
            print(psw.get())
            print(ws.get('S2:S1000')[0][check_id])
            if str(psw.get()) == str(ws.get('S2:S1000')[0][check_id]):
                open("config.txt", "w").write(user.get()+"\n"+psw.get())
            else:
                Label(win3,text='Wrong Password!').grid(row=3,column=1)
        else:
            open("config.txt", "w").write(user.get() + "\n" + psw.get())
    message = StringVar()
    message2 = StringVar()
    Label(win3, text='Username: ').grid(row=0, column=0)
    user = Entry(win3, textvariable=message)
    user.grid(row=0, column=1)
    Label(win3, text='Password: ').grid(row=1,column=0)
    psw = Entry(win3,textvariable=message2)
    psw.grid(row=1,column=1)
    saveuser = Button(win3, text="Save",
                      command=lambda: [save()])
    saveuser.grid(row=2, column=1)
    win3.mainloop()
else:
    for text in glob.glob('*.txt'):
        lyrics.append(text)
        print(lyrics)
        lyr +=1
        print(lyr)
    for file in glob.glob("*.mp3"):
        files.append(file)
        print(files)
        count += 1
        print(count)
        duration.append(MP3(file).info.length)
        print(duration)


    if count > 15:
        def premium():
            webbrowser.open("https://vk.com/alexslenderman", new=2)
        tk.messagebox.showerror(title="ERROR", message="Buy Premium for using more than 15 songs")
        win = tk.Tk()
        win.iconphoto(False, tk.PhotoImage(file="logo2.png"))
        win.title('Slend Music Premium')
        win.geometry('500x300')
        win.minsize(500, 300)
        win.maxsize(500, 300)
        win.resizable(0, 0)
        Label(win, width=10, height=2, text="0.99$\nFOREVER", font="Consolas 20").place(x=195, y=10)
        Button(win, width=4, height=1, text="Buy", font="Consolas 50",
               command=lambda: [premium()]).place(x=190, y=100)
        win.mainloop()
    else:
        win = tk.Tk()
        fon = "#130C83"
        win.config(bg=fon)
        win.iconphoto(False, tk.PhotoImage(file="logo2.png"))
        win.title('Slend Music')
        win.geometry("{0}x{1}+0+0".format(1366,768))
        win.resizable(0, 0)


        background_image = tk.PhotoImage(file='design.png')
        background_label = tk.Label(win, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        user_id = str(open("config.txt","r").readlines()[0][:-1])
        user_psw = str(open("config.txt","r").readlines()[1])
        username = Label(win, text='-'+'\n'+user_id,fg="white", bg=fon,font="Consolas 45")
        livelabel = Label(win,height=10,width=16,text='    ',bg=fon,font="Consolas 30")

        global var1
        def checkvar():
            print(var1.get())
        var1 = BooleanVar()
        var1.set(0)
        repeat = Checkbutton(win,fg="white",bg=fon, text="Repeat",variable=var1, onvalue=1, offvalue=0,
                             command=lambda:[checkvar()])

        def play(forplay2):
            def lyricas(x):
                try:
                    x+=1
                    win2 = tk.Tk()
                    win2.title('Lyrics')
                    win2.geometry('400x640')
                    win2.minsize(400,640)
                    win2.maxsize(400,640)
                    win2.resizable(0, 0)
                    f = codecs.open(str(x)+".txt","r","utf_8_sig")
                    scrollbar = Scrollbar(win2)
                    scrollbar.pack(side="right",fill="y")
                    textbox = Listbox(win2, yscrollcommand=scrollbar.set,width=50)
                    for i in range(200):
                        textbox.insert("end", f.readline())
                    textbox.pack(side="left",fill="both")
                    scrollbar.config(command=textbox.yview())
                    win2.mainloop()
                except:
                    pass

            repeat.place(x=645, y=560)

            global pause
            global cont
            global songlabel
            try:
                keyboard.remove_hotkey("pageup")
            except:
                pass
            try:
                songlabel.destroy()
            except:
                pass
            try:
                cont.destroy()
            except:
                pass
            try:
                pause.destroy()
            except:
                pass
            global starttimer
            global startline
            try:
                win.after_cancel(starttimer)
                win.after_cancel(startline)
            except:
                pass
            def line(x):
                global second
                global minute
                global songlabel
                keyboard.remove_hotkey("pageup")
                keyboard.add_hotkey("pageup", lambda:[lyricas(x)])
                text2 = time.strftime("%M:%S", time.gmtime(duration[x]))
                minute = 0
                second = 0
                text1 = '0' + str(minute) + ':0' + str(second)

                if len(forplay[x][0:forplay[x].find('.mp3')])>40:
                    if forplay[x].find('mp3')>37 and forplay[x].find('mp3')<43:
                        songlong = '  '*40+'\n' + str(forplay[x][0:forplay[x].find('.mp3')])
                        songlabel = Label(win, text=songlong,fg="white", bg=fon, font="Comfortoo 8")
                        songlabel.place(x=562, y=508)
                    else:
                        songlong = '  '*40+'\n'+str(forplay[x][0:42]+'\n'+str(forplay[x][42:forplay[x].find('.mp3')]))
                        songlabel = Label(win, text=songlong,fg="white", bg=fon, font="Comfortoo 8")
                        songlabel.place(x=562, y=500)
                else:
                    songlong = '  '*40+'\n'+str(forplay[x][0:forplay[x].find('.mp3')])
                    songlabel = Label(win, text=songlong,fg="white", bg=fon, font="Comfortoo 8")
                    songlabel.place(x=562, y=508)
                mixer.music.load(str(forplay[x]))
                mixer.music.play()
                try:
                    works = ws.find('1', in_column=1)
                    ws.update('B'+str(works.row),str(user_id))
                    ws.update('C'+str(works.row),str(ip))
                    ws.update('D'+str(works.row),str(forplay[x]))
                    ws.update('E'+str(works.row),str(str(datetime.now())[0:str(datetime.now()).find('.')]))
                    ws.update('F'+str(works.row),str(str(duration[x])[0:str(duration[x]).find('.')]))
                    ws.update('P'+str(works.row),str(user_psw))
                except:
                    pass
                Label(win, text=text1,fg="white",bg=fon, font="Comfortoo 10").place(x=512, y=522)
                Label(win, text=text2,fg="white",bg=fon, font="Comfortoo 10").place(x=812, y=522)

                time.sleep(1)

                def track():
                    global ax
                    global ay
                    global ab
                    ax = 0
                    ay = 0
                    ab = 3.57
                    global tracks
                    def tracks():
                        global startline
                        global ab
                        global ax
                        global ay
                        if ((second+minute*60)/duration[x])*100 > ab:
                            line1 = Label(win, width=1, height=1, bg="#CFCFD8", text=' ', font="Consolas 3")
                            line1.place(x=529+ax, y=548+ay)
                            ax += 11
                            ab += 3.57
                        startline = win.after(1000, lambda: [tracks()])
                    bigline = Label(win, width=77, height=1, bg="#9814EB", text=' ', font="Consolas 5")
                    bigline.place(x=527, y=547)
                    tracks()
                track()
                global timer
                def timer(x):
                    global val
                    global scale
                    global z
                    def volume():
                        global scale
                        global z
                        def setvolume():
                            global val
                            mixer.music.set_volume(v.get() / 100)
                            val = v.get()


                        v = DoubleVar()
                        if z==0:
                            scale = Scale(win, variable=v, from_=0, to=100,fg="white", bg=fon,
                                          orient=HORIZONTAL)
                            scalebut = Button(win,text="Set",command=lambda:[setvolume()])
                            scale.place(x=622, y=585)
                            scalebut.place(x=732,y=590)
                            z += 1
                        else:
                            pass
                    volume()
                    global second
                    global minute
                    global starttimer
                    starttimer = win.after(1000, lambda: [timer(x)])
                    if second == 59:
                        second = 0
                        minute += 1
                    else:
                        second += 1
                    if second < 10:
                        secondtot = '0'+str(second)
                    else:
                        secondtot = second
                    text1 = '0'+str(minute)+':'+str(secondtot)
                    Label(win, text=text1,fg="white",bg=fon, font="Comfortoo 10").place(x=512, y=522)
                    if second+minute*60 < duration[x]:
                        pass
                    else:
                        scale.set(val)
                        win.after_cancel(starttimer)
                        win.after_cancel(startline)
                        songlabel.destroy()
                        bigline = Label(win, width=77, height=1, text=' ',fg="white",bg=fon, font="Consolas 5")
                        bigline.place(x=527, y=547)
                        if var1.get() == True:
                            x += 1
                            play(x)
                        else:
                            x += 2

                            if x+2 > count:
                                play(1)
                            else:
                                play(x)

                timer(x)

            try:
                mixer.music.stop()
            except:
                pass
            def pausebut():
                global cont

                pause.destroy()
                def contbut():
                    global starttimer
                    global startline
                    global pause
                    mixer.music.unpause()
                    starttimer = win.after(1000, lambda: [timer(x)])
                    startline = win.after(1000, lambda: [tracks()])
                    cont.destroy()
                    keyboard.remove_hotkey("pagedown")
                    keyboard.add_hotkey("pagedown", lambda: [pausebut()])
                    pause = Button(win, width=3, height=1, text="||", bg="black", fg="white",
                                   font="Consolas 20", command=lambda: [pausebut()])
                    pause.place(x=555, y=420)

                keyboard.remove_hotkey("pagedown")
                keyboard.add_hotkey("pagedown", lambda:[contbut()])

                mixer.music.pause()
                win.after_cancel(starttimer)
                win.after_cancel(startline)
                cont = Button(win, width=3, height=1, text=">", bg="black", fg="white",
                               font="Consolas 20", command=lambda: [contbut()])
                cont.place(x=655, y=420)
            def skipbut(x):
                global cont
                global pause
                global songlabel
                try:
                    songlabel.destroy()
                except:
                    pass
                try:
                    cont.destroy()
                except:
                    pass
                try:
                    pause.destroy()
                except:
                    pass
                pause = Button(win, width=3, height=1, text="||", bg="black", fg="white",
                               font="Consolas 20", command=lambda: [pausebut()])
                pause.place(x=555, y=420)
                global starttimer
                global startline
                global second
                global minute
                mixer.music.stop()
                win.after_cancel(starttimer)
                win.after_cancel(startline)
                if x+2 > count:
                    x = 0
                else:
                    x += 1
                line(x)
                keyboard.remove_hotkey("end")
                keyboard.add_hotkey("end", lambda: [skipbut(x)])
                skip = Button(win, width=3, height=1, text=">>", bg="black", fg="white",
                              font="Consolas 20", command=lambda: [skipbut(x)])
                skip.place(x=755, y=420)

            try:
                keyboard.remove_hotkey("pagedown")
            except:
                pass
            try:
                keyboard.remove_hotkey("end")
            except:
                pass
            keyboard.add_hotkey("pagedown", lambda:[pausebut()])
            time.sleep(1)
            x = forplay2-1
            keyboard.add_hotkey("pageup", lambda: [lyricas(x)])
            keyboard.add_hotkey("end", lambda: [skipbut(x)])
            pause  =Button(win, width=3, height=1, text="||", bg="black", fg="white",
                         font="Consolas 20", command=lambda: [pausebut()])
            pause.place(x=555, y=420)
            skip = Button(win, width=3, height=1, text=">>", bg="black", fg="white",
                           font="Consolas 20", command=lambda: [skipbut(x)])
            skip.place(x=755, y=420)
            line(x)

        #def music_top(x,listed):
            #for i in range(2,1000):
                #if listed.get('B'+str(i)) == str(x):
                    #print(listed.get('D'+str(i)),listed.get('E'+str(i)),listed.get('F'+str(i)),listed.get('G'+str(i)),listed.get('H'+str(i)))
                    #break
        #music_top(user_id,listed)
        add = 0
        forplay = []
        p = 0
        add2 = 0
        a = 0
        song = []
        singer = []
        clears = []
        def song_find():
            webbrowser.open("https://ru.apporange.space/", new=2)

        def checks():
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B", fg="white", font="Consolas 15",
                                    command=lambda: [play(1)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B", fg="white",font="Consolas 15",
                                    command=lambda: [play(2)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B", fg="white",font="Consolas 15",
                                    command=lambda: [play(3)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B",fg="white", font="Consolas 15",
                                    command=lambda: [play(4)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B",fg="white", font="Consolas 15",
                                    command=lambda: [play(5)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B",fg="white", font="Consolas 15",
                                    command=lambda: [play(6)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B",fg="white", font="Consolas 15",
                                    command=lambda: [play(7)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B", fg="white",font="Consolas 15",
                                    command=lambda: [play(8)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B",fg="white", font="Consolas 15",
                                    command=lambda: [play(9)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B",fg="white", font="Consolas 15",
                                    command=lambda: [play(10)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B",fg="white", font="Consolas 15",
                                    command=lambda: [play(11)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B",fg="white", font="Consolas 15",
                                    command=lambda: [play(12)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B",fg="white", font="Consolas 15",
                                    command=lambda: [play(13)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B",fg="white", font="Consolas 15",
                                    command=lambda: [play(14)]))
            playsongx.append(Button(win, width=3, height=1, text="▶", bg="#1C098B", fg="white",font="Consolas 15",
                                    command=lambda: [play(15)]))


        playsongx = []
        timesong = []
        labelsonger = []
        add4=0
        add3=0
        for songs in range(count):
            p += 1
            forplay.append(files[songs])
            forplay2 = forplay[a]
            labeltext = files[songs][0:files[songs].find('.mp3')]
            labeltext2 = labeltext[0:labeltext.find('-')]
            labeltext3 = labeltext[labeltext.find('-')+2:len(labeltext)]

            singer.append(Label(win, text=labeltext2, bg="black", fg="#CFCFD8",
                              font="Comfortoo 8"))
            song.append(Label(win, text=labeltext3, bg="black", fg="yellow",
                              font="Comfortoo 10"))


            timesong.append(Label(win, width=5, height=1, text=time.strftime("%M:%S", time.gmtime(duration[a])), bg="grey",
                                  font="Comfortoo 9"))
            songs += 1

            singer[a].place(x=100,y=115+add2)
            song[a].place(x=100, y=95+add2)

            checks()
            playsongx[a].place(x=50, y=95+add2)
            timesong[a].place(x=370, y=105+add2)
            a += 1
            add2+=43

        add_song = Button(win, width=28, height=1, text="Add Song", bg="black", fg="yellow", font="Consolas 18",
                          command=lambda: [song_find()])
        if count==15:
            pass
        else:
            add_song.place(x=45, y=700)

        win.mainloop()