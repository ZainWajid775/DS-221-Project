import pandas as pd                 # Data manipulation and analysis library
import os                           # A way to interact with the os
import numpy as np                  # Numerical computations and array handling
from scipy.stats import skew        # Adavanced statistical calculations
from scipy.stats import norm
import scipy.stats as stats
from termcolor import colored       # For coloured text printing
import matplotlib.pyplot as plt     # For data visualisation
import seaborn as sns               # Statistical visualisation
import time                         # To wait create a delay when restarting system

# f-string used is printing for direct insertion of variables into the string
# .strip() is used in input validation to remove any leading or trailing white spaces
# Lambda functions are used to create functions without requiring a def block
# The code is structured in a way that the user can easily navigate through parts of the programSD

# Clear the terminal screen
# nt for windows , clear for linux based systems
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')       


# Prompt the user to press enter
def enter_to_continue():
    print(colored("Press Enter to continue...", "green"))           # Print the message in green
    input()                                                         # Wait for user input

# Prints a line in colur for header
def print_coloured_line(text, color):

    length = 100

    if length < len(text) + 2:
        length = len(text) + 2

    side_length = (length - len(text)) // 2                         # Number of dashes on each side of the text
    line = "-" * side_length + f" {text} " + "-" * side_length      # Line to print

    if len(line) < length:                                          # If the line is shorter than the length in cases of odd numbered text
        line += "-"

    print(colored(line, color))
    print()





# Create a new file from user input and store them in a csv
def create_student_scores():

    students = []                                                   # Stores student data in dictionary
    student_names = set()                                           # Ensure name uniqueness
    student_count = 0   

    # Outer loop to repeat until user is done entering student data
    while True:
        # Inner loop to get student names and scores
        while True:

            clear_terminal()
            print_coloured_line("Student Scores Input", "green")

            print("Enter student names and scores (type 'done' when finished):")
            name = input(f"Student name ({student_count+1}): ").strip()
            # If 'done' is entered, break the loop
            if name.lower() == 'done':
                break

            # Ensure the name is not empty
            if name == '':
                print(colored("Invalid name. Please enter a valid name." , "red"))
                enter_to_continue()
                clear_terminal()
                continue 

            if name in student_names:
                print(colored("Name must be unique. This name has already been entered." , "red"))
                enter_to_continue()
                clear_terminal()
                continue
            
            break

        # If 'done' is entered, break the loop
        if name.lower() == 'done':
            break

        score = input(f"Score for {name}: ").strip()

        try:
            # Convert the score to a float and append the student record
            score = float(score)

            # Ensure the score is within the range 0-100
            if 0 <= score <= 100:
                students.append({"Name": name, "Score": score})
                student_names.add(name)                             # Add name to the set of unique names

                student_count += 1

                clear_terminal()
                print_coloured_line("Student Scores Input", "green")

                print(f"Total students added: {student_count}")     # Display current student count
                enter_to_continue()                                 # Prompt to continue
            else:
                print(colored("Invalid score. Please enter a value between 0 and 100." , "red"))
                enter_to_continue()
                clear_terminal()

        except ValueError:

            # Handle invalid score input
            print(colored("Invalid score. Please enter a numeric value." , "red"))
            enter_to_continue()
            clear_terminal()

    if not students:
        clear_terminal()
        print_coloured_line("Student Scores Input", "green")
        print("No student data provided.")
        enter_to_continue();
        return None
    
    # Create a new file with the student data
    filename = "student_scores.csv"
    df = pd.DataFrame(students)
    df.to_csv(filename , index=False)                   # Index false ensures no row indexs are written to the file

    clear_terminal()
    print_coloured_line("Student Scores Saved", "green")
    print(f"Student scores saved to {filename}.")
    enter_to_continue()
    return filename

# Read a file 
def read_file(filename):

    # Check if the file exists
    if not os.path.exists(filename):
        clear_terminal()
        print_coloured_line("Student Scores Input" , "green")
        print(colored(f"Error: The file '{filename}' does not exist." , "red"))
        enter_to_continue()
        return None

    # Attempt to read the file based on its extension
    try:
        if filename.endswith('.csv'):
            data = pd.read_csv(filename)
            print(f"Successfully read the CSV file: {filename}")
            enter_to_continue()

        elif filename.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(filename)
            print(f"Successfully read the Excel file: {filename}")
            enter_to_continue()

        else:
            clear_terminal()
            print_coloured_line("Student Scores Input" , "green")

            print(colored("Error: Unsupported file format. Please provide a CSV or Excel file." , "red"))
            print('\n')
            enter_to_continue()
            return None

        # Show the first few rows of the data as a preview
        clear_terminal()
        print_coloured_line("Student Scores Input" , "green")
        print("\nPreview of the data:")
        print(data.head())
        print('\n')
        enter_to_continue()

        return data

    except Exception as e:
        print(colored(f"An error occurred while reading the file: {e}" < "red"))
        return None

# Save grades to CSV
def save_grades_to_csv(student_data, filename="graded_students.csv"):

    try:
        save_data = student_data[['Name', 'Score', 'Grade']]                        # Save only the relevant columns
        save_data.to_csv(filename, index=False)                                     # Save the data to a CSV file
        print(colored(f"Graded student data saved to {filename}.", "green"))
        
    except Exception as e:
        print(colored(f"Error saving file: {e}", "red"))

# Plot grade distribution
def plot_grade_distribution(student_data):

    grade_counts = student_data['Grade'].value_counts()                             # Count the occurences of each grade
    total_students = len(student_data)                                              # Total number of students

    plt.figure(figsize=(8, 6))                                                      # Set the figure size

    # If there are fewer than 30 students, show a pie chart
    if total_students < 30:
        # Show a pie chart with percentage labels
        plt.pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        plt.title('Grade Distribution (Pie Chart)', fontsize=16)
        plt.axis('equal')                                                           # Equal aspect ratio ensures the pie is drawn as a circle.


    else:
        # Otherwise, show a bar chart
        plt.bar(grade_counts.index, grade_counts.values, color='skyblue')           # Create a bar chart with grades on x-axis and their count on y-axis
        plt.title('Grade Distribution (Bar Chart)', fontsize=16)                    # Title
        plt.xlabel('Grades', fontsize=14)                                           # X-axis title
        plt.ylabel('Number of Students', fontsize=14)                               # Y-axis title
        plt.xticks(fontsize=12)                                                     # Adjust x-axis font size
        plt.yticks(fontsize=12)                                                     # Adjust y-axis font size
        plt.grid(axis='y', linestyle='--', alpha=0.7)                               # Add gridlines for better readability on y-axis

    plt.show()

# Show score histogram with a normal line to show how well the dataset follows a normal distribution
def plot_normal_curve(student_data):
    # Ensure the 'Score' column exists in the dataset
    if 'Score' not in student_data.columns:
        print(colored("Error: No 'Score' column in the dataset.", "red"))
        return

    # Extract the 'Score' column from the student_data DataFrame
    student_scores = student_data['Score'].values

    # Check if there are scores available
    if len(student_scores) == 0:
        print(colored("Error: No scores available to plot.", "red"))
        return

    # Calculate mean and standard deviation of the scores using numpy
    mean_score = np.mean(student_scores)
    std_deviation = np.std(student_scores)

    # Generate a range of values for the x-axis (scores range)
    # The range is set to 4 standard deviations from the mean
    # 3 standard deviations cover about 99.7% of the data in a normal distribution , 4 ensures entire data coverage
    x = np.linspace(mean_score - 4*std_deviation, mean_score + 4*std_deviation, 1000)

    # Generate normal distribution based on mean and standard deviation using scipy.stats
    y = norm.pdf(x, mean_score, std_deviation)

    # Plotting the normal curve
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label='Normal Distribution', color='blue')

    # Plotting the histogram of the students' scores
    plt.hist(student_scores, bins=15, density=True, alpha=0.6, color='green', edgecolor='black', label='Student Scores')

    # Adding titles and labels
    plt.title('Normal Curve of Student Scores', fontsize=16)
    plt.xlabel('Scores', fontsize=14)
    plt.ylabel('Density', fontsize=14)
    plt.legend()

    # Show the plot
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

# Plot boxplot of student scores
def plot_boxplot(student_data):

    # Ensure the 'Score' column exists in the dataset
    if 'Score' not in student_data.columns:
        print(colored("Error: No 'Score' column in the dataset.", "red"))
        return

    # Extract the 'Score' column from the student_data DataFrame
    student_scores = student_data['Score']

    # Check if there are scores available
    if len(student_scores) == 0:
        print(colored("Error: No scores available to plot.", "red"))
        return

    # Create the boxplot using Seaborn
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=student_scores, color='skyblue')

    # Adding titles and labels
    plt.title('Boxplot of Student Scores', fontsize=16)
    plt.xlabel('Scores', fontsize=14)
    
    # Show the plot
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

# Plot score distribution
def plot_score_distribution(student_data):
    plt.figure(figsize=(8, 6))
    plt.hist(student_data['Score'], bins=10, color='lightcoral', edgecolor='black')         # Create a histogram with 10 bars
    plt.title('Score Distribution', fontsize=16)
    plt.xlabel('Scores', fontsize=14)
    plt.ylabel('Number of Students', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


# Calculate absolute grades
def calculate_absolute_grades(student_data, grade_percentages):

    try:
        # Ensure required columns are present
        if 'Name' not in student_data.columns or 'Score' not in student_data.columns:
            print(colored("Error: The dataset must contain 'Name' and 'Score' columns.", "red"))
            enter_to_continue()
            return student_data                                                                     # Returning the original data as a fallback

        # Sort grades in descending order of percentages for comparison
        sorted_grades = sorted(grade_percentages.items(), key=lambda x: x[1], reverse=True)         # Lambda creates function without requiring a def block

        # Assign grades to students
        # Lambda function takes score as argument, iterates over the score and assign a grade depending on the grade thereshold defined by user
        student_data['Grade'] = student_data['Score'].apply(
            lambda score: next((grade for grade, threshold in sorted_grades if score >= threshold), 'F')
        )

        # Calculate grade distribution and show it
        grade_counts = student_data['Grade'].value_counts()
        total_students = len(student_data)

        clear_terminal()
        print_coloured_line("Absolute Grading Results", "magenta")

        # Overall occurences of each grade
        print("Grade Distribution:")
        for grade, count in grade_counts.items():
            percentage = (count / total_students) * 100
            print(f"Grade {grade}: {count} students ({percentage:.2f}%)")

        # Each individual students grades
        print("\nStudent Grades:")
        for _, row in student_data.iterrows():
            print(f"{row['Name']}: {row['Score']} -> Grade {row['Grade']}")

        # Plot grade distribution and score distribution
        plot_grade_distribution(student_data)
        plot_score_distribution(student_data)
        plot_boxplot(student_data)

        enter_to_continue()

        # Returning the updated dataframe with grades
        return student_data

    except Exception as e:
        print(colored(f"An error occurred while calculating grades: {e}", "red"))
        enter_to_continue()
        return student_data                                                                               # Returning the original data as a fallback

# Relative grading
def calculate_relative_grades(student_data, grade_percentages):
    try:
        # Ensure required columns are present
        if 'Name' not in student_data.columns or 'Score' not in student_data.columns:
            print(colored("Error: The dataset must contain 'Name' and 'Score' columns.", "red"))
            enter_to_continue()
            return
        
        # Sort students by scores in descending order
        student_data = student_data.sort_values(by='Score', ascending=False).reset_index(drop=True)        # Reset Index removes old indexes

        # Calculate the number of students per grade based on percentages
        total_students = len(student_data)                                                                 # Get number of students
        cumulative_students = 0                                                                            # Track cumulative students assigned a grade
        grade_assignments = []                                                                             # Stores each students grade according to index

        print_coloured_line("Relative Grading Results", "cyan")
        
        # Assigns a grade to each student depending on the thereshold defined by the user
        for grade, percentage in grade_percentages.items():
            num_students_for_grade = round(percentage / 100 * total_students)                              # Calculate number of students for the grade
            start_idx = cumulative_students                                                                # Start index for the grade
            end_idx = min(cumulative_students + num_students_for_grade, total_students)                    # End index for the grade

            # Ensure that last grade covers any remaining students (due to rounding)
            grade_assignments += [grade] * (end_idx - start_idx)
            cumulative_students += num_students_for_grade

        # Handle any remaining students due to rounding
        # Automatically assigned a F due to descending order of scores
        if len(grade_assignments) < total_students:
            remaining_students = total_students - len(grade_assignments)
            grade_assignments += [list(grade_percentages.keys())[-1]] * remaining_students

        # Assign grades back to the dataframe
        student_data['Grade'] = grade_assignments

        # Reorder the grades to ensure top scores get "A"
        # Helps avoid situations where some students get a grade that is not part of the predefined grades
        student_data['Grade'] = student_data['Grade'].apply(
            lambda grade: list(grade_percentages.keys())[-1] if grade == "F" else grade
        )

        # Calculate grade distribution
        grade_counts = student_data['Grade'].value_counts()
        print("Grade Distribution:")
        for grade, count in grade_counts.items():
            print(f"Grade {grade}: {count} students")

        # Calculate descriptive statistics using numpy and scipy
        mean_score = np.mean(student_data['Score'])
        variance_score = np.var(student_data['Score'])
        standard_deviation_score = np.std(student_data['Score'])
        skewness_score = skew(student_data['Score'])

        print(f"\nDescriptive Statistics for Scores:")
        print(f"Mean: {mean_score:.2f}")
        print(f"Variance: {variance_score:.2f}")
        print(f"Standard Deviation: {standard_deviation_score:.2f}")
        print(f"Skewness: {skewness_score:.2f}")

        # Display the students' grades
        print("\nStudent Grades:")
        for _, row in student_data.iterrows():
            print(f"{row['Name']}: {row['Score']} -> Grade {row['Grade']}")

        # Plot grade distribution and scores
        plot_normal_curve(student_data)
        plot_grade_distribution(student_data)
        plot_score_distribution(student_data)
        plot_boxplot(student_data)

        enter_to_continue()

        # Return updated data frame with assigned grades
        return student_data

    except Exception as e:
        print(colored(f"An error occurred while calculating relative grades: {e}", "red"))
        enter_to_continue()
        return None
    
# Calculate z-scores and applu updated grades
def apply_z_score_grading(student_data):
    # Ensure the 'Score' column exists in the dataset
    if 'Score' not in student_data.columns:
        print("Error: No 'Score' column in the dataset.")
        return

    # Calculate mean and standard deviation of scores
    mean_score = student_data['Score'].mean()
    std_dev = student_data['Score'].std()

    # Calculate z-scores for each student
    student_data['z_score'] = (student_data['Score'] - mean_score) / std_dev

    # Assign letter grades based on z-scores
    # Grades are assigned by how much the z-score deviates from the mean
    def assign_grade(z):
        if z >= 1.0:
            return 'A'
        elif z >= 0.0:
            return 'B'
        elif z >= -1.0:
            return 'C'
        else:
            return 'D'
    
    # Apply grade assignment function
    student_data['Relative Grade'] = student_data['z_score'].apply(assign_grade)
    
    # Calculate how many students moved and track grade shifts
    before_grades = student_data['Grade'].copy()                                                # Original grades
    moved_students = {}                                                                         # Store students who moved grades

    # Store moved students
    for index, row in student_data.iterrows():
        original_grade = row['Grade']
        new_grade = row['Relative Grade']
        if original_grade != new_grade:
            moved_students[row['Name']] = {'from': original_grade, 'to': new_grade}

    # Print out grade movements
    if moved_students:
        print(f"Grade Changes (students who were moved):")
        for student, grades in moved_students.items():
            print(f"{student} moved from {grades['from']} to {grades['to']}")
    
    # Generate new statistics after grading adjustment
    new_statistics = {
        "mean": student_data['Score'].mean(),
        "std_dev": student_data['Score'].std(),
        "median": student_data['Score'].median(),
        "min": student_data['Score'].min(),
        "max": student_data['Score'].max()
    }

    # Print new statistics
    print("\nNew Statistics after Z-Score Adjustment:")
    for stat, value in new_statistics.items():
        print(f"{stat.capitalize()}: {value:.2f}")

    # Grade column after applying Z-score grading
    student_data['Grade'] = student_data['Relative Grade']

    # Plot the updated distributions (Z-score graded)
    plot_grade_distribution(student_data)   
    plot_score_distribution(student_data)
    plot_boxplot(student_data)

    # Show the Z-Score grading plot
    sns.histplot(student_data['Score'], kde=True)
    plt.title("Adjusted Distribution After Z-Score Grading")
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.show()

    # Return updated grades using z-score grading
    return student_data



def main():

    clear_terminal()

    # Outer Loop for file selection and reading
    while True:
        # Bool to check if a file with valid data has been read
        file_selected = False

        while not file_selected:
            print_coloured_line("Input Module" , "green")
            print("Choose an option:\n")
            print("1. Create a new student scores file")
            print("2. Provide an existing file")
            choice = input("\nType here : ").strip()

            if choice == '1':
                filename = create_student_scores()                              # Create a new file
                if filename:                                                    # If a file is created
                    student_data = read_file(filename)                          # Read the file
                    if student_data is not None:                                # If the file is read successfully
                        file_selected = True

            elif choice == '2':
                clear_terminal()
                print_coloured_line("Student Scores Input" , "green")

                # Loop until a valid file is selected
                while True:
                    clear_terminal()
                    print_coloured_line("Student Scores Input", "green")

                    print("Enter the filename (with extension, e.g., file.csv or file.xlsx)")
                    print("If file is not in the same directory , please specify the directory as well")
                    print("Enter '0' to go back")
                    filename = input("\nType here : ").strip()

                    if filename == '0':
                        file_selected = False
                        clear_terminal()
                        break

                    student_data = read_file(filename)
                    if student_data is not None:
                        file_selected = True
                        break

                    if os.path.exists(filename):
                        read_file(filename)
                        file_selected = True
                        clear_terminal()
                        break
                    else:
                        clear_terminal()
                        print_coloured_line("Student Scores Input", "green")
                        print(colored(f"Error: The file '{filename}' does not exist. Please provide a valid file.", "red"))
                        enter_to_continue()

            else:
                print(colored("\nInvalid choice." , "red"))
                enter_to_continue()
                clear_terminal()


        # Input for relative or absolute grading
        grading_method_seleted = False

        # Loop for selecting a grading method
        while not grading_method_seleted:
            clear_terminal()
            print_coloured_line("Grading method" , "yellow")

            print("Select grading type:")
            print(colored("\n1. Relative Grading" , "cyan"))
            print(colored("2. Absolute Grading\n" , "magenta"))

            grading_choice = input("Enter the number of your choice: ").strip()

            if grading_choice == '1':
                clear_terminal()
                print_coloured_line("Relative Grading selected" , "cyan")
                print("\nYou chose relative grading.")
                enter_to_continue()
                grading_method_seleted = True

            elif grading_choice == '2':
                clear_terminal()
                print_coloured_line("Absolute Grading selected" , "magenta")
                print("\nYou chose absolute grading.")
                enter_to_continue()
                grading_method_seleted = True

            else:
                print(colored("\nInvalid choice." , "red"))
                enter_to_continue()

        # Input for the grading scale
        grading_scale_selected = False

        grade_category = ['A', 'B', 'C', 'D', 'F']              # Store grades
        grade_percentages = {}                                  # Stores grades theresholds
        total_percentage = 0                                    # Total percentage of grades entered in relative grading

        while not grading_scale_selected:

            # Relative
            if grading_choice == '1':
            
                    for grade in grade_category:
                        while True:
                            clear_terminal()
                            print_coloured_line("Grading Scale" , "cyan")
                            print(f"Enter percentage for grade {grade}", "cyan")

                            user_input = input(f"Enter percentage for grade {grade}: ").strip()

                            # Validate input
                            try:
                                percentage = float(user_input)

                                if 0 <= percentage <= 100:                                              # Ensure percentage is valid
                                    total_percentage += percentage

                                    # Check if total exceeds 100 while entering
                                    if total_percentage > 100:
                                        print(colored(f"The total percentage exceeds 100%.", "red"))
                                        enter_to_continue()
                                        break                                                           # Break out to restart the whole process from A if percentage exceeds 100

                                    grade_percentages[grade] = percentage
                                    break                                                               # Exit the loop once valid input is entered
                                else:
                                    print(colored("Please enter a percentage between 0 and 100.", "red"))
                                    enter_to_continue()

                            except ValueError:                                                           # Handle invalid input above 100
                                print(colored("Invalid input. Please enter a numeric value between 0 and 100.", "red"))
                                enter_to_continue()

                        # If the total exceeded during the input for this grade, restart from A
                        if total_percentage > 100:
                            break

                    # Final check after all grades have been entered
                    if total_percentage == 100:
                        grading_scale_selected = True
                        break  # Exit the process if everything is valid

                    else:
                        print(colored("The total percentage is not exactly 100%. Restarting from grade A!", "red"))
                        total_percentage = 0
                        enter_to_continue()

            # Absolute
            elif grading_choice == '2':
                previous_threshold = 100
                for grade in grade_category[:-1]:                                                       # Exclude 'F' as F is calculated as D - 1
                    while True:
                        clear_terminal()
                        print_coloured_line("Grading Scale", "magenta")
                        user_input = input(f"Enter minimum percentage thresehold for grade {grade}: ").strip()

                        # Validate input
                        try:
                            threshold = float(user_input)
                            if 0 <= threshold <= previous_threshold:                                    # Ensure thresholds are valid and descending
                                grade_percentages[grade] = threshold
                                previous_threshold = threshold
                                break

                            else:
                                print(colored(f"Please enter a value between 0 and {previous_threshold}.", "red"))
                                enter_to_continue()

                        except ValueError:
                            print(colored("Invalid input. Please enter a numeric value.", "red"))
                            enter_to_continue()

                grade_percentages['F'] = grade_percentages['D'] - 1
                grading_scale_selected = True

        clear_terminal()
        print_coloured_line("Grading scale" , "yellow")

        # Show the percentages entered
        print("Percentages entered\n")

        for grade, percentage in grade_percentages.items():
            print(f"Grade {grade}: {percentage}%")
        print('\n')

        enter_to_continue()


    # STATISTICAL ANALYSIS 
        clear_terminal()

        if grading_choice == '1':

            student_data = calculate_relative_grades(student_data, grade_percentages)
            # A copy of is made after relative grading to keep the original data in case user wants to store according to their percentages
            original_data = student_data.copy()
            adjusted_data = apply_z_score_grading(student_data)



        elif grading_choice == '2':

            student_data = calculate_absolute_grades(student_data , grade_percentages)


    # Save graded data to CSV

        clear_terminal()
        print_coloured_line("Save File Creation" , "green")
        print("Grade Calculation Completed")

        save = input("Would you like to save the grades in a CSV? (y/n): ").strip()

        while True:
            if save == 'y':
                clear_terminal()
                print_coloured_line("Save File Creation", "green")

                if grading_choice == '1':
                    while True:
                        clear_terminal()
                        print_coloured_line("Save File Creation", "green")

                        print("1. Save grades with your parameters")
                        print("2. Save grades fitted to a normal distribution\n")

                        save_choice = input(
                            "Would you like to save the grades with your parameters or the grades fitted to a normal distribution? ").strip()

                        if save_choice == '1':
                            print("\nSaving grades to CSV file with your parameters...\n")
                            save_grades_to_csv(original_data, "graded_students_relative.csv")
                            enter_to_continue()
                            break
                        
                        elif save_choice == '2':
                            print("\nSaving grades to CSV file (fitted to normal distribution)...\n")
                            save_grades_to_csv(adjusted_data, "graded_students_z_score.csv")
                            enter_to_continue()
                            break
                        
                        else:
                            clear_terminal()
                            print_coloured_line("Save File Creation", "green")
                            print(colored("\nInvalid Option. Please try again.", "red"))
                            enter_to_continue()
                    
                    break

                elif grading_choice == '2':
                    print("\nSaving grades to CSV file...\n")
                    save_grades_to_csv(student_data)
                    enter_to_continue()
                    break
                
                else:
                    print("\nInvalid grading choice. Please try again.")
                    break
                
            elif save == 'n':
                print("\nGrades were not saved.")
                break
            
            else:
                print(colored("Invalid input. Please enter 'y' or 'n'.", "red"))
                save = input("Would you like to save the grades in a CSV? (y/n): ").strip()

        clear_terminal()
        print_coloured_line("Restart or Exit", "yellow")
        restart_choice = input("\nWould you like to process another file? (y/n): ").strip().lower()

        if restart_choice != 'y':
            print(colored("Exiting the program. Goodbye!", "green"))
            break                                                                                               # Exit the loop and program

        else:
            clear_terminal()
            print_coloured_line("Restarting" , "green")
            time.sleep(1)
            clear_terminal()
                



if __name__ == "__main__":
    main()
