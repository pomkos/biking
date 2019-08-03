import PySimpleGUI as sg

layout = [[sg.Text('Your print statements appear here:'), sg.Text('', size=(15,1), key='_OUTPUT_')],
          [sg.Input()],
          [sg.Button('Show'), sg.Button('Exit')]]

window = sg.Window('Window Title', layout)

while True:  # Event Loop
    event, values = window.Read()
    values_added = int(values[0]) + 2
    print(values_added)
    #print(event, values)
    if event is None or event == 'Exit':
        break
    if event == 'Show':
        # Update the "output" element to be the value of "input" element
        window.Element('_OUTPUT_').Update(values_added)

window.Close()