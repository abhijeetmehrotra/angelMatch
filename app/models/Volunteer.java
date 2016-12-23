package models;

/**
 * Created by akshay on 12/20/2016.
 */
public class Volunteer {
    String firstName,lastName,skills,issues,yearsExperience,location;
    Volunteer(String firstName, String lastname,String skills,String issues,String yearsExperience,String location){
        this.firstName = firstName;
        this.lastName = lastname;
        this.skills = skills;
        this.issues = issues;
        this.yearsExperience = yearsExperience;
        this.location = location;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getSkills() {
        return skills;
    }

    public String getIssues() {
        return issues;
    }

    public String getYearsExperience() {
        return yearsExperience;
    }

    public String getLocation() {
        return location;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public void setSkills(String skills) {
        this.skills = skills;
    }

    public void setIssues(String issues) {
        this.issues = issues;
    }

    public void setYearsExperience(String yearsExperience) {
        this.yearsExperience = yearsExperience;
    }

    public void setLocation(String location) {
        this.location = location;
    }
}
