from rl.io.lib.engines.blessed import colors
s1 = colors.ColorString("This string is colored.")
print s1
s1.add_color(colors.blue, 5, 11)
s1.add_color(colors.red, 11, len(s1))
print s1

s2 = colors.ColorString("  This one is too.")
print s2

s2.add_color(colors.green, 2, 6)
print s2

print s1 + s2