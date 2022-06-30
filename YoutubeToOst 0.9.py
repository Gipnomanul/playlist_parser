from tkinter import *          #Для GUI
from tkinter import filedialog #Для открытия диалога выбора папки сохранения
from pytube import YouTube     #YouTube для возможности скачивания видео (mp3 или mp4)
from pytube import Playlist    #Playlist для быстрого и удобного парсинга ссылок в плейлисте
import pafy    				   #Для получения информации о видео, такой как лайки, просмотры
import os 				       #Для работы с путем файла

root = Tk()
root.title("Youtube playlist viewer")
root.geometry("915x500")

links = []   #Массив с ссылками на видео
info_t = []  #Массив с названием видео
info_v = []  #Массив с просмотрами видео
info_l = []  #Массив с лайками видео
data_links = []   #Массив с номерами, нужен для связи в других массивах
views_links = []  #Массив для скачивания самых "просматриваемых" видео

selected_one = -1   #Выбранное видео в левом листбоксе
selected = []       #Массив выбранных видео (сохраняются их номера)
selected_chosen = -1  #Массив выбранного видео в выбранных

def find_links():
	global views_links
	
	lb_status.configure(text = 'Инициализация плейлиста...')
	btn_playlist.configure(state = 'disabled')
	playlist_en.configure(state = 'disabled')
	root.update()
	
	pl_link = playlist_en.get()
	p = Playlist(pl_link)
	
	for url in p.video_urls:
		links.append(url)
	print(links)
	 
	for i in range(len(links)):
		#if i == 3: break      #Для отладки, чтобы не скачивать слишком много видео
		lb_status.configure(text = f'Обрабатываю видео #{i+1}')
		print(links[i])
		data_links.append(i)
		# getting video
		video = pafy.new(links[i]) 
		# getting info of the video
		likes = video.likes
		views = video.viewcount
		title = video.title
		# printing the value
		info_t.append(str(title)); info_v.append(str(views)); info_l.append(str(likes))
		views_links.append([views, links[i]])
		vids_playlist.insert(END, info_t[i])
		root.update()
	
	lb_status.configure(text = 'Готово!')
	views_links.sort(reverse=True)
	print(views_links)

def callback(event):     #При выборе значения из Listbox выполняет действие
	global selected_one
	selection = event.widget.curselection()
	if selection:
		selected_one = selection[0]
		print(selected_one)
		data = event.widget.get(selected_one)
		lb_title.configure(text = info_t[selected_one])
		lb_views.configure(text = info_v[selected_one])
		lb_likes.configure(text = info_l[selected_one])
		print(data)
	else:
		print()
		
def callback_2(event):
	global selected_chosen
	selection = event.widget.curselection()
	if selection:
		selected_chosen = selection[0]
		print(selected_chosen)
		#data = event.widget.get(selected_one)

def choose():
	global selected
	if selected_one != -1 and selected_one not in selected:
		selected.append(selected_one)
		selected_playlist.insert(END, info_t[selected_one])
		
def choose_all():
	global selected
	selected_playlist.delete(0, END)
	selected = []
	for i in data_links:
		selected.append(i)
	print(selected)
	for i in info_t:
		selected_playlist.insert(END, i)
		
def delete():
	global selected_chosen, selected
	if selected_chosen != -1:
		selected_playlist.delete(selected_chosen, selected_chosen)
		del selected[selected_chosen]
		print(selected)
	selected_chosen = -1
	
def delete_all():
	global selected
	selected = []
	selected_playlist.delete(0, END)
	
def download():
	global selected
	dirname = filedialog.askdirectory()
	print(dirname)
	lb_status.configure(text = 'Загрузка началась!')
	root.update()
	k = 0
	for i in selected:
		k += 1
		yt = YouTube(links[i])
		video = yt.streams.filter(only_audio=True).first()
		out_file = video.download(output_path=dirname)
		base, ext = os.path.splitext(out_file)
		new_file = base + '.mp3'
		os.rename(out_file, new_file)
		lb_status.configure(text = f'Загружен {k} трек из {len(selected)}')
		root.update()
		
	print("Download completed!")
	lb_status.configure(text = f'Загрузка завершена! Скачано {k} треков')
	
def download_n():
	global views_links
	dirname = filedialog.askdirectory()
	print(dirname)
	lb_status.configure(text = 'Загрузка началась!')
	root.update()
	kol = int(chosen_v.get())
	k = 0
	for i in range(0, kol):
		k += 1
		print(views_links[i][1])
		yt = YouTube(views_links[i][1])
		video = yt.streams.filter(only_audio=True).first()
		out_file = video.download(output_path=dirname)
		base, ext = os.path.splitext(out_file)
		new_file = base + '.mp3'
		os.rename(out_file, new_file)
		lb_status.configure(text = f'Загружен {k} трек из {len(selected)}')
		root.update()
		
	print("Download completed!")
	lb_status.configure(text = f'Скачано {k} треков')

tit = Label(text = "Youtube playlist viewer", font = "Arial 16")
tit.grid(row = 0, column = 0, columnspan = 8)

lb1 = Label(text = "Ссылка на плейлист:", font = "Arial")
lb1.grid(row = 1, column = 0, columnspan = 2, padx = 10)

playlist_en = Entry(width = 50)
playlist_en.grid(row = 1, column = 2, columnspan = 3)
playlist_en.insert(0, "https://www.youtube.com/watch?v=qDnrdeNDRio&list=PL4CFrY25ig_hqow33aufz3L8w5Xv4oK00&ab_channel=DavidJ.")
#playlist_en.insert(0, "https://www.youtube.com/watch?v=lcJzw0JGfeE&list=PLqM7alHXFySENpNgw27MzGxLzNJuC_Kdj")

btn_playlist = Button(text = 'Найти!', command = find_links, width = 10)
btn_playlist.grid(row = 1, column = 5, padx = 20)

#lb7 = Label(text = "Статус:")
#lb7.grid(row = 2, column = 3)

#lb_status = Label(text = "")
#lb_status.grid(row = 2, column = 4, columnspan = 2)

lb2 = Label(text = "Название видео:", font = "Arial")
lb2.grid(row = 3, column = 0, columnspan = 2, pady = 40)

lb3 = Label(text = "Информация о видео:", font = "Arial")
lb3.grid(row = 3, column = 3, columnspan = 2)

vids_playlist = Listbox(width = 40, height = 20)
vids_playlist.grid(row = 4, column = 0, columnspan = 2, rowspan = 20)
vids_playlist.bind("<<ListboxSelect>>", callback)

lb4 = Label(text = "Название видео:")
lb4.grid(row = 4, column = 2, columnspan = 2)

frame_title = Frame(width=200, height = 20)
frame_title.grid(row = 4, column = 4, columnspan = 2)
frame_title.pack_propagate(False)
lb_title = Label(frame_title, anchor="w", justify=LEFT)
lb_title.pack()
#lb_title.grid(row = 4, column = 4, columnspan = 2)

lb5 = Label(text = "Количество просмотров:")
lb5.grid(row = 5, column = 2, columnspan = 2)

lb_views = Label()
lb_views.grid(row = 5, column = 4, columnspan = 2)

lb6 = Label(text = "Лайки:")
lb6.grid(row = 6, column = 2, columnspan = 2)

lb_likes = Label()
lb_likes.grid(row = 6, column = 4, columnspan = 2)

btn_choose = Button(text = 'Добавить для скачивания', command = choose, width = 20)
btn_choose.grid(row = 7, column = 2, columnspan = 2)

btn_choose_all = Button(text = 'Выбрать все', command = choose_all, width = 20)
btn_choose_all.grid(row = 8, column = 2, columnspan = 2)

btn_del = Button(text = 'Удалить выбранное', command = delete, width = 20)
btn_del.grid(row = 7, column = 4, columnspan = 2)

btn_del_all = Button(text = 'Удалить все выбранные', command = delete_all, width = 20)
btn_del_all.grid(row = 8, column = 4, columnspan = 2)

btn_download = Button(text = 'Скачать выбранные видео', command = download, width = 20)
btn_download.grid(row = 9, column = 4, columnspan = 2)

lb9 = Label(text = "Статус загрузки:")
lb9.grid(row = 14, column = 2, columnspan = 2)

lb_status = Label(text = "Файлы не загружаются")
lb_status.grid(row = 14, column = 4, columnspan = 2)

lb_chosen = Label(text = "Скачать выбранное количество видео:")
lb_chosen.grid(row = 15, column = 2, columnspan = 2)

chosen_v = Entry(width = 5)
chosen_v.grid(row = 16, column = 2, columnspan = 2)
chosen_v.insert(0, '9')

btn_download_n = Button(text = 'Скачать', command = download_n, width = 20)
btn_download_n.grid(row = 15, column = 4, columnspan = 2)

lb8 = Label(text = "Выбранные видео:", font = "Arial")
lb8.grid(row = 3, column = 6, columnspan = 2)

selected_playlist = Listbox(width = 40, height = 20)
selected_playlist.grid(row = 4, column = 6, columnspan = 2, rowspan = 15)
selected_playlist.bind("<<ListboxSelect>>", callback_2)

root.mainloop()
