package controllers;
import models.Volunteer;
import play.data.FormFactory;
import play.db.jpa.JPA;
import play.db.jpa.Transactional;
import play.mvc.Controller;
import play.mvc.Result;
import views.html.*;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Map;

import javax.inject.Inject;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
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

    public Result volunteerCompleteProfile(String fname,String lname,String email, String vid,String location,String numCons, String imgURL) throws UnsupportedEncodingException {
        System.out.println(fname);
        System.out.println(lname);
        System.out.println(vid);
        System.out.println(location);
        URLDecoder u = new URLDecoder();
        String cleanLocation = u.decode(location, "UTF-8");
        System.out.println(numCons);
        System.out.println(imgURL);
        System.out.println(email);

        try {
            HttpURLConnection con = (HttpURLConnection) new URL("http://search-angelmatch-6k3puk6rfr3ks6deaxk6qmgfgm.us-east-1.es.amazonaws.com/data/volunteer/_search").openConnection();
            con.setRequestMethod("GET");
            con.setDoOutput(true);
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("Accept", "application/json");
            con.connect();

            String query =  "{ \"query\": { \"term\":{ \"name\": \""+vid+"\"} } }";
            byte[] outputBytes = query.getBytes("UTF-8");
            OutputStream os = con.getOutputStream();
            os.write(outputBytes);

            os.close();
            System.out.println(con.getResponseMessage());

        } catch (MalformedURLException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        }



        return ok(vfillprofile.render(fname,lname,email,vid,cleanLocation,numCons,imgURL));
    }
}
