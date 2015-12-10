from rl.ui.terminal.modes.menu import SingleSelectMenuMode
from rl.save import list_saves, load_world

def load_selected_world(selected):
    w = load_world(selected)
    return w

load_save_menu = SingleSelectMenuMode(
    items={str(num + 1): save for num, save in enumerate(list_saves())},
    selected_callback=load_selected_world,
    exit_on_select=True
)