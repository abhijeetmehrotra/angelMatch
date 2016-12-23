package models;

/**
 * Created by akshay on 12/23/2016.
 */
public class Event {
    String fromTime, toTime, date, skillsRequired,location,name,issues;



    public Event(String fromTime, String toTime, String date, String skillsRequired, String location, String name, String issues) {
        this.fromTime = fromTime;
        this.toTime = toTime;
        this.date = date;
        this.skillsRequired = skillsRequired;
        this.location = location;
        this.name = name;
        this.issues = issues;
    }

    public String getIssues() {
        return issues;
    }

    public String getFromTime() {
        return fromTime;
    }
    public String getName() {
        return name;
    }

    public String getToTime() {
        return toTime;
    }

    public String getDate() {
        return date;
    }

    public String getSkillsRequired() {
        return skillsRequired;
    }

    public String getLocation() {
        return location;
    }

    public void setFromTime(String fromTime) {
        this.fromTime = fromTime;
    }

    public void setToTime(String toTime) {
        this.toTime = toTime;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public void setSkillsRequired(String skillsRequired) {
        this.skillsRequired = skillsRequired;
    }

    public void setLocation(String location) {
        this.location = location;
    }
}
