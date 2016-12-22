package controllers;
import play.data.DynamicForm;
import play.data.FormFactory;
import play.mvc.Controller;
import play.mvc.Result;
import views.html.*;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import javax.inject.Inject;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.TimeZone;

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

    public Result processVolunteerForm() throws ParseException, IOException {
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
        String[] issues = new String[7];
        issues[0] = volunteerData.get("we");
        issues[1] = volunteerData.get("ce");
        issues[2] = volunteerData.get("lg");
        issues[3] = volunteerData.get("vet");
        issues[4] = volunteerData.get("hs");
        issues[5] = volunteerData.get("sa");
        issues[6] = volunteerData.get("aw");
        StringBuilder issuesString = new StringBuilder();
        for(int i=0;i<issues.length;i++){
            if(issues[i]!=null){
                issuesString.append(issues[i]);
                issuesString.append(",");
            }
        }
        String issuesSupported = issuesString.toString();
        issuesSupported = issuesSupported.substring(0,issuesSupported.length()-1);
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
        long ts1start=0, ts1end=0, ts2start=0, ts2end=0, ts3start=0, ts3end=0;
        try {
             ts1start = convertToMillis(d1,tf1);
             ts1end = convertToMillis(d1,tt1);
             ts2start = convertToMillis(d2,tf2);
             ts2end = convertToMillis(d2,tt2);
             ts3start = convertToMillis(d3,tf3);
             ts3end = convertToMillis(d3,tt3);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        boolean exists = userExists(vid);
        if(!exists) {
            try {
                HttpURLConnection con = (HttpURLConnection) new URL("http://search-angelmatch-6k3puk6rfr3ks6deaxk6qmgfgm.us-east-1.es.amazonaws.com/data/volunteer").openConnection();
                con.setRequestMethod("POST");
                con.setDoOutput(true);
                con.setRequestProperty("Content-Type", "application/json");
                con.setRequestProperty("Accept", "application/json");
                con.connect();

                StringBuilder user = new StringBuilder();
                user.append("{ \"uid\":\"");
                user.append(System.currentTimeMillis() + vid.trim());
                user.append("\", \"id\":\"");
                user.append(vid);
                user.append("\", \"fname\":\"");
                user.append(firstName);
                user.append("\", \"lname\":\"");
                user.append(lastName);
                user.append("\", \"email\":\"");
                user.append(email);
                user.append("\", \"image_url\":\"");
                user.append(imageURL);
                user.append("\", \"skills\":[\"");
                user.append(skills);
                user.append("\"], \"endorsements\":[\"");
                user.append(endorsements);
                user.append("\"], \"volunteer_experience\":");
                user.append(yearsExperience);
                user.append(", \"num_connections\":");
                user.append(numCons);
                user.append(", \"location\":\"");
                user.append(location);
                user.append("\", \"causes_supported\":[\"");
                user.append(issuesSupported);
                user.append("\"], \"industry\":\"");
                user.append(industry);
                user.append("\", \"time_from\":");
                user.append(ts1start);
                user.append(", \"time_to\":");
                user.append(ts1end);
                user.append(" }");
                String query = user.toString();
                byte[] outputBytes = query.getBytes("UTF-8");
                OutputStream os = con.getOutputStream();
                os.write(outputBytes);

                os.close();
            } catch (MalformedURLException e1) {
                // TODO Auto-generated catch block
                e1.printStackTrace();
            } catch (IOException e1) {
                // TODO Auto-generated catch block
                e1.printStackTrace();
            }
        }
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
    public long convertToMillis(String day, String time) throws ParseException {
        String time_slot = day + " " + time;
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        sdf.setTimeZone(TimeZone.getTimeZone("EST"));
        Date date = sdf.parse(time_slot);
        return date.getTime();
    }

    public boolean userExists(String id) throws IOException {
        try {
            HttpURLConnection con = (HttpURLConnection) new URL("http://search-angelmatch-6k3puk6rfr3ks6deaxk6qmgfgm.us-east-1.es.amazonaws.com/data/volunteer/_search").openConnection();
            con.setRequestMethod("GET");
            con.setDoOutput(true);
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("Accept", "application/json");
            con.connect();

            String query =  "{ \"query\": { \"term\":{ \"id\": \""+id+"\"} } }";
            byte[] outputBytes = query.getBytes("UTF-8");
            OutputStream os = con.getOutputStream();
            os.write(outputBytes);

            os.close();
            BufferedReader br = new BufferedReader(new InputStreamReader((con.getInputStream())));
            StringBuilder sb = new StringBuilder();
            String output;
            while ((output = br.readLine()) != null) {
                sb.append(output);
            }
            if(sb.toString().contains("\"hits\":{\"total\":1,")){
                return true;
            }
            return false;


        } catch (MalformedURLException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        }
        return true;
    }

    public Result processOrgForm(){
        DynamicForm orgData = formFactory.form().bindFromRequest();
        String oid = orgData.get("org_id");
        String name = orgData.get("name");
        String location = orgData.get("location");
        String email = orgData.get("email");
        String[] issues = new String[7];
        issues[0] = orgData.get("we");
        issues[1] = orgData.get("ce");
        issues[2] = orgData.get("lg");
        issues[3] = orgData.get("vet");
        issues[4] = orgData.get("hs");
        issues[5] = orgData.get("sa");
        issues[6] = orgData.get("aw");
        StringBuilder issuesString = new StringBuilder();
        for(int i=0;i<issues.length;i++){
            if(issues[i]!=null){
                issuesString.append(issues[i]);
                issuesString.append(",");
            }
        }
        String issuesSupported = issuesString.toString();
        issuesSupported = issuesSupported.substring(0,issuesSupported.length()-1);

        String operationYears = orgData.get("yearsOperation");
        System.out.println(oid);
        System.out.println(name);
        System.out.println(email);
        System.out.println(location);
        System.out.println(operationYears);
        System.out.println(issuesSupported);
        /////////////////////////////////////////
        /////// Push to ES Here (Abhijeet) //////
        /// DONT FORGET BLANK START END TIMES////
        /////////////////////////////////////////
        return(ok(organization.render()));
    }

    public Result addEvent(){
        DynamicForm eventData = formFactory.form().bindFromRequest();
        String eventName = eventData.get("event_name");
        String eventDate = eventData.get("event_date");
        String eventStartTime = eventData.get("eventStartTime");
        String eventEndTime = eventData.get("eventEndTime");
        String eventSkills = eventData.get("eventSkills");

        /////////////////////////////////////////////////////////////
        /////// Push to ES Here (Abhijeet) //////////////////////////
        // for now push to org with any NAME and other properties ///
        /////////////////////////////////////////////////////////////
        return ok(organization.render());
    }
    public Result orgCompleteProfile(){
        return ok(ofillprofile.render());
    }
}
