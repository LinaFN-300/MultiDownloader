import tkinter as tk
from tkinter import scrolledtext

from subprocess import Popen, PIPE
import threading


#--------------------------------------------------
def execute_command(command, text_widget):
    process = Popen(command, stdout=PIPE, stderr=PIPE, text=True, shell=True)
    
    for line in iter(process.stdout.readline, ''):
        text_widget.insert(tk.END, line)
        text_widget.see(tk.END)
    
    process.stdout.close()
    process.wait()

def start_thread(command, text_widget):
    threading.Thread(target=execute_command, args=(command, text_widget)).start()

def download_video(url, text_widget):
    URLentry.delete(0, tk.END)
    try:
        start_thread('bin\yt-dlp.exe --embed-thumbnail --write-subs --sub-langs ja --embed-chapters --output "yt-dlp/video/%(extractor)s/%(title)s.%(ext)s" --cookies "cookies.txt" -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" ' + url, text_widget)
    except:
        text_widget.insert(tk.END, "エラーが発生しました。")

def download_audio(url):
    URLentry.delete(0, tk.END)
    start_thread('bin\yt-dlp.exe --output "yt-dlp/audio/%(extractor)s/%(title)s.%(ext)s" --cookies "cookies.txt" -f "bestaudio[ext=m4a]/best" ' + url, logTextArea)

def download_image(url):
    URLentry.delete(0, tk.END)
    start_thread('bin\gallery-dl.exe --cookies "cookies.txt" ' + url, logTextArea)

def download_image_recursive(url):
    URLentry.delete(0, tk.END)
    start_thread('bin\gallery-dl.exe --recursive --cookies "cookies.txt" ' + url, logTextArea)

#--------------------------------------------------
#GUI
root = tk.Tk()
root.title("LinaMultiDownloader")
root.geometry("420x270")

#URL Entry
URLlabel = tk.Label(root, text="URL")
URLlabel.place(x=10, y=5)

URLentry = tk.Entry(root, width=66)
URLentry.place(x=10, y=30)

#Download Button
#動画
DLButtonMovie = tk.Button(root, text="動画をダウンロード", width=27)
DLButtonMovie.bind("<Button-1>", lambda event: download_video(URLentry.get(), logTextArea))
DLButtonMovie.place(x=10, y=60)
#音声
DLButtonAudio = tk.Button(root, text="音声をダウンロード", width=27)
DLButtonAudio.bind("<Button-1>", lambda event: download_audio(URLentry.get()))
DLButtonAudio.place(x=212, y=60)
#画像
DLButtonImage = tk.Button(root, text="画像をダウンロード", width=27)
DLButtonImage.bind("<Button-1>", lambda event: download_image(URLentry.get()))
DLButtonImage.place(x=10, y=90)
#画像(サイトから一括)
DLButtonImageSite = tk.Button(root, text="画像を総当たりで一括ダウンロード", width=27)
DLButtonImageSite.bind("<Button-1>", lambda event: download_image_recursive(URLentry.get()))
DLButtonImageSite.place(x=212, y=90)

#exit Button
exitButton = tk.Button(root, text="終了", width=56)
exitButton.bind("<Button-1>", lambda event: exit())
exitButton.place(x=10, y=120)


#Download Progress
logTextArea= scrolledtext.ScrolledText(root, width=55, height=8)
logTextArea.place(x=10, y=155)


root.mainloop()

root.destroy()