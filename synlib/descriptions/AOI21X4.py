Desc = cellDescClass("AOI21X4")
Desc.properties["cell_leakage_power"] = "1254.852324"
Desc.properties["cell_footprint"] = "aoi21"
Desc.properties["area"] = "33.264000"
Desc.pinOrder = ['A0', 'A1', 'B0', 'Y']
Desc.add_arc("A0","Y","combi")
Desc.add_arc("A1","Y","combi")
Desc.add_arc("B0","Y","combi")
Desc.add_param("area",33.264000);
Desc.add_pin("A1","input")
Desc.add_pin("A0","input")
Desc.add_pin("B0","input")
Desc.add_pin("Y","output")
Desc.add_pin_func("Y","unknown")
CellLib["AOI21X4"]=Desc
