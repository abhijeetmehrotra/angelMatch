package controllers;
import play.data.DynamicForm;
import play.data.FormFactory;
import play.mvc.Controller;
import play.mvc.Result;
import views.html.*;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import javax.inject.Inject;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.List;

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

    public Result volunteerCompleteProfile(String fname,String lname,String email, String vid,String location,String numCons, String imgURL, String industry) throws UnsupportedEncodingException {
        System.out.println(fname);
        System.out.println(lname);
        System.out.println(vid);
        System.out.println(location);
        URLDecoder u = new URLDecoder();
        String cleanLocation = u.decode(location, "UTF-8");
        System.out.println(numCons);
        System.out.println(imgURL);
        System.out.println(email);
        System.out.println(industry);

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
        return ok(vfillprofile.render(fname,lname,email,vid,cleanLocation,numCons,imgURL,industry));
    }

    public Result processVolunteerForm(){
        DynamicForm volunteerData = formFactory.form().bindFromRequest();
        String vid = volunteerData.get("vid");
        String firstName = volunteerData.get("fname");
        String lastName = volunteerData.get("lname");
        String location = volunteerData.get("location");
        String email = volunteerData.get("email");
        String industry = volunteerData.get("industry");
        String imageURL = volunteerData.get("imageURL");
        String skills = volunteerData.get("skills");
        String endorsements = volunteerData.get("endorsements");
        String numCons = volunteerData.get("numCons");
        String we = volunteerData.get("we");
        String ce = volunteerData.get("ce");
        String lg = volunteerData.get("lg");
        String vet = volunteerData.get("vet");
        String hs = volunteerData.get("hs");
        String sa = volunteerData.get("sa");
        String aw = volunteerData.get("aw");
        String issuesSupported = "";
        if(we!=null){
            issuesSupported+=we;
        }
        String yearsExperience = volunteerData.get("yearsExperience");
        String d1 = volunteerData.get("ts1");
        String tf1 = volunteerData.get("ts1_from");
        String tt1 = volunteerData.get("ts1_to");
        String d2 = volunteerData.get("ts2");
        String tf2 = volunteerData.get("ts2_from");
        String tt2 = volunteerData.get("ts2_to");
        String d3 = volunteerData.get("ts3");
        String tf3 = volunteerData.get("ts3_from");
        String tt3 = volunteerData.get("ts3_to");

        System.out.println("FORM SUBMITTED DATA");
        System.out.println(vid);
        System.out.println(firstName);
        System.out.println(lastName);
        System.out.println(location);
        System.out.println(email);
        System.out.println(imageURL);
        System.out.println(skills);
        System.out.println(endorsements);
        System.out.println(numCons);
        System.out.println(issuesSupported);
        System.out.println(yearsExperience);
        System.out.println(d1);
        System.out.println(tf1);
        System.out.println(tt1);
        System.out.println(d2);
        System.out.println(tf2);
        System.out.println(tt2);
        System.out.println(d3);
        System.out.println(tf3);
        System.out.println(tt3);
        System.out.println(industry);

        return(ok(volunteer.render()));
    }
}
