import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

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

# Matriz de efectividad de tipos (Atacante -> Defensor)
# Si no está en el diccionario secundario, el daño es neutral (1.0)
TYPE_EFFECTIVENESS = {
    'Normal': {'Rock': 0.5, 'Ghost': 0.0, 'Steel': 0.5},
    'Fire': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2.0, 'Ice': 2.0, 'Bug': 2.0, 'Rock': 0.5, 'Dragon': 0.5, 'Steel': 2.0},
    'Water': {'Fire': 2.0, 'Water': 0.5, 'Grass': 0.5, 'Ground': 2.0, 'Rock': 2.0, 'Dragon': 0.5},
    'Electric': {'Water': 2.0, 'Electric': 0.5, 'Grass': 0.5, 'Ground': 0.0, 'Flying': 2.0, 'Dragon': 0.5},
    'Grass': {'Fire': 0.5, 'Water': 2.0, 'Grass': 0.5, 'Poison': 0.5, 'Ground': 2.0, 'Flying': 0.5, 'Bug': 0.5, 'Rock': 2.0, 'Dragon': 0.5, 'Steel': 0.5},
    'Ice': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2.0, 'Ice': 0.5, 'Ground': 2.0, 'Flying': 2.0, 'Dragon': 2.0, 'Steel': 0.5},
    'Fighting': {'Normal': 2.0, 'Ice': 2.0, 'Fighting': 1.0, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Rock': 2.0, 'Ghost': 0.0, 'Dark': 2.0, 'Steel': 2.0, 'Fairy': 0.5},
    'Poison': {'Grass': 2.0, 'Poison': 0.5, 'Ground': 0.5, 'Rock': 0.5, 'Ghost': 0.5, 'Steel': 0.0, 'Fairy': 2.0},
    'Ground': {'Fire': 2.0, 'Electric': 2.0, 'Grass': 0.5, 'Poison': 2.0, 'Flying': 0.0, 'Bug': 0.5, 'Rock': 2.0, 'Steel': 2.0},
    'Flying': {'Electric': 0.5, 'Grass': 2.0, 'Fighting': 2.0, 'Bug': 2.0, 'Rock': 0.5, 'Steel': 0.5},
    'Psychic': {'Fighting': 2.0, 'Poison': 2.0, 'Psychic': 0.5, 'Dark': 0.0, 'Steel': 0.5},
    'Bug': {'Fire': 0.5, 'Fighting': 0.5, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 2.0, 'Ghost': 0.5, 'Grass': 2.0, 'Dark': 2.0, 'Steel': 0.5, 'Fairy': 0.5},
    'Rock': {'Fire': 2.0, 'Ice': 2.0, 'Fighting': 0.5, 'Ground': 0.5, 'Flying': 2.0, 'Bug': 2.0, 'Steel': 0.5},
    'Ghost': {'Normal': 0.0, 'Psychic': 2.0, 'Ghost': 2.0, 'Dark': 0.5},
    'Dragon': {'Dragon': 2.0, 'Steel': 0.5, 'Fairy': 0.0},
    'Dark': {'Fighting': 0.5, 'Psychic': 2.0, 'Ghost': 2.0, 'Dark': 0.5, 'Fairy': 0.5},
    'Steel': {'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Ice': 2.0, 'Rock': 2.0, 'Steel': 0.5, 'Fairy': 2.0},
    'Fairy': {'Fire': 0.5, 'Fighting': 2.0, 'Poison': 0.5, 'Dragon': 2.0, 'Dark': 2.0, 'Steel': 0.5}
}

# ==============================================================================
# CARGA Y PROCESAMIENTO DE DATOS (MOCK / VISTA PROVISIONAL)
# ==============================================================================
def cargar_pokemon_desde_csv():
    pokemon_list = []
    if not os.path.exists("Pokemon.csv"):
        return pokemon_list
    
    try:
        with open("Pokemon.csv", mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['Name'].strip()
                form = row['Form'].strip() if row.get('Form') else ''
                
                # Normalización de nombre en consonancia con pokehash.c
                if form and form != '':
                    if name in form:
                        nombre_completo = form
                    else:
                        nombre_completo = f"{name} ({form})"
                else:
                    nombre_completo = name
                
                p = {
                    'id': int(row['ID']),
                    'nombre': nombre_completo,
                    'tipo1': row['Type1'].strip(),
                    'tipo2': row['Type2'].strip() if row.get('Type2') else '',
                    'total': int(row['Total']),
                    'hp': int(row['HP']),
                    'ataque': int(row['Attack']),
                    'defensa': int(row['Defense']),
                    'ataque_esp': int(row['Sp. Atk']),
                    'defensa_esp': int(row['Sp. Def']),
                    'velocidad': int(row['Speed']),
                    'gen': int(row['Generation'])
                }
                pokemon_list.append(p)
    except Exception as e:
        print(f"Error al cargar Pokemon.csv: {e}")
    return pokemon_list

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
        
        # Cargar datos
        self.all_pokemon = cargar_pokemon_desde_csv()
        self.filtered_pokemon = list(self.all_pokemon)
        
        # Equipo Activo (Pila LIFO)
        self.equipo = []  # Stack de diccionarios Pokémon
        
        # Configurar estilos generales
        self.setup_styles()
        
        # Crear componentes
        self.create_widgets()
        
        # Seleccionar primer Pokémon por defecto
        if self.filtered_pokemon:
            self.pokedex_listbox.selection_set(0)
            self.on_select_pokemon()

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
        self.tipo_combo = ttk.Combobox(filters_frame, textvariable=self.tipo_filter_var, values=tipos_disponibles, state="readonly", width=12)
        self.tipo_combo.grid(row=1, column=0, sticky='we', padx=(0, 5))
        self.tipo_combo.bind("<<ComboboxSelected>>", self.filter_pokemon)
        
        # Filtro de Generación
        gen_lbl = tk.Label(filters_frame, text="Generación:", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=('Helvetica', 9, 'bold'))
        gen_lbl.grid(row=0, column=1, sticky='w', pady=(0, 2))
        self.gen_filter_var = tk.StringVar(value="Todas")
        self.gen_combo = ttk.Combobox(filters_frame, textvariable=self.gen_filter_var, values=["Todas", "1", "2", "3", "4", "5", "6", "7", "8", "9"], state="readonly", width=10)
        self.gen_combo.grid(row=1, column=1, sticky='we')
        self.gen_combo.bind("<<ComboboxSelected>>", self.filter_pokemon)
        
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
        self.btn_export = tk.Button(action_buttons_frame, text="💾 Exportar Equipo (C y Python)", bg=COLOR_SUCCESS, fg=COLOR_TEXT_PRIMARY,
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
        
        analysis_subtitle = tk.Label(team_right_panel, text="Multiplicadores de daño elementales compuestos sobre el equipo activo:",
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
        
        self.alert_lbl = tk.Label(self.alert_frame, text="Forma un equipo para ver alertas tácticas.",
                                  bg='#25252d', fg=COLOR_TEXT_MUTED, font=('Helvetica', 10, 'italic'),
                                  bd=0, height=3, relief='flat', padx=10, justify='left', wraplength=400)
        self.alert_lbl.pack(fill='both', expand=True)

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
        
        filtered = []
        for p in self.all_pokemon:
            # Filtro por texto de búsqueda (Nombre o ID)
            matches_query = False
            if query == "":
                matches_query = True
            elif query.isdigit():
                if query in str(p['id']):
                    matches_query = True
            else:
                if query in p['nombre'].lower():
                    matches_query = True
                    
            # Filtro por tipo
            matches_tipo = False
            if tipo_sel == "Todos":
                matches_tipo = True
            else:
                if p['tipo1'] == tipo_sel or p['tipo2'] == tipo_sel:
                    matches_tipo = True
                    
            # Filtro por generación
            matches_gen = False
            if gen_sel == "Todas":
                matches_gen = True
            else:
                if str(p['gen']) == gen_sel:
                    matches_gen = True
                    
            if matches_query and matches_tipo and matches_gen:
                filtered.append(p)
                
        self.filtered_pokemon = filtered
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
    # GESTIÓN DEL EQUIPO (PILA LIFO) Y OPERACIONES
    # ==============================================================================
    def add_selected_to_team(self):
        selection = self.pokedex_listbox.curselection()
        if not selection:
            return
            
        if len(self.equipo) >= 6:
            messagebox.showwarning("Equipo Completo", "Tu equipo ya tiene el límite máximo de 6 Pokémon. Elimina o deshace un integrante.")
            return
            
        p = self.filtered_pokemon[selection[0]]
        
        # Agregar a la pila
        self.equipo.append(p)
        
        # Feedback visual temporal
        self.add_team_btn.config(text="¡Añadido Exitosamente!")
        self.root.after(800, self.update_add_button_text)
        
        # Actualizar vistas
        self.update_team_tab_view()
        
    def undo_last_addition(self):
        if not self.equipo:
            messagebox.showinfo("Pila Vacía", "No hay Pokémon en el equipo para deshacer.")
            return
            
        # Operación Pop (LIFO Stack)
        removed = self.equipo.pop()
        messagebox.showinfo("Acción Deshecha (LIFO)", f"Se eliminó a {removed['nombre']} del equipo (última adición revertida).")
        
        # Actualizar vistas
        self.update_team_tab_view()
        self.update_add_button_text()
        
    def remove_from_team_at(self, idx):
        if idx < len(self.equipo):
            removed = self.equipo.pop(idx)
            messagebox.showinfo("Eliminado", f"Se eliminó a {removed['nombre']} del equipo.")
            
            # Actualizar vistas
            self.update_team_tab_view()
            self.update_add_button_text()

    # ==============================================================================
    # ACTUALIZACIÓN Y ANÁLISIS DE LA PESTAÑA EQUIPO
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
                
        # Calcular debilidades y actualizar grid estratégico
        self.calculate_team_weaknesses()

    def calculate_team_weaknesses(self):
        if not self.equipo:
            # Resetear cuadrícula si el equipo está vacío
            for tname, widgets in self.type_weakness_widgets.items():
                widgets['count_lbl'].config(text="-", fg=COLOR_TEXT_MUTED)
                widgets['box'].config(bg='#25252d')
            self.alert_lbl.config(text="Forma un equipo para ver alertas tácticas.", fg=COLOR_TEXT_MUTED, bg='#25252d')
            return
            
        # Calcular multiplicadores elementales para los 18 tipos
        # Para cada tipo atacante, vemos cuántos miembros del equipo lo resisten (< 1.0) o son débiles a él (> 1.0)
        team_weaknesses = {} # atacante -> { 'weak': count, 'resist': count, 'double_weak': count }
        
        types_list = list(TYPE_COLORS.keys())
        double_weaknesses_alerts = [] # Lista de tuplas (Pokemon, Tipo) con debilidad 4x
        
        for atk_type in types_list:
            weak_count = 0
            resist_count = 0
            double_weak_count = 0
            
            for p in self.equipo:
                # Multiplicador del tipo atacante al Pokémon defendiendo
                mult = TYPE_EFFECTIVENESS.get(atk_type, {}).get(p['tipo1'], 1.0)
                if p['tipo2']:
                    mult *= TYPE_EFFECTIVENESS.get(atk_type, {}).get(p['tipo2'], 1.0)
                    
                if mult > 1.0:
                    weak_count += 1
                    if mult >= 4.0:
                        double_weak_count += 1
                        double_weaknesses_alerts.append((p['nombre'], atk_type))
                elif mult < 1.0:
                    resist_count += 1
                    
            team_weaknesses[atk_type] = {
                'weak': weak_count,
                'resist': resist_count,
                'double_weak': double_weak_count
            }
            
        # Actualizar los labels del grid en base al cálculo
        for tname, widgets in self.type_weakness_widgets.items():
            stats = team_weaknesses[tname]
            w_cnt = stats['weak']
            r_cnt = stats['resist']
            dw_cnt = stats['double_weak']
            
            txt_repr = ""
            bg_color = '#25252d'
            text_color = COLOR_TEXT_MUTED
            
            if w_cnt > 0 or r_cnt > 0:
                parts = []
                if w_cnt > 0:
                    parts.append(f"▲ {w_cnt}")
                    bg_color = '#382226' # Tinte rojo suave por debilidad
                    text_color = COLOR_ACCENT
                    if dw_cnt > 0:
                        bg_color = '#4c1c24' # Rojo más oscuro por debilidad extrema x4
                if r_cnt > 0:
                    parts.append(f"▼ {r_cnt}")
                    if w_cnt == 0:
                        bg_color = '#1b3024' # Tinte verde suave por resistencia
                        text_color = COLOR_SUCCESS
                        
                txt_repr = "  ".join(parts)
            else:
                txt_repr = "Neutral"
                bg_color = '#25252d'
                text_color = COLOR_TEXT_MUTED
                
            widgets['count_lbl'].config(text=txt_repr, fg=text_color)
            widgets['box'].config(bg=bg_color)
            
        # Actualizar alerta táctica
        if double_weaknesses_alerts:
            alert_text = "⚠️ ADVERTENCIA TÁCTICA:\n"
            alerts_str = [f"{pmon} tiene debilidad crítica (x4) a {tipo.upper()}" for pmon, tipo in double_weaknesses_alerts]
            alert_text += "\n".join(alerts_str[:3])
            if len(alerts_str) > 3:
                alert_text += f"\n... y {len(alerts_str)-3} más."
            self.alert_lbl.config(text=alert_text, fg='#ff9f43', bg='#3b2d1c')
        else:
            self.alert_lbl.config(text="✓ Balance de Tipos Estable:\nTu equipo actual no tiene debilidades críticas x4 de tipo.", fg=COLOR_SUCCESS, bg='#1b3024')

    # ==============================================================================
    # EXPORTACIÓN DEL EQUIPO Y REPORTE
    # ==============================================================================
    def export_team_file(self):
        if not self.equipo:
            messagebox.showwarning("Exportar", "No puedes exportar un equipo vacío.")
            return
            
        filename = "equipo.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("========================================\n")
                f.write("        POKEHASH: REPORTE DE EQUIPO     \n")
                f.write("========================================\n\n")
                
                f.write(f"Total Integrantes: {len(self.equipo)} / 6\n\n")
                f.write("Integrantes del Equipo:\n")
                
                for idx, p in enumerate(self.equipo):
                    t_str = p['tipo1']
                    if p['tipo2']:
                        t_str += f" / {p['tipo2']}"
                    f.write(f"Slot {idx+1}: {p['nombre']} (ID: #{p['id']}) - Generación: {p['gen']}\n")
                    f.write(f"  Tipos: {t_str}\n")
                    f.write(f"  Estadísticas: HP: {p['hp']} | ATK: {p['ataque']} | DEF: {p['defensa']} | "
                            f"SPA: {p['ataque_esp']} | SPD: {p['defensa_esp']} | SPE: {p['velocidad']}\n")
                    f.write(f"  Total BST: {p['total']}\n")
                    f.write("-" * 40 + "\n")
                    
                # Cálculo de debilidades elementales
                f.write("\n========================================\n")
                f.write("    ANÁLISIS TÁCTICO DE DEBILIDADES\n")
                f.write("========================================\n")
                
                types_list = list(TYPE_COLORS.keys())
                f.write("\n[Debilidades compuestas por tipo de daño]\n")
                for atk_type in types_list:
                    weak_count = 0
                    double_weak_count = 0
                    resist_count = 0
                    
                    for p in self.equipo:
                        mult = TYPE_EFFECTIVENESS.get(atk_type, {}).get(p['tipo1'], 1.0)
                        if p['tipo2']:
                            mult *= TYPE_EFFECTIVENESS.get(atk_type, {}).get(p['tipo2'], 1.0)
                        
                        if mult > 1.0:
                            weak_count += 1
                            if mult >= 4.0:
                                double_weak_count += 1
                        elif mult < 1.0:
                            resist_count += 1
                            
                    if weak_count > 0 or resist_count > 0:
                        report_line = f" - Tipo {atk_type.upper():<10} : "
                        if weak_count > 0:
                            report_line += f"Debilidad x{weak_count} "
                            if double_weak_count > 0:
                                report_line += f"(incluye {double_weak_count} crít. x4) "
                        if resist_count > 0:
                            report_line += f"Resistencia x{resist_count}"
                        f.write(report_line + "\n")
                
                f.write("\nGenerado por PokeHash GUI (Provisional) - C/Python Integrado.\n")
                
            messagebox.showinfo("Exportar", f"¡Equipo exportado con éxito a '{filename}'!\nContiene la ficha táctica y el análisis completo.")
        except Exception as e:
            messagebox.showerror("Error al Exportar", f"No se pudo guardar el archivo: {e}")

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