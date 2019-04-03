import csv

class f_manager:
    def __init__(self):
        pass

    def create_save_file(self,world_ar):
        with open("world.csv",'wb') as csvfile:
            filewriter = csv.writer(csvfile)

            for row in world_ar:
                filewriter.writerow(row)

    def read_save_file(self,name):
        rtn_ar = []
        with open(name) as f:
            reader = csv.reader(f)

            for row in reader:
                rtn_ar.append(row)

        return rtn_ar

    def csv_str_convert(self,input_ar):
        ar = []

        y_len = len(input_ar)
        x_len = len(input_ar[0])

        for r in range(0,y_len):
            ar.insert(r, [])
      
            for c in range(0,x_len):
                b_type = None
                if input_ar[r][c] == "0": b_type = 0
                elif input_ar[r][c] == "1": b_type = 1
        
                ar[r].insert(c,b_type)
        return ar
