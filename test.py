ar = []
for r in range(0,len(input_ar)):
  ar.insert(r, [])
  
  for c in range(0,len(input_ar[r])):
    b_type = None
    if input_ar[r][c] == "0": b_type = 0
    elif input_ar[r][c] == "1": b_type = 1
    
    ar[r].insert(c,b_type)
    
    #--------------------------------------------------
    
    
