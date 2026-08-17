"""
es necesario
    -pygame
    -threading
"""

#necesario para reproducir
from pygame import mixer
import pygame
import threading

#interfaz
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import webbrowser

#variables globales
reset =True
val = 0
reproduciendo=False
rutaNueva = ""
rutaAnterior="anterior"
root = Tk()
lista_de_reproduccion= []
contador_lista=0

#iniciar mixer
mixer.init()
pygame.display.init()

#config. Tkinter
root.geometry("520x280")

#hilos de procesamiento
threads = []


##################
#AREA DE PROCESOS#
##################

class Buttons:
    #detener
    def stop():
        global val
        global rutaAnterior
        mixer.music.stop()
        val = 0
        rutaAnterior="anterior"
        
    #pausar/despausar/reproducir
    def pause_play():
        global rutaAnterior
        global val
        global reproduciendo
        
        
        if val ==0:
            if rutaAnterior != Historial.get("anchor"):
                try:
                    rutaNueva = Historial.get("anchor")
                    mixer.music.load(rutaNueva)
                    mixer.music.play()
                    
                    #habilita la posibilidad de pausar
                    reproduciendo=True
                    rutaAnterior=rutaNueva
                
                #sino muestra un mensaje de error
                except Exception as i:
                    messagebox.showerror(title="Error", message="Ningun archivo seleccionado\nError: "+str(i))
                    val=0
        
            #reproduce
            elif reproduciendo==False:
                mixer.music.unpause()
                reproduciendo = True

            #pausa
            elif reproduciendo==True:
                mixer.music.pause()
                reproduciendo = False
            
    def search():
    
        #inicia un bloque de dialogo para buscar un archivo y luego guarda la ruta
        rutaNueva =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp3 files","*.mp3"),("wav files","*.wav"),("all files","*.*")))

        #agrega la cancion al historial
        if rutaNueva!="":
            Historial.insert(END,rutaNueva)


    def BuscaVideo():##nueva funcion en fase beta para acceder al buscador de youtube(Escobar)
         #entra al buscador de youtube
         #inicio de navegador
         webbrowser.open("https://www.youtube.com/",new=2, autoraise=True)
         #Simplemente ingresa a youtube para darle mas variedad al usuario, o tambien puede utilizarlo para descargar archivos de audio.
       
    ##Esta funcion servira de guia para el usuario a la hora de realizar una descarga y conversion de video.
    def Descargar():##Funcion de instrucciones de descarga.
        messagebox.showinfo(message="Primero clickee su video, omita los anuncios y luego por favor copie la URL del video(es la que esta en la parte superior de la pestaña del navegador, tambien puede seleccionar todo y utilizar el comando CTRL+C para copiar la URL, Confirme con un (si o no) despues del ""OK"" para ayudarlo en el siguiente paso",title="Ayuda de Descarga")
        Confirmador=messagebox.askyesno(message="¿Lo logro?", title="Confirmacion")##Confirma entendimiento y exito del usuario a la hora de seguir las instrucciones
       
        if(Confirmador== True):
            webbrowser.open("www.example.com",new=2, autoraise=True)
 
            messagebox.showinfo(message="Ahora esta en la pagina del convertidor, debe pegar la URL que ya copio del video que selecciono lo puede hacer con el comando CTRL+V, luego puede elegir en las opciones el formato de conversion, luego clickee convertir a y Confirme con un (si o no) despues del ""OK"" para ayudarlo en el siguiente paso,", title="Conversion")
  

            Confirmador=messagebox.askyesno(message="¿Lo logro?", title="Confirmacion")      ##Confirma entendimiento y exito del usuario a la hora de seguir las instrucciones
      

            if(Confirmador==True):
  
                messagebox.showinfo(message="Ya esta en la parte final del procedimiento, tiene que clickear en descargar y cerrar los anuncios que aparezcan, luego de eso podra ver en la parte inferior el archivo de video convertido en el formato deseado, y tocando la flechita que apunta arriba(la que esta a la derecha del archivo) y seleccionando: ""mostrar en carpeta.., podra ver la ruta donde guardo el archivo, para luego poder reproducirlo con el reproductor.",title="Final del Procedimiento")


        
class Lista:
    
    #agrega una cancion a la lista
    def listAdd():
        global lista_de_reproduccion
        cont=0
        rutaSeleccionada=Historial.get("anchor")
        if rutaSeleccionada != "":
            for rutaExistente in lista_de_reproduccion:
                if rutaSeleccionada == rutaExistente: cont+=1
            if cont==0:
                lista_de_reproduccion.append(rutaSeleccionada)
                """añade la ruta a la lista visible"""
                Lista_reproduccion.insert(END,rutaSeleccionada)

    #remueve una cancion a la lista
    def listRemove():
        global lista_de_reproduccion
        indiceSeleccionado = lista_de_reproduccion.index(Lista_reproduccion.get(Lista_reproduccion.curselection()))
        #lo borra de la lista visible
        Lista_reproduccion.delete(indiceSeleccionado)
        #lo borra de la lista interna
        lista_de_reproduccion.pop(indiceSeleccionado)

    ######################
    #HILO DE REPRODUCCION#
    ######################
    def Play_Thread():
        global lista_de_reproduccion
        global contador_lista
        global reproduciendo
        global val
        global threads

        #copia la lista a una lista auxiliar
        aux=lista_de_reproduccion.copy()
        aux.reverse()
        reproduciendo =False
        
        if reproduciendo==False:
            #se verifica si la lista tiene mas de una cancion
            
                
            if len(aux)>1 :
                mixer.music.load ( aux.pop() )  #carga y reproduce el primer tema
                mixer.music.set_endevent ( pygame.USEREVENT ) #configura el evento de finalizado
                mixer.music.play()
                reproduciendo = True
                
                val=1
                
                while reproduciendo:
                    for event in pygame.event.get():
                        #verifica el evento de finalizado
                        if event.type == 24: 
                            #verifica que hayan mas canciones
                            if len ( aux ) > 0:
                                mixer.music.load ( aux.pop() ) 
                                mixer.music.play()
                                                    
                            #detiene la reproduccion
                            else:
                                reproduciendo = False
            else:
                print("ulti")
                if len(lista_de_reproduccion)>0:
                    mixer.music.load(lista_de_reproduccion[0])
                    mixer.music.play()
                    reproduciendo = True
                    val=1

            
    def reset():
        global threads
    
        t = threading.Thread(target=Lista.Play_Thread,args=())
        threads.append(t)
        t.start()

        
    #reproduce y pausa la cancion
    def pause_play():
        global lista_de_reproduccion
        global contador_lista
        global reproduciendo
        global val

        if val == 0:
            mixer.music.unpause()
            reproduciendo = True
            val=1
    
        elif val==1:
            mixer.music.pause()
            reproduciendo = False
            val = 0

######################
#AREA DE PRESENTACION#
######################
Label(root,text="historial de canciones").grid(row=0,column=0)
Historial = Listbox(root,width=40)
Historial.grid(row =1,column=0)

Label(root,text="Lista de reproduccion").grid(row=0,column=2)
Lista_reproduccion = Listbox(root,width=40)
Lista_reproduccion.grid(row =1,column=2)


"""Botones basicos"""
pause_play = Button(root,text="Play/Pause", command=Buttons.pause_play).grid(row =2,column=0,sticky=W,padx=15)

stop = Button(root,text="Stop", command=Buttons.stop).grid(row =2,column=0,ipadx=21)

search = Button(root,text="Buscar",command=Buttons.search).grid(row =2,column=0,sticky=E,padx=15,ipadx=12)

"""Botones lista de reproduccion"""
Button(root,text="+1",command=Lista.listAdd).grid(row =2,column=2,sticky=W,padx=10)
Button(root,text="-1",command=Lista.listRemove).grid(row =2,column=2,sticky=W,padx=40,ipadx=1)

Button(root,text="Play/Reset",command=Lista.reset).grid(row =2,column=2,sticky=W,padx=70)

Button(root,text="Pause",command=Lista.pause_play).grid(row =2,column=2,sticky=E,padx=40)

Internet=Button(root,text="Buscar mas musica o Videos",command=Buttons.BuscaVideo).grid(row=4 ,column=0) # nuevo boton para acceder al navegador, para que el usuario pueda ver videos, musica, y tambien pueda descargar musica siguiendo las instrucciones del siguiente boton(Escobar)

Descargar=Button(root,text="Explicacion de descarga",command=Buttons.Descargar).grid(row=5 ,column=0)#Introduccion al usuario para que sepa como convertir y descargar videos

root.mainloop()