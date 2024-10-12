import numpy as np

def calculate_angle(v1, v2):
    cos_theta = np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1, 1)
    return np.degrees(np.arccos(cos_theta))

def cubic_zone_angle(hkl1, hkl2):
    return calculate_angle(np.array(hkl1), np.array(hkl2))

def hexagonal_zone_angle(hkil1, hkil2):
    v1 = np.array([hkil1[0] - hkil1[1], hkil1[1], hkil1[2], hkil1[3]])
    v2 = np.array([hkil2[0] - hkil2[1], hkil2[1], hkil2[2], hkil2[3]])
    return calculate_angle(v1, v2)

def calculate_and_display_angle(system_var, x1, x2, x3, x4, y1, y2, y3, y4, result_label):
    system = system_var.get()
    zone1 = [int(x1.get()), int(x2.get()), int(x3.get())] if system == 'Cubic' else [int(x1.get()), int(x2.get()), int(x3.get()), int(x4.get())]
    zone2 = [int(y1.get()), int(y2.get()), int(y3.get())] if system == 'Cubic' else [int(y1.get()), int(y2.get()), int(y3.get()), int(y4.get())]
    
    if system == 'Cubic':
        angle = cubic_zone_angle(zone1, zone2)
    else:
        angle = hexagonal_zone_angle(zone1, zone2)
    
    result_label.config(text=f"Angle between zone axes: {angle:.2f}°")

# Remove the main GUI part from this file, as it's now handled in main-gui.py
