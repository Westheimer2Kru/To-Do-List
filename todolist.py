from sqlalchemy import create_engine
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime,timedelta, date

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline =  Column(Date,default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

exit = True
weeks = ["Monday","Tuesday","Wednesday",
         "Thursday","Friday","Saturday",
         "Sunday"]
today = datetime.today()

def print_all_tasks(rows):
    for i in range(len(rows)):
        print(f"{i+1}. {rows[i]}. {rows[i].deadline.strftime('%#d %b')}")
    print()

def days_tasks(date):
    rows = session.query(Table).\
            filter(Table.deadline == date.date()).all()
    if len(rows) == 0:
            print("Nothing to do!")
            print()
    else:
        print_all_tasks(rows)

while(exit):
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    print()

    answer = int(input())
    if answer == 0:
        exit = False
        print()

    elif answer == 1:
        print("Today:", today.strftime('%d %b'))
        days_tasks(today)

    elif answer == 2:
        for i in range(7):
            print(f"{weeks[(today + timedelta(days=i)).weekday()]}. {(today + timedelta(days=i)).strftime('%d %b')}:")
            days_tasks(today + timedelta(days=i))
            print()

    elif answer == 3:
        print("All tasks:")
        rows = session.query(Table).order_by(Table.deadline).all()
        print_all_tasks(rows)

    elif answer == 4:
        print("Missed tasks:")
        rows = session.query(Table).filter(Table.deadline < today.date()).all()
        if len(rows) == 0:
            print("Nothing is missed!")
            print()
        else:
            print_all_tasks(rows)

    elif answer == 5:
        print("Enter task")
        task = input()
        print("Enter deadline")
        year, month, day = input().split('-')
        deadline = date(int(year), int(month), int(day))
        print(deadline)
        new_row = Table(task = task,
                        deadline = deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
        print()

    elif answer == 6:
        print("Choose the number of the task you want to delete:")
        rows = session.query(Table).order_by(Table.deadline).all()
        print_all_tasks(rows)
        num = int(input())
        session.delete(rows[num-1])
        session.commit()
        print("The task has been deleted!")
        print()


print("Bye!")
