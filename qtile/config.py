import os, subprocess
from libqtile import hook
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

colors = ['#2d0ecc',    # Purple
          '#30343F',    # Gray Background Bar
          '#ffffff',    # White
          '#000000',    # Black
          '#607fc4',    # Purplish Blue
          '#1793D1',    # Arch Blue
          '#57585b']    # Gray again

mod = "mod4"
alt = "mod1"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Switch between monitors
    Key([mod], "comma", lazy.to_screen(0)),
    Key([mod], "period", lazy.to_screen(1)),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "shift"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Launch applications
    Key([mod], "w", lazy.spawn('firefox'), desc="Launch Firefox"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "d", lazy.spawn('rofi -show drun'), desc="Launch Rofi"),
    Key([mod], "n", lazy.spawn('Thunar'), desc="Launch Thunar"),
    Key([mod], "p", lazy.spawn('flameshot gui'), desc="Screenshot"),
    Key([mod, "shift"], "p", lazy.spawn('flameshot full'), desc="Take Fullscreen Screenshot"),

    # Rofi shortcuts
    Key([alt], "Tab", lazy.spawn('rofi -show window'), desc="See Open Apps"),
    Key([alt], "e", lazy.spawn('rofi -show emoji'), desc="Emoji Selector"),
    Key([alt], "c", lazy.spawn('rofi -show calc -no-show-match -no-sort'), desc="Calculator"),

    # Picom shortcuts
    Key([alt], "p", lazy.spawn('picom -b'), desc="Launch picom"),
    Key([alt, "shift"], "p", lazy.spawn('killall picom'), desc="Kill picom"),


    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "shift"], "s", lazy.spawn('sudo poweroff'), desc="Shutdown System"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Media control
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer --decrease 5")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer --increase 5")),
    Key([], "XF86AudioMute", lazy.spawn("pamixer --toggle-mute")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),

    # Brightness control
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    # Choose monitor setup
    Key([mod, "control"], "1", lazy.spawn("autorandr main"), desc="Monitor only setup"),
    Key([mod, "control"], "2", lazy.spawn("autorandr laptop"), desc="Laptop only setup"),
    Key([mod, "control"], "3", lazy.spawn("autorandr duplicate"), desc="Duplicate setup"),

]

# groups = [Group(i) for i in "123456789"]
groups =[]

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

group_labels = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name = group_names[i],
            layout = group_layouts[i].lower(),
            label = group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
    "border_width": 2,
    "margin": 6,
    "border_focus": colors[4],
    "border_normal": colors[1]
}

layouts = [
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.MonadTall(**layout_theme),
    layout.Bsp(
        **layout_theme,
        border_on_single = True,
        margin_on_single = 6,
        grow_amount = 5,
        ),
    layout.Max(**layout_theme),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def unicode_arrow_widget(primary, secondary):
    return widget.TextBox(
               text = '???',
               background = colors[primary],
               foreground = colors[secondary],
               padding = -7,
               fontsize = 46,
           )

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    background = colors[1],
                ),
                widget.TextBox(
                    text = "??? ",
                    font = "FontAwesome",
                    fontsize = "20",
                    background = colors[1],
                    foreground = colors[5],
                    mouse_callbacks = {'Button1': lazy.spawn(terminal)}
                ),
                
                widget.GroupBox(
                    font="Ubuntu Bold",
                    fontsize = 14,
                    highlight_method="text",
                    margin_y = 3,
                    margin_x = 0,
                    padding_x = 6,
                    background = colors[1],
                    disable_drag = True,
                    this_current_screen_border = colors[5],
                    inactive = colors[6],
                    active   = colors[2],
                ),
                unicode_arrow_widget(1, 0),
                widget.WindowName(
                    foreground= colors[2],
                    font="Ubuntu Bold",
                    background = colors[0],
                    padding = 0,
                    fontsize = 12,
                ),
                widget.Cmus(
                    font = "Ubuntu Bold",
                    fontsize = "14",
                    foreground = colors[2],
                    background = colors[0],
                    padding = 12,
                    play_color = colors[2],
                    noplay_color = colors[6],
                    update_interval = 0.1,
                    ),
                unicode_arrow_widget(0, 1),
                widget.CurrentLayout(
                    font = "Ubuntu Bold",
                    background = colors[1],
                    padding = 2,
                    fontsize = 14,
                ),
                widget.TextBox(
                    text = "???",
                    font = "FontAwesome",
                    fontsize = 20,
                    padding = 10,
                    background = colors[1],
                    mouse_callbacks = {'Button1': lazy.next_layout()}
                ),
                
                widget.Sep(
                    linewidth = 0,
                    padding = 10,
                    background = colors[1],
                ),
                unicode_arrow_widget(1, 0),
                widget.TextBox(
                    text = "???",
                    font = "FontAwesome",
                    fontsize = 16,
                    padding = 8,
                    background = colors[0],
                    mouse_callbacks = {'Button1': lazy.spawn('pavucontrol')}
                ),
                widget.PulseVolume(
                    font = "Ubuntu Bold",
                    background = colors[0],
                    padding = 0,
                    device = 'ALC236 Analog',
                    fontsize = 14,
                ),
                
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    background = colors[0],
                ),
                unicode_arrow_widget(0, 1),
                widget.TextBox(
                    text = '???',
                    font = "FontAwesome",
                    padding = 10,
                    fontsize = 20,
                    background = colors[1],
                    mouse_callbacks = {'Button1': lazy.spawn('Thunar')}
                ),
                widget.DF(
                    font = "Ubuntu Bold",
                    visible_on_warn = False,
                    format = '{uf}{m} - {r:.0f}%',
                    background = colors[1],
                    fontsize = 14,
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    background = colors[1],
                ),
                unicode_arrow_widget(1, 0),
                widget.TextBox(
                    text = "???",
                    font = "FontAwesome",
                    fontsize = 20,
                    padding = 10,
                    background = colors[0],
                    mouse_callbacks = {'Button1': lazy.spawn('firefox   https://www.accuweather.com/en/ro/beclean/272299/current-weather/272299')}
                ),
                widget.OpenWeather(
                    font = "Ubuntu Bold",
                    cityid = 685204,
                    format = '{main_temp} ??{units_temperature}',
                    update_interval = "600",
                    background = colors[0],
                    fontsize = 14
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 10,
                    background = colors[0],
                ),
                unicode_arrow_widget(0, 1),
                widget.TextBox(
                    font = "FontAwesome",
                    text = "???",
                    foreground = colors[2],
                    background = colors[1],
                    padding = 6,
                    fontsize = 14,
                ),
                widget.Battery(
                    font = "Ubuntu Bold",
                    foreground = colors[2],
                    background = colors[1],
                    update_interval = 60,
                    format = '{percent:2.0%}  ',
                    fontsize = 14
                ),
                unicode_arrow_widget(1, 0),
                widget.TextBox(
                    font = "FontAwesome",
                    text = "???",
                    foreground = colors[2],
                    background = colors[0],
                    padding = 6,
                    fontsize = 20,                    
                    mouse_callbacks = {'Button1': lazy.spawn(terminal + ' -e calcure')}
                ),
                widget.Clock(
                    font = "Ubuntu Bold",
                    format="%A, %B %d - %H:%M:%S ",
                    background = colors[0],
                    foreground = colors[2],
                    padding=6,
                    fontsize = 14,
                ),
                unicode_arrow_widget(0, 1),
                widget.Systray(
                    background = colors[1],
                    padding=6,
                ),
                widget.QuickExit(
                    fontsize = 14,
                    font = "FontAwesome",
                    default_text = "???",
                    background = colors[1],
                    padding=12,
                    countdown_format = '[ {} ]'
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 12,
                    background = colors[1],
                ),
            ],
            24,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    background = colors[1],
                ),
                widget.TextBox(
                    text = "??? ",
                    font = "FontAwesome",
                    fontsize = "20",
                    background = colors[1],
                    foreground = colors[5],
                    mouse_callbacks = {'Button1': lazy.spawn(terminal)}
                ),
                
                widget.GroupBox(
                    font="Ubuntu Bold",
                    fontsize = 14,
                    highlight_method="text",
                    margin_y = 3,
                    margin_x = 0,
                    padding_x = 6,
                    background = colors[1],
                    disable_drag = True,
                    this_current_screen_border = colors[5],
                    inactive = colors[6],
                    active   = colors[2],
                ),
                unicode_arrow_widget(1, 0),
                widget.WindowName(
                    foreground= colors[2],
                    font="Ubuntu Bold",
                    background = colors[0],
                    padding = 0,
                    fontsize = 14,
                ),
                widget.Cmus(
                    font = "Ubuntu Bold",
                    fontsize = "14",
                    foreground = colors[2],
                    background = colors[0],
                    padding = 12,
                    play_color = colors[2],
                    noplay_color = colors[6],
                    update_interval = 0.1,
                    ),
                unicode_arrow_widget(0, 1),
                widget.TextBox(
                    text = "???",
                    font = "FontAwesome",
                    fontsize = 20,
                    padding = 10,
                    background = colors[1],
                    mouse_callbacks = {'Button1': lazy.spawn('firefox   crypto.com/price')}
                ),
                widget.CryptoTicker(
                    font = "Ubuntu Bold",
                    background = colors[1],
                    padding = 2,
                    fontsize = 14,
                    format = '{symbol}{amount:.2f}'
                ),
                
                widget.Sep(
                    linewidth = 0,
                    padding = 10,
                    background = colors[1],
                ),
                unicode_arrow_widget(1, 0),
                widget.TextBox(
                    text = "???",
                    font = "FontAwesome",
                    fontsize = 16,
                    padding = 8,
                    background = colors[0],
                    mouse_callbacks = {'Button1': lazy.spawn('pavucontrol')}
                ),
                widget.PulseVolume(
                    font = "Ubuntu Bold",
                    background = colors[0],
                    padding = 0,
                    device = 'ALC236 Analog',
                    fontsize = 14,
                ),
                
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    background = colors[0],
                ),
                unicode_arrow_widget(0, 1),
                widget.TextBox(
                    text = '???',
                    font = "FontAwesome",
                    padding = 10,
                    fontsize = 20,
                    background = colors[1],
                    mouse_callbacks = {'Button1': lazy.spawn('Thunar')}
                ),
                widget.DF(
                    font = "Ubuntu Bold",
                    visible_on_warn = False,
                    format = '{uf}{m} - {r:.0f}%',
                    background = colors[1],
                    fontsize = 14,
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    background = colors[1],
                ),
                unicode_arrow_widget(1, 0),
                widget.TextBox(
                    text = "???",
                    font = "FontAwesome",
                    fontsize = 20,
                    padding = 10,
                    background = colors[0],
                    mouse_callbacks = {'Button1': lazy.spawn('firefox   https://www.accuweather.com/en/ro/beclean/272299/current-weather/272299')}
                ),
                widget.OpenWeather(
                    font = "Ubuntu Bold",
                    cityid = 685204,
                    format = '{main_temp} ??{units_temperature}',
                    update_interval = "600",
                    background = colors[0],
                    fontsize = 14
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 10,
                    background = colors[0],
                ),
                unicode_arrow_widget(0, 1),
                widget.TextBox(
                    font = "FontAwesome",
                    text = "???",
                    foreground = colors[2],
                    background = colors[1],
                    padding = 6,
                    fontsize = 14,
                ),
                widget.Battery(
                    font = "Ubuntu Bold",
                    foreground = colors[2],
                    background = colors[1],
                    update_interval = 60,
                    format = '{percent:2.0%}  ',
                    fontsize = 14
                ),
                unicode_arrow_widget(1, 0),
                widget.TextBox(
                    font = "FontAwesome",
                    text = "???",
                    foreground = colors[2],
                    background = colors[0],
                    padding = 6,
                    fontsize = 20,                    
                    mouse_callbacks = {'Button1': lazy.spawn(terminal + ' -e calcure')}
                ),
                widget.Clock(
                    font = "Ubuntu Bold",
                    format="%A, %B %d - %H:%M:%S ",
                    background = colors[0],
                    foreground = colors[2],
                    padding=6,
                    fontsize = 14,
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 12,
                    background = colors[0],
                ),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])
