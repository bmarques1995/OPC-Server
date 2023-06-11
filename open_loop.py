prev_in = 0.0
prev_out = 0.0

sys_in = 1

for i in range(400):
    
    sys_out = prev_in*.0306 + prev_out*.9235
    prev_in = sys_in
    prev_out = sys_out
    print(i, sys_out)