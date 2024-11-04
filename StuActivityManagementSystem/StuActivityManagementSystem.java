import java.io.*;
import java.util.InputMismatchException;
import java.util.Scanner;

class StuActivityManagementSystem {

    private static Student[] students = new Student[100];
    private static int studentCount = 0;

    //------------------CHECK AVAILABLE STUDENTS------------------------
	public static void checkAvailableSeats(){
		Scanner input = new Scanner(System.in);
        int availableSeats = 100 - studentCount;
        System.out.println("\n\n\n\tAvailable seats: " + availableSeats);
        System.out.println("\nPress Enter to go to the main menu...");
        input.nextLine();
        clearConsole();
        homePage();
	}

	//-----------------------REGISTER STUDENT---------------------------
    public static void registerStudent() {
        Scanner input = new Scanner(System.in);
        System.out.println("\t------------ Register Student------------ ");
    
        while (true) {
            String studentID;
            boolean studentExists = false;
            do {
                System.out.print("\n\tEnter student ID : ");
                studentID = input.nextLine();
    
                if (!studentIDValidating(studentID)) {
                    System.out.print("\n\tDo you want to enter student ID again (Y/N): ");
                    char yesNO = input.next().charAt(0);
                    input.nextLine();
                    if (yesNO == 'Y' || yesNO == 'y') {
                        continue;
                    } else {
                        clearConsole();
                        return;
                    }
                }
    
                studentExists = checkStudentExists(studentID);
                if (studentExists) {
                    System.out.println("\n\tStudent ID already exists.");
                    System.out.print("\nDo you want to enter a different student ID (Y/N): ");
                    char yesNO = input.next().charAt(0);
                    input.nextLine();
                    if (yesNO == 'Y' || yesNO == 'y') {
                        clearConsole();
                        continue;
                    } else {
                        clearConsole();
                        return;
                    }
                }
    
            } while (!studentIDValidating(studentID) || studentExists);
    
            System.out.print("\n\tEnter student name: ");
            String studentName = input.nextLine();
    
            int[] moduleMarks = new int[3];
            int totalMarks = 0;
            boolean marksValid = true;
    
            for (int i = 0; i < 3; i++) {
                do {
                    System.out.print("\n\tEnter marks for Module " + (i + 1) + " : ");
                    try {
                        moduleMarks[i] = Integer.parseInt(input.nextLine());
    
                        if (moduleMarks[i] < 0 || moduleMarks[i] > 100) {
                            System.out.println("\n\t\tInvalid marks.\n\t\tMarks should be between 0 and 100.");
                            marksValid = false;
                        } else {
                            totalMarks += moduleMarks[i];
                            marksValid = true;
                        }
                    } catch (NumberFormatException e) {
                        System.out.println("\n\t\tInvalid input type. Please enter a numeric value.");
                        marksValid = false;
                    }
                } while (!marksValid);
            }
    
            Student newStudent = new Student(studentID, studentName);
            newStudent.setModuleMarks(moduleMarks);
    
            students[studentCount] = newStudent;
            studentCount++;
    
            System.out.println("\nStudent registered successfully!");
    
            System.out.print("\n\nDo you want to add another student (Y/N): ");
            char yesNO = input.next().charAt(0);
            input.nextLine();
            if (yesNO == 'Y' || yesNO == 'y') {
                clearConsole();
                continue;
            } else if (yesNO == 'N' || yesNO == 'n') {
                clearConsole();
                homePage();
            }
        }
    }      
    //-----------------------VALIDATE STU ID-----------------------------
    public static boolean studentIDValidating(String studentID) {
        if (studentID.length() != 8) {
            System.out.println("\nStudent ID must be 8 characters long.");
            return false;
        }
        if (studentID.charAt(0) != 'w') {
            System.out.println("Student ID must start with 'w'.");
            return false;
        }
        for (int i = 1; i < studentID.length(); i++) {
            if (!Character.isDigit(studentID.charAt(i))) {
                System.out.println("Student ID must contain only digits after the first character.");
                return false;
            }
        }
        return true;
    }
    
    //-----------------------CHECK IF STUDENT EXISTS-----------------------------
    public static boolean checkStudentExists(String studentID) {
        for (int i = 0; i < studentCount; i++) {
            if (students[i].getId().equals(studentID)) {
                return true;
            }
        }
        return false;
    }
    
    //-----------------------DELETE STUDENT-----------------------------
    public static void deleteStudent() {
        System.out.println("\t------------ Delete Student ------------ ");
        Scanner input = new Scanner(System.in);

        if (studentCount == 0) {
            System.out.println("No students to delete.");
            return;
        }

        boolean continueDeleting = true;

        while (continueDeleting) {
            System.out.println("\n\n\t+--------------------------------------+");
            System.out.println("\t|    ID     |       Name               |");
            System.out.println("\t+--------------------------------------+");
            for (int i = 0; i < studentCount; i++) {
                Student student = students[i];
                System.out.printf("\t|%-12s|%-25s|\n",
                        student.getId(),
                        student.getName());
            }
            System.out.println("\t+--------------------------------------+");

            System.out.print("\nEnter the ID of the student to delete: ");
            String idToDelete = input.nextLine();

            boolean studentFound = false;
            for (int i = 0; i < studentCount; i++) {
                if (students[i].getId().equalsIgnoreCase(idToDelete)) {
                    for (int j = i; j < studentCount - 1; j++) {
                        students[j] = students[j + 1];
                    }
                    students[studentCount - 1] = null;
                    studentCount--;
                    studentFound = true;
                    System.out.println("\n\n\tStudent deleted successfully!");
                    break;
                }
            }

            if (!studentFound) {
                System.out.println("Student not found.");
            }

            System.out.print("\n\nDo you want to delete another student (Y/N): ");
            char yesNO = input.next().charAt(0);
            input.nextLine();

            if (yesNO == 'Y' || yesNO == 'y') {
                clearConsole();
            } else if (yesNO == 'N' || yesNO == 'n') {
                clearConsole();
                homePage();
                break;
            } else {
                System.out.println("Invalid choice. Returning to the homepage.");
                homePage();
                break;
            }
        }
    }
    //--------------------------FIND STUDENT----------------------------
    public static void findStudent(){
        System.out.println("\t------------ Find Student ------------ ");
        Scanner input = new Scanner(System.in);

        if (studentCount == 0) {
            System.out.println("No students in the system.");
            return;
        }

        do {
            System.out.print("\n\tEnter the ID of the student to find: ");
            String idToFind = input.nextLine();

            boolean studentFound = false;
            for (int i = 0; i < studentCount; i++) {
                if (students[i].getId().equalsIgnoreCase(idToFind)) {
                    Student student = students[i];

                    System.out.println("\n\n\t+--------------------------------------+");
                    System.out.println("\t|    ID     |       Name               |");
                    System.out.println("\t+--------------------------------------+");
                    System.out.printf("\t|%-12s|%-25s|\n",
                            student.getId(),
                            student.getName());
                    System.out.println("\t+--------------------------------------+");

                    studentFound = true;
                    break;
                }
            }

            if (!studentFound) {
                System.out.println("\n\tStudent not found.");
            }

            System.out.print("\nDo you want to search another student (Y/N): ");
            char yesNO = input.next().charAt(0);
            input.nextLine();

            if (yesNO == 'Y' || yesNO == 'y') {
                clearConsole();
            } else if (yesNO == 'N' || yesNO == 'n') {
                clearConsole();
                homePage();
                break;
            }
        } while (true);
    }
    //-----------------------EXPORT TXT FILE----------------------------
    public static void storeStudentDetailsIntoTxtFile() {
        Scanner input = new Scanner(System.in);
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter("student_details.txt"));

            for (int i = 0; i < studentCount; i++) {
                Student student = students[i];
                int[] marks = student.getModuleMarks();
                String grade = student.calculateGrade();

                String studentDetails = String.format("%s|%s|%d|%d|%d|%s",
                        student.getId(),
                        student.getName(),
                        marks[0],
                        marks[1],
                        marks[2],
                        grade);

                writer.write(studentDetails);
                writer.newLine();
            }

            writer.close();
            clearConsole();
            System.out.println("\n\tStudent details stored successfully in student_details.txt.");

            System.out.print("\nDo you want to export again (Y/N): ");
            char yesNO = input.next().charAt(0);
            input.nextLine();

            if (yesNO == 'Y' || yesNO == 'y') {
                clearConsole();
                storeStudentDetailsIntoTxtFile();
            } else if (yesNO == 'N' || yesNO == 'n') {
                clearConsole();
                homePage(); // Assuming homePage() is a method to return to main menu or home screen
            }
        } catch (IOException e) {
            System.out.println("An error occurred while writing to the file: " + e.getMessage());
        }
    }
	//-----------------------IMPORT TXT FILE----------------------------
	public static void loadStudentDetailsfromTxtFile() {
        Scanner input = new Scanner(System.in);
        try {
            File file = new File("student_details.txt");
            FileReader fr = new FileReader(file);
            BufferedReader br = new BufferedReader(fr);

            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split("\\|");
                if (parts.length == 6) {
                    String studentID = parts[0].trim();
                    String studentName = parts[1].trim();
                    int module1 = Integer.parseInt(parts[2].trim());
                    int module2 = Integer.parseInt(parts[3].trim());
                    int module3 = Integer.parseInt(parts[4].trim());
                    String moduleGrade = parts[5].trim();

                    Student student = new Student(studentID, studentName);
                    student.setModuleMarks(new int[]{module1, module2, module3});
                    student.setModuleGrade(moduleGrade);

                    students[studentCount] = student;
                    studentCount++;
                } else {
                    System.out.println("Invalid data format: " + line);
                }
            }

            br.close();
            clearConsole();
            System.out.println("\n\tStudent details loaded successfully from file.");

            System.out.print("\nDo you want to import again (Y/N): ");
            char yesNO = input.next().charAt(0);
            input.nextLine();

            if (yesNO == 'Y' || yesNO == 'y') {
                clearConsole();
                loadStudentDetailsfromTxtFile();
            } else if (yesNO == 'N' || yesNO == 'n') {
                clearConsole();
                homePage(); // Assuming homePage() is a method to return to main menu or home screen
            }
        } catch (IOException e) {
            System.out.println("Error reading from file: " + e.getMessage());
        } catch (NumberFormatException e) {
            System.out.println("Error parsing module marks: " + e.getMessage());
        }
    }

	//-------------------------VIEW STUDENT LIST------------------------
	public static void viewSortedStudent() {
        Scanner input = new Scanner(System.in);
    
        // Assuming students and studentCount are accessible
        for (int i = 0; i < studentCount - 1; i++) {
            for (int j = 0; j < studentCount - 1 - i; j++) {
                // Compare student names ignoring case
                if (students[j].getName().compareToIgnoreCase(students[j + 1].getName()) > 0) {
                    // Swap students
                    Student temp = students[j];
                    students[j] = students[j + 1];
                    students[j + 1] = temp;
                }
            }
        }
    
        clearConsole();
        System.out.println("\n\n\t+----------------------+");
        System.out.println("\t|   Student Names      |");
        System.out.println("\t+----------------------+");
        for (int i = 0; i < studentCount; i++) {
            System.out.printf("\t|%-22s|\n", students[i].getName());
        }
        System.out.println("\t+----------------------+");
    
        System.out.println("\n\nPress Enter to go to the main menu...");
    
        input.nextLine();
    
        clearConsole();
        homePage();
    }
    
	//------------------GENERATE SUMMURY OF SYSTEM----------------------
	public static void generateSummaryOfSystem() {
        if (studentCount == 0) {
            System.out.println("No students in the system.");
            return;
        }
    
        int totalStudents = studentCount;
        int studentsModule1Above40 = 0;
        int studentsModule2Above40 = 0;
        int studentsModule3Above40 = 0;
    
        for (int i = 0; i < studentCount; i++) {
            int[] marks = students[i].getModuleMarks();
            if (marks[0] > 40) {
                studentsModule1Above40++;
            }
            if (marks[1] > 40) {
                studentsModule2Above40++;
            }
            if (marks[2] > 40) {
                studentsModule3Above40++;
            }
        }
    
        clearConsole();
        System.out.println("\t------------ Summary of the System ------------");
        System.out.println("\nTotal student registrations: " + totalStudents);
        System.out.println("\n\nTotal students who scored more than 40 marks");
        System.out.println("\nModule 1: " + studentsModule1Above40);
        System.out.println("Module 2: " + studentsModule2Above40);
        System.out.println("Module 3: " + studentsModule3Above40);
    
        System.out.print("\nPress Enter to return to the homepage...");
        new Scanner(System.in).nextLine();
        clearConsole();
        homePage();
    }
    
	//-------------------------GENERATE REPORT--------------------------
	public static void generateCompleteReport() {
        if (studentCount == 0) {
            System.out.println("No students in the system.");
            return;
        }
        bubbleSortByAverageMarks();
    
        System.out.println("\n\t------------ Report of Students ------------ ");
        System.out.println("\n\n\t+-------------------------------------------------------------------------------------------------------+");
        System.out.println("\t|    ID     |       Name        |  Module 1  |  Module 2  |  Module 3  |  Total  | Average | Grade      |");
        System.out.println("\t+-------------------------------------------------------------------------------------------------------+");
    
        for (int i = 0; i < studentCount; i++) {
            Student student = students[i];
            int[] marks = student.getModuleMarks();
            int total = marks[0] + marks[1] + marks[2];
            double average = getAverageMarks(student);
            String grade = student.getModuleGrade();
    
            System.out.printf("\t|%-12s|%-18s|%-12d|%-12d|%-12d|%-9d|%-9.2f|%-12s|\n",
                    student.getId(),
                    student.getName(),
                    marks[0],
                    marks[1],
                    marks[2],
                    total,
                    average,
                    grade);
        }
    
        System.out.println("\t+-------------------------------------------------------------------------------------------------------+");
    
        System.out.print("\nPress Enter to return to the homepage...");
        new Scanner(System.in).nextLine();
        clearConsole();
        homePage();
    }
    
    private static double getAverageMarks(Student student) {
        int[] marks = student.getModuleMarks();
        return (marks[0] + marks[1] + marks[2]) / 3.0;
    }
    
    private static void bubbleSortByAverageMarks() {
        for (int i = 0; i < studentCount - 1; i++) {
            for (int j = 0; j < studentCount - i - 1; j++) {
                if (getAverageMarks(students[j]) < getAverageMarks(students[j + 1])) {
                    Student temp = students[j];
                    students[j] = students[j + 1];
                    students[j + 1] = temp;
                }
            }
        }
    }
    
	//-----------------------ADDITIONAL CONTROLS------------------------
    public static void additionalControls() {
        clearConsole();
        Scanner input = new Scanner(System.in);
        boolean run = true;
    
        while (run) {
            System.out.println("\t------------ Additional Controls ------------ ");
            System.out.println("\n\n\t[01] Generate a summary of the system");
            System.out.println("\n\t[02] Generate a detailed report");
            System.out.print("\n Enter an option to continue -> ");
    
            try {
                int choice = input.nextInt();
                input.nextLine();
    
                switch (choice) {
                    case 1:
                        clearConsole();
                        generateSummaryOfSystem();
                        break;
                    case 2:
                        clearConsole();
                        generateCompleteReport();
                        break;
                    default:
                        System.out.println("\n\tInvalid Input...");
                        break;
                }
            } catch (InputMismatchException e) {
                System.out.println("\n\tInvalid Input. Please enter a number.");
                input.next(); 
            }
    
            System.out.print("\n\nDo you want to input another number (Y/N) -> ");
            char yesNO = input.next().charAt(0);
            clearConsole();
            char tempOption = Character.toLowerCase(yesNO);
            if (tempOption != 'y') {
                run = false;
                clearConsole();
            }
        }
    }
    //-----------------------------HOME PAGE----------------------------
    public static void homePage() {
        Scanner input = new Scanner(System.in);
        boolean run = true;

        while (run) {
            System.out.println("\t------------ Student Activity Management System ------------ ");
            System.out.println("\n\n\n\t[01] Check available seats");
            System.out.println("\n\t[02] Register student");
            System.out.println("\n\t[03] Delete student ");
            System.out.println("\n\t[04] Find student");
            System.out.println("\n\t[05] Store student details into a file ");
            System.out.println("\n\t[06] Load student details from the file to the system ");
            System.out.println("\n\t[07] View the list of students ");
            System.out.println("\n\t[08] Additional Controls");
            System.out.print("\n Enter an option to continue -> ");

            try {
                int choice = input.nextInt();
                input.nextLine();

                switch (choice) {
                    case 1:
                        clearConsole(); checkAvailableSeats();
                        break;
                    case 2:
                        clearConsole(); registerStudent();
                        break;
                    case 3:
                        clearConsole(); deleteStudent();
                        break;
                    case 4:
                        clearConsole(); findStudent();
                        break;
                    case 5:
                        clearConsole(); storeStudentDetailsIntoTxtFile();
                        break;
                    case 6:
                        clearConsole(); loadStudentDetailsfromTxtFile();
                        break;
                    case 7:
                        clearConsole(); viewSortedStudent();
                        break;
                    case 8:
                        clearConsole(); additionalControls();
                        break;
                    default:
                        System.out.println("\n\tInvalid Input...");
                        break;
                }
            } catch (InputMismatchException e) {
                clearConsole();
                System.out.println("\n\tInvalid Input. Please enter a number.");
                input.next(); 
            }

            System.out.print("\n\nDo you want to input another number (Y/N) -> ");
            char yesNO = input.next().charAt(0);
            clearConsole();
            char tempOption = Character.toLowerCase(yesNO);
            if (tempOption != 'y') {
                run = false;
                clearConsole();
            }
        }
    }
    //-----------------------CLEAR CONSOLE------------------------------
    public final static void clearConsole(){
        try {
            final String os = System.getProperty("os.name");
            if (os.contains("Windows")) {
                new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
            } else {
                System.out.print("\033[H\033[2J");
                System.out.flush();
            }
        } catch (final Exception e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args){
        homePage();

    }
