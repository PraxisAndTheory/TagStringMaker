'''
Simple GUI that allows for easy creation a subset of delimiter separated strings
Developed using the Add and "Delete" Rows from a window recipe from PySimpleGUI as a base
'''

import PySimpleGUI as sg


def item_row(item_num):
    """
    A "Row" in this case is a Button with an "X", an Input element and a Text element showing the current counter
    :param item_num: The number to use in the tuple for each element
    :type:           int
    :return:         List
    """
    row =  [sg.pin(sg.Col([[sg.Checkbox(f'{item_num}', k=('-STATUS-', item_num))]], k=('-ROW-', item_num))),
                            sg.In(size=(20,1), k=('-DESC-', item_num)),
                            sg.B("X", border_width=0, button_color=(sg.theme_text_color(), sg.theme_background_color()), k=('-DEL-', item_num), tooltip='Delete this item')]
    return row


def make_window(title):

    layout = [  [sg.Text('Create and Select the tags you need then press Generate!', font='_ 15')],
                [sg.Col([item_row(0)], k='-TRACKING SECTION-')],
                [sg.pin(sg.Text(size=(35,1), font='_ 8', k='-REFRESHED-',))],
                [sg.Text('Output', font='_ 15'), sg.In(size=(20,1), disabled=True, k='-OUTPUT-')],
                [sg.T('+', enable_events=True, k='Add Item', pad = (40, 0), tooltip='Add Another Item'), sg.T('Generate', enable_events=True, k='Generate',  pad = (40, 0), tooltip='Save Changes & Refresh'), sg.T("X", enable_events=True, k='Exit', pad = (40, 0), tooltip='Exit Application')]]

    right_click_menu = [[''], ['Add Item',  'Version']]

    window = sg.Window(title, layout,  right_click_menu=right_click_menu, use_default_focus=False, font='_ 15', metadata=0)

    return window


def main():

    window = make_window("Tag String Maker")
    while True:
        event, values = window.read()     # wake every hour
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Add Item':
            window.metadata += 1
            window.extend_layout(window['-TRACKING SECTION-'], [item_row(window.metadata)])
        elif event == 'Version':
            sg.popup_scrolled(__file__, sg.get_versions(), location=window.current_location(), keep_on_top=True, non_blocking=True)
        elif event[0] == '-DEL-':
            window[('-ROW-', event[1])].update(visible=False)
        elif event == 'Generate':
            checked_values = []
            delimiter = ' '
            for value in values:
                if len(value) == 2 and value[0] == '-STATUS-' and values[value] == True:
                    print(f'{value} is true!')
                    checked_values.append(values[('-DESC-', value[1])])
            window['-OUTPUT-'].update(value = delimiter.join(checked_values))
    window.close()


if __name__ == '__main__':
    main()
