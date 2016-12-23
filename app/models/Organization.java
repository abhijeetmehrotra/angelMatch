package models;

/**
 * Created by akshay on 12/20/2016.
 */
public class Organization {
    String id,name,location,email,issuesSupported;

    Organization(String id,String name,String location,String email,String issuesSupported){
        this.id = id;
        this.name = name;
        this.location = location;
        this.email = email;
        this.issuesSupported = issuesSupported;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getLocation() {
        return location;
    }

    public String getEmail() {
        return email;
    }

    public String getIssuesSupported() {
        return issuesSupported;
    }

    public void setId(String id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setIssuesSupported(String issuesSupported) {
        this.issuesSupported = issuesSupported;
    }
}
