import psutil
import tkinter as tk
from tkinter import ttk
import platform
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches

class DiscoInfo:
    def __init__(self):
        # Configuración de la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Kiwi Diks")
        self.ventana.configure(bg='#2C3E50')
        self.ventana.geometry("1200x900")
        
        # Estilo para los widgets
        style = ttk.Style()
        style.configure('TFrame', background='#2C3E50')
        style.configure('TButton', padding=8, relief="flat", background="#3498DB",
                       font=('Arial', 10, 'bold'))
        style.configure('TLabel', background='#2C3E50', foreground='white',
                       font=('Arial', 10))
        style.configure('Disco.TFrame', background='#34495E', relief='raised')
        
        # Frame principal
        self.frame_principal = ttk.Frame(self.ventana)
        self.frame_principal.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Frame superior para título
        self.frame_titulo = ttk.Frame(self.frame_principal)
        self.frame_titulo.pack(fill='x', pady=(0, 30))
        
        titulo = ttk.Label(self.frame_titulo, text="Kiwi Disk - Monitor de Disco",
                          font=('Arial', 32, 'bold'), foreground='#ECF0F1')
        titulo.pack()
        
        # Frame contenedor
        self.frame_contenedor = ttk.Frame(self.frame_principal)
        self.frame_contenedor.pack(expand=True, fill='both')
        
        # Frame izquierdo para información
        self.frame_izq = ttk.Frame(self.frame_contenedor)
        self.frame_izq.pack(side='left', expand=True, fill='both', padx=(0, 20))
        
        # Canvas con scrollbar para los frames de disco
        self.canvas = tk.Canvas(self.frame_izq, bg='#2C3E50', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame_izq, orient="vertical", command=self.canvas.yview)
        self.frame_discos = ttk.Frame(self.canvas, style='TFrame')
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Frame derecho para gráficos
        self.frame_der = ttk.Frame(self.frame_contenedor)
        self.frame_der.pack(side='right', expand=True, fill='both')
        
        # Configuración del gráfico
        self.fig = plt.figure(figsize=(10, 10))
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.frame_der)
        self.canvas_plot.get_tk_widget().pack(expand=True, fill='both')
        
        # Frame inferior para botones
        self.frame_botones = ttk.Frame(self.frame_principal)
        self.frame_botones.pack(fill='x', pady=(30, 0))
        
        # Botón de actualizar
        self.btn_actualizar = ttk.Button(self.frame_botones,
                                       text="Actualizar Información",
                                       command=self.mostrar_info)
        self.btn_actualizar.pack(pady=10)
        
        # Configurar el canvas para el scrolling
        self.canvas.create_window((0, 0), window=self.frame_discos, anchor="nw")
        self.frame_discos.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        
        # Mostrar información inicial
        self.mostrar_info()
    
    def crear_frame_disco(self, particion, uso):
        frame_disco = ttk.Frame(self.frame_discos, style='Disco.TFrame')
        frame_disco.pack(fill='x', padx=10, pady=5, ipadx=10, ipady=10)
        
        # Título del disco
        ttk.Label(frame_disco, 
                 text=f"Disco: {particion.device}",
                 font=('Arial', 12, 'bold'),
                 foreground='#ECF0F1').pack(anchor='w', padx=10, pady=5)
        
        # Información del disco en grid
        info_frame = ttk.Frame(frame_disco)
        info_frame.pack(fill='x', padx=10)
        
        # Barra de progreso personalizada
        progreso_frame = ttk.Frame(frame_disco)
        progreso_frame.pack(fill='x', padx=10, pady=10)
        
        barra_total = ttk.Frame(progreso_frame, height=20)
        barra_total.pack(fill='x')
        barra_total.configure(style='TFrame')
        
        ancho_usado = uso.percent
        barra_usada = tk.Frame(barra_total, 
                              bg='#E74C3C', 
                              height=20,
                              width=ancho_usado)
        barra_usada.place(relwidth=uso.percent/100, rely=0, relheight=1)
        
        # Etiquetas de información
        labels = [
            ('Punto de montaje:', particion.mountpoint),
            ('Sistema de archivos:', particion.fstype),
            (f'Espacio total:', f'{self.bytes_a_gb(uso.total):.2f} GB'),
            (f'Espacio usado:', f'{self.bytes_a_gb(uso.used):.2f} GB'),
            (f'Espacio libre:', f'{self.bytes_a_gb(uso.free):.2f} GB'),
            (f'Porcentaje usado:', f'{uso.percent}%')
        ]
        
        for i, (label, valor) in enumerate(labels):
            ttk.Label(info_frame, 
                     text=label,
                     foreground='#BDC3C7').grid(row=i, column=0, sticky='w', pady=2)
            ttk.Label(info_frame,
                     text=valor,
                     foreground='#ECF0F1').grid(row=i, column=1, sticky='w', padx=10, pady=2)
    
    def bytes_a_gb(self, bytes):
        return bytes / (1024**3)
    
    def mostrar_info(self):
        # Limpiar frames anteriores
        for widget in self.frame_discos.winfo_children():
            widget.destroy()
            
        # Mostrar información del sistema operativo
        frame_so = ttk.Frame(self.frame_discos, style='Disco.TFrame')
        frame_so.pack(fill='x', padx=10, pady=5, ipadx=10, ipady=10)
        
        ttk.Label(frame_so,
                 text="Sistema Operativo",
                 font=('Arial', 12, 'bold'),
                 foreground='#ECF0F1').pack(anchor='w', padx=10, pady=5)
        
        ttk.Label(frame_so,
                 text=f"{platform.system()} {platform.version()}",
                 foreground='#ECF0F1').pack(anchor='w', padx=10)
        
        # Mostrar información de cada disco
        for particion in psutil.disk_partitions():
            try:
                if self.es_disco_valido(particion):
                    uso = psutil.disk_usage(particion.mountpoint)
                    self.crear_frame_disco(particion, uso)
            except:
                continue
                
        # Actualizar gráfico
        self.actualizar_grafico()
    
    def actualizar_grafico(self):
        self.fig.clear()
        self.fig.set_facecolor('#2C3E50')
        particiones = psutil.disk_partitions()
        num_discos = len([p for p in particiones if self.es_disco_valido(p)])
        
        filas = (num_discos + 1) // 2
        columnas = min(2, num_discos)
        
        pos = 1
        for particion in particiones:
            try:
                if not self.es_disco_valido(particion):
                    continue
                    
                uso = psutil.disk_usage(particion.mountpoint)
                ax = self.fig.add_subplot(filas, columnas, pos)
                ax.set_facecolor('#34495E')
                
                sizes = [uso.used, uso.free]
                labels = ['Usado', 'Libre']
                colors = ['#E74C3C', '#2ECC71']
                explode = (0.05, 0)
                
                wedges, texts, autotexts = ax.pie(sizes, explode=explode,
                                                 labels=labels, colors=colors,
                                                 autopct='%1.1f%%', shadow=True,
                                                 startangle=90)
                
                plt.setp(autotexts, size=9, weight="bold", color="white")
                plt.setp(texts, size=9, color="white")
                
                ax.set_title(f'Disco {particion.device}\n{self.bytes_a_gb(uso.total):.1f} GB',
                           pad=20, fontsize=11, fontweight='bold', color='white')
                pos += 1
            except:
                continue
        
        self.fig.tight_layout(pad=3.5)
        self.canvas_plot.draw()
    
    def es_disco_valido(self, particion):
        try:
            psutil.disk_usage(particion.mountpoint)
            return True
        except:
            return False
    
    def iniciar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = DiscoInfo()
    app.iniciar()
