import math

tooth_count = int(input("Please enter tooth count: "))
pitch = int(input("Please enter pitch (mm): "))

interior_angle = (180 + (tooth_count - 3) * 180) / 16
radius = math.sin(math.radians(interior_angle / 2)) / (math.sin(math.radians(180 - interior_angle)) / pitch )
arc_length = (2 * radius * math.pi) / tooth_count

print(f"Diameter: {2 * radius}mm")
print(f"Arc Length (tooth width): {arc_length}mm")