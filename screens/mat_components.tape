# Configuration Settings
Output openmc_material_components.gif
Set Theme "Dracula"
Set FontSize 18
Set Width 900
Set Height 650
Set Padding 0
Set Margin 0
Set BorderRadius 0
Set TypingSpeed 100ms
Set PlaybackSpeed 2.0

# Launch IPython (autoindent off so typed indentation renders exactly as written)
Type "ipython --no-autoindent"
Enter
Sleep 2s

# Step 1: Import library
Type "import openmc"
Enter
Sleep 500ms

# Step 2: Create materials with components
Type "components = {"
Enter
Sleep 200ms
Type "    'Li': {'percent': 4,"
Enter
Sleep 200ms
Type "           'enrichment': 60.0,"
Enter
Sleep 200ms
Type "           'enrichment_target': 'Li7'},"
Enter
Sleep 200ms
Type "    'Si': 1.0,"
Enter
Sleep 200ms
Type "    'O': 4"
Enter
Sleep 200ms
Type "}"
Enter
Sleep 500ms

Type "fuel = openmc.Material("
Enter
Sleep 200ms
Type "    name='lithium_silicate',"
Enter
Sleep 200ms
Type "    components=components,"
Enter
Sleep 200ms
Type "    percent_type='ao',"
Enter
Sleep 200ms
Type "    density=1.11,"
Enter
Sleep 200ms
Type "    density_units='g/cm3'"
Enter
Sleep 200ms
Type ")"
Enter
Sleep 500ms

# Step 3: Add materials to a material collection
Type "materials = openmc.Materials([fuel])"
Enter
Sleep 500ms

# Step 4: View the materials
Type "materials"
Sleep 1s
Enter             # Displays the materials collection

# Final hold to let the user review the generated data
Sleep 5s
