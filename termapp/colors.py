black = 0
red = 1
green = 2
yellow = 3
blue = 4
magenta = 5
cyan = 6
white = 7
bright_black = 8
bright_red = 9
bright_green = 10
bright_yellow = 11
bright_blue = 12
bright_magenta = 13
bright_cyan = 14
bright_white = 15

color_codes = {
    black: '\x1b[30m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m',
    white: '\x1b[37m',
    bright_black: '\x1b[90m',
    bright_red: '\x1b[91m',
    bright_green: '\x1b[92m',
    bright_yellow: '\x1b[93m',
    bright_blue: '\x1b[94m',
    bright_magenta: '\x1b[95m',
    bright_cyan: '\x1b[96m',
    bright_white: '\x1b[97m',
}

bgcolor_codes = {
    black: '\x1b[40m',
    red: '\x1b[41m',
    green: '\x1b[42m',
    yellow: '\x1b[43m',
    blue: '\x1b[44m',
    magenta: '\x1b[45m',
    cyan: '\x1b[46m',
    white: '\x1b[47m',
    bright_black: '\x1b[100m',
    bright_red: '\x1b[101m',
    bright_green: '\x1b[102m',
    bright_yellow: '\x1b[103m',
    bright_blue: '\x1b[104m',
    bright_magenta: '\x1b[105m',
    bright_cyan: '\x1b[106m',
    bright_white: '\x1b[107m',
}

colors = {
    'black': 0,
    'red': 1,
    'green': 2,
    'yellow': 3,
    'blue':4,
    'magenta':5,
    'cyan':6,
    'white':7,
    'bright_black':8,
    'bright_red':9,
    'bright_green':10,
    'bright_yellow':11,
    'bright_blue':12,
    'bright_magenta':13,
    'bright_cyan':14,
    'bright_white':15
}

color_names = dict(zip(colors.values(), colors.keys()))
bg_colors = {'_on_'+color_name: colors[color_name] for color_name in colors.keys()}
bg_color_names = dict(zip(bg_colors.values(), bg_colors.keys()))


