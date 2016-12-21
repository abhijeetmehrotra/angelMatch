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

    @Transactional
    public Result addPerson() {
        Volunteer volunteer = formFactory.form(Volunteer.class).bindFromRequest().get();
        JPA.em().persist(volunteer);
        return redirect(routes.Application.index());
    }

    @Transactional(readOnly = true)
    public Result getPersons() {
        List<Volunteer> volunteers = (List<Volunteer>) JPA.em().createQuery("select p from Person p").getResultList();
        return ok(toJson(volunteers));
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
}
