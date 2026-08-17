# necesario para reproducir
from pygame import mixer
import pygame
import threading

# interfaz
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import webbrowser

# variables globales
playlist_playing = False
song_playing = False
ruta_nueva = ""
ruta_anterior=""
root = Tk()
playlist_songs= []

# iniciar mixer
mixer.init()
pygame.display.init()

# config Tkinter
root.geometry("520x280")
root.title("MP3 Player PyGame")

# hilos de procesamiento
threads = []

def play_song(path):
    global song_playing
    mixer.music.load(path)
    mixer.music.play()
    song_playing=True

# detener
def stop_song():
    global playlist_playing
    global ruta_anterior
    mixer.music.stop()
    playlist_playing = False
    ruta_anterior=""

# pausar/despausar/reproducir
def play_pause_song():
    global ruta_anterior
    global playlist_playing
    global song_playing

    if playlist_playing == False:
        if ruta_anterior != added_songs_ui.get("anchor"):
            try:
                ruta_nueva = added_songs_ui.get("anchor")
                play_song(ruta_nueva)

                ruta_anterior=ruta_nueva

            # sino muestra un mensaje de error
            except Exception as i:
                messagebox.showerror(title="Error", message="Ningun archivo seleccionado\nError: "+str(i))
                playlist_playing = False

        # reproduce
        elif song_playing==False:
            mixer.music.unpause()
            song_playing = True

        # pausa
        elif song_playing==True:
            mixer.music.pause()
            song_playing = False

def add_song():
    # inicia un bloque de dialogo para buscar un archivo y luego guarda la ruta
    ruta_nueva =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp3 files","*.mp3"),("wav files","*.wav"),("all files","*.*")))

    # agrega la cancion al historial "added_songs_ui"
    if ruta_nueva != "":
        added_songs_ui.insert(END,ruta_nueva)

# nueva funcion en fase beta para acceder al buscador de youtube (Escobar)
def busca_video():
        # entra al buscador de youtube
        # inicio de navegador
        webbrowser.open("https://www.youtube.com/",new=2, autoraise=True)
        # Simplemente ingresa a youtube para darle mas variedad al usuario, o tambien puede utilizarlo para descargar archivos de audio.

        
# agrega una cancion a la lista
def add_to_playlist():
    global playlist_songs
    cont=0
    rutaSeleccionada=added_songs_ui.get("anchor")
    if rutaSeleccionada != "":
        for rutaExistente in playlist_songs:
            if rutaSeleccionada == rutaExistente: cont+=1
        if cont==0:
            playlist_songs.append(rutaSeleccionada)
            # añade la ruta a la lista visible
            playlist_songs_ui.insert(END,rutaSeleccionada)

# remueve una cancion a la lista
def remove_from_playlist():
    global playlist_songs
    indiceSeleccionado = playlist_songs.index(playlist_songs_ui.get(playlist_songs_ui.curselection()))
    # lo borra de la lista visible
    playlist_songs_ui.delete(indiceSeleccionado)
    # lo borra de la lista interna
    playlist_songs.pop(indiceSeleccionado)

# reproduce y pausa la cancion
def play_pause_playlist():
    global playlist_songs
    global song_playing
    global playlist_playing

    if playlist_playing == False:
        mixer.music.unpause()
        song_playing = True
        playlist_playing = True

    elif playlist_playing == True:
        mixer.music.pause()
        song_playing = False
        playlist_playing = False

################
#PLAYLIST LOGIC#
################
def start_playlist():
    global playlist_songs
    global song_playing
    global playlist_playing

    # copia la lista a una lista auxiliar
    aux = playlist_songs.copy()
    aux.reverse()
    song_playing = False
    
    # se verifica si la lista tiene mas de una cancion
    if len(aux)>1:
        # configura el evento de finalizado
        mixer.music.set_endevent ( pygame.USEREVENT ) 
        
        # carga y reproduce el primer tema
        play_song(aux.pop())
        playlist_playing = True

        while song_playing:
            for event in pygame.event.get():
                # verifica el evento de finalizado
                if event.type == 24 or event.type == 32866:
                    # verifica que hayan mas canciones
                    if len ( aux ) > 0:
                        play_song(aux.pop())

                    # detiene la reproduccion
                    else:
                        song_playing = False
    else:
        if len(aux)>0:
            play_song(aux[0])
            playlist_playing = True
                
def reset_playlist():
    global threads

    thread = threading.Thread(target=start_playlist,args=())
    threads.append(thread)
    thread.start()


######################
#AREA DE PRESENTACION#
######################
if __name__=='__main__':
    Label(root,text="Songs").grid(row=0,column=0)
    added_songs_ui = Listbox(root,width=40)
    added_songs_ui.grid(row =1,column=0)

    Label(root,text="Playlist").grid(row=0,column=2)
    playlist_songs_ui = Listbox(root,width=40)
    playlist_songs_ui.grid(row =1,column=2)


    """Botones basicos"""
    Button(root,text="Play/Pause", command=play_pause_song).grid(row =2,column=0,sticky=W,padx=15)
    Button(root,text="Stop", command=stop_song).grid(row =2,column=0,ipadx=21)
    Button(root,text="Add",command=add_song).grid(row =2,column=0,sticky=E,padx=15,ipadx=12)

    """Botones lista de reproduccion"""
    Button(root,text="+1",command=add_to_playlist).grid(row =2,column=2,sticky=W,padx=10)
    Button(root,text="-1",command=remove_from_playlist).grid(row =2,column=2,sticky=W,padx=40,ipadx=1)
    Button(root,text="Play/Reset",command=reset_playlist).grid(row =2,column=2,sticky=W,padx=70)
    Button(root,text="Play/Pause",command=play_pause_playlist).grid(row =2,column=2,sticky=E,padx=40)

    # nuevo boton para acceder al navegador, para que el usuario pueda ver videos, musica. (Escobar)
    Button(root,text="Search online",command=busca_video).grid(row=4 ,column=0) 

    root.mainloop()