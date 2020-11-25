import csv
import random
from collections import OrderedDict
from math import floor

class Day:
    def __init__(self, exams = [], name = None, day_num = None):
        self.exams = exams
        self.name = name
        self.day_num = day_num
        
        
class Node:
    def __init__(self, cargo = None, left = None, right = None):
        self.cargo = cargo
        self.left = left
        self.right = right
       
    def __str__(self):
        return str(self.cargo)


class Heap:
    def __init__(self, input_array = []):
        self.array = input_array
        if (input_array):
            self.build(input_array)

    def build(self, input_array):
        start = int(floor(len(input_array)/2)) - 1
        for i in range(start, -1, -1):
            self.heapify(i)

    def parent(self, i):
        return int(floor((i-1)/2))

    def left(self, i):
        return (2 * i + 1)

    def right(self, i):
        return (2 * i + 2)

    def heapify(self, i):
        l = self.left(i)
        r = self.right(i)
        size = self.size()
        if (l < size) and (self.array[l].cargo[1][5] < self.array[i].cargo[1][5]):
            smallest = l
        else:
            smallest = i
        if (r < size) and (self.array[r].cargo[1][5] < self.array[smallest].cargo[1][5]):
            smallest = r
        if (smallest != i):
            self.array[i], self.array[smallest] = self.array[smallest], self.array[i]
            self.heapify(smallest)

    def size(self):
        return len(self.array)

    def __str__(self):
        return str(self.array)

    def update_key(self, i, key):
        if(key > self.array[i]):
            self.array[i] = key
            self.heapify(i)
        else:
            self.array[i] = key
            parent = self.parent(i)
            while ((i > 0) and (self.array[parent] > self.array[i])):
                self.array[i], self.array[parent] = self.array[parent], self.array[i]
                i = parent
                parent = self.parent(i)

    def insert(self, key):
        size = self.size()
        i = size
        self.array.append(key)
        self.update_key(i, key)


class Scheduler:
    def __init__(self, file_name, prioritized = None):
        information = {}
        with open(file_name) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                information.update({row[0]: [row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]})
            self.dictionary = OrderedDict(information)
            #self.dictionary.pop('')
            self.dictionary.pop('\ufeffCourse Code')
        self.prioritized = prioritized
            
        # key: course code
        # value: ['Course Name', 'Course Instructor', 'Location', 'Start Time', 'Duration', 'Priority', 'Class', 'Date']
    
    def remove_exam(self, course_code):
        removed = self.dictionary.pop(course_code)
        return self.dictionary
    
    def input_exam(self):
        key = input("Enter course code: ")
        name = input("Enter course name: ")
        instructor = input("Enter course instructor: ")
        location = input("Enter location: ")
        start = input("Enter start time: ")
        duration = input("Enter duration: ")
        priority = input("Enter priority: ")
        studentclass = input("Enter class: ")
        info = [name, instructor, location, start, duration, priority, studentclass]
        self.dictionary.update({key : info})
        return self.dictionary
    
    def suggest_time_location_date(self):
        #parse through values in dictionary & if empty at indexes 2 & 3 suggest random location/time respectively
        times = [930, 1400, 1830]
        locations = ['MY-315', 'GB-304', 'BA-1180', 'MY-380', 'BA-2159', 'WB-119', 'BA-2185', 'EX-200', 'EX-100', 'EX-310', 'EX-320', 'WB-116', 'EX-300', 'MY-360', 'SF-3202', 'HA-403', 'WB-130', 'BA-1130', 'HA-410', 'WB-219', 'HA-316', 'MY-150', 'MS-3153', 'MS-2172', 'BA-2175', 'MY-330', 'GB-303', 'ZZ-VLAD', 'BA-1170', 'WY-119','HI-CART', 'ZZ-KNOX', 'HA-401', 'APSCDept-ComputerLab', 'BN-2N', 'BA-1160', 'SF-2202', 'MP-102', 'BA-2195']
        date = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
        for key, value in self.dictionary.items():
            if value[2] == '':
                value[2] = random.choice(locations) 
            if value [3] == '':
                value[3] = random.choice(times) 
            if value [7] == '':
                value[7] = random.choice(date)             
                
                
    def check_for_conflict(self):
        conflict = False
        for key, val in self.dictionary.items():
            temptime = val[3] 
            tempclass = val[6]
            temploc = val[2]
            for key2, val2 in self.dictionary.items():
                if key != key2:
                    if (temptime == val2[3] and tempclass == val2[6]):
                        conflict = True
                    elif (temptime == val2[3] and temploc == val2[2]):
                        conflict = True
        return conflict                
        
    def prioritize(self):
        exams = []
        for key, val in self.dictionary.items():
            temp = Node([key, val])
            exams.append(temp)
        prioritized = Heap(exams)
        self.prioritized = prioritized.array
        return self.prioritized
    
    
    def check_for_overload(self, input_class):
        output = False
        for i in range(len(self.prioritized)):
            #print(self.prioritized[i].cargo)
            exams1 = self.prioritized[i].cargo
            class1 = exams1[1][6]
            date1 = exams1[1][7]
            time1 = exams1[1][3]
            #print(class1, date1, time1)
            for j in range(len(self.prioritized)):
                #print(self.prioritized[j].cargo)
                exams2 = self.prioritized[j].cargo
                class2 = exams2[1][6]
                date2 = exams2[1][7]
                time2 = exams2[1][3]
                #print(class2, date2, time2)  
                for k in range(len(self.prioritized)):
                    #print(self.prioritized[k].cargo)
                    exams3 = self.prioritized[k].cargo
                    class3 = exams3[1][6]
                    date3 = exams3[1][7]
                    time3 = exams3[1][3]
                    #print(class3, date3, time3)  
                    if ((exams1 != exams2) and (exams2 != exams3) and (exams1 != exams3)):
                        if ((class1 == input_class) and (class2 == input_class) and (class3 == input_class)):
                            important = [[class1, int(date1), int(time1)], [class2, int(date2), int(time2)], [class3, int(date3), int(time3)]]
                            sort = sorted(sorted(important, key = lambda x: x[2]), key = lambda x: x[1])   
                            print(sort)
                            #if 3 consecutive in one day
                            if ((sort[0][1] == sort[1][1]) and (sort[1][1] == sort[2][1]) and (sort[0][1] == sort[2][1])):
                                if ((sort[0][2] == 930) and (sort[1][2] == 1400) and (sort[2][2] == 1830)):
                                    return True           
                                else:
                                    return False
                            #two exams on first day, one on second day
                            elif ((sort[0][1] == sort[1][1]) and ((sort[0][1] + 1) == sort[2][1])):
                                if ((sort[0][2] == 1400) and (sort[1][2] == 1830) and (sort[2][2] == 930)):
                                    return True
                                else:
                                    return False
                            #one exam on first day, two on second day
                            elif ((sort[1][1] == sort[2][1]) and ((sort[1][1] - 1) == sort[0][1])):
                                if ((sort[0][2] == 1830) and (sort[1][2] == 930) and (sort[2][2] == 1400)):
                                    return True
                                else:
                                    return False    
                            else:
                                return False
        return False

                            
    def display_schedule(self, output_file_name):
        with open(output_file_name, mode='w') as csv_file:
            fieldnames = ['Course Code', 'Course Name', 'Course Instructor', 'Location', 'Start Time', 'Duration', 'Priority', 'Class', 'Date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
            writer.writeheader()
            for i in range(len(self.prioritized)):
                exams = self.prioritized[i].cargo
                writer.writerow({'Course Code': exams[0], 'Course Name': exams[1][0], 'Course Instructor': exams[1][1], 'Location': exams[1][2], 'Start Time': exams[1][3], 'Duration': exams[1][4], 'Priority': exams[1][5], 'Class': exams[1][6], 'Date': exams[1][7]})        
                            
        
    def print_student_schedule(self, students_class):
        enrolled = []
        enrolled.append(["Course Code", "Course Name", "Course Instructor", "Location", 
                         "Start Time", "Duration", "Date"])
        for node in self.prioritized:
            temp = []
            if node.cargo[1][6] == students_class:
                temp.append(node.cargo[0])
                temp.append(node.cargo[1][0])
                temp.append(node.cargo[1][1])
                temp.append(node.cargo[1][2])
                temp.append(node.cargo[1][3])
                temp.append(node.cargo[1][4])
                temp.append(node.cargo[1][5])
                temp.append(node.cargo[1][7])
                enrolled.append(temp)
        filename = str(students_class + "schedule.csv")
        myFile = open(filename, 'w')
        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(enrolled)

if __name__ == "__main__":
    hi = Scheduler('small_tester_new.csv')
    lol = hi.dictionary
    print (lol)
    #hi.suggest_time_location_date()
    #print(lol)
    #print(hi.remove_exam('AER210H1'))
    #print(hi.input_exam())
    #print(hi.check_for_conflict()) 
    inorder = hi.prioritize()
    for node in inorder:
        print(node.cargo)
    print('\n')
    print(hi.check_for_overload('ECE'))
    #hi.display_schedule('hi2.csv')
    #hi.print_student_schedule("T1")
