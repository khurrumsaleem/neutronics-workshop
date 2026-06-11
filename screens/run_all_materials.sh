#!/bin/bash

# Run all material creation VHS tape files

echo "Running OpenMC Materials VHS demonstrations..."
echo ""

export VHS_NO_SANDBOX=true
export PYTHONWARNINGS=ignore

echo "1. Making materials from nuclides..."
vhs mat_nuclides.tape
# vhs --publish mat_nuclides.tape
echo ""

echo "2. Making materials from elements..."
vhs mat_elements.tape
# vhs --publish mat_elements.tape
echo ""

echo "3. Making materials from formulas..."
vhs mat_formulas.tape
# vhs --publish mat_formulas.tape
echo ""

echo "4. Making materials from components..."
vhs mat_components.tape
# vhs --publish mat_components.tape
echo ""

echo "All demonstrations completed!"
