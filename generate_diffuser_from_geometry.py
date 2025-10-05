from func_core import generate_diffuser_from_geometry

# basic geometry parameters
AC_deg = 90                 # 4 quadrant angle of vector A in degrees
BC_deg = 180                # 4 quadrant angle of vector B in degrees

# chord parameters
chord = 200                 # chord length of OUTER diffuser curve
stretch = 0.70              # stretch of CENTRAL curve (height / width)

# diffuser parameters
thick = 2                   # thickness of the vanes
inlet = 21 - thick          # width of inlet
outlet = 42 - thick         # width of outlet

# simulation parameters
acc = 0.000000001           # solution accuracy
limit = 100                 # maximum number of iterations
verb = False                # change verbosity of script

# Recommended settings
suggested_gap_to_chord = 0.230  # This value comes from my PhD research
suggested_chord = ((inlet + thick)**2 + (outlet + thick)**2)**0.5 / suggested_gap_to_chord
print(f'suggested chord is {suggested_chord} based on a gap-to-chord ratio of {suggested_gap_to_chord}')

# Execute core function
generate_diffuser_from_geometry(inlet, outlet, stretch, chord, AC_deg, BC_deg, thick, acc, limit)