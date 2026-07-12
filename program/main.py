import json
import os

class TaskCLI:
  def __init__(self): 
   print("\n\twelcome to task Manager, hope you will find it helpfull 😇".upper())

   base_file = os.path.dirname(os.path.realpath(__file__))
   add_file = os.path.join(base_file, "tasks") 

   if not os.path.exists(add_file):
     os.makedirs(add_file)
   self.task_file = os.path.join(add_file, "task.json")

   self.load_task()      

  ##loads task from json file   
  def load_task(self):
    if not os.path.exists(self.task_file):
      with open(self.task_file, "w") as f:
          json.dump({"active": [], "completed": []}, f)
    try:
       with open(self.task_file, "r") as f:
         self.task_list = json.load(f)
    except json.JSONDecodeError:
      self.task_list = {"active": [], "completed": []}
       
  ##save task to file   
  def store_task(self):
      print("saving data....".upper())
      with open(self.task_file, 'w') as f:
       json.dump(self.task_list, f, indent=4)    
             
  def add_task(self):
     deadline = ""    
     while True:
       task_input = input(f"enter your task: ".title())
       if not task_input.strip():
         print("error! you didn't enter anything")
         continue
       else:
         priority = self.priority_mark()

       #"deadline"
       due_date = input("enter a due date and time dd-mm-yyyy hh:mm) or leave blank (enter m for menu): ")
       if due_date == 'm':
         return 
       if due_date.strip():
         deadline = due_date

       # "storing task in task"
       conform_deadline = input(f"you entered {task_input} & '{deadline if deadline else 'No deadline'}' y/n: ")

       if conform_deadline == 'y':
          storing_task = {"task": task_input, "status": "active", "priority": priority, "deadline": deadline} 
          self.task_list["active"].append(storing_task)
          self.store_task()
       elif conform_deadline.lower() == 'n':
          print("\tdidn'T saved, coming back to menu.....".title())  
          return
       else:
          print("try again".title())
          continue        
     
       option = input("\ny) for another task \nm) for menu \n\tenter choice: ".title())
       if option.lower() != 'y':
         break
             
  def delete_task(self):
    while True:
      self.show_tasks()
      input_delete = input("which task do your wish to delete or 'm': ".title())

      if input_delete.lower() == 'm':
       return
      if not input_delete.isdigit():
        print("invalid") 
        continue
       
      delete_this = int(input_delete)-1
      if delete_this <0 or delete_this >= len(self.task_list["active"]):
        print("out of range")
        continue
  
      this_task = self.task_list["active"].pop(delete_this)
      print(f"\n\t done!: '{this_task['task']}' has been removed".title())
      self.store_task()

  #showing task   
  def show_tasks(self):
    if not self.task_list['active']:
      print("\nno task to be found...".title())
    else:
      print("\n\tshowing your task...".title())
      active_task = self.task_list["active"]

      for i, item in enumerate(active_task, start=1):
        deadline = item.get('deadline')
        print(f"\nID: {i}. task: {item['task']} || priority: {item['priority']} || deadline: {deadline if deadline else 'no deadline'} || status: {item['status']}".title())

    priority_type = self.task_list["active"]
    print("\nyou can filter your task based on its priority".title())

    see_priority = set()
    j = 1
    for priority in priority_type:
      current_priority = priority['priority']

      if current_priority in see_priority:
        continue

      see_priority.add(current_priority)  
      print(f"{j}. {priority['priority']}")
      j += 1 

    num_list = {1: "high \u2b50", 2: "medium \u2b50", 3: "low \u2b50"}

    while True:
      user_input = input("enter your choice (or n to exit): ")
      if user_input == 'n':
        break
      if user_input.isdigit():
        take_input = int(user_input)  
        if take_input not in  num_list:
          print("try again!")
          continue
        search_key = num_list.get(take_input)
  
        for priority in priority_type:
          if search_key == priority['priority']:
            print(f'''
            task: {priority['task']}
            status: {priority['status']}    
            priority: {priority['priority']}
            daad line: {priority['deadline']}
            ''')
      else:
       print("\ninvalid try again".title())

   
         
  def mark_complete(self):
    while True:
      self.show_tasks() 
      if not self.task_list['active']:
        print("\nno avtive task to be found redirecting to menu".title())
        return
      else:
         complete_task = input("\nwhich task do you need to mark completed ✅: ".title())
         if complete_task == 'm':
           return
         if not complete_task.isdigit():
           print("invalid eneter vaid number....")
           continue
         elif complete_task == '':
           print("enter a option...😊")
           continue 
         else: 
           want_comp = int(complete_task)-1
           if want_comp < 0 or want_comp >= len(self.task_list['active']):
            print(f"invalid cant find {complete_task}")
            continue
           look_active = self.task_list["active"].pop(want_comp)
     
         self.task_list["completed"].append(look_active)
         print(f"\ndone! '{look_active['task']}' has been completed")
         self.store_task()
   
         option = input("still want to mark? 'y' or 'n': ")
         
         if option.lower() != 'y':
          return  

    
  def show_completed_task(self):
    while True:
     if not self.task_list['completed']:
       print("\n no completed task found...redirecting to menu".upper())
       return
     else:
       print("\ncompleted task...🫡".title())
       completed_task_show = self.task_list['completed']
 
       for i, task in enumerate(completed_task_show, start=1):
         deadline = task.get('deadline')
         print(f"{i}: ✅ {task['task']} || deadline: {deadline if deadline else 'no deadline'} || status: completed")
       
       delete_completed_in = input("enter 'y' to clear all completed task or 'm': ".title())  
       if delete_completed_in == 'y':
         self.task_list["completed"] = []
         self.store_task()
         print("\nall clear")
         break
       elif delete_completed_in == 'm':
         return
       else:
         print("\nsometing went wrong... retry".title())
         continue   

  def priority_mark(self):
    while True:
      pr_choice = input("""
      1. high
      2. medium
      3. low
      set a priority: """)

      if not pr_choice.isdigit():
        print("enter a valid number...")
        continue

      choice = int(pr_choice)
      if choice == 1:
        return "high ⭐"      
      elif choice == 2:
        return "medium 📊"      
      elif choice == 3:
        return "low 🎈" 
      else:
        print("enter a valid number....")
        continue       
    
  def menu(self):
    a = ("""\n====TASK MANAGER====\n
    1. add task 
    2. delete task
    3. show tasks
    4. mark competed task
    5. show completed task
    6. save & exit""".title())
    print(a)
  
  def run_app(self): 
    while True:
     self.menu()
     choice = input("\nenter your choice or 'm' for menu: ".title())
     if choice == '1':
       self.add_task()
     elif choice == '2':
       self.delete_task() 
     elif choice == '3':    
       self.show_tasks()
     elif choice == '4':
       self.mark_complete()
     elif choice == '5':
       self.show_completed_task() 
     elif choice == '6':
       print(""" \nData Saved
       Exiting...""") 
       break
     elif choice.lower() == 'm':
        continue
     else: 
       print("someting went wrong, enter a valid number".title())

if __name__ == "__main__":
  app = TaskCLI()
  app.run_app()



