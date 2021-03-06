import PySimpleGUI as sg
import psutil
import operator

"""
    PSUTIL Desktop Widget
    Creates a floating CPU utilization window that is always on top of other windows
    You move it by grabbing anywhere on the window
    Good example of how to do a non-blocking, polling program using PySimpleGUI
    Use the spinner to adjust the number of seconds between readings of the CPU utilizaiton

    NOTE - you will get a warning message printed when you exit using exit button.
    It will look something like:
            invalid command name "1616802625480StopMove"
"""

# ----------------  Create Form  ----------------
sg.ChangeLookAndFeel('Black')
form_rows = [[sg.Text('', size=(8,1), font=('Helvetica', 20),text_color=sg.YELLOWS[0], justification='center', key='text')],
             [sg.Text('', size=(30, 8), font=('Courier', 10),text_color='white', justification='left', key='processes')],
             [sg.Exit(button_color=('white', 'firebrick4'), pad=((15,0), 0)), sg.Spin([x+1 for x in range(10)], 1, key='spin')]]

form = sg.FlexForm('CPU Utilization', no_titlebar=True, auto_size_buttons=False, keep_on_top=True, grab_anywhere=True)
form.Layout(form_rows)

# ----------------  main loop  ----------------
while (True):
    # --------- Read and update window --------
    button, values = form.ReadNonBlocking()

    # --------- Do Button Operations --------
    if values is None or button == 'Exit':
        break
    try:
        interval = int(values['spin'])
    except:
        interval = 1

    cpu_percent = psutil.cpu_percent(interval=interval)

    # --------- Create list of top % CPU porocesses --------
    top = {proc.name() : proc.cpu_percent() for proc in psutil.process_iter()}

    top_sorted = sorted(top.items(), key=operator.itemgetter(1), reverse=True)
    top_sorted.pop(0)
    display_string = ''
    for proc, cpu in top_sorted:
        display_string += '{} {}\n'.format(cpu, proc)

    # --------- Display timer in window --------
    form.FindElement('text').Update('CPU {}'.format(cpu_percent))
    # form.FindElement('processes').Update('\n'.join(top_sorted))
    form.FindElement('processes').Update(display_string)

# Broke out of main loop. Close the window.
form.CloseNonBlockingForm()
