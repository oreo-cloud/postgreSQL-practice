import psycopg2
import configparser

# import config file
config = configparser.ConfigParser()
config.read('config.ini')
insert = False

def create_tables(sql, db):
  # Create four tables ( employee, works, company, manages )
  sql.execute("""
              CREATE TABLE employee (
                  employee_name VARCHAR(255) PRIMARY KEY, 
                  street VARCHAR(255), 
                  city VARCHAR(255)
              )
              """)

  sql.execute("""
              CREATE TABLE works (
                  employee_name VARCHAR(255) PRIMARY KEY, 
                  company_name VARCHAR(255), 
                  salary INT
              )
              """)

  sql.execute("""
              CREATE TABLE company (
                  company_name VARCHAR(255), 
                  city VARCHAR(255),
                  PRIMARY KEY (company_name, city)
              )
              """)

  sql.execute("""
              CREATE TABLE manages (
                  employee_name VARCHAR(255) PRIMARY KEY, 
                  manager_name VARCHAR(255)
              )
              """)
  
  db.commit()
  
def insert_data(sql, db):
  # 插入 employee 資料
  employee_data = [
    ('Ken', '123 Maple St', 'First-City'),
    ('Jane Smith', '456 Oak St', 'Land-City'),
    ('Emily Johnson', '789 Pine St', 'Third-City'),
    ('Michael Brown', '101 Birch St', 'First-City'),
    ('Sarah Davis', '202 Cedar St', 'Land-City'),
    ('David Wilson', '303 Elm St', 'First-City'),
    ('Laura White', '404 Ash St', 'Land-City'),
    ('James Moore', '505 Poplar St', 'First-City')
  ]

  sql.executemany('INSERT INTO employee (employee_name, street, city) VALUES (%s, %s, %s)', employee_data)

  # 插入 company 資料
  company_data = [
    ('First-Bank', 'First-City'),
    ('First-Bank', 'Land-City'),
    ('First-Bank', 'Third-City'),
    ('Land-Bank', 'Land-City'),
    ('Land-Bank', 'First-City'),
    ('Third-Bank', 'Third-City'),
    ('Third-Bank', 'First-City')
  ]

  sql.executemany('INSERT INTO company (company_name, city) VALUES (%s, %s)', company_data)

  # 插入 works 資料
  works_data = [
      ('Ken', 'First-Bank', 70000),
      ('Jane Smith', 'Land-Bank', 80000),
      ('Emily Johnson', 'Third-Bank', 75000),
      ('Michael Brown', 'First-Bank', 72000),
      ('Sarah Davis', 'Land-Bank', 83000),
      ('David Wilson', 'First-Bank', 78000),
      ('Laura White', 'Land-Bank', 69000),
      ('James Moore', 'First-Bank', 85000)
  ]

  sql.executemany('INSERT INTO works (employee_name, company_name, salary) VALUES (%s, %s, %s)', works_data)

  # 插入 manages 資料
  manages_data = [
      ('Ken', 'Jane Smith'),
      ('Jane Smith', 'Emily Johnson'),
      ('Michael Brown', 'David Wilson'),
      ('Sarah Davis', 'James Moore')
  ]

  sql.executemany('INSERT INTO manages (employee_name, manager_name) VALUES (%s, %s)', manages_data)
  
  db.commit()

def print_selection():
    print( "======postgreSQL practice======" )
    print( "0  : EXIT" )
    print( "=============================" )
    print( "1 : 5-1" )
    print( "2 : 5-2" )
    print( "3 : 5-3" )
    print( "4 : 5-4" )
    print( "5 : 5-8" )
    print( "=============================" )
    print( "6 : Help", end="\n\n" )

def print_help():
    print( "Welcom to postgreSQL testing system" )
    print( "(0:  EXIT): quit system." )
    print( "================================================================================================" )
    print( "(1:  5-1): a). Find the employees of all employees who not work for First Bank." )
    print( "           b). Find the employees whose salary is higher than their company's average salary." )
    print( "(2:  5-2): a). Find the employees who earn more than each employee of Land Bank" )
    print( "           b). Find the company that has the most employees." )
    print( "(3:  5-3): Find all companies located in every city in which Land Bank is located" )
    print( "(4:  5-4): a). Find the company that has smallest payroll" )
    print( "           b). Find those companies whose employees earn a higher salary, on average, than the average salary at First Bank" )
    print( "(5:  5-8): Find the manager name and the average salary of all employees who work for that manager." )
    print( "================================================================================================" )
    print( end="\n\n" )

def check_selection( command ):
    if command >= 0 and command <= 12:
        return True
    else:
        return False

def check_part( part ):
    return part.lower()

def question_5_1(sql, db, part):
  if part == 'a':
    # Find the employees of all employees who not work for First Bank.
    sql.execute("""
                CREATE OR REPLACE VIEW question_5_1_a AS
                SELECT employee_name, company_name
                FROM works 
                WHERE company_name != 'First-Bank'
                """)
    db.commit()
    
    sql.execute("""SELECT * FROM question_5_1_a;""")
    
    employees = sql.fetchall()
  
    print( "People who don't work in First bank :" )
    
    for employee in employees:
        print( f'\033[34m{employee[0]}\033[0m is work in \033[34m{employee[1]}\033[0m' )
        
  elif part == 'b':
    # Find the average salary of each company ( to compare not for ans )
    sql.execute("""
                CREATE OR REPLACE VIEW question_5_1_b_compare AS
                SELECT company_name, AVG(salary) as avg_salary
                FROM works
                GROUP BY company_name;
                """)
    db.commit()
    
    sql.execute("""SELECT * FROM question_5_1_b_compare;""")
    avg_salary = sql.fetchall()
    
    
    # subquery to find the employees whose salary is higher than their company's average salary.
    sql.execute("""
                CREATE OR REPLACE VIEW question_5_1_b AS
                SELECT w1.employee_name, company_name, salary
                FROM works w1 
                WHERE w1.salary > (
                    SELECT AVG(w2.salary) as avg
                    FROM works w2 
                    WHERE w1.company_name = w2.company_name
                )
                """)
    
    db.commit()
    
    sql.execute("""SELECT * FROM question_5_1_b;""")
    employees = sql.fetchall()
    
  
    print( "People whose salary is higher than the average salary in their bank :" )
    
    for employee in employees:
      avg = [round(x[1]) for x in avg_salary if x[0] == employee[1]]
      print( f"""\033[34m{employee[0]}\033[0m is work in \033[34m{employee[1]}\033[0m got \033[34m${employee[2]}\033[0m, and the average of the bank is \033[34m${avg}\033[0m""" )
    
  else:
    raise Exception(f"Invalid part {part}")
  
def question_5_2(sql, db, part):
  if part == 'a':
    # Find largest salary in Land Bank ( for compare )
    sql.execute("""
                CREATE OR REPLACE VIEW question_5_2_a_compare AS
                SELECT employee_name, salary
                FROM works
                WHERE company_name = 'Land-Bank' AND salary = (
                  SELECT MAX(salary)
                  FROM works
                  WHERE company_name = 'Land-Bank'
                )
                """)
    
    db.commit()
    
    sql.execute("""SELECT * FROM question_5_2_a_compare;""")
    
    land_max_salary = sql.fetchall()

    # Find the employees who earn more than each employee of Land Bank
    sql.execute("""
                CREATE OR REPLACE VIEW question_5_2_a AS
                SELECT w1.employee_name, w1.salary
                FROM works w1 
                WHERE w1.salary > ALL (
                    SELECT w2.salary 
                    FROM works w2 
                    WHERE w2.company_name = 'Land-Bank'
                )
                """)
    db.commit()
    
    sql.execute("""SELECT * FROM question_5_2_a;""")
    
    employees = sql.fetchall()
    
    
    for salary in land_max_salary:
      print( f"Whose salary is more than each employee of Land Bank ( MAX ${salary[1]} )" )
    
    for employee in employees:
      print( f"\033[34m{employee[0]}\033[0m got \033[34m{employee[1]}\033[0m" )

  elif part == 'b':
    # Find the company that has the most employees.
    # Sorted and get the first one
    sql.execute("""
                CREATE OR REPLACE VIEW question_5_2_b AS
                SELECT company_name, COUNT(employee_name) as employee_count
                FROM works
                GROUP BY company_name
                ORDER BY employee_count DESC
                LIMIT 1
                """)
    db.commit()
    
    sql.execute("""SELECT * FROM question_5_2_b;""")
    
    company = sql.fetchone()
    
    print( f"\033[34m{company[0]}\033[0m has the most employees( \033[34m{company[1]}\033[0m people in this company )" )
    
  else:
    raise Exception(f"Invalid part {part}")

def question_5_3(sql, db):
  # Find all companies located in every city in which Land Bank is located
  # Using EXCEPT to find the difference between two sets
  # Use Not Exists to check if the difference is empty
  sql.execute("""
              CREATE OR REPLACE VIEW question_5_3 AS
              SELECT DISTINCT company_name
              FROM company AS c1
              WHERE NOT EXISTS (
                  SELECT city
                  FROM company
                  WHERE company_name = 'Land-Bank'
                  EXCEPT
                  SELECT city
                  FROM company AS c2
                  WHERE c1.company_name = c2.company_name
              )
              """)
  
  db.commit()
  
  sql.execute("""SELECT * FROM question_5_3;""")
  companies = sql.fetchall()
  

  print("Companies located in every city where Land Bank is located:")
  for company in companies:
      print(f'\033[34m{company[0]}\033[0m')

def question_5_4(sql, db, part):
  if part == 'a':
    sql.execute("""
                CREATE OR REPLACE VIEW question_5_4_a AS
                SELECT company_name, SUM(salary) as total_payroll
                FROM works
                GROUP BY company_name
                ORDER BY total_payroll ASC
                LIMIT 1
                """)
    
    db.commit()
    
    sql.execute("""SELECT * FROM question_5_4_a;""")
    smallest_payroll_company = sql.fetchone()
    

    print(f"Company with the smallest payroll: \033[34m{smallest_payroll_company[0]}\033[0m with total payroll \033[34m${smallest_payroll_company[1]}\033[0m")

  elif part == 'b':
    # Find the average salary at First-Bank
    sql.execute("""
                CREATE OR REPLACE VIEW question_5_4_b_compare AS
                SELECT company_name, AVG(salary) as avg_salary
                FROM works
                WHERE company_name = 'First-Bank'
                GROUP BY company_name
                """)
    
    db.commit()
    
    sql.execute("""SELECT * FROM question_5_4_b_compare;""")
    first_bank_avg = sql.fetchone()
    
    sql.execute("""
                CREATE OR REPLACE VIEW question_5_4_b AS
                SELECT company_name, AVG(salary) as avg_salary
                FROM works
                GROUP BY company_name
                HAVING AVG(salary) > (
                    SELECT AVG(salary)
                    FROM works
                    WHERE company_name = 'First-Bank'
                )
                """)
    
    db.commit()
    
    sql.execute("""SELECT * FROM question_5_4_b;""")
    companies = sql.fetchall()
    
    print( f"Companies whose employees earn a higher salary, on average, than the average salary at First-Bank( $\033[34m{round(first_bank_avg[1], 2)}\033[0m ):")
    for company in companies:
        print(f"\033[34m{company[0]}\033[0m with average salary \033[34m${round(company[1], 2)}\033[0m")

  else:
    raise Exception(f"Invalid part {part}")

def question_5_8(sql, db):
  sql.execute("""
              CREATE OR REPLACE VIEW question_5_8 AS
              SELECT m.manager_name, AVG(w.salary) as avg_salary
              FROM manages m
              JOIN works w ON m.employee_name = w.employee_name
              GROUP BY m.manager_name;
              """)

  db.commit()

  sql.execute("SELECT * FROM question_5_8;")
  results = sql.fetchall()
  
  print("The average salary of employees managed by each manager:")
  for result in results:
    print(f"\033[34m{result[0]}\033[0m: \033[34m${round(result[1], 2)}\033[0m")
    
def add_referential_integrity_constraint(sql, db):
    sql.execute("""
        ALTER TABLE works
        ADD CONSTRAINT fk_employee_name
        FOREIGN KEY (employee_name) REFERENCES employee(employee_name)
    """)
    db.commit()

def add_check_constraint(sql, db):
    sql.execute("""
                ALTER TABLE works
                ADD CONSTRAINT check_employee_exists
                CHECK (employee_name IN (SELECT employee_name FROM employee))
                """)
    db.commit()

def test_constraints(sql, db):
    try:
        sql.execute("""
            INSERT INTO works (employee_name, company_name, salary)
            VALUES ('NonExistentEmployee', 'Test-Company', 50000)
        """)
        db.commit()
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")    

def create_check_trigger_function(sql, db):
  sql.execute("""
              CREATE OR REPLACE FUNCTION check_employee_exists()
              RETURNS TRIGGER AS $$
              BEGIN
                  IF NOT EXISTS (SELECT 1 FROM employee WHERE employee_name = NEW.employee_name) THEN
                      RAISE EXCEPTION 'Employee % does not exist', NEW.employee_name;
                  END IF;
                  RETURN NEW;
              END;
              $$ LANGUAGE plpgsql;
              """)
  db.commit()

def create_check_trigger(sql, db):
  sql.execute("""
              CREATE TRIGGER check_employee_exists_trigger
              BEFORE INSERT OR UPDATE ON works
              FOR EACH ROW
              EXECUTE FUNCTION check_employee_exists();
              """)
  db.commit()

if __name__ == '__main__':
  command = -1

  # Establish a connection to the PostgreSQL database
  conn = psycopg2.connect(
    host=config['postgresql']['host'],
    port=config['postgresql']['port'],
    database=config['postgresql']['database'],
    user=config['postgresql']['user'],
    password=config['postgresql']['password']
  )

  sql = conn.cursor()
  if insert:
      create_tables(sql, conn)
      insert_data(sql, conn)
      add_referential_integrity_constraint(sql, conn)
      create_check_trigger_function(sql, conn)
      create_check_trigger(sql, conn)
      print("\033[46minsert data and add constraints!!!\033[0m")


  while ( True ):
    try:
        while True:
            print_selection()
            command = int(input("Enter a command : "))
            if check_selection( command ):
                break
            raise Exception("Invalid command")

        if command == 0:
            print("\033[92mThank you for using the system. Goodbye!\033[0m")
            break
          
        elif command == 1:
          # question 5-1
          part = check_part(input("Which part do you want to do? (a or b) : "))
          print()
          question_5_1(sql, conn, part)
          print()
        
        elif command == 2:
          # question 5-2
          part = check_part(input("Which part do you want to do? (a or b) : "))
          print()
          question_5_2(sql, conn, part)
          print()
          
        elif command == 3:
          print()
          question_5_3(sql, conn)
          print()

        elif command == 4:
          part = check_part(input("Which part do you want to do? (a or b) : "))
          print()
          question_5_4(sql, conn, part)
          print()

        elif command == 5:
          print()
          question_5_8(sql, conn)
          print()

        elif command == 6:
          print_help()
            
        else:
          print("Invalid command")
        
    except Exception as ex:
      # exception handling, the error message will be printed
      # the message shouldn't include .
      print( f"\033[91mError: {ex}. Please try again.\033[0m", end="\n\n" )
      continue

  # Close the cursor and connection
  sql.close()
  conn.close()