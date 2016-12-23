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
}
