import sqlite3

def create_database(course_name, questions):
    # Connect to SQLite database (it will be created if it doesn't exist)
    database_name = f"{course_name}.db"
    conn = sqlite3.connect(f"{course_name}.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_text TEXT,
                    option_A TEXT,
                    option_B TEXT,
                    option_C TEXT,
                    option_D TEXT,
                    correct_answer TEXT)''')
    print("Table 'questions' created (if it didn't exist).")
    
    for question in questions:
        cursor.execute('''INSERT INTO questions (question_text, option_A, option_B, option_C, option_D, correct_answer)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (question['question_text'], question['option_A'], question['option_B'], 
                        question['option_C'], question['option_D'], question['correct_answer']))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database for {course_name} created successfully.")

def get_questions_from_database(course_name):
    # Connect to the appropriate SQLite database based on the course name
    conn = sqlite3.connect(f"{course_name}.db")
    cursor = conn.cursor()
    
    # Fetch all questions from the 'questions' table
    cursor.execute("SELECT question_text, option_A, option_B, option_C, option_D, correct_answer FROM questions")
    questions = cursor.fetchall()
    
    # Close the connection to the database
    conn.close()

    # Return the questions as a list of dictionaries
    question_list = []
    for q in questions:
        question_list.append({
            'question_text': q[0],
            'option_A': q[1],
            'option_B': q[2],
            'option_C': q[3],
            'option_D': q[4],
            'correct_answer': q[5]
        })
    
    return question_list
    
# Define the questions for each class
principles_of_managerial_finance = [
    {'question_text':"What is the primary goal of financial management?",'option_A': "Minimizing expenses", 'option_B': "Maximizing profits", 'option_C': "Maximizing shareholder wealth", 'option_D': "Increasing market share", 'correct_answer': "C"},
    {'question_text': "Which of the following is a source of long-term financing?", 'option_A': "Trade credit", 'option_B': "Commercial paper", 'option_C': "Common stock", 'option_D': "Bank overdraft", 'correct_answer': "C"},
    {'question_text': "The time value of money concept suggests?", 'option_A': "A dollar today is worth less than a dollar in the future", 'option_B': "Money loses value only due to inflation", 'option_C': "A dollar today is worth more than a dollar in the future", 'option_D': "Future cash flows are not important", 'correct_answer': "C"},
    {'question_text': 'The weighted average cost of capital (WACC) is:', 'option_A': 'The average interest rate on loans', 'option_B': 'The average cost of all assets', 'option_C': 'The cost of capital adjusted for inflation', 'option_D': 'The average rate of return required by investors', 'correct_answer': 'D'},
    {'question_text': 'A higher debt-to-equity ratio indicates:', 'option_A': 'More equity financing', 'option_B': 'More debt financing', 'option_C': 'Lower financial leverage', 'option_D': 'Stronger profitability', 'correct_answer': 'B'},
    {'question_text': 'Which financial statement shows a firm’s revenues and expenses?', 'option_A': 'Balance Sheet', 'option_B': 'Cash Flow Statement', 'option_C': 'Statement of Retained Earnings', 'option_D': 'Income Statement', 'correct_answer': 'D'},
    {'question_text': 'Which of the following is a capital budgeting decision?', 'option_A': 'Issuing new shares', 'option_B': 'Buying new machinery', 'option_C': 'Paying dividends', 'option_D': 'Borrowing from a bank', 'correct_answer': 'B'},
    {'question_text': 'If a project\'s NPV is positive, it means:', 'option_A': 'The project should be rejected', 'option_B': 'The project\'s IRR is less than the cost of capital', 'option_C': 'The project will destroy value', 'option_D': 'The project adds value to the firm', 'correct_answer': 'D'},
    {'question_text': 'Which financial ratio measures a firm\'s ability to meet short-term obligations?', 'option_A': 'Debt ratio', 'option_B': 'Current ratio', 'option_C': 'Return on equity', 'option_D': 'Inventory turnover', 'correct_answer': 'B'},
    {'question_text': 'The DuPont identity breaks down ROE into:', 'option_A': 'Profit margin, total asset turnover, and equity multiplier', 'option_B': 'Gross profit, liabilities, and equity', 'option_C': 'Net income, revenue, and capital', 'option_D': 'Earnings per share, dividends, and cash flow', 'correct_answer': 'A'} 
]

mgmt_organizational_behavior = [
    {'question_text': "What are the four functions of management?", 'option_A': "Plan, Organize, Control, Hire", 'option_B': "Plan, Lead, Organize, Control", 'option_C': "Lead, Motivate, Supervise, Hire", 'option_D': "Plan, Direct, Sell, Manage", 'correct_answer': "B"},
    {'question_text': "Which of the following is an example of intrinsic motivation?", 'option_A': "Bonus", 'option_B': "Promotion", 'option_C': "Praise", 'option_D': "Personal satisfaction", 'correct_answer': "D"},
    {'question_text': 'What does "span of control" refer to?', 'option_A': 'The number of departments in a company', 'option_B': 'The number of levels in the hierarchy', 'option_C': 'The number of subordinates a manager oversees', 'option_D': 'The number of tasks a worker completes', 'correct_answer': 'C'},
    {'question_text': 'According to Maslow’s hierarchy, which need comes first?', 'option_A': 'Safety', 'option_B': 'Esteem', 'option_C': 'Physiological', 'option_D': 'Belongingness', 'correct_answer': 'C'},
    {'question_text': 'Which leadership style is most participative?', 'option_A': 'Autocratic', 'option_B': 'Democratic', 'option_C': 'Laissez-faire', 'option_D': 'Transactional', 'correct_answer': 'B'},
    {'question_text': 'What is organizational culture?', 'option_A': 'The company’s product strategy', 'option_B': 'The shared values, beliefs, and norms in an organization', 'option_C': 'The formal structure of departments', 'option_D': 'The employee handbook', 'correct_answer': 'B'},
    {'question_text': 'Which of the following is NOT a Big Five personality trait?', 'option_A': 'Openness', 'option_B': 'Conscientiousness', 'option_C': 'Intuition', 'option_D': 'Agreeableness', 'correct_answer': 'C'},
    {'question_text': 'A team that works across departments or functions is called:', 'option_A': 'A task force', 'option_B': 'A cross-functional team', 'option_C': 'A line team', 'option_D': 'A hierarchical unit', 'correct_answer': 'B'},
    {'question_text': 'Which conflict-handling style involves low concern for both self and others?', 'option_A': 'Competing', 'option_B': 'Collaborating', 'option_C': 'Avoiding', 'option_D': 'Accommodating', 'correct_answer': 'C'},
    {'question_text': 'What does SWOT analysis evaluate?', 'option_A': 'Employee productivity', 'option_B': 'Market segmentation', 'option_C': 'Strengths, Weaknesses, Opportunities, Threats', 'option_D': 'Stock market trends', 'correct_answer': 'C'}
]

business_applications_develop = [
    {'question_text': "What is the primary purpose of business application software?", 'option_A': "Entertainment", 'option_B': "Managing databases", 'option_C': "Solving business problems and improving processes", 'option_D': "Browsing the internet", 'correct_answer': "C"},
    {'question_text': "Which language is commonly used for server-side web application development?", 'option_A': "HTML", 'option_B': "JavaScript", 'option_C': "Python", 'option_D': "CSS", 'correct_answer': "C"},
    {'question_text': 'What does CRUD stand for in application development?', 'option_A': 'Create, Read, Update, Delete', 'option_B': 'Code, Run, Upload, Deploy', 'option_C': 'Connect, Route, Update, Display', 'option_D': 'Create, Run, Utilize, Design', 'correct_answer': 'A'},
    {'question_text': 'What is an API used for in application development?', 'option_A': 'Designing interfaces', 'option_B': 'Connecting and communicating between systems', 'option_C': 'Managing databases', 'option_D': 'Storing user data', 'correct_answer': 'B'},
    {'question_text': 'Which of the following is a front-end development tool?', 'option_A': 'Django', 'option_B': 'Flask', 'option_C': 'React', 'option_D': 'Node.js', 'correct_answer': 'C'},
    {'question_text': 'What is the function of a database in a business application?', 'option_A': 'Displaying the user interface', 'option_B': 'Storing and managing data', 'option_C': 'Designing reports', 'option_D': 'Sending emails', 'correct_answer': 'B'},
    {'question_text': 'What is the role of version control (e.g., Git) in development?', 'option_A': 'To test software', 'option_B': 'To monitor network performance', 'option_C': 'To manage changes to source code over time', 'option_D': 'To format code', 'correct_answer': 'C'},
    {'question_text': 'What is the best development methodology for flexibility and rapid change?', 'option_A': 'Waterfall', 'option_B': 'Agile', 'option_C': 'V-Model', 'option_D': 'Spiral', 'correct_answer': 'B'},
    {'question_text': 'What is UML primarily used for?', 'option_A': 'Writing database queries', 'option_B': 'Creating user interfaces', 'option_C': 'Modeling software systems', 'option_D': 'Encrypting applications', 'correct_answer': 'C'},
    {'question_text': 'What does “responsive design” ensure in web applications?', 'option_A': 'Secure login', 'option_B': 'Fast performance', 'option_C': 'Compatibility across devices and screen sizes', 'option_D': 'Real-time updates', 'correct_answer': 'C'}
]

business_database_mgmt= [
    {'question_text': 'What does SQL stand for?', 'option_A': 'Structured Question Language', 'option_B': 'Standard Query Language', 'option_C': 'Structured Query Language', 'option_D': 'System Query Logic', 'correct_answer': 'C'},
    {'question_text': 'Which command is used to retrieve data from a database?', 'option_A': 'GET', 'option_B': 'SELECT', 'option_C': 'SHOW', 'option_D': 'FETCH', 'correct_answer': 'B'},
    {'question_text': 'What is a primary key?', 'option_A': 'A key used to open the database', 'option_B': 'A unique identifier for each record in a table', 'option_C': 'A foreign key in another table', 'option_D': 'A column that can have duplicate values', 'correct_answer': 'B'},
    {'question_text': 'Which of the following is a relational database management system (RDBMS)?', 'option_A': 'Excel', 'option_B': 'MongoDB', 'option_C': 'Oracle', 'option_D': 'Notepad', 'correct_answer': 'C'},
    {'question_text': 'What is a foreign key used for?', 'option_A': 'Encrypting data', 'option_B': 'Linking records in different tables', 'option_C': 'Identifying primary records', 'option_D': 'Creating indexes', 'correct_answer': 'B'},
    {'question_text': 'What type of relationship exists when one record in a table relates to many records in another table?', 'option_A': 'One-to-One', 'option_B': 'Many-to-Many', 'option_C': 'One-to-Many', 'option_D': 'No Relationship', 'correct_answer': 'C'},
    {'question_text': 'Which SQL statement is used to insert a new record into a table?', 'option_A': 'INSERT INTO', 'option_B': 'ADD NEW', 'option_C': 'CREATE RECORD', 'option_D': 'INPUT DATA', 'correct_answer': 'A'},
    {'question_text': 'What is data normalization?', 'option_A': 'A backup process', 'option_B': 'Removing all data', 'option_C': 'Structuring a database to reduce redundancy', 'option_D': 'Encrypting the database', 'correct_answer': 'C'},
    {'question_text': 'Which clause is used to filter rows returned by a query?', 'option_A': 'ORDER BY', 'option_B': 'GROUP BY', 'option_C': 'WHERE', 'option_D': 'HAVING', 'correct_answer': 'C'},
    {'question_text': 'What does ACID stand for in database systems?', 'option_A': 'Access, Control, Information, Data', 'option_B': 'Atomicity, Consistency, Isolation, Durability', 'option_C': 'Array, Column, Index, Data', 'option_D': 'Audit, Copy, Insert, Delete', 'correct_answer': 'B'}
]

principles_of_marketing = [
    {'question_text': 'What is the core concept of marketing?', 'option_A': 'Selling products', 'option_B': 'Advertising', 'option_C': 'Satisfying customer needs and wants', 'option_D': 'Reducing costs', 'correct_answer': 'C'},
    {'question_text': 'The 4Ps of the marketing mix include Product, Price, Place, and:', 'option_A': 'People', 'option_B': 'Promotion', 'option_C': 'Process', 'option_D': 'Packaging', 'correct_answer': 'B'},
    {'question_text': 'Which of the following is part of market segmentation?', 'option_A': 'Market positioning', 'option_B': 'Dividing the market based on shared characteristics', 'option_C': 'Branding the product', 'option_D': 'Setting prices', 'correct_answer': 'B'},
    {'question_text': 'What does brand equity refer to?', 'option_A': 'The cost of a product', 'option_B': 'The value of a brand in the marketplace', 'option_C': 'The ownership of the brand', 'option_D': 'The product\'s expiration', 'correct_answer': 'B'},
    {'question_text': 'What type of marketing focuses on creating long-term relationships with customers?', 'option_A': 'Transactional marketing', 'option_B': 'Guerrilla marketing', 'option_C': 'Relationship marketing', 'option_D': 'Direct marketing', 'correct_answer': 'C'},
    {'question_text': 'A SWOT analysis examines:', 'option_A': 'Market prices', 'option_B': 'Market segments', 'option_C': 'Strengths, Weaknesses, Opportunities, Threats', 'option_D': 'Sales growth only', 'correct_answer': 'C'},
    {'question_text': 'What is the primary goal of promotional strategies?', 'option_A': 'To raise product prices', 'option_B': 'To create brand loyalty', 'option_C': 'To inform, persuade, or remind customers', 'option_D': 'To reduce advertising costs', 'correct_answer': 'C'},
    {'question_text': 'A product\'s life cycle typically includes: Introduction, Growth, Maturity, and:', 'option_A': 'Recovery', 'option_B': 'Peak', 'option_C': 'Decline', 'option_D': 'Termination', 'correct_answer': 'C'},
    {'question_text': 'What is target marketing?', 'option_A': 'Creating ads that appeal to everyone', 'option_B': 'Designing products for international markets', 'option_C': 'Focusing marketing efforts on specific customer segments', 'option_D': 'Targeting competitors\' customers', 'correct_answer': 'C'},
    {'question_text': 'What is a USP (Unique Selling Proposition)?', 'option_A': 'The slogan of a brand', 'option_B': 'The low price point', 'option_C': 'The unique benefit that sets a product apart from competitors', 'option_D': 'The place a product is sold', 'correct_answer': 'C'}
]

# Create databases for each class
create_database("Principles_of_Managerial_Finance", principles_of_managerial_finance)
create_database("Mgmt_Organizational_Behavior", mgmt_organizational_behavior)
create_database("Business_Applications_Develop", business_applications_develop)
create_database("Business_Database_Mgmt", business_database_mgmt)
create_database("Principles_of_Marketing", principles_of_marketing)

questions_from_finance = get_questions_from_database("Principles_of_Managerial_Finance")
print(questions_from_finance)  # This will print the list of questions for the selected class

print("Databases and tables created successfully.")