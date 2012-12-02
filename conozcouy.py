#! /usr/bin/env python
# Conozco Uruguay
# Copyright (C) 2008,2009 Gabriel Eirea
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Gabriel Eirea geirea@gmail.com
# Ceibal Jam http://ceibaljam.org

import sys, pygame, random, os
import olpcgames
import gtk
import imp

from gettext import gettext as _

RADIO = 10
RADIO2 = RADIO**2
XMAPAMAX = 786
DXPANEL = 414
XCENTROPANEL = 1002
YGLOBITO = 310
DXBICHO = 218
DYBICHO = 268
XBICHO = 1200-DXBICHO
YBICHO = 900-DYBICHO
XNAVE = 800
YNAVE = 650
DXNAVE = 100
DYNAVE = 200
CAMINODATOS = "datos"
ARCHIVODEPTOS = "departamentos"
ARCHIVOLUGARES = "ciudades"
ARCHIVONIVELES = "niveles.txt"
ARCHIVOEXPLORACIONES = "exploraciones.txt"
ARCHIVORIOS = "rios"
ARCHIVOCUCHILLAS = "cuchillas"
ARCHIVOCREDITOS = "creditos.txt"
ARCHIVOPRESENTACION = "presentacion"
CAMINOIMAGENES = "imagenes"
CAMINOSONIDOS = "sonidos"
COLORNOMBREDEPTO = (200,60,60)
COLORNOMBRECAPITAL = (10,10,10)
COLORNOMBRERIO = (10,10,10)
COLORNOMBREELEVACION = (10,10,10)
COLORPREGUNTAS = (80,80,155)
COLORPANEL = (156,158,172)
TOTALAVANCE = 7
EVENTORESPUESTA = pygame.USEREVENT+1
TIEMPORESPUESTA = 2300
EVENTODESPEGUE = EVENTORESPUESTA+1
TIEMPODESPEGUE = 40
EVENTOREFRESCO = EVENTODESPEGUE+1
TIEMPOREFRESCO = 250

# variables globales para adaptar la pantalla a distintas resoluciones
scale = 1
shift_x = 0
shift_y = 0
xo_resolution = True

clock = pygame.time.Clock()

def wait_events():
    """ Funcion para esperar por eventos de pygame sin consumir CPU """
    global clock
    clock.tick(20)
    return pygame.event.get()

class Punto():
    """Clase para objetos geograficos que se pueden definir como un punto.

    La posicion esta dada por un par de coordenadas (x,y) medida en pixels
    dentro del mapa.
    """
    
    def __init__(self,nombre,tipo,simbolo,posicion,postexto):
        global scale, shift_x, shift_y
        self.nombre = nombre
        self.tipo = int(tipo)
        self.posicion = (int(int(posicion[0])*scale+shift_x),
                         int(int(posicion[1])*scale+shift_y))
        self.postexto = (int(int(postexto[0])*scale)+self.posicion[0],
                         int(int(postexto[1])*scale)+self.posicion[1])
        self.simbolo = simbolo

    def estaAca(self,pos):
        """Devuelve un booleano indicando si esta en la coordenada pos,
        la precision viene dada por la constante global RADIO"""
        if (pos[0]-self.posicion[0])**2+\
                (pos[1]-self.posicion[1])**2 < RADIO2:
            return True
        else:
            return False

    def dibujar(self,pantalla,flipAhora):
        """Dibuja un punto en su posicion"""
        pantalla.blit(self.simbolo, (self.posicion[0]-8,self.posicion[1]-8))
        if flipAhora:
            pygame.display.flip()

    def mostrarNombre(self,pantalla,fuente,color,flipAhora):
        """Escribe el nombre del punto en su posicion"""
        text = fuente.render(self.nombre, 1, color)
        textrect = text.get_rect()
        textrect.center = (self.postexto[0],self.postexto[1])
        pantalla.blit(text, textrect)
	if flipAhora:
            pygame.display.flip()


class Zona():
    """Clase para objetos geograficos que se pueden definir como una zona.

    La posicion esta dada por una imagen bitmap pintada con un color
    especifico, dado por la clave (valor 0 a 255 del componente rojo).
    """

    def __init__(self,mapa,nombre,claveColor,tipo,posicion,rotacion):
        self.mapa = mapa # esto hace una copia en memoria o no????
        self.nombre = nombre
        self.claveColor = int(claveColor)
        self.tipo = int(tipo)
        self.posicion = (int(int(posicion[0])*scale+shift_x),
                         int(int(posicion[1])*scale+shift_y))
        self.rotacion = int(rotacion)

    def estaAca(self,pos):
        """Devuelve True si la coordenada pos esta en la zona"""
        if pos[0] < XMAPAMAX*scale+shift_x:
            colorAca = self.mapa.get_at((pos[0]-shift_x, pos[1]-shift_y))
            if colorAca[0] == self.claveColor:
                return True
            else:
                return False
        else:
            return False

    def mostrarNombre(self,pantalla,fuente,color,flipAhora):
        """Escribe el nombre de la zona en su posicion"""
        text = fuente.render(self.nombre, 1, color)
        textrot = pygame.transform.rotate(text,self.rotacion)
        textrect = textrot.get_rect()
        textrect.center = (self.posicion[0],self.posicion[1])
        pantalla.blit(textrot, textrect)
	if flipAhora:
            pygame.display.flip()


class Nivel():
    """Clase para definir los niveles del juego.

    Cada nivel tiene un dibujo inicial, los elementos pueden estar etiquetados
    con el nombre o no, y un conjunto de preguntas.
    """

    def __init__(self,nombre):
        self.nombre = nombre
        self.dibujoInicial = list()
        self.nombreInicial = list()
        self.preguntas = list()
        self.indicePreguntaActual = 0
        self.elementosActivos = list()

    def prepararPreguntas(self):
        """Este metodo sirve para preparar la lista de preguntas al azar."""
        random.shuffle(self.preguntas)

    def siguientePregunta(self,listaSufijos,listaPrefijos):
        """Prepara el texto de la pregunta siguiente"""
        self.preguntaActual = self.preguntas[self.indicePreguntaActual]
        self.sufijoActual = random.randint(1,len(listaSufijos))-1
        self.prefijoActual = random.randint(1,len(listaPrefijos))-1
        lineas = listaPrefijos[self.prefijoActual].split("\\")
        lineas.extend(self.preguntaActual[0].split("\\"))
        lineas.extend(listaSufijos[self.sufijoActual].split("\\"))
        self.indicePreguntaActual = self.indicePreguntaActual+1
        if self.indicePreguntaActual == len(self.preguntas):
            self.indicePreguntaActual = 0
        return lineas

    def devolverAyuda(self):
        """Devuelve la linea de ayuda"""
	self.preguntaActual = self.preguntas[self.indicePreguntaActual-1]
        return self.preguntaActual[3].split("\\")

    def mostrarPregunta(self,pantalla,fuente,sufijo,prefijo):
        """Muestra la pregunta en el globito"""
        self.preguntaActual = self.preguntas[self.indicePreguntaActual]
        lineas = prefijo.split("\\")
        lineas.extend(self.preguntaActual[0].split("\\"))
        lineas.extend(sufijo.split("\\"))
        yLinea = 100
        for l in lineas:
            text = fuente.render(l, 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (XCENTROPANEL,yLinea)
            pantalla.blit(text, textrect)
            yLinea = yLinea + fuente.get_height()
	pygame.display.flip()


class ConozcoUy():
    """Clase principal del juego.

    """

    def mostrarTexto(self,texto,fuente,posicion,color):
        """Muestra texto en una determinada posicion"""
        text = fuente.render(texto, 1, color)
        textrect = text.get_rect()
        textrect.center = posicion
        self.pantalla.blit(text, textrect)

    def cargarDepartamentos(self):
        """Carga las imagenes y los datos de los departamentos"""
        self.deptos = self.cargarImagen("deptos.png")
        self.deptosLineas = self.cargarImagen("deptosLineas.png")
        self.listaDeptos = list()
        # falta sanitizar manejo de archivo
        r_path = os.path.join(CAMINODATOS,ARCHIVODEPTOS + '.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source(ARCHIVODEPTOS, a_path)
        except:
            print "Cannot open %s" % (ARCHIVODEPTOS,)
        if f:
            if hasattr(f, 'DEPARTMENTS'):
                for department in f.DEPARTMENTS:
                    [nombreDepto, claveColor, posx, posy, rotacion] = department
                    nuevoDepto = Zona(self.deptos,unicode(nombreDepto,'iso-8859-1'),
                              claveColor,1,(posx,posy),rotacion)
                    self.listaDeptos.append(nuevoDepto)
    def cargarRios(self):
        """Carga las imagenes y los datos de los rios"""
        self.rios = self.cargarImagen("rios.png")
        self.riosDetectar = self.cargarImagen("riosDetectar.png")
        self.listaRios = list()
        # falta sanitizar manejo de archivo
        r_path = os.path.join(CAMINODATOS,ARCHIVORIOS + '.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source(ARCHIVORIOS, a_path)
        except:
            print "Cannot open %s" % (ARCHIVORIOS,)

        if f:
            if hasattr(f, 'RIOS'):
                for rio in f.RIOS:
                    [nombreRio,claveColor,posx,posy,rotacion] = rio
                    nuevoRio = Zona(self.riosDetectar,
                                    unicode(nombreRio,'iso-8859-1'),
                                    claveColor,1,(posx,posy),rotacion)
                    self.listaRios.append(nuevoRio)

    def cargarCuchillas(self):
        """Carga las imagenes y los datos de las cuchillas"""
        self.cuchillas = self.cargarImagen("cuchillas.png")
        self.cuchillasDetectar = self.cargarImagen("cuchillasDetectar.png")
        self.listaCuchillas = list()
        # falta sanitizar manejo de archivo
        r_path = os.path.join(CAMINODATOS,ARCHIVOCUCHILLAS + '.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source(ARCHIVOCUCHILLAS, a_path)
        except:
            print "Cannot open %s" % (ARCHIVOCUCHILLAS,)
        if f:
            if hasattr(f, 'BLADES'):
                for blade in f.BLADES:
                    [nombreCuchilla,claveColor,posx,posy,rotacion] = blade
                    nuevaCuchilla = Zona(self.cuchillasDetectar,
                                         unicode(nombreCuchilla,'iso-8859-1'),
                                         claveColor,1,(posx,posy),rotacion)
                    self.listaCuchillas.append(nuevaCuchilla)

    def cargarLugares(self):
        """Carga los datos de las ciudades y otros puntos de interes"""
        self.simboloCapital = pygame.image.load( \
            os.path.join(CAMINOIMAGENES,"capital.png"))
        self.simboloCiudad = pygame.image.load( \
            os.path.join(CAMINOIMAGENES,"ciudad.png"))
        self.simboloCerro = pygame.image.load( \
            os.path.join(CAMINOIMAGENES,"cerro.png"))
        self.listaLugares = list()
        # falta sanitizar manejo de archivo
        r_path = os.path.join(CAMINODATOS,ARCHIVOLUGARES + '.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source(ARCHIVOLUGARES, a_path)
        except:
            print "Cannot open %s" % (ARCHIVOLUGARES,)
        if f:
            if hasattr(f, 'CITIES'):
                for city in f.CITIES:
                    [nombreLugar,posx,posy,tipo,incx,incy] = city
                    if int(tipo) == 1:
                        simbolo = self.simboloCapital
                    elif int(tipo) == 2:
                        simbolo = self.simboloCiudad
                    elif int(tipo) == 5:
                        simbolo = self.simboloCerro
                    else:
                        simbolo = self.simboloCiudad

                    nuevoLugar = Punto(unicode(nombreLugar,'iso-8859-1'),
                                       int(tipo),simbolo,
                                       (posx,posy),(incx,incy))
                    self.listaLugares.append(nuevoLugar)

    def cargarNiveles(self):
        """Carga los niveles del archivo de configuracion"""
        self.listaNiveles = list()
        self.listaPrefijos = list()
        self.listaSufijos = list()
        self.listaCorrecto = list()
        self.listaMal = list()
        self.listaDespedidas = list()
        # falta sanitizar manejo de archivo
        f = open(os.path.join(CAMINODATOS,ARCHIVONIVELES),"r")
        linea = f.readline()
        while linea:
            if linea[0] == "#":
                linea = f.readline()
                continue
            if linea[0] == "[":
                # empieza nivel
                nombreNivel = linea.strip("[]\n")
                nuevoNivel = Nivel(nombreNivel)
                self.listaNiveles.append(nuevoNivel)
                linea = f.readline()
                continue
            if linea.find("=") == -1:
                linea = f.readline()
                continue         
            [var,valor] = linea.strip().split("=")
            if var.startswith("Prefijo"):
                self.listaPrefijos.append(unicode(valor.strip(),'iso-8859-1'))
            elif var.startswith("Sufijo"):
                self.listaSufijos.append(unicode(valor.strip(),'iso-8859-1'))
            elif var.startswith("Correcto"):
                self.listaCorrecto.append(unicode(valor.strip(),'iso-8859-1'))
            elif var.startswith("Mal"):
                self.listaMal.append(unicode(valor.strip(),'iso-8859-1'))
            elif var.startswith("Despedida"):
                self.listaDespedidas.append(unicode(valor.strip(),'iso-8859-1'))
            elif var.startswith("dibujoInicial"):
                listaDibujos = valor.split(",")
                for i in listaDibujos:
                    nuevoNivel.dibujoInicial.append(i.strip())
            elif var.startswith("nombreInicial"):
                listaNombres = valor.split(",")
                for i in listaNombres:
                    nuevoNivel.nombreInicial.append(i.strip())
            elif var.startswith("Pregunta"):
                [texto,tipo,respuesta,ayuda] = valor.split("|")
                nuevoNivel.preguntas.append(
                    (unicode(texto.strip(),'iso-8859-1'),
                     int(tipo),
                     unicode(respuesta.strip(),'iso-8859-1'),
                     unicode(ayuda.strip(),'iso-8859-1')))
            linea = f.readline()
        f.close()
        self.indiceNivelActual = 0
        self.numeroNiveles = len(self.listaNiveles)
        self.numeroSufijos = len(self.listaSufijos)
        self.numeroPrefijos = len(self.listaPrefijos)
        self.numeroCorrecto = len(self.listaCorrecto)
        self.numeroMal = len(self.listaMal)
        self.numeroDespedidas = len(self.listaDespedidas)

    def cargarExploraciones(self):
        """Carga los niveles de exploracion del archivo de configuracion"""
        self.listaExploraciones = list()
        # falta sanitizar manejo de archivo
        f = open(os.path.join(CAMINODATOS,ARCHIVOEXPLORACIONES),"r")
        linea = f.readline()
        while linea:
            if linea[0] == "#":
                linea = f.readline()
                continue
            if linea[0] == "[":
                # empieza nivel
                nombreNivel = linea.strip("[]\n")
                nuevoNivel = Nivel(nombreNivel)
                self.listaExploraciones.append(nuevoNivel)
                linea = f.readline()
                continue
            if linea.find("=") == -1:
                linea = f.readline()
                continue         
            [var,valor] = linea.strip().split("=")
            if var.startswith("dibujoInicial"):
                listaDibujos = valor.split(",")
                for i in listaDibujos:
                    nuevoNivel.dibujoInicial.append(i.strip())
            elif var.startswith("nombreInicial"):
                listaNombres = valor.split(",")
                for i in listaNombres:
                    nuevoNivel.nombreInicial.append(i.strip())
            elif var.startswith("elementosActivos"):
                listaNombres = valor.split(",")
                for i in listaNombres:
                    nuevoNivel.elementosActivos.append(i.strip())
            linea = f.readline()
        f.close()
        self.numeroExploraciones = len(self.listaExploraciones)

    def pantallaAcercaDe(self):
        """Pantalla con los datos del juego, creditos, etc"""
        global scale, shift_x, shift_y, xo_resolution
        self.pantallaTemp = pygame.Surface((self.anchoPantalla,self.altoPantalla))
        self.pantallaTemp.blit(self.pantalla,(0,0))
        self.pantalla.fill((0,0,0))
        self.pantalla.blit(self.terron,
                           (int(20*scale+shift_x),
                            int(20*scale+shift_y)))
        self.mostrarTexto(_("I know about Peru"),
                          self.fuente40,
                          (int(600*scale+shift_x),int(100*scale+shift_y)),
                          (255,255,255))
        # falta sanitizar acceso a archivo
        f = open(os.path.join(CAMINODATOS,ARCHIVOCREDITOS),"r")
        yLinea = int(200*scale+shift_y)
        for linea in f:
            self.mostrarTexto(linea.strip(),
                              self.fuente32,
                              (int(600*scale+shift_x),yLinea),
                              (155,155,255))
            yLinea = yLinea + int(40*scale)
        f.close()
        self.mostrarTexto(_("Press any key to return"),
                          self.fuente32,
                          (int(600*scale+shift_x),int(800*scale+shift_y)),
                          (255,155,155))
	pygame.display.flip()
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    self.click.play()
                    self.pantalla.blit(self.pantallaTemp,(0,0))
                    pygame.display.flip()
                    return
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()

    def pantallaInicial(self):
        global scale, shift_x, shift_y
        """Pantalla con el menu principal."""
        self.pantalla.fill((0,0,0))
        self.mostrarTexto(_("I know Peru"),
                          self.fuente40,
                          (int(600*scale+shift_x),int(100*scale+shift_y)),
                          (255,255,255))
        self.mostrarTexto(_("Game"),
                          self.fuente40,
                          (int(300*scale+shift_x),int(200*scale+shift_y)),
                          (200,100,100))
        yLista = int(300*scale+shift_y)
        for n in self.listaNiveles:
            self.pantalla.fill((20,20,20),
                               (int(10*scale+shift_x),yLista-int(24*scale),
                                int(590*scale),int(48*scale)))
            self.mostrarTexto(n.nombre,
                              self.fuente40,
                              (int(300*scale+shift_x),yLista),
                              (200,100,100))
            yLista += int(50*scale)
        self.mostrarTexto(_("Explore"),
                          self.fuente40,
                          (int(900*scale+shift_x),int(200*scale+shift_y)),
                          (100,100,200))
        yLista = int(300*scale+shift_y)
        for n in self.listaExploraciones:
            self.pantalla.fill((20,20,20),
                               (int(610*scale+shift_x),yLista-int(24*scale),
                                int(590*scale),int(48*scale)))
            self.mostrarTexto(n.nombre,
                              self.fuente40,
                              (int(900*scale+shift_x),yLista),
                              (100,100,200))
            yLista += int(50*scale)
        self.pantalla.fill((20,20,20),
                           (int(10*scale+shift_x),int(801*scale+shift_y),
                            int(590*scale),int(48*scale)))
        self.mostrarTexto(_("About this game"),
                          self.fuente40,
                          (int(300*scale+shift_x),int(825*scale+shift_y)),
                          (100,200,100))
        self.pantalla.fill((20,20,20),
                           (int(610*scale+shift_x),int(801*scale+shift_y),
                            int(590*scale),int(48*scale)))
        self.mostrarTexto(_("Leave"),
                          self.fuente40,
                          (int(900*scale+shift_x),int(825*scale+shift_y)),
                          (100,200,100))
        pygame.display.flip()
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27: # escape
                        self.click.play()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click.play()
                    pos = event.pos
                    if pos[1] > 275*scale+shift_y:
                        if pos[0] < 600*scale+shift_x:
                            if pos[1] < 275*scale+shift_y+len(self.listaNiveles)*50*scale:
                                self.indiceNivelActual = int((pos[1]-int(275*scale+shift_y))//int(50*scale))
                                self.jugar = True
                                return
                            elif pos[1] > 800*scale+shift_y and pos[1] < 850*scale+shift_y:
                                self.pantallaAcercaDe()
                        else:
                            if pos[1] < 275*scale+shift_y+len(self.listaExploraciones)*50*scale:
                                self.indiceNivelActual = int((pos[1]-int(275*scale+shift_y))//int(50*scale))
                                self.jugar = False
                                return
                            elif pos[1] > 800*scale+shift_y and pos[1] < 850*scale+shift_y:
                                sys.exit()
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()

    def cargarImagen(self,nombre):
        global scale, xo_resolution
        if xo_resolution:
            imagen = pygame.image.load( \
                os.path.join(CAMINOIMAGENES,nombre))
        else:
            imagen0 = pygame.image.load( \
                os.path.join(CAMINOIMAGENES,nombre))
            imagen = pygame.transform.scale(imagen0,
                          (int(imagen0.get_width()*scale),
                           int(imagen0.get_height()*scale)))
            del imagen0
        return imagen

    def __init__(self):
        """Esta es la inicializacion del juego"""
        pygame.init()
        # crear pantalla
        self.anchoPantalla = gtk.gdk.screen_width()
        self.altoPantalla = gtk.gdk.screen_height()
        self.pantalla = pygame.display.set_mode((self.anchoPantalla,
                                                 self.altoPantalla))
        global scale, shift_x, shift_y, xo_resolution
        if self.anchoPantalla==1200 and self.altoPantalla==900:
            xo_resolution = True
            scale = 1
            shift_x = 0
            shift_y = 0
        else:
            xo_resolution = False
            if self.anchoPantalla/1200.0<self.altoPantalla/900.0:
                scale = self.anchoPantalla/1200.0
                shift_x = 0
                shift_y = int((self.altoPantalla-scale*900)/2)
            else:
                scale = self.altoPantalla/900.0
                shift_x = int((self.anchoPantalla-scale*1200)/2)
                shift_y = 0
        # cargar imagenes generales
        self.bicho = self.cargarImagen("bicho.png")
        self.globito = self.cargarImagen("globito.png")
        self.nave = list()
        self.nave.append(self.cargarImagen("nave1.png"))
        self.nave.append(self.cargarImagen("nave2.png"))
        self.nave.append(self.cargarImagen("nave3.png"))
        self.nave.append(self.cargarImagen("nave4.png"))
        self.nave.append(self.cargarImagen("nave5.png"))
        self.nave.append(self.cargarImagen("nave6.png"))
        self.nave.append(self.cargarImagen("nave7.png"))
        self.fuego = list()
        self.fuego.append(self.cargarImagen("fuego1.png"))
        self.fuego.append(self.cargarImagen("fuego2.png"))
        self.tierra = self.cargarImagen("tierra.png")
        self.navellegando = self.cargarImagen("navellegando.png")
        self.bichotriste = self.cargarImagen("bichotriste.png")
        self.alerta = self.cargarImagen("alerta.png")
        self.alertarojo = self.cargarImagen("alertarojo.png")
        self.pedazo1 = self.cargarImagen("pedazo1.png")
        self.pedazo2 = self.cargarImagen("pedazo2.png")
        self.paracaidas = self.cargarImagen("paracaidas.png")
        self.terron = self.cargarImagen("terron.png")
        # cargar sonidos
        self.despegue = pygame.mixer.Sound(os.path.join(\
                CAMINOSONIDOS,"NoiseCollector_boom2.ogg"))
        self.click = pygame.mixer.Sound(os.path.join(\
                CAMINOSONIDOS,"junggle_btn045.wav"))
        self.click.set_volume(0.2)
        self.chirp = pygame.mixer.Sound(os.path.join(\
                CAMINOSONIDOS,"chirp_alerta.ogg"))
        # cargar fuentes
        self.fuente40 = pygame.font.Font(None, int(40*scale))
        self.fuente32 = pygame.font.Font(None, int(32*scale))
        self.fuente24 = pygame.font.Font(None, int(24*scale))
        # cursor
        datos_cursor = (
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  ",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ",
            "XXX.........................XXXX",
            "XXX..........................XXX",
            "XXX..........................XXX",
            "XXX.........................XXXX",
            "XXX.......XXXXXXXXXXXXXXXXXXXXX ",
            "XXX........XXXXXXXXXXXXXXXXXXX  ",
            "XXX.........XXX                 ",
            "XXX..........XXX                ",
            "XXX...........XXX               ",
            "XXX....X.......XXX              ",
            "XXX....XX.......XXX             ",
            "XXX....XXX.......XXX            ",
            "XXX....XXXX.......XXX           ",
            "XXX....XXXXX.......XXX          ",
            "XXX....XXXXXX.......XXX         ",
            "XXX....XXX XXX.......XXX        ",
            "XXX....XXX  XXX.......XXX       ",
            "XXX....XXX   XXX.......XXX      ",
            "XXX....XXX    XXX.......XXX     ",
            "XXX....XXX     XXX.......XXX    ",
            "XXX....XXX      XXX.......XXX   ",
            "XXX....XXX       XXX.......XXX  ",
            "XXX....XXX        XXX.......XXX ",
            "XXX....XXX         XXX.......XXX",
            "XXX....XXX          XXX......XXX",
            "XXX....XXX           XXX.....XXX",
            "XXX....XXX            XXX....XXX",
            "XXXX..XXXX             XXXXXXXX ",
            " XXXXXXX                XXXXXX  ",
            "  XXXXX                  XXXX   ")
        cursor= pygame.cursors.compile(datos_cursor)
        pygame.mouse.set_cursor((32,32),(1,1),*cursor)
        #
        # cargar imagenes especificas
        self.fondo = self.cargarImagen("fondo.png")
        # cargar datos especificos
        self.cargarDepartamentos()
        self.cargarRios()
        self.cargarCuchillas()
        self.cargarLugares()
        self.cargarNiveles()
        self.cargarExploraciones()

    def mostrarTodo(self):
        """Muestra todos los nombres, solo de prueba."""
        for d in self.listaDeptos:
            d.mostrarNombre(self.pantalla,self.fuente32,
                            COLORNOMBREDEPTO,False)
        for l in self.listaLugares:
            l.dibujar(self.pantalla,False)
            l.mostrarNombre(self.pantalla,self.fuente24,
                            COLORNOMBRECAPITAL,False)
        pygame.display.flip()
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27: # escape
                        sys.exit()

    def descubrirNombres(self):
        """Este es un jueguito point-and-click, solo de prueba."""
        self.pantalla.blit(self.deptosLineas, (shift_x, shift_y))
        for l in self.listaLugares:
            l.dibujar(self.pantalla,False)
        pygame.display.flip()
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27: # escape
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click.play()
                    encontro = False
                    for l in self.listaLugares:
                        if l.estaAca(event.pos):
                            l.mostrarNombre(self.pantalla,self.fuente24,
                                            COLORNOMBRECAPITAL,True)
                            encontro = True
                            break
                    if not encontro:
                        for d in self.listaDeptos:
                            if d.estaAca(event.pos):
                                d.mostrarNombre(self.pantalla,self.fuente32,
                                                COLORNOMBREDEPTO,True)
                                break

    def mostrarGlobito(self,lineas):
        """Muestra texto en el globito"""
        global scale, shift_x, shift_y
        self.pantalla.blit(self.globito,
                           (int(XMAPAMAX*scale+shift_x),
                            int(YGLOBITO*scale+shift_y)))
        yLinea = int(YGLOBITO*scale)+shift_y+self.fuente32.get_height()*3
        for l in lineas:
            text = self.fuente32.render(l, 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(XCENTROPANEL*scale+shift_x),yLinea)
            self.pantalla.blit(text, textrect)
            yLinea = yLinea + self.fuente32.get_height()+int(10*scale)
	pygame.display.flip()

    def borrarGlobito(self):
        """ Borra el globito, lo deja en blanco"""
        global scale, shift_x, shift_y
        self.pantalla.blit(self.globito,
                           (int(XMAPAMAX*scale+shift_x),
                            int(YGLOBITO*scale+shift_y)))

    def correcto(self):
        """Muestra el texto en el globito cuando la respuesta es correcta"""
        global scale, shift_x, shift_y
        self.pantalla.blit(self.nave[self.avanceNivel],
                           (int(XNAVE*scale+shift_x),
                            int(YNAVE*scale+shift_y)))
        self.correctoActual = random.randint(1,self.numeroCorrecto)-1
        self.mostrarGlobito([self.listaCorrecto[self.correctoActual]])
        self.esCorrecto = True
        pygame.time.set_timer(EVENTORESPUESTA,TIEMPORESPUESTA)
        
    def mal(self):
        """Muestra el texto en el globito cuando la respuesta es incorrecta"""
        self.malActual = random.randint(1,self.numeroMal)-1
        self.mostrarGlobito([self.listaMal[self.malActual]])
        self.esCorrecto = False
        self.nRespuestasMal += 1
        pygame.time.set_timer(EVENTORESPUESTA,TIEMPORESPUESTA)

    def esCorrecta(self,nivel,pos):
        """Devuelve True si las coordenadas cliqueadas corresponden a la
        respuesta correcta
        """
        respCorrecta = nivel.preguntaActual[2]
        # primero averiguar tipo
        if nivel.preguntaActual[1] == 1: # DEPTO
            # buscar depto correcto
            encontrado = False
            for d in self.listaDeptos:
                if d.nombre.startswith(respCorrecta):
                    encontrado = True
                    break
            if not encontrado:
                print "Error: no se encontro respuesta depto "+respCorrecta
                return False
            if d.estaAca(pos):
                d.mostrarNombre(self.pantalla,
                                self.fuente32,
                                COLORNOMBREDEPTO,
                                True)
                return True
            else:
                return False
        elif nivel.preguntaActual[1] == 2: #CAPITAL o CIUDAD
            # buscar lugar correcto
            encontrado = False
            for l in self.listaLugares:
                if l.nombre.startswith(respCorrecta):
                    encontrado = True
                    break
            if not encontrado:
                print "Error: no se encontro respuesta ciudad "+respCorrecta
                return False
            if l.estaAca(pos):
                l.mostrarNombre(self.pantalla,
                                self.fuente24,
                                COLORNOMBRECAPITAL,
                                True)
                return True
            else:
                return False
        if nivel.preguntaActual[1] == 3: # RIO
            # buscar rio correcto
            encontrado = False
            for d in self.listaRios:
                if d.nombre.startswith(respCorrecta):
                    encontrado = True
                    break
            if not encontrado:
                print "Error: no se encontro respuesta rio "+respCorrecta
                return False
            if d.estaAca(pos):
                d.mostrarNombre(self.pantalla,
                                self.fuente24,
                                COLORNOMBRERIO,
                                True)
                return True
            else:
                return False
        if nivel.preguntaActual[1] == 4: # CUCHILLA
            # buscar cuchilla correcta
            encontrado = False
            for d in self.listaCuchillas:
                if d.nombre.startswith(respCorrecta):
                    encontrado = True
                    break
            if not encontrado:
                print "Error: no se encontro respuesta cuchilla "+respCorrecta
                return False
            if d.estaAca(pos):
                d.mostrarNombre(self.pantalla,
                                self.fuente24,
                                COLORNOMBREELEVACION,
                                True)
                return True
            else:
                return False
        elif nivel.preguntaActual[1] == 5: # CERRO
            # buscar lugar correcto
            encontrado = False
            for l in self.listaLugares:
                if l.nombre.startswith(respCorrecta):
                    encontrado = True
                    break
            if not encontrado:
                print "Error: no se encontro respuesta cerro "+respCorrecta
                return False
            if l.estaAca(pos):
                l.mostrarNombre(self.pantalla,
                                self.fuente24,
                                COLORNOMBREELEVACION,
                                True)
                return True
            else:
                return False

    def explorarNombres(self):
        """Juego principal en modo exploro."""
        self.nivelActual = self.listaExploraciones[self.indiceNivelActual]
        # presentar nivel
        for i in self.nivelActual.dibujoInicial:
            if i.startswith("lineasDepto"):
                self.pantalla.blit(self.deptosLineas, (shift_x, shift_y))
            elif i.startswith("rios"):
                self.pantalla.blit(self.rios, (shift_x, shift_y))
            elif i.startswith("cuchillas"):
                self.pantalla.blit(self.cuchillas, (shift_x, shift_y))
            elif i.startswith("capitales"):
                for l in self.listaLugares:
                    if l.tipo == 1:
                        l.dibujar(self.pantalla,False)
            elif i.startswith("ciudades"):
                for l in self.listaLugares:
                    if l.tipo == 2:
                        l.dibujar(self.pantalla,False)
            elif i.startswith("cerros"):
                for l in self.listaLugares:
                    if l.tipo == 5:
                        l.dibujar(self.pantalla,False)
        for i in self.nivelActual.nombreInicial:
            if i.startswith("deptos"):
                for d in self.listaDeptos:
                    d.mostrarNombre(self.pantalla,self.fuente32,
                                    COLORNOMBREDEPTO,False)
            elif i.startswith("rios"):
                for d in self.listaRios:
                    d.mostrarNombre(self.pantalla,self.fuente32,
                                    COLORNOMBRERIO,False)
            elif i.startswith("cuchillas"):
                for d in self.listaCuchillas:
                    d.mostrarNombre(self.pantalla,self.fuente32,
                                    COLORNOMBREELEVACION,False)
            elif i.startswith("capitales"):
                for l in self.listaLugares:
                    if l.tipo == 1:
                        l.mostrarNombre(self.pantalla,self.fuente24,
                                        COLORNOMBRECAPITAL,False)
            elif i.startswith("ciudades"):
                for l in self.listaLugares:
                    if l.tipo == 2:
                        l.mostrarNombre(self.pantalla,self.fuente24,
                                        COLORNOMBRECAPITAL,False)
            elif i.startswith("cerros"):
                for l in self.listaLugares:
                    if l.tipo == 5:
                        l.mostrarNombre(self.pantalla,self.fuente24,
                                        COLORNOMBREELEVACION,False)
        self.pantalla.fill((100,20,20),(int(975*scale+shift_x),
                                        int(26*scale+shift_y),
                                        int(200*scale),
                                        int(48*scale)))
        self.mostrarTexto(_("End"),
                          self.fuente40,
                          (int(1075*scale+shift_x),
                           int(50*scale+shift_y)),
                          (255,155,155))
        pygame.display.flip()
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27: # escape
                        self.click.play()
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click.play()
                    if event.pos[0] < XMAPAMAX*scale+shift_x:
                        for i in self.nivelActual.elementosActivos:
                            if i.startswith("capitales"):
                                for l in self.listaLugares:
                                    if l.tipo == 1 and l.estaAca(event.pos):
                                        l.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBRECAPITAL,
                                                        True)
                                        break
                            elif i.startswith("ciudades"):
                                for l in self.listaLugares:
                                    if l.tipo == 2 and l.estaAca(event.pos):
                                        l.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBRECAPITAL,
                                                        True)
                                        break
                            elif i.startswith("rios"):
                                for d in self.listaRios:
                                    if d.estaAca(event.pos):
                                        d.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBRERIO,
                                                        True)
                                        break
                            elif i.startswith("cuchillas"):
                                for d in self.listaCuchillas:
                                    if d.estaAca(event.pos):
                                        d.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBREELEVACION,
                                                        True)
                                        break
                            elif i.startswith("cerros"):
                                for l in self.listaLugares:
                                    if l.tipo == 5 and l.estaAca(event.pos):
                                        l.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBREELEVACION,
                                                        True)
                                        break
                            elif i.startswith("deptos"):
                                for d in self.listaDeptos:
                                    if d.estaAca(event.pos):
                                        d.mostrarNombre(self.pantalla,
                                                        self.fuente32,
                                                        COLORNOMBREDEPTO,
                                                        True)
                                        break
                    elif event.pos[0] > 975*scale+shift_x and \
                            event.pos[0] < 1175*scale+shift_x and \
                            event.pos[1] > 25*scale+shift_y and \
                            event.pos[1] < 75*scale+shift_y:
                        return
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()


    def jugarNivel(self):
        """Juego principal de preguntas y respuestas"""
        self.nivelActual = self.listaNiveles[self.indiceNivelActual]
        self.avanceNivel = 0
        self.nivelActual.prepararPreguntas()
        # presentar nivel
        for i in self.nivelActual.dibujoInicial:
            if i.startswith("lineasDepto"):
                self.pantalla.blit(self.deptosLineas, (shift_x, shift_y))
            elif i.startswith("rios"):
                self.pantalla.blit(self.rios, (shift_x, shift_y))
            elif i.startswith("cuchillas"):
                self.pantalla.blit(self.cuchillas, (shift_x, shift_y))
            elif i.startswith("capitales"):
                for l in self.listaLugares:
                    if l.tipo == 1:
                        l.dibujar(self.pantalla,False)
            elif i.startswith("ciudades"):
                for l in self.listaLugares:
                    if l.tipo == 2:
                        l.dibujar(self.pantalla,False)
            elif i.startswith("cerros"):
                for l in self.listaLugares:
                    if l.tipo == 5:
                        l.dibujar(self.pantalla,False)
        for i in self.nivelActual.nombreInicial:
            if i.startswith("deptos"):
                for d in self.listaDeptos:
                    d.mostrarNombre(self.pantalla,self.fuente32,
                                    COLORNOMBREDEPTO,False)
            if i.startswith("rios"):
                for d in self.listaRios:
                    d.mostrarNombre(self.pantalla,self.fuente32,
                                    COLORNOMBRERIO,False)
            if i.startswith("cuchillas"):
                for d in self.listaCuchillas:
                    d.mostrarNombre(self.pantalla,self.fuente32,
                                    COLORNOMBREELEVACION,False)
            elif i.startswith("capitales"):
                for l in self.listaLugares:
                    if l.tipo == 1:
                        l.mostrarNombre(self.pantalla,self.fuente24,
                                        COLORNOMBRECAPITAL,False)
            elif i.startswith("ciudades"):
                for l in self.listaLugares:
                    if l.tipo == 2:
                        l.mostrarNombre(self.pantalla,self.fuente24,
                                        COLORNOMBRECAPITAL,False)
            elif i.startswith("cerros"):
                for l in self.listaLugares:
                    if l.tipo == 5:
                        l.mostrarNombre(self.pantalla,self.fuente24,
                                        COLORNOMBREELEVACION,False)
        self.pantalla.fill((100,20,20),
                           (int(975*scale+shift_x),
                            int(26*scale+shift_y),
                            int(200*scale),
                            int(48*scale)))
        self.mostrarTexto("Terminar",
                          self.fuente40,
                          (int(1075*scale+shift_x),
                           int(50*scale+shift_y)),
                          (255,155,155))
        pygame.display.flip()
        # presentar pregunta
        self.lineasPregunta = self.nivelActual.siguientePregunta(\
                self.listaSufijos,self.listaPrefijos)
        self.mostrarGlobito(self.lineasPregunta)
        self.nRespuestasMal = 0
        # leer eventos y ver si la respuesta es correcta
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27: # escape
                        self.click.play()
                        pygame.time.set_timer(EVENTORESPUESTA,0)
                        pygame.time.set_timer(EVENTODESPEGUE,0)
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click.play()
                    if self.avanceNivel < TOTALAVANCE:
                        if event.pos[0] < XMAPAMAX*scale+shift_x:
                            self.borrarGlobito()
                            if self.esCorrecta(self.nivelActual,
                                               event.pos):
                                self.correcto()
                            else:
                                self.mal()
                        elif event.pos[0] > 975*scale+shift_x and \
                                event.pos[0] < 1175*scale+shift_x and \
                                event.pos[1] > 25*scale+shift_y and \
                                event.pos[1] < 75*scale+shift_y:
                            return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    if self.esCorrecto:
                        self.avanceNivel = self.avanceNivel + 1
                        if self.avanceNivel == TOTALAVANCE:
                            self.lineasPregunta =  self.listaDespedidas[\
                                random.randint(1,self.numeroDespedidas)-1]\
                                .split("\\")
                            self.mostrarGlobito(self.lineasPregunta)
                            self.yNave = int(YNAVE*scale+shift_y)
                            self.fuego1 = True
                            pygame.time.set_timer(EVENTODESPEGUE,
                                                  TIEMPORESPUESTA*2)
                        else:
                            self.lineasPregunta = \
                                self.nivelActual.siguientePregunta(\
                                self.listaSufijos,self.listaPrefijos)
                            self.mostrarGlobito(self.lineasPregunta)
                            self.nRespuestasMal = 0
                    else:
                        if self.nRespuestasMal >= 2:
                            self.mostrarGlobito(self.nivelActual.devolverAyuda())
                            self.nRespuestasMal = 0
                            pygame.time.set_timer(EVENTORESPUESTA,TIEMPORESPUESTA)
                        else:
                            self.mostrarGlobito(self.lineasPregunta)
                elif event.type == EVENTODESPEGUE:
                    if self.yNave == int(YNAVE*scale+shift_y):
                        self.pantalla.fill(COLORPANEL,
                                           (int(XBICHO*scale+shift_x),
                                            int(YBICHO*scale+shift_y),
                                            int(DXBICHO*scale),
                                            int(DYBICHO*scale)))
                        self.pantalla.fill(COLORPANEL,
                                           (int(XMAPAMAX*scale+shift_x),0,
                                            int(DXPANEL*scale),
                                            int(900*scale)))
                        self.despegue.play()
                    self.pantalla.fill(COLORPANEL,
                                       (int(XNAVE*scale+shift_x),
                                        self.yNave,
                                        int(DXNAVE*scale),
                                        int((DYNAVE+30)*scale)))
                    self.yNave = self.yNave-8
                    if self.yNave<1:
                        pygame.time.set_timer(EVENTODESPEGUE,0)
                        return
                    else:
                        pygame.time.set_timer(EVENTODESPEGUE,TIEMPODESPEGUE)
                        self.pantalla.blit(self.nave[6],
                                           (int(XNAVE*scale+shift_x),
                                            self.yNave))
                        if self.fuego1:
                            self.pantalla.blit(self.fuego[0],
                                               (int((XNAVE+30)*scale+shift_x),
                                                self.yNave+int(DYNAVE*scale)))
                        else:
                            self.pantalla.blit(self.fuego[1],
                                               (int((XNAVE+30)*scale+shift_x),
                                                self.yNave+int(DYNAVE*scale)))
                        self.fuego1 = not self.fuego1
                        pygame.display.flip()
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()

    def presentacion(self):
        """Presenta una animacion inicial"""
        # falta sanitizar manejo de archivo
        self.listaPresentacion = list()
        r_path = os.path.join(CAMINODATOS,ARCHIVOPRESENTACION + '.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source(ARCHIVOPRESENTACION, a_path)
        except:
            print "Cannot open %s" % (ARCHIVOPRESENTACION,)

        if f:
            if hasattr(f, 'PRESENT_ACTIONS'):
                for action in f.PRESENT_ACTIONS:
                    self.listaPresentacion.append(unicode(action,'iso-8859-1'))

        # cuadro 1: nave llegando
        self.pantalla.blit(self.tierra,(int(200*scale+shift_x),
                                        int(150*scale+shift_y)))
        self.mostrarTexto(_("Press any key to skip"),
                          self.fuente32,
                          (int(600*scale+shift_x),int(800*scale+shift_y)),
                          (255,155,155))
	pygame.display.flip()
        pygame.time.set_timer(EVENTODESPEGUE,TIEMPODESPEGUE)
        self.despegue.play()
        self.paso = 0
        terminar = False
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    self.click.play()
                    pygame.time.set_timer(EVENTODESPEGUE,0)
                    return
                elif event.type == EVENTODESPEGUE:
                    self.paso += 1
                    if self.paso == 150:
                        pygame.time.set_timer(EVENTODESPEGUE,0)
                        terminar = True
                    else:
                        pygame.time.set_timer(EVENTODESPEGUE,TIEMPODESPEGUE)
                        self.pantalla.fill((0,0,0),
                                           (int((900-(self.paso-1)*3)*scale+shift_x),
                                            int((150+(self.paso-1)*1)*scale+shift_y),
                                            int(100*scale),int(63*scale)))
                        self.pantalla.blit(self.navellegando,
                                           (int((900-self.paso*3)*scale+shift_x),
                                            int((150+self.paso*1)*scale+shift_y)))
                        pygame.display.flip()
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break
        # cuadro 2: marcianito hablando
        self.pantalla.fill((0,0,0))
        self.pantalla.blit(self.bicho,(int(600*scale+shift_x),
                                       int(450*scale+shift_y)))
        self.pantalla.blit(self.globito,
                           (int(350*scale+shift_x),int(180*scale+shift_y)))
        yLinea = int((180+self.fuente32.get_height()*3)*scale+shift_y)
        lineas = self.listaPresentacion[0].split("\\")
        for l in lineas:
            text = self.fuente32.render(l.strip(), 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(557*scale+shift_x),yLinea)
            self.pantalla.blit(text, textrect)
            yLinea = yLinea + self.fuente32.get_height()+int(10*scale)
        self.mostrarTexto(_("Press any key to skip"),
                          self.fuente32,
                          (int(600*scale+shift_x),int(800*scale+shift_y)),
                          (255,155,155))
        pygame.display.flip()
        terminar = False
        pygame.time.set_timer(EVENTORESPUESTA,4000)
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    self.click.play()
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    terminar = True
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break
        # cuadro 3: alerta
        self.pantalla.fill((0,0,0))
        self.pantalla.blit(self.alerta,(int(264*scale+shift_x),
                                        int(215*scale+shift_y)))
        self.pantalla.blit(self.alertarojo,(int(459*scale+shift_x),
                                            int(297*scale+shift_y)))
        self.mostrarTexto(_("Press any key to skip"),
                          self.fuente32,
                          (int(600*scale+shift_x),int(800*scale+shift_y)),
                          (255,155,155))
        pygame.display.flip()
        self.chirp.play()
        pygame.time.set_timer(EVENTORESPUESTA,500)
        self.paso = 0
        terminar = False
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    self.click.play()
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    return
                elif event.type == EVENTORESPUESTA:
                    self.paso += 1
                    if self.paso == 10:
                        pygame.time.set_timer(EVENTORESPUESTA,0)
                        terminar = True
                    else:
                        pygame.time.set_timer(EVENTORESPUESTA,500)
                        if self.paso % 2 == 0:
                            self.pantalla.blit(self.alerta,
                                               (int(264*scale+shift_x),
                                                int(215*scale+shift_y)))
                            self.pantalla.blit(self.alertarojo,
                                               (int(459*scale+shift_x),
                                                int(297*scale+shift_y)))
                            self.chirp.play()
                        else:
                            self.pantalla.blit(self.alerta,
                                               (int(264*scale+shift_x),
                                                int(215*scale+shift_y)))
                        pygame.display.flip()
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break
        # cuadro 4: marcianito asustado
        self.pantalla.fill((0,0,0))
        self.pantalla.blit(self.bichotriste,(int(600*scale+shift_x),
                                             int(450*scale+shift_y)))
        self.pantalla.blit(self.globito,(int(350*scale+shift_x),
                                         int(180*scale+shift_y)))
        yLinea = int(180*scale+shift_y)+self.fuente32.get_height()*3
        lineas = self.listaPresentacion[1].split("\\")
        for l in lineas:
            text = self.fuente32.render(l.strip(), 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(557*scale+shift_x),yLinea)
            self.pantalla.blit(text, textrect)
            yLinea = yLinea + self.fuente32.get_height()+int(10*scale)
        self.mostrarTexto(_("Press any key to skip"),
                          self.fuente32,
                          (int(600*scale+shift_x),int(800*scale+shift_y)),
                          (255,155,155))
        pygame.display.flip()
        terminar = False
        pygame.time.set_timer(EVENTORESPUESTA,4000)
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    self.click.play()
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    terminar = True
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break
        # cuadro 5: explota nave
        self.pantalla.blit(self.tierra,(int(200*scale+shift_x),
                                        int(150*scale+shift_y)))
        self.mostrarTexto(_("Press any key to skip"),
                          self.fuente32,
                          (int(600*scale+shift_x),int(800*scale+shift_y)),
                          (255,155,155))
        pygame.display.flip()
        pygame.time.set_timer(EVENTODESPEGUE,TIEMPODESPEGUE)
        self.despegue.play()
        self.paso = 0
        terminar = False
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    self.click.play()
                    pygame.time.set_timer(EVENTODESPEGUE,0)
                    return
                elif event.type == EVENTODESPEGUE:
                    self.paso += 1
                    if self.paso == 130:
                        pygame.time.set_timer(EVENTODESPEGUE,0)
                        terminar = True
                    else:
                        pygame.time.set_timer(EVENTODESPEGUE,TIEMPODESPEGUE)
                        self.pantalla.fill((0,0,0),
                                           (int((430-(self.paso-1)*.1)*scale+shift_x),
                                            int((280+(self.paso-1)*.6)*scale+shift_y),
                                            int(30*scale),int(35*scale)))
                        self.pantalla.blit(self.pedazo1,
                                           (int((430-self.paso*.2)*scale+shift_x),
                                            int((290+self.paso*1)*scale+shift_y)))
                        self.pantalla.blit(self.pedazo1,
                                           (int((430+self.paso*.15)*scale+shift_x),
                                            int((290+self.paso*.9)*scale+shift_y)))
                        self.pantalla.blit(self.pedazo2,
                                           (int((430+self.paso*.25)*scale+shift_x),
                                            int((290+self.paso*.75)*scale+shift_y)))
                        self.pantalla.blit(self.pedazo2,
                                           (int((430-self.paso*.15)*scale+shift_x),
                                            int((290+self.paso*.8)*scale+shift_y)))
                        self.pantalla.blit(self.paracaidas,
                                           (int((430-self.paso*.1)*scale+shift_x),
                                            int((280+self.paso*.6)*scale+shift_y)))
                        pygame.display.flip()
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break
        # cuadro 6: marcianito hablando
        self.pantalla.fill((0,0,0))
        self.pantalla.blit(self.bicho,(int(600*scale+shift_x),
                                       int(450*scale+shift_y)))
        self.pantalla.blit(self.globito,(int(350*scale+shift_x),
                                         int(180*scale+shift_y)))
        yLinea = int(180*scale+shift_y)+self.fuente32.get_height()*3
        lineas = self.listaPresentacion[2].split("\\")
        for l in lineas:
            text = self.fuente32.render(l.strip(), 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(557*scale+shift_x),yLinea)
            self.pantalla.blit(text, textrect)
            yLinea = yLinea + self.fuente32.get_height()+int(10*scale)
        self.mostrarTexto(_("Press any key to skip"),
                          self.fuente32,
                          (int(600*scale+shift_x),int(800*scale+shift_y)),
                          (255,155,155))
        pygame.display.flip()
        terminar = False
        pygame.time.set_timer(EVENTORESPUESTA,6000)
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    self.click.play()
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    terminar = True
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break
        return

    def principal(self):
        """Este es el loop principal del juego"""
        global scale, shift_x, shift_y
        pygame.time.set_timer(EVENTOREFRESCO,TIEMPOREFRESCO)
        self.presentacion()
        while 1:
            # pantalla inicial
            self.pantallaInicial()
            # dibujar fondo y panel
            self.pantalla.blit(self.fondo, (shift_x, shift_y))
            self.pantalla.fill(COLORPANEL,
                               (int(XMAPAMAX*scale+shift_x),shift_y,
                                int(DXPANEL*scale),int(900*scale)))
            if self.jugar:
                self.pantalla.blit(self.bicho,
                                   (int(XBICHO*scale+shift_x),
                                    int(YBICHO*scale+shift_y)))
            # mostrar pantalla
            pygame.display.flip()
            # ir al juego
            if self.jugar:
                self.jugarNivel()
            else:
                self.explorarNombres()


def main():
    juego = ConozcoUy()
    juego.principal()
#    juego.mostrarTodo()

if __name__ == "__main__":
    main()
