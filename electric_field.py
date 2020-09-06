import PySimpleGUI as sg

import math
import csv

class Charge:
    def __init__(self, id, x, y, charge):
        self.id = id
        self.x = x
        self.y = y
        self.charge = charge / 1000000000
    
    def as_csv_row(self):
        return [self.id, self.x, self.y, self.charge]

class Vector:
    def __init__(self, line_id, line_color, x_location, y_location, x_component, y_component, field_strength):
        self.line_id = line_id
        self.line_color = line_color
        self.x_location = x_location
        self.y_location = y_location
        self.x_component = x_component
        self.y_component = y_component
        self.field_strength = field_strength
    
    def as_csv_row(self):
        return [self.line_id, self.line_color, self.x_location, self.y_location, self.x_component, self.y_component, self.field_strength]

HEIGHT = WIDTH = 600
ARROW_SIZE = 8
ARROWS = 4900
PERMEABILITY = 8987551792

charges = []
vectors = []

point_display_value_x = 0
point_display_value_y = 0

description_text = '''\
This simulator allows you to view how 
the electric fields of point charges 
interact.

Calculations done with all distances
in metres and all charges in nano
Coloumbs. 

Pos field/charge red, neg is blue.

Num of vectors works best with perfect
squares, default is 4900 (70^2). 
Default line size is 8.

WARNING: No upper bound on charges and 
displayed vectors (aka memory leak).
Don't crash your computer :)
'''

field_layout = [
    [
        sg.Graph(
            canvas_size=(HEIGHT, WIDTH),
            graph_bottom_left=(HEIGHT / -2, WIDTH / -2),
            graph_top_right=(HEIGHT / 2, WIDTH / 2),
            background_color='white', 
            key='graph')
        ],
]

menu_layout = [
    [sg.Text(description_text)],
    [sg.Button('Add Charge')],
    [
        sg.Text('x'), sg.InputText('', size=(6,10), key='x'), 
        sg.Text('y'), sg.InputText('', size=(6,10), key='y'),
        sg.Text('charge'), sg.InputText('', size=(6,10), key='charge')
    ],
    [sg.HorizontalSeparator()],
    [sg.Button('Get Component Vector From Point')],
    [
        sg.Text('from x'), sg.InputText('', size=(6,10), key='cx'), 
        sg.Text('from y'), sg.InputText('', size=(6,10), key='cy'),
    ],
    [sg.Text('x val:                 ', key='ox')],
    [sg.Text('y val:                 ', key='oy')],
    [sg.HorizontalSeparator()],
    [sg.Button('Clear All Charges'), sg.Button('Clear All Vectors')],
    [sg.HorizontalSeparator()],
    [sg.Button('Show Vectors'), sg.Button('Export Data')],
    [sg.HorizontalSeparator()],
    [sg.Button("New Num Vectors"), sg.Button("New Vector Length")],
    [
        sg.Text('vectors'), sg.InputText('', size=(10,10), key='num_vectors'),
        sg.Text('length'), sg.InputText('', size=(10,10), key='vector_length')
    ], 
    [sg.HorizontalSeparator()],
    [sg.Button("Exit")],
    [sg.HorizontalSeparator()],
]

master_layout = [
    [
        sg.Column(menu_layout),
        sg.VSeparator(),
        sg.Column(field_layout)
    ]
]

window = sg.Window("Point Charge Electric Field Simulator")
window.Layout(master_layout)
window.Finalize()

graph = window['graph']

def draw_charge(x, y, charge):
    if charge < 0:
        return graph.DrawPoint((x, y), 12, color='blue')
    if charge == 0:
        return graph.DrawPoint((x, y), 12, color='green')
    return graph.DrawPoint((x, y), 12, color='red')

def single_vector_draw(center_x, center_y):
    vector_sum_x = 0
    vector_sum_y = 0
    field_charge_sign = 0
    for charge in charges:
        radius = math.sqrt((charge.x - center_x)**2 + (charge.y - center_y)**2)
        field_strength = charge.charge * PERMEABILITY / (radius**2)
        field_charge_sign += field_strength
        vector_sum_x += field_strength * ((charge.x - center_x) / (radius))
        vector_sum_y += field_strength * ((charge.y - center_y) / (radius))

    unit_vector_x = vector_sum_x / math.sqrt(vector_sum_x**2 + vector_sum_y**2)
    unit_vector_y = vector_sum_y / math.sqrt(vector_sum_x**2 + vector_sum_y**2)

    vector_start_point_x = center_x - (unit_vector_x * ARROW_SIZE / 2)
    vector_start_point_y = center_y - (unit_vector_y * ARROW_SIZE / 2)
    vector_end_point_x = center_x + (unit_vector_x * ARROW_SIZE / 2)
    vector_end_point_y = center_y + (unit_vector_y * ARROW_SIZE / 2)

    field_charge_color = field_charge_sign * 100000000

    if field_charge_color > 0.0:
        this_line_color = 'red'
    elif field_charge_color == 0:
        this_line_color = 'white'
    else:
        this_line_color = 'blue'
    

    line = graph.DrawLine((vector_start_point_x, vector_start_point_y), (vector_end_point_x, vector_end_point_y), color=this_line_color)

    this_vector = Vector(line, this_line_color, center_x, center_y, vector_sum_x, vector_sum_y, field_charge_sign)
    vectors.append(this_vector)

def get_field_strength_from_point():
    from_x, from_y = int(values['cx']), int(values['cy'])
    vector_sum_x, vector_sum_y = 0, 0
    for charge in charges:
        radius = math.sqrt((charge.x - from_x)**2 + (charge.y - from_y)**2)
        field_strength = charge.charge * PERMEABILITY / (radius**2)
        vector_sum_x += field_strength * ((charge.x - from_x) / (radius))
        vector_sum_y += field_strength * ((charge.y - from_y) / (radius))
    return vector_sum_x, vector_sum_y

def mass_vector_draw():
    box_size = HEIGHT * WIDTH / ARROWS
    box_side = math.sqrt(box_size)
    increment = int(box_side / 2)
    arrows_side = int(math.sqrt(ARROWS))
    x = WIDTH / -2 + increment
    y = HEIGHT / 2 - increment

    for i in range(arrows_side):
        for j in range(arrows_side):
            # new_vector = graph.DrawPoint((x, y), 15, color='green')
            single_vector_draw(x, y)
            x += box_side
        x = WIDTH / -2 + increment
        y -= box_side

def create_charge():
    try:
        x = float(values['x'])
        y = float(values['y'])
        charge = float(values['charge'])
        if x > 300 or x < -300 or y > 300 or y < -300:
            raise ValueError('Postive charge value must be in the interval [-300, 300]')
        this_charge = draw_charge(x, y, charge)
        charge = Charge(this_charge, x, y, charge)
        charges.append(charge)
    except:
        return None

def clear_all_vectors():
    while vectors:
        this_vector = vectors.pop()
        graph.DeleteFigure(this_vector.line_id)

def export_data():
    with open('charge_locations.csv', 'w') as charge_csv:
        w = csv.writer(charge_csv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Object ID', 'X Position', 'Y Position', 'Charge (C)'])
        for charge in charges:
            w.writerow(charge.as_csv_row())    

    with open('force_vectors.csv', 'w') as force_csv:
        w = csv.writer(force_csv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Object ID', 'Line Color', 'X Position', 'Y Position', 'X Force Vector Comp.', 'Y Force Vector Comp.', 'Field Strength'])   
        for vector in vectors:
            w.writerow(vector.as_csv_row())    

while True:
    event, values = window.read()

    if event == 'Add Charge':
        try:
            if values['charge'] == 0:
                continue
            create_charge()
            clear_all_vectors()
            mass_vector_draw()
        except Exception as e:
            print(e)

    if event == 'Clear All Charges':
        try:
            while charges:
                this_charge = charges.pop()
                graph.DeleteFigure(this_charge.id)
        except Exception as e:
            print(e)
            
    if event == 'Show Vectors':
        try:
            mass_vector_draw()
        except Exception as e:
            print(e)
    
    if event == 'Clear All Vectors':
        try:
            clear_all_vectors()
        except Exception as e:
            print(e)
    
    if event == 'Get Component Vector From Point':
        try:
            point_display_value_x, point_display_value_y = get_field_strength_from_point()
            window['ox'].update(value=f'x: {point_display_value_x:.6e}')
            window['oy'].update(value=f'y: {point_display_value_y:.6e}')
            window.Refresh()
        except Exception as e:
            print(e)

    if event == 'Export Data':
        try:
            export_data()
        except Exception as e:
            print(e)

    if event == 'New Num Vectors':
        try:
            clear_all_vectors()
            ARROWS = int(values['num_vectors'])
            mass_vector_draw()
        except Exception as e:
            print(e)
    
    if event == 'New Vector Length':
        try:
            clear_all_vectors()
            ARROW_SIZE = int(values['vector_length'])
            mass_vector_draw()
        except Exception as e:
            print(e)

    if event == "Exit" or event == sg.WINDOW_CLOSED:
        break

window.close()
