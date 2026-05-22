from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField()
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()

    def grade(self):

        if self.marks >= 80:
            return "A+"

        elif self.marks >= 70:
            return "A"

        elif self.marks >= 60:
            return "A-"

        elif self.marks >= 50:
            return "B"

        elif self.marks >= 40:
            return "C"

        elif self.marks >= 33:
            return "D"

        return "F"


    def average_grade(self):

        students = Student.objects.filter(
            name=self.name,
            roll=self.roll
        )

        total_points = 0

        for student in students:

            if student.marks >= 80:
                total_points += 5

            elif student.marks >= 70:
                total_points += 4

            elif student.marks >= 60:
                total_points += 3.5

            elif student.marks >= 50:
                total_points += 3

            elif student.marks >= 40:
                total_points += 2

            elif student.marks >= 33:
                total_points += 1

        avg = total_points / students.count()

        if avg >= 4.5:
            return "A+"

        elif avg >= 3.75:
            return "A"

        elif avg >= 3.25:
            return "A-"

        elif avg >= 2.5:
            return "B"

        elif avg >= 1.5:
            return "C"

        elif avg >= 1:
            return "D"

        return "F"