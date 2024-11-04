public class Student {
    private String id;
    private String name;
    private Module[] modules;
    private String moduleGrade;

    public Student(String id, String name) {
        this.id = id;
        this.name = name;
        this.modules = new Module[3];
        for (int i = 0; i < 3; i++) {
            modules[i] = new Module();
        }
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setModuleMarks(int[] marks) {
        for (int i = 0; i < marks.length; i++) {
            modules[i].setMark(marks[i]);
        }
    }

    public int[] getModuleMarks() {
        int[] marks = new int[modules.length];
        for (int i = 0; i < modules.length; i++) {
            marks[i] = modules[i].getMark();
        }
        return marks;
    }

    public String getModuleGrade() {
        return moduleGrade;
    }

    public void setModuleGrade(String grade) {
        this.moduleGrade = grade;
    }

    public String calculateGrade() {
        double total = 0;
        for (Module module : modules) {
            total += module.getMark();
        }
        double average = total / modules.length;

        if (average >= 80) {
            return "Distinction";
        } else if (average >= 70) {
            return "Merit";
        } else if (average >= 40) {
            return "Pass";
        } else {
            return "Fail";
        }
    }
}
