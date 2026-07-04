class Student:
    def __init__(self, name, rollno):
        self.name = name;
        self.rollno = rollno;

class Employee:
    def __init__(self, emp_id, salary):
        self.emp_id = emp_id;
        self.salary = salary;

class TA(Student, Employee):
    def __init__(self, name, rollno, emp_id, salary):
        Student.__init__(self, name=name, rollno=rollno);
        Employee.__init__(self, emp_id=emp_id, salary=salary);

    # updating the structure of the object while printing the object;
    def __str__(self):
        objStruct = {
            "Name" : self.name,
            "Rollno" : self.rollno,
            "EmpID" : self.emp_id,
            "Salary" : self.salary
        }

        return f"{objStruct}"

    def update_name(self, name):
        """updating the name of the object"""
        self.name = name;

if __name__=='__main__':
    mohit = Student("Mohit Soni", 9);
    obj = TA("Mohit Soni", 145, "45656", 458);
    obj.update_name("Ishita");
    print(obj);
