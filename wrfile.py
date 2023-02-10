import csv
   
        
def read():
    namelist=[]
    with open('./useridentification/driverdataset/csv/driver.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            if len(line)==2:
                namelist.append(line[0])
    
    
    return namelist

def read_ear(name):
     with open('./useridentification/driverdataset/csv/driver.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            if len(line)==2:
                if line[0]==name:
                    return line[1]
    

def write(text):
    with open('./useridentification/driverdataset/csv/driver.csv', mode='a') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(text)    
            