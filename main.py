import curses
import time


def make_directions(lines):
    directions = []
    for line in lines:
        if line < 4:
            y = (line - 1) * 3
            for x in range(4):
                directions.append([x, y])
        elif line == 4 or line == 5:
            x = 0 if line == 4 else 3
            for y in range(4):
                directions.append([x, y])
        elif line == 6 or line == 7:
            x = 0 if line == 6 else 3
            for y in range(3, 7):
                directions.append([x, y])

    return directions


digit_directions_dic = {
    0: [1, 5, 7, 3, 6, 4],
    1: [5, 7],
    2: [1, 5, 2, 6, 3],
    3: [1, 5, 2, 7, 3],
    4: [4, 2, 5, 7],
    5: [1, 4, 2, 7, 3],
    6: [1, 4, 6, 3, 7, 2],
    7: [1, 5, 7],
    8: [1, 2, 3, 4, 5, 6, 7],
    9: [2, 4, 1, 5, 7, 3],
                        }

digit_directions = {}

d_dirs = [
    [1, 2],
    [1, 4],
]

source = open('main.py').read()
source = source.splitlines()
source.remove('')
source = ' '.join(source)

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)

curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)

lines_len = len(source) // 25
lines_count = 25 if len(source) % 5 == 1 else 26
source_lines = []
for i in range(lines_count):
    stdscr.addstr(i + 4, 4, source[i * lines_len: (i + 1) * lines_len])
    source_lines.append(source[i * lines_len: (i + 1) * lines_len])
stdscr.refresh()
time_check = ''
t = ''


def get_time():
    global time, time_check, t
    hours = time.localtime().tm_hour
    mins = time.localtime().tm_min
    secs = time.localtime().tm_sec
    time_check = f'{hours} : {mins} : {secs}'
    t = f'{hours} : {mins} : {secs}'
    t = f'0{hours} : {mins} : {secs}' if hours < 10 else t
    t = f'{hours} : 0{mins} : {secs}' if mins < 10 else t
    t = f'{hours} : {mins} : 0{secs}' if secs < 10 else t
    return t


def print_time(tm, color):
    count = 0
    for c in tm:
        try:
            int(c)
            is_digit = True
        except:
            is_digit = False
        if is_digit:
            if c not in digit_directions:
                dirs = make_directions(digit_directions_dic[int(c)])
                digit_directions[c] = dirs
            for n in digit_directions[c]:
                if color == 1:
                    stdscr.addstr(n[1] + 8, n[0] + 8 + count, source_lines[n[1] + 4][n[0] + 4 + count], curses.color_pair(1))
                else:
                    stdscr.addstr(n[1] + 8, n[0] + 8 + count, source_lines[n[1] + 4][n[0] + 4 + count])
            count += 5
        elif c == ':':
            for n in d_dirs:
                if color == 1:
                    stdscr.addstr(n[1] + 8, n[0] + 8 + count, source_lines[n[1] + 4][n[0] + 4 + count], curses.color_pair(1))
                else:
                    stdscr.addstr(n[1] + 8, n[0] + 8 + count, source_lines[n[1] + 4][n[0] + 4 + count])
            count += 4
        else:
            count += 1
    stdscr.refresh()


print_time(get_time(), 1)

running = True
while running:
    if time_check != f'{time.localtime().tm_hour} : {time.localtime().tm_min} : {time.localtime().tm_sec}':
        print_time(t, 0)
        print_time(get_time(), 1)

curses.napms(3000)
curses.endwin()
