import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import json
import os
import sys

# ==============================================================================
# CONFIGURACIÓN DE COLORES Y CONSTANTES ESTRATÉGICAS
# ==============================================================================
COLOR_BG = '#121214'          # Fondo principal ultra oscuro
COLOR_CARD = '#1e1e24'        # Fondo de paneles y tarjetas
COLOR_INPUT = '#2a2a32'       # Fondo de campos de entrada y listas
COLOR_TEXT_PRIMARY = '#ffffff'# Texto principal (blanco)
COLOR_TEXT_MUTED = '#a4b0be'  # Texto secundario (gris)
COLOR_ACCENT = '#ff4757'      # Rojo Pokéball
COLOR_ACCENT_HOVER = '#ff6b81'# Rojo claro para hover
COLOR_SECONDARY = '#feca57'   # Amarillo Eléctrico
COLOR_SECONDARY_HOVER = '#ffdd59' # Amarillo claro para hover
COLOR_SUCCESS = '#2ed573'     # Verde Éxito
COLOR_SUCCESS_HOVER = '#7bed9f' # Verde claro para hover
COLOR_BORDER = '#2f3542'      # Borde sutil

# Colores oficiales de los tipos de Pokémon para los badges
TYPE_COLORS = {
    'Normal': '#A8A878',
    'Fire': '#F08030',
    'Water': '#6890F0',
    'Electric': '#F8D030',
    'Grass': '#78C850',
    'Ice': '#98D8D8',
    'Fighting': '#C03028',
    'Poison': '#A040A0',
    'Ground': '#E0C068',
    'Flying': '#A890F0',
    'Psychic': '#F85888',
    'Bug': '#A8B820',
    'Rock': '#B8A038',
    'Ghost': '#705898',
    'Dragon': '#7038F8',
    'Dark': '#705848',
    'Steel': '#B8B8D0',
    'Fairy': '#EE99AC'
}

# ==============================================================================
# BACKEND C — Comunicación vía subprocess stdin/stdout JSON
# Toda la lógica reside en el binario C (pokehash_api).
# Python solo envía comandos y renderiza los resultados.
# ==============================================================================
class PokeHashBackend:
    def __init__(self):
        # Determinar ruta del binario
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if sys.platform == 'win32':
            binary = os.path.join(script_dir, 'pokehash_api.exe')
        else:
            binary = os.path.join(script_dir, 'pokehash_api')

        # Auto-compilar si no existe el binario
        if not os.path.exists(binary):
            print("[PokeHash] Compilando backend C...")
            try:
                subprocess.run(
                    ['gcc', '-Wall', '-Wextra', '-o', binary,
                     os.path.join(script_dir, 'pokehash_api.c'),
                     os.path.join(script_dir, 'pokehash.c'),
                     os.path.join(script_dir, 'tdas', 'extra.c'),
                     os.path.join(script_dir, 'tdas', 'list.c'),
                     os.path.join(script_dir, 'tdas', 'map.c')],
                    check=True, capture_output=True, text=True,
                    cwd=script_dir
                )
                print("[PokeHash] Backend compilado exitosamente.")
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Error al compilar backend C:\n{e.stderr}")

        # Lanzar el proceso C
        self.process = subprocess.Popen(
            [binary],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=script_dir
        )

    def send(self, cmd_dict):
        """Envía un comando JSON al backend C y retorna la respuesta parseada."""
        try:
            json_str = json.dumps(cmd_dict, ensure_ascii=False, separators=(',', ':'))
            self.process.stdin.write(json_str + '\n')
            self.process.stdin.flush()
            response_line = self.process.stdout.readline()
            if not response_line:
                return {"status": "error", "message": "El backend C se cerró inesperadamente."}
            return json.loads(response_line)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_all(self):
        return self.send({"cmd": "list_all"})

    def search_name(self, name):
        return self.send({"cmd": "search_name", "name": name})

    def search_id(self, pokemon_id):
        return self.send({"cmd": "search_id", "id": pokemon_id})

    def team_add(self, name):
        return self.send({"cmd": "team_add", "name": name})

    def team_undo(self):
        return self.send({"cmd": "team_undo"})

    def team_remove(self, index):
        return self.send({"cmd": "team_remove", "index": index})

    def team_view(self):
        return self.send({"cmd": "team_view"})

    def team_analyze(self):
        return self.send({"cmd": "team_analyze"})

    def team_export(self, path):
        return self.send({"cmd": "team_export", "path": path})

    def close(self):
        try:
            self.process.stdin.write('{"cmd":"quit"}\n')
            self.process.stdin.flush()
            self.process.wait(timeout=2)
        except Exception:
            self.process.kill()

# ==============================================================================
# WIDGET PERSONALIZADO: BARRA DE ESTADÍSTICAS RE-ESCALABLE
# ==============================================================================
class StatBar(tk.Canvas):
    def __init__(self, parent, value, max_value=255, color='#ff4757', **kwargs):
        super().__init__(parent, height=12, bg='#2a2a32', highlightthickness=0, bd=0, **kwargs)
        self.value = value
        self.max_value = max_value
        self.color = color
        self.bind("<Configure>", self.draw)
        
    def draw(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w > 10:
            fill_w = int((self.value / self.max_value) * w)
            # Dibujar fondo redondeado simulado
            self.create_rectangle(0, 0, w, h, fill='#2a2a32', outline="")
            self.create_rectangle(0, 0, fill_w, h, fill=self.color, outline="")

# ==============================================================================
# CLASE PRINCIPAL DE LA INTERFAZ GRÁFICA
# ==============================================================================
class PokeHashGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PokeHash - Gestor Táctico de Pokémon")
        self.root.geometry("1080x720")
        self.root.configure(bg=COLOR_BG)
        self.root.minsize(960, 640)
        
        # Inicializar backend C
        try:
            self.backend = PokeHashBackend()
        except RuntimeError as e:
            messagebox.showerror("Error de Backend", str(e))
            sys.exit(1)
        
        # Cargar datos desde el backend C
        result = self.backend.list_all()
        if result['status'] == 'ok':
            self.all_pokemon = result['data']
        else:
            messagebox.showerror("Error", f"No se pudieron cargar los datos:\n{result.get('message','')}")
            self.all_pokemon = []
        
        self.filtered_pokemon = list(self.all_pokemon)
        
        # Equipo Activo (cache local, fuente de verdad es el backend C)
        self.equipo = []
        
        # Configurar estilos generales
        self.setup_styles()
        
        # Crear componentes
        self.create_widgets()
        
        # Seleccionar primer Pokémon por defecto
        if self.filtered_pokemon:
            self.pokedex_listbox.selection_set(0)
            self.on_select_pokemon()
        
        # Cerrar backend al cerrar ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.backend.close()
        self.root.destroy()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        
        # Configuración de estilos ttk
        style.configure('TFrame', background=COLOR_BG)
        style.configure('Card.TFrame', background=COLOR_CARD, borderwidth=0)
        
        # Scrollbar estilizada
        style.configure("Vertical.TScrollbar", gripcount=0, background=COLOR_CARD, 
                        troughcolor=COLOR_BG, bordercolor=COLOR_BORDER, arrowcolor=COLOR_TEXT_PRIMARY)
        
        # Combobox estilizada
        style.configure("TCombobox", fieldbackground=COLOR_INPUT, background=COLOR_CARD, 
                        foreground=COLOR_TEXT_PRIMARY, arrowcolor=COLOR_TEXT_PRIMARY)
        
    def create_widgets(self):
        # ----------------------------------------------------------------------
        # CABECERA PRINCIPAL (HEADER)
        # ----------------------------------------------------------------------
        header_frame = tk.Frame(self.root, bg=COLOR_CARD, height=60, bd=0)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)
        
        # Logo simulado con texto Pokéball
        logo_label = tk.Label(header_frame, text="PokeHash", bg=COLOR_CARD, fg=COLOR_ACCENT,
                              font=('Helvetica', 18, 'bold'))
        logo_label.pack(side='left', padx=(20, 5))
        
        subtitle_label = tk.Label(header_frame, text="•  Gestor Táctico de Pokémon", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                                  font=('Helvetica', 11, 'italic'))
        subtitle_label.pack(side='left', padx=5, pady=(4, 0))
        
        # Indicador de backend
        backend_lbl = tk.Label(header_frame, text="⚡ Backend C Activo", bg=COLOR_CARD, fg=COLOR_SUCCESS,
                               font=('Helvetica', 9, 'bold'))
        backend_lbl.pack(side='right', padx=20)
        
        # ----------------------------------------------------------------------
        # MENÚ DE PESTAÑAS PERSONALIZADO (TABS)
        # ----------------------------------------------------------------------
        self.tabs_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.tabs_frame.pack(fill='x', side='top', pady=(10, 0), padx=20)
        
        self.tab_pokedex_btn = tk.Button(self.tabs_frame, text="Explorar Pokédex", bg=COLOR_ACCENT, fg=COLOR_TEXT_PRIMARY,
                                         font=('Helvetica', 11, 'bold'), bd=0, activebackground=COLOR_ACCENT_HOVER,
                                         activeforeground=COLOR_TEXT_PRIMARY, height=2, width=18, command=self.show_pokedex_tab)
        self.tab_pokedex_btn.pack(side='left', padx=(0, 5))
        
        self.tab_team_btn = tk.Button(self.tabs_frame, text="Mi Equipo y Análisis", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                                      font=('Helvetica', 11, 'bold'), bd=0, activebackground=COLOR_CARD,
                                      activeforeground=COLOR_TEXT_PRIMARY, height=2, width=18, command=self.show_team_tab)
        self.tab_team_btn.pack(side='left')
        
        # Línea de separación estética
        sep = tk.Frame(self.root, bg=COLOR_BORDER, height=2)
        sep.pack(fill='x', side='top', padx=20)
        
        # ----------------------------------------------------------------------
        # CONTENEDOR PRINCIPAL DE PANELES
        # ----------------------------------------------------------------------
        self.content_container = tk.Frame(self.root, bg=COLOR_BG)
        self.content_container.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Instanciar pestañas
        self.create_pokedex_tab()
        self.create_team_tab()
        
        # Mostrar pestaña por defecto
        self.show_pokedex_tab()

    # ==============================================================================
    # CONTROL DE NAVEGACIÓN ENTRE PESTAÑAS
    # ==============================================================================
    def show_pokedex_tab(self):
        self.tab_pokedex_btn.config(bg=COLOR_ACCENT, fg=COLOR_TEXT_PRIMARY)
        self.tab_team_btn.config(bg=COLOR_CARD, fg=COLOR_TEXT_MUTED)
        self.team_frame.pack_forget()
        self.pokedex_frame.pack(fill='both', expand=True)
        
    def show_team_tab(self):
        self.tab_pokedex_btn.config(bg=COLOR_CARD, fg=COLOR_TEXT_MUTED)
        self.tab_team_btn.config(bg=COLOR_ACCENT, fg=COLOR_TEXT_PRIMARY)
        self.pokedex_frame.pack_forget()
        self.team_frame.pack(fill='both', expand=True)
        self.refresh_team_from_backend()
        self.update_team_tab_view()

    # ==============================================================================
    # PESTAÑA 1: EXPLORAR POKÉDEX
    # ==============================================================================
    def create_pokedex_tab(self):
        self.pokedex_frame = tk.Frame(self.content_container, bg=COLOR_BG)
        
        # 1. BARRA LATERAL IZQUIERDA: BUSCADOR Y LISTA (1/3 del ancho)
        left_panel = tk.Frame(self.pokedex_frame, bg=COLOR_CARD, width=320, bd=0)
        left_panel.pack(side='left', fill='both', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Buscador input
        search_title = tk.Label(left_panel, text="Buscar Pokémon", bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY,
                                font=('Helvetica', 12, 'bold'), anchor='w')
        search_title.pack(fill='x', padx=15, pady=(15, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_pokemon())
        self.search_entry = tk.Entry(left_panel, textvariable=self.search_var, bg=COLOR_INPUT, fg=COLOR_TEXT_PRIMARY,
                                     insertbackground=COLOR_TEXT_PRIMARY, bd=0, font=('Helvetica', 11))
        self.search_entry.pack(fill='x', padx=15, pady=(0, 15), ipady=8)
        
        # Agregar placeholder simulado si está vacío
        self.search_entry.insert(0, "")
        
        # Filtros de Generación y Tipo
        filters_frame = tk.Frame(left_panel, bg=COLOR_CARD)
        filters_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Filtro de Tipo
        tipo_lbl = tk.Label(filters_frame, text="Tipo:", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=('Helvetica', 9, 'bold'))
        tipo_lbl.grid(row=0, column=0, sticky='w', pady=(0, 2))
        self.tipo_filter_var = tk.StringVar(value="Todos")
        tipos_disponibles = ["Todos"] + list(TYPE_COLORS.keys())
        self.tipo_combo = tk.OptionMenu(filters_frame, self.tipo_filter_var, *tipos_disponibles, command=self.filter_pokemon)
        self.tipo_combo.config(bg=COLOR_INPUT, fg=COLOR_TEXT_PRIMARY, activebackground=COLOR_CARD, activeforeground=COLOR_TEXT_PRIMARY, highlightthickness=0, bd=0, indicatoron=0)
        self.tipo_combo["menu"].config(bg=COLOR_INPUT, fg=COLOR_TEXT_PRIMARY, activebackground=COLOR_ACCENT, activeforeground=COLOR_TEXT_PRIMARY)
        self.tipo_combo.grid(row=1, column=0, sticky='we', padx=(0, 5))
        
        # Filtro de Generación
        gen_lbl = tk.Label(filters_frame, text="Generación:", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=('Helvetica', 9, 'bold'))
        gen_lbl.grid(row=0, column=1, sticky='w', pady=(0, 2))
        self.gen_filter_var = tk.StringVar(value="Todas")
        gens_disponibles = ["Todas", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.gen_combo = tk.OptionMenu(filters_frame, self.gen_filter_var, *gens_disponibles, command=self.filter_pokemon)
        self.gen_combo.config(bg=COLOR_INPUT, fg=COLOR_TEXT_PRIMARY, activebackground=COLOR_CARD, activeforeground=COLOR_TEXT_PRIMARY, highlightthickness=0, bd=0, indicatoron=0)
        self.gen_combo["menu"].config(bg=COLOR_INPUT, fg=COLOR_TEXT_PRIMARY, activebackground=COLOR_ACCENT, activeforeground=COLOR_TEXT_PRIMARY)
        self.gen_combo.grid(row=1, column=1, sticky='we')
        
        filters_frame.columnconfigure(0, weight=1)
        filters_frame.columnconfigure(1, weight=1)
        
        # Lista de Pokémon (Listbox)
        list_lbl = tk.Label(left_panel, text="Catálogo Pokedex", bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY,
                            font=('Helvetica', 11, 'bold'), anchor='w')
        list_lbl.pack(fill='x', padx=15, pady=(5, 5))
        
        list_container = tk.Frame(left_panel, bg=COLOR_INPUT)
        list_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.pokedex_listbox = tk.Listbox(list_container, bg=COLOR_INPUT, fg=COLOR_TEXT_PRIMARY, bd=0,
                                          selectbackground=COLOR_ACCENT, selectforeground=COLOR_TEXT_PRIMARY,
                                          font=('Helvetica', 10), highlightthickness=0, activestyle='none')
        self.pokedex_listbox.pack(side='left', fill='both', expand=True)
        self.pokedex_listbox.bind("<<ListboxSelect>>", self.on_select_pokemon)
        
        # Scrollbar de la lista
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.pokedex_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.pokedex_listbox.config(yscrollcommand=scrollbar.set)
        
        # 2. PANEL DERECHO: DETALLES DEL POKÉMON SELECCIONADO (2/3 del ancho)
        self.details_panel = tk.Frame(self.pokedex_frame, bg=COLOR_CARD, bd=0)
        self.details_panel.pack(side='right', fill='both', expand=True)
        
        # Contenedor para cuando no hay selección
        self.empty_details_label = tk.Label(self.details_panel, text="Selecciona un Pokémon de la lista\npara ver su ficha táctica.",
                                            bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=('Helvetica', 12, 'italic'))
        self.empty_details_label.pack(fill='both', expand=True)
        
        # Elementos del panel de detalles (inicialmente ocultos en un contenedor secundario)
        self.details_content = tk.Frame(self.details_panel, bg=COLOR_CARD)
        
        # Encabezado del Pokémon (Nombre, ID, Tipo)
        self.pmon_header_frame = tk.Frame(self.details_content, bg=COLOR_CARD)
        self.pmon_header_frame.pack(fill='x', padx=25, pady=(25, 15))
        
        self.pmon_name_lbl = tk.Label(self.pmon_header_frame, text="Cargando...", bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY,
                                      font=('Helvetica', 22, 'bold'), anchor='w')
        self.pmon_name_lbl.pack(fill='x')
        
        self.pmon_meta_lbl = tk.Label(self.pmon_header_frame, text="ID: #000  •  Generación: 0", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                                      font=('Helvetica', 11), anchor='w')
        self.pmon_meta_lbl.pack(fill='x', pady=(2, 8))
        
        # Contenedor de badges de tipo
        self.pmon_types_frame = tk.Frame(self.pmon_header_frame, bg=COLOR_CARD)
        self.pmon_types_frame.pack(fill='x')
        
        # Separador
        sep_det = tk.Frame(self.details_content, bg=COLOR_BORDER, height=1)
        sep_det.pack(fill='x', padx=25, pady=10)
        
        # Estadísticas Base Grid
        stats_title = tk.Label(self.details_content, text="Estadísticas Base", bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY,
                               font=('Helvetica', 13, 'bold'), anchor='w')
        stats_title.pack(fill='x', padx=25, pady=(5, 10))
        
        self.stats_container = tk.Frame(self.details_content, bg=COLOR_CARD)
        self.stats_container.pack(fill='x', padx=25)
        
        # Botón para añadir al equipo
        self.add_team_btn = tk.Button(self.details_content, text="Agregar al Equipo Activo (0/6)", bg=COLOR_SUCCESS, fg=COLOR_TEXT_PRIMARY,
                                      font=('Helvetica', 12, 'bold'), bd=0, activebackground=COLOR_SUCCESS_HOVER,
                                      activeforeground=COLOR_TEXT_PRIMARY, height=2, command=self.add_selected_to_team)
        self.add_team_btn.pack(fill='x', padx=25, pady=25, side='bottom')
        self.add_hover_effect(self.add_team_btn, COLOR_SUCCESS_HOVER, COLOR_SUCCESS)
        
        # Rellenar lista de Pokémon por primera vez
        self.populate_pokemon_list()

    def add_hover_effect(self, widget, hover_color, normal_color):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_color))

    # ==============================================================================
    # PESTAÑA 2: MI EQUIPO Y ANÁLISIS TÁCTICO
    # ==============================================================================
    def create_team_tab(self):
        self.team_frame = tk.Frame(self.content_container, bg=COLOR_BG)
        
        # 1. PANEL IZQUIERDO: INTEGRANTES DEL EQUIPO (1/2 del ancho)
        team_left_panel = tk.Frame(self.team_frame, bg=COLOR_BG)
        team_left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        team_title_frame = tk.Frame(team_left_panel, bg=COLOR_BG)
        team_title_frame.pack(fill='x', pady=(5, 15))
        
        self.team_qty_lbl = tk.Label(team_title_frame, text="Miembros del Equipo (0/6)", bg=COLOR_BG, fg=COLOR_TEXT_PRIMARY,
                                     font=('Helvetica', 14, 'bold'))
        self.team_qty_lbl.pack(side='left')
        
        # Contenedor de las tarjetas de los 6 slots
        self.slots_container = tk.Frame(team_left_panel, bg=COLOR_BG)
        self.slots_container.pack(fill='both', expand=True)
        
        # Crear los 6 slots visuales vacíos inicialmente
        self.slot_cards = []
        for i in range(6):
            card = tk.Frame(self.slots_container, bg=COLOR_CARD, bd=0, height=75)
            card.pack(fill='x', pady=4)
            card.pack_propagate(False)
            
            # Número de slot
            lbl_num = tk.Label(card, text=f"{i+1}", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=('Helvetica', 14, 'bold'), width=3)
            lbl_num.pack(side='left', padx=5)
            
            # Contenedor de contenido
            info_frame = tk.Frame(card, bg=COLOR_CARD)
            info_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            
            name_lbl = tk.Label(info_frame, text="Slot Vacío", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=('Helvetica', 11, 'italic'), anchor='w')
            name_lbl.pack(fill='x')
            
            type_frame = tk.Frame(info_frame, bg=COLOR_CARD)
            type_frame.pack(fill='x', pady=(2, 0))
            
            # Botón de remover
            btn_remove = tk.Button(card, text="✕", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=('Helvetica', 10, 'bold'),
                                   bd=0, activebackground=COLOR_CARD, activeforeground=COLOR_ACCENT, width=4,
                                   command=lambda idx=i: self.remove_from_team_at(idx))
            btn_remove.pack(side='right', fill='y')
            self.add_hover_effect(btn_remove, '#2c2c35', COLOR_CARD)
            
            self.slot_cards.append({
                'card_frame': card,
                'name_lbl': name_lbl,
                'type_frame': type_frame,
                'btn_remove': btn_remove
            })
            
        # Botones inferiores (Deshacer LIFO y Exportar)
        action_buttons_frame = tk.Frame(team_left_panel, bg=COLOR_BG)
        action_buttons_frame.pack(fill='x', pady=(15, 0))
        
        # Botón Deshacer última adición (Pila LIFO)
        self.btn_undo = tk.Button(action_buttons_frame, text="↩ Deshacer última adición (Pila LIFO)", bg=COLOR_SECONDARY, fg='#1e1e24',
                                  font=('Helvetica', 11, 'bold'), bd=0, activebackground=COLOR_SECONDARY_HOVER,
                                  activeforeground='#1e1e24', height=2, command=self.undo_last_addition)
        self.btn_undo.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.add_hover_effect(self.btn_undo, COLOR_SECONDARY_HOVER, COLOR_SECONDARY)
        
        # Botón Exportar Equipo
        self.btn_export = tk.Button(action_buttons_frame, text="💾 Exportar Equipo", bg=COLOR_SUCCESS, fg=COLOR_TEXT_PRIMARY,
                                    font=('Helvetica', 11, 'bold'), bd=0, activebackground=COLOR_SUCCESS_HOVER,
                                    activeforeground=COLOR_TEXT_PRIMARY, height=2, command=self.export_team_file)
        self.btn_export.pack(side='right', fill='x', expand=True, padx=(5, 0))
        self.add_hover_effect(self.btn_export, COLOR_SUCCESS_HOVER, COLOR_SUCCESS)
        
        # 2. PANEL DERECHO: ANÁLISIS DE DEBILIDADES (1/2 del ancho)
        team_right_panel = tk.Frame(self.team_frame, bg=COLOR_CARD, bd=0, width=450)
        team_right_panel.pack(side='right', fill='both', padx=(10, 0))
        team_right_panel.pack_propagate(False)
        
        analysis_title = tk.Label(team_right_panel, text="Análisis Táctico de Debilidades", bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY,
                                  font=('Helvetica', 14, 'bold'), anchor='w')
        analysis_title.pack(fill='x', padx=20, pady=(20, 5))
        
        analysis_subtitle = tk.Label(team_right_panel, text="Datos calculados por el backend C (pokehash_api):",
                                     bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=('Helvetica', 9), anchor='w', justify='left')
        analysis_subtitle.pack(fill='x', padx=20, pady=(0, 15))
        
        # Cuadrícula/Grid de las debilidades
        self.weakness_grid_frame = tk.Frame(team_right_panel, bg=COLOR_CARD)
        self.weakness_grid_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Generar los 18 elementos de tipo vacíos en la cuadrícula (6 filas x 3 columnas)
        self.type_weakness_widgets = {}
        types_list = list(TYPE_COLORS.keys())
        
        for idx, tname in enumerate(types_list):
            row = idx // 3
            col = idx % 3
            
            type_box = tk.Frame(self.weakness_grid_frame, bg='#25252d', bd=0)
            type_box.grid(row=row, column=col, padx=4, pady=4, sticky='nsew')
            
            # Nombre del tipo (encabezado pequeño de color del tipo)
            t_lbl = tk.Label(type_box, text=tname.upper(), bg=TYPE_COLORS[tname], fg='#ffffff',
                             font=('Helvetica', 8, 'bold'), height=1)
            t_lbl.pack(fill='x')
            
            # Contenedor de contadores
            count_frame = tk.Frame(type_box, bg='#25252d')
            count_frame.pack(fill='both', expand=True, pady=5)
            
            weak_cnt_lbl = tk.Label(count_frame, text="-", bg='#25252d', fg=COLOR_TEXT_MUTED, font=('Helvetica', 9, 'bold'))
            weak_cnt_lbl.pack(side='left', fill='x', expand=True)
            
            self.type_weakness_widgets[tname] = {
                'box': type_box,
                'count_lbl': weak_cnt_lbl
            }
            
        for r in range(6):
            self.weakness_grid_frame.rowconfigure(r, weight=1)
        for c in range(3):
            self.weakness_grid_frame.columnconfigure(c, weight=1)
            
        # Panel inferior de alertas tácticas
        self.alert_frame = tk.Frame(team_right_panel, bg=COLOR_CARD, height=80)
        self.alert_frame.pack(fill='x', side='bottom', padx=20, pady=15)
        self.alert_frame.pack_propagate(False)
        
        self.alert_scrollbar = ttk.Scrollbar(self.alert_frame)
        self.alert_text_widget = tk.Text(self.alert_frame, bg='#25252d', fg=COLOR_TEXT_MUTED, font=('Helvetica', 10, 'italic'),
                                         bd=0, height=3, padx=10, pady=5, state='normal', wrap='word')
        self.alert_text_widget.insert('1.0', "Forma un equipo para ver alertas tácticas.")
        self.alert_text_widget.config(state='disabled')
        self.alert_text_widget.configure(yscrollcommand=self.alert_scrollbar.set)
        self.alert_scrollbar.configure(command=self.alert_text_widget.yview)
        
        self.alert_text_widget.pack(fill='both', expand=True)

    # ==============================================================================
    # LÓGICA DE FILTRADO Y ACTUALIZACIÓN DE POKÉDEX
    # ==============================================================================
    def populate_pokemon_list(self):
        self.pokedex_listbox.delete(0, tk.END)
        for p in self.filtered_pokemon:
            # Formato: 001 - Bulbasaur [Grass/Poison]
            types_str = p['tipo1']
            if p['tipo2']:
                types_str += f"/{p['tipo2']}"
            display_text = f"{p['id']:03d} - {p['nombre']} [{types_str}]"
            self.pokedex_listbox.insert(tk.END, display_text)

    def filter_pokemon(self, event=None):
        query = self.search_var.get().lower().strip()
        tipo_sel = self.tipo_filter_var.get()
        gen_sel = self.gen_filter_var.get()
        
        gen_val = 0
        if gen_sel != "Todas":
            gen_val = int(gen_sel)
            
        type_val = ""
        if tipo_sel != "Todos":
            type_val = tipo_sel
            
        result = self.backend.send({
            "cmd": "filter",
            "gen": gen_val,
            "type": type_val,
            "query": query
        })
        
        if result['status'] == 'ok':
            self.filtered_pokemon = result['data']
        else:
            self.filtered_pokemon = []
            
        self.populate_pokemon_list()
        
        # Seleccionar automáticamente la primera coincidencia
        if self.filtered_pokemon:
            self.pokedex_listbox.selection_set(0)
            self.on_select_pokemon()
        else:
            self.show_empty_details()

    def show_empty_details(self):
        self.details_content.pack_forget()
        self.empty_details_label.pack(fill='both', expand=True)

    # ==============================================================================
    # INTERACCIÓN CON EL DETALLE DEL POKÉMON SELECCIONADO
    # ==============================================================================
    def on_select_pokemon(self, event=None):
        selection = self.pokedex_listbox.curselection()
        if not selection:
            return
            
        p = self.filtered_pokemon[selection[0]]
        self.selected_pokemon = p
        
        # Mostrar panel de contenido, ocultar mensaje vacío
        self.empty_details_label.pack_forget()
        self.details_content.pack(fill='both', expand=True)
        
        # Nombre e ID
        self.pmon_name_lbl.config(text=p['nombre'])
        self.pmon_meta_lbl.config(text=f"ID de Pokédex: #{p['id']:03d}   •   Generación: {p['gen']}ª")
        
        # Limpiar y re-dibujar badges de tipo
        for child in self.pmon_types_frame.winfo_children():
            child.destroy()
            
        t1_lbl = tk.Label(self.pmon_types_frame, text=p['tipo1'].upper(), bg=TYPE_COLORS.get(p['tipo1'], '#777'),
                          fg='#ffffff', font=('Helvetica', 10, 'bold'), padx=10, pady=3)
        t1_lbl.pack(side='left', padx=(0, 5))
        
        if p['tipo2']:
            t2_lbl = tk.Label(self.pmon_types_frame, text=p['tipo2'].upper(), bg=TYPE_COLORS.get(p['tipo2'], '#777'),
                              fg='#ffffff', font=('Helvetica', 10, 'bold'), padx=10, pady=3)
            t2_lbl.pack(side='left')
            
        # Re-dibujar estadísticas
        for child in self.stats_container.winfo_children():
            child.destroy()
            
        stats_data = [
            ("Vida (HP)", p['hp'], '#2ed573'),
            ("Ataque (ATK)", p['ataque'], '#ff4757'),
            ("Defensa (DEF)", p['defensa'], '#feca57'),
            ("At. Especial (SPA)", p['ataque_esp'], '#54a0ff'),
            ("Def. Especial (SPD)", p['defensa_esp'], '#9b59b6'),
            ("Velocidad (SPE)", p['velocidad'], '#ff7675')
        ]
        
        for idx, (sname, sval, scolor) in enumerate(stats_data):
            row_f = tk.Frame(self.stats_container, bg=COLOR_CARD)
            row_f.pack(fill='x', pady=5)
            
            lbl_name = tk.Label(row_f, text=sname, bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=('Helvetica', 10, 'bold'), width=16, anchor='w')
            lbl_name.pack(side='left')
            
            lbl_val = tk.Label(row_f, text=str(sval), bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY, font=('Helvetica', 10, 'bold'), width=4, anchor='e')
            lbl_val.pack(side='left', padx=(5, 10))
            
            # Barra de estadísticas
            bar = StatBar(row_f, sval, max_value=255, color=scolor)
            bar.pack(side='left', fill='x', expand=True, pady=2)
            
        # Fila de Total
        tot_f = tk.Frame(self.stats_container, bg=COLOR_CARD)
        tot_f.pack(fill='x', pady=(10, 5))
        
        lbl_tot_name = tk.Label(tot_f, text="Total Estadísticas (BST)", bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY, font=('Helvetica', 11, 'bold'), width=16, anchor='w')
        lbl_tot_name.pack(side='left')
        
        lbl_tot_val = tk.Label(tot_f, text=str(p['total']), bg=COLOR_CARD, fg=COLOR_SECONDARY, font=('Helvetica', 12, 'bold'), width=4, anchor='e')
        lbl_tot_val.pack(side='left', padx=(5, 10))
        
        # Barra del total
        bar_tot = StatBar(tot_f, p['total'], max_value=780, color=COLOR_SECONDARY)
        bar_tot.pack(side='left', fill='x', expand=True, pady=2)
        
        # Actualizar texto del botón de agregar
        self.update_add_button_text()

    def update_add_button_text(self):
        p_name = self.selected_pokemon['nombre'] if hasattr(self, 'selected_pokemon') and self.selected_pokemon else 'Pokémon'
        self.add_team_btn.config(text=f"Agregar a {p_name} al Equipo ({len(self.equipo)}/6)")
        if len(self.equipo) >= 6:
            self.add_team_btn.config(bg=COLOR_BORDER, text="Equipo Completo (6/6)", state="disabled")
        else:
            self.add_team_btn.config(bg=COLOR_SUCCESS, state="normal")

    # ==============================================================================
    # GESTIÓN DEL EQUIPO — Operaciones delegadas al backend C
    # ==============================================================================
    def refresh_team_from_backend(self):
        """Sincroniza el estado local del equipo con el backend C."""
        result = self.backend.team_view()
        if result['status'] == 'ok':
            self.equipo = result['team']
    
    def add_selected_to_team(self):
        selection = self.pokedex_listbox.curselection()
        if not selection:
            return
            
        if len(self.equipo) >= 6:
            messagebox.showwarning("Equipo Completo", "Tu equipo ya tiene el límite máximo de 6 Pokémon.")
            return
            
        p = self.filtered_pokemon[selection[0]]
        
        # Enviar comando al backend C
        result = self.backend.team_add(p['nombre'])
        if result['status'] != 'ok':
            messagebox.showwarning("Error", result.get('message', 'Error al agregar'))
            return
        
        # Sincronizar equipo desde C
        self.refresh_team_from_backend()
        
        # Feedback visual temporal
        self.add_team_btn.config(text="¡Añadido Exitosamente!")
        self.root.after(800, self.update_add_button_text)
        
        # Actualizar vistas
        self.update_team_tab_view()
        
    def undo_last_addition(self):
        if not self.equipo:
            messagebox.showinfo("Pila Vacía", "No hay Pokémon en el equipo para deshacer.")
            return
        
        # Operación Pop (LIFO) en el backend C
        result = self.backend.team_undo()
        if result['status'] == 'ok':
            removed_name = result.get('removed', '???')
            messagebox.showinfo("Acción Deshecha (LIFO)", f"Se eliminó a {removed_name} del equipo (última adición revertida).")
            self.refresh_team_from_backend()
            self.update_team_tab_view()
            self.update_add_button_text()
        else:
            messagebox.showwarning("Error", result.get('message', 'Error'))
        
    def remove_from_team_at(self, idx):
        if idx < len(self.equipo):
            result = self.backend.team_remove(idx)
            if result['status'] == 'ok':
                removed_name = result.get('removed', '???')
                messagebox.showinfo("Eliminado", f"Se eliminó a {removed_name} del equipo.")
                self.refresh_team_from_backend()
                self.update_team_tab_view()
                self.update_add_button_text()

    # ==============================================================================
    # ACTUALIZACIÓN Y ANÁLISIS — Datos del backend C
    # ==============================================================================
    def update_team_tab_view(self):
        # Actualizar cabecera de cantidad
        self.team_qty_lbl.config(text=f"Miembros del Equipo ({len(self.equipo)}/6)")
        
        # Actualizar tarjetas de slots
        for i in range(6):
            card_widgets = self.slot_cards[i]
            
            # Limpiar badges de tipo previos
            for child in card_widgets['type_frame'].winfo_children():
                child.destroy()
                
            if i < len(self.equipo):
                p = self.equipo[i]
                card_widgets['card_frame'].config(bg='#1c2330') # Color destacado
                card_widgets['name_lbl'].config(text=f"{p['nombre']} (ID: #{p['id']})", fg=COLOR_TEXT_PRIMARY, font=('Helvetica', 11, 'bold'))
                
                # Re-dibujar badges de tipo
                t1 = tk.Label(card_widgets['type_frame'], text=p['tipo1'].upper(), bg=TYPE_COLORS.get(p['tipo1'], '#777'),
                              fg='#ffffff', font=('Helvetica', 8, 'bold'), padx=6, pady=1)
                t1.pack(side='left', padx=(0, 4))
                
                if p['tipo2']:
                    t2 = tk.Label(card_widgets['type_frame'], text=p['tipo2'].upper(), bg=TYPE_COLORS.get(p['tipo2'], '#777'),
                                  fg='#ffffff', font=('Helvetica', 8, 'bold'), padx=6, pady=1)
                    t2.pack(side='left')
                    
                # Mostrar botón de remover
                card_widgets['btn_remove'].config(state='normal', fg=COLOR_TEXT_MUTED)
            else:
                # Slot vacío
                card_widgets['card_frame'].config(bg=COLOR_CARD)
                card_widgets['name_lbl'].config(text="Slot Vacío", fg=COLOR_TEXT_MUTED, font=('Helvetica', 11, 'italic'))
                card_widgets['btn_remove'].config(state='disabled', fg=COLOR_CARD)
                
        # Solicitar análisis de debilidades al backend C
        self.calculate_team_weaknesses()

    def calculate_team_weaknesses(self):
        """Obtiene el análisis de debilidades del backend C y actualiza la vista."""
        if not self.equipo:
            # Resetear cuadrícula si el equipo está vacío
            for tname, widgets in self.type_weakness_widgets.items():
                widgets['count_lbl'].config(text="-", fg=COLOR_TEXT_MUTED)
                widgets['box'].config(bg='#25252d')
            self.alert_lbl.config(text="Forma un equipo para ver alertas tácticas.", fg=COLOR_TEXT_MUTED, bg='#25252d')
            return
        
        # === TODA LA LÓGICA DE CÁLCULO VIENE DEL BACKEND C ===
        result = self.backend.team_analyze()
        if result['status'] != 'ok':
            return
        
        grid = result['grid']          # [{type, weak, resist, immune, x4}, ...]
        x4_alerts = result['x4_alerts']  # [{pokemon, type}, ...]
            
        # Actualizar los labels del grid en base al cálculo del backend C
        for entry in grid:
            tname = entry['type']
            if tname not in self.type_weakness_widgets:
                continue
            
            widgets = self.type_weakness_widgets[tname]
            w_cnt = entry['weak']
            r_cnt = entry['resist']
            dw_cnt = entry['x4']
            imm_cnt = entry.get('immune', 0)
            
            txt_repr = ""
            bg_color = '#25252d'
            text_color = COLOR_TEXT_MUTED
            
            if w_cnt > 0 or r_cnt > 0 or imm_cnt > 0:
                parts = []
                if w_cnt > 0:
                    parts.append(f"▲ {w_cnt}")
                if r_cnt > 0:
                    parts.append(f"▼ {r_cnt}")
                if imm_cnt > 0:
                    parts.append(f"⊘ {imm_cnt}")
                        
                txt_repr = "  ".join(parts)
                
                # Lógica de color visual basada en el balance de resistencias vs debilidades
                if (r_cnt + imm_cnt) > w_cnt:
                    bg_color = '#1b3024' # Tinte verde suave por resistencia
                    text_color = COLOR_SUCCESS
                elif w_cnt > (r_cnt + imm_cnt):
                    bg_color = '#382226' # Tinte rojo suave por debilidad
                    text_color = COLOR_ACCENT
                    if dw_cnt > 0:
                        bg_color = '#4c1c24' # Rojo más oscuro por debilidad extrema x4
                else:
                    # Empate
                    bg_color = '#302b1c' # Tinte amarillento/neutral
                    text_color = COLOR_SECONDARY
            else:
                txt_repr = "Neutral"
                bg_color = '#25252d'
                text_color = COLOR_TEXT_MUTED
                
            widgets['count_lbl'].config(text=txt_repr, fg=text_color)
            widgets['box'].config(bg=bg_color)
            
        # Actualizar alerta táctica con datos del backend C
        self.alert_text_widget.config(state='normal')
        self.alert_text_widget.delete('1.0', tk.END)
        
        if x4_alerts:
            alert_text = "⚠️ ADVERTENCIA TÁCTICA:\n"
            alerts_str = [f"{a['pokemon']} tiene debilidad crítica (x4) a {a['type'].upper()}" for a in x4_alerts]
            alert_text += "\n".join(alerts_str)
            
            self.alert_text_widget.insert(tk.END, alert_text)
            self.alert_text_widget.config(fg='#ff9f43', bg='#3b2d1c', state='disabled')
            
            # Mostrar scrollbar solo si hay 3 o más alertas
            if len(alerts_str) >= 3:
                self.alert_text_widget.pack_forget()
                self.alert_scrollbar.pack(side='right', fill='y')
                self.alert_text_widget.pack(side='left', fill='both', expand=True)
            else:
                self.alert_scrollbar.pack_forget()
                self.alert_text_widget.pack_forget()
                self.alert_text_widget.pack(fill='both', expand=True)
        else:
            self.alert_text_widget.insert(tk.END, "✓ Balance de Tipos Estable:\nTu equipo actual no tiene debilidades críticas x4 de tipo.")
            self.alert_text_widget.config(fg=COLOR_SUCCESS, bg='#1b3024', state='disabled')
            
            self.alert_scrollbar.pack_forget()
            self.alert_text_widget.pack_forget()
            self.alert_text_widget.pack(fill='both', expand=True)

    # ==============================================================================
    # EXPORTACIÓN DEL EQUIPO Y REPORTE
    # ==============================================================================
    def export_team_file(self):
        if not self.equipo:
            messagebox.showwarning("Exportar", "No puedes exportar un equipo vacío.")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Guardar Equipo Pokémon",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile="equipo_pokehash.txt"
        )
        if not filename:
            return # El usuario canceló
            
        result = self.backend.team_export(filename)
        
        if result['status'] == 'ok':
            messagebox.showinfo("Exportar", f"¡Equipo exportado con éxito a '{filename}'!\nContiene la ficha táctica y el análisis completo.")
        else:
            messagebox.showerror("Error al Exportar", f"No se pudo guardar el archivo: {result.get('message', 'Error desconocido')}")

    # ==============================================================================
    # HELPERS DE DISEÑO Y EFECTOS
    # ==============================================================================
    def add_hover_effect(self, widget, hover_bg, normal_bg):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

# ==============================================================================
# INICIO DE LA APLICACIÓN
# ==============================================================================
if __name__ == "__main__":
    ventana = tk.Tk()
    app = PokeHashGUI(ventana)
    ventana.mainloop()