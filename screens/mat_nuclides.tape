# Configuration Settings
Output openmc_material_nuclides.gif
Set Theme "Dracula"
Set FontSize 18
Set Width 900
Set Height 650
Set Padding 0
Set Margin 0
Set BorderRadius 0
Set TypingSpeed 100ms
Set PlaybackSpeed 2.0

# Launch IPython
Type "ipython"
Enter
Sleep 2s

# Step 1: Import library
Type "import openmc"
Enter
Sleep 500ms

# Step 2: Create a Material object
Type "mat1 = openmc.Material()"
Enter
Sleep 500ms

# Step 3: Add a nuclide
Type "mat1.add_nuclide('Li6', 1)"
Enter
Sleep 500ms

# Step 4: Set the density
Type "mat1.set_density('g/cm3', 2.1)"
Enter
Sleep 500ms

# Step 5: Evaluate the object representation
Type "mat1"
Sleep 1s
Enter             # Displays the underlying REPL object printout

# Final hold to let the user review the generated data
Sleep 5s
