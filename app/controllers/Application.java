package controllers;
import models.Volunteer;
import play.data.FormFactory;
import play.db.jpa.JPA;
import play.db.jpa.Transactional;
import play.mvc.Controller;
import play.mvc.Result;
import views.html.*;

import javax.inject.Inject;
import java.util.List;

import static play.libs.Json.toJson;

public class Application extends Controller {

    @Inject
    FormFactory formFactory;

    public Result index() {
        return ok(index.render());
    }

    public Result showVolunteerPage(){
        return ok(volunteer.render());
    }

    public Result showOrganizationPage(){
        return ok(organization.render());
    }

    public Result showVolunteerSearchPage(){
        return ok(searchVolunteer.render());
    }
    public Result showOrganizationSearchPage(){
        return ok(searchOrganization.render());
    }

    public Result volunteerCompleteProfile(String fname,String lname,String vid,String location,String numCons, String imgURL){
        System.out.println(fname);
        System.out.println(lname);
        System.out.println(vid);
        System.out.println(location);
        System.out.println(numCons);
        System.out.println(imgURL);

//        PRINT "EXISTS' IF ES HAS USER ELSE PRINT NEW USER  (ABHIJEET)

        return ok(vfillprofile.render());
    }
}
