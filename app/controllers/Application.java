package controllers;
import com.amazonaws.AmazonServiceException;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.*;
import models.Event;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import com.amazonaws.AmazonClientException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.regions.Region;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.simpleemail.AmazonSimpleEmailServiceClient;
import com.amazonaws.services.simpleemail.model.*;
import com.amazonaws.services.sqs.AmazonSQS;
import com.amazonaws.services.sqs.AmazonSQSClient;
import com.amazonaws.services.sqs.model.SendMessageRequest;

import models.Organization;
import play.data.DynamicForm;
import play.data.FormFactory;
import play.mvc.Controller;
import play.mvc.Result;
import views.html.*;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import javax.inject.Inject;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.TimeZone;

import com.amazonaws.services.sqs.model.DeleteMessageRequest;
import com.amazonaws.services.sqs.model.ReceiveMessageRequest;

public class Application extends Controller {

    @Inject
    FormFactory formFactory;

    public Result index() {
        pushToS3("hello","bye.json");
        return ok(index.render());
    }

    public Result showVolunteerPage(){
        return ok(volunteer.render());
    }

    public Result showOrganizationPage(){
        ArrayList<Event> eventList = new ArrayList<Event>();
        for(int i=0;i<5;i++){
            eventList.add(new Event("2:00","4:00","12 Dec 2016","CS, Java","New York","Social Event Name"));
        }

        return ok(organization.render(eventList));
    }

    public Result showVolunteerSearchPage(){
        return ok(searchVolunteer.render());
    }
    public Result showOrganizationSearchPage(){
        return ok(searchOrganization.render());
    }

    public Result volunteerCompleteProfile(String fname,String lname,String email, String vid,String location,String numCons, String imgURL, String industry) throws UnsupportedEncodingException {
//        System.out.println(fname);
//        System.out.println(lname);
//        System.out.println(vid);
//        System.out.println(location);
//        URLDecoder u = new URLDecoder();
//        String cleanLocation = u.decode(location, "UTF-8");
//        System.out.println(numCons);
//        System.out.println(imgURL);
//        System.out.println(email);
//        System.out.println(industry);

//        try {
//            HttpURLConnection con = (HttpURLConnection) new URL("http://search-angelmatch-6k3puk6rfr3ks6deaxk6qmgfgm.us-east-1.es.amazonaws.com/data/volunteer/_search").openConnection();
//            con.setRequestMethod("GET");
//            con.setDoOutput(true);
//            con.setRequestProperty("Content-Type", "application/json");
//            con.setRequestProperty("Accept", "application/json");
//            con.connect();
//
//            String query =  "{ \"query\": { \"term\":{ \"name\": \""+vid+"\"} } }";
//            byte[] outputBytes = query.getBytes("UTF-8");
//            OutputStream os = con.getOutputStream();
//            os.write(outputBytes);
//
//            os.close();
//            System.out.println(con.getResponseMessage());
//
//        } catch (MalformedURLException e1) {
//            // TODO Auto-generated catch block
//            e1.printStackTrace();
//        } catch (IOException e1) {
//            // TODO Auto-generated catch block
//            e1.printStackTrace();
//        }
        return ok(vfillprofile.render(fname,lname,email,vid,location,numCons,imgURL,industry));
    }

    public Result processVolunteerForm() throws ParseException, IOException {
        DynamicForm volunteerData = formFactory.form().bindFromRequest();
        String vid = volunteerData.get("vid");
        String firstName = volunteerData.get("fname");
        String lastName = volunteerData.get("lname");
        String location = volunteerData.get("location");
        String email = volunteerData.get("email");
        sendEmail(email,"Thanks for signing up for Angelmatch","Angelmatch Registration");
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

    public String[] convertfromMillis(long millis) throws ParseException {

        Calendar calendar = Calendar.getInstance();
        calendar.setTimeInMillis(millis);

        int mYear = calendar.get(Calendar.YEAR);
        int mMonth = calendar.get(Calendar.MONTH);
        int mDay = calendar.get(Calendar.DAY_OF_MONTH);

        int mHour = calendar.get(Calendar.HOUR_OF_DAY);
        int mMinute = calendar.get(Calendar.MINUTE);

        String[] date = {mYear+"-"+mMonth+"-"+mDay,mHour+"-"+mMinute};


        return date;
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

        try {
            HttpURLConnection con = (HttpURLConnection) new URL("http://search-angelmatch-6k3puk6rfr3ks6deaxk6qmgfgm.us-east-1.es.amazonaws.com/data_org/organization").openConnection();
            con.setRequestMethod("POST");
            con.setDoOutput(true);
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("Accept", "application/json");
            con.connect();

            StringBuilder user = new StringBuilder();
            user.append("{ \"uid\":\"");
            user.append(System.currentTimeMillis() + oid.trim());
            user.append("\", \"id\":\"");
            user.append(oid);
            user.append("\", \"name\":\"");
            user.append(name);
            user.append("\", \"email\":\"");
            user.append(email);
            user.append("\", \"num_years\":");
            user.append(operationYears);
            user.append(", \"location\":\"");
            user.append(location);
            user.append("\", \"causes_supported\":[\"");
            user.append(issuesSupported);
            user.append("\"] } ");
            String query = user.toString();
            byte[] outputBytes = query.getBytes("UTF-8");
            OutputStream os = con.getOutputStream();
            os.write(outputBytes);

            os.close();
            System.out.println("ORG_POSTED"+con.getResponseCode());
        } catch (MalformedURLException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        }
        ArrayList<Event> eventList = new ArrayList<Event>();
        for(int i=0;i<5;i++){
            eventList.add(new Event("2:00","4:00","12 Dec 2016","CS, Java","New York","Social Event Name"));
        }

        return(ok(organization.render(eventList)));
    }

    public Result addEvent() throws org.json.simple.parser.ParseException, ParseException {
        DynamicForm eventData = formFactory.form().bindFromRequest();
        String eventName = eventData.get("event_name");
        String eventDate = eventData.get("event_date");
        String eventStartTime = eventData.get("eventStartTime");
        String eventEndTime = eventData.get("eventEndTime");
        String eventSkills = eventData.get("event_skills");

        String org_id = "12345678"; //TODO: replace with actual org_id

        try {
            HttpURLConnection con = (HttpURLConnection) new URL("http://search-angelmatch-6k3puk6rfr3ks6deaxk6qmgfgm.us-east-1.es.amazonaws.com/data_org/organization/_search").openConnection();
            con.setRequestMethod("GET");
            con.setDoOutput(true);
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("Accept", "application/json");
            con.connect();

            String query =  "{ \"query\": { \"term\":{ \"id\": \""+org_id+"\"} } }";
            byte[] outputBytes = query.getBytes("UTF-8");
            OutputStream os = con.getOutputStream();
            os.write(outputBytes);

            os.close();
            System.out.println(con.getResponseMessage());
            BufferedReader br = new BufferedReader(new InputStreamReader((con.getInputStream())));
            StringBuilder sb = new StringBuilder();
            String output;
            while ((output = br.readLine()) != null) {
                sb.append(output);
            }
            String responseString = sb.toString();

            JSONParser parser = new JSONParser();
            JSONObject json = (JSONObject) parser.parse(responseString);
            JSONObject hitsInner = (JSONObject) json.get("hits");
            JSONArray dataArray = (JSONArray) hitsInner.get("hits");
            JSONObject firstObject = (JSONObject) dataArray.get(0);
            JSONObject data = (JSONObject) firstObject.get("_source");

            System.out.println(data.toString());

            try {
                HttpURLConnection con_new = (HttpURLConnection) new URL("http://search-angelmatch-6k3puk6rfr3ks6deaxk6qmgfgm.us-east-1.es.amazonaws.com/data_org/organization").openConnection();
                con_new.setRequestMethod("POST");
                con_new.setDoOutput(true);
                con_new.setRequestProperty("Content-Type", "application/json");
                con_new.setRequestProperty("Accept", "application/json");
                con_new.connect();

                StringBuilder user = new StringBuilder();
                user.append("{ \"uid\":\"");
                user.append(String.valueOf(System.currentTimeMillis()) + data.get("id"));
                user.append("\", \"id\":\"");
                user.append(data.get("id"));
                user.append("\", \"name\":\"");
                user.append(data.get("name"));
                user.append("\", \"email\":\"");
                user.append(data.get("email"));
                user.append("\", \"num_years\":");
                user.append(data.get("num_years"));
                user.append(", \"location\":\"");
                user.append(data.get("location"));
                user.append("\", \"skills\":[\"");
                user.append(eventSkills);
                user.append("\"], \"event_name\":\"");
                user.append(eventName);
                user.append("\", \"time_from\":");
                long eStart = convertToMillis(eventDate,eventStartTime);
                long eEnd = convertToMillis(eventDate,eventEndTime);
                user.append(eStart);
                user.append(", \"time_to\":");
                user.append(eEnd);
                user.append(", \"summary\":\"");
                user.append("Lorem Ipsum"); //TODO: get summary
                user.append("\", \"causes_supported\":");
                user.append(data.get("causes_supported"));
                user.append(" }");
                String query_new = user.toString();
                byte[] outputBytes_new = query_new.getBytes("UTF-8");
                OutputStream os_new = con_new.getOutputStream();
                os_new.write(outputBytes_new);

                os.close();
                System.out.println("ORG_POSTED"+con_new.getResponseCode());
            } catch (MalformedURLException e1) {
                // TODO Auto-generated catch block
                e1.printStackTrace();
            } catch (IOException e1) {
                // TODO Auto-generated catch block
                e1.printStackTrace();
            }



        } catch (MalformedURLException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        }
        ArrayList<Event> eventList = new ArrayList<Event>();
        for(int i=0;i<5;i++){
            eventList.add(new Event("2:00","4:00","12 Dec 2016","CS, Java","New York","Social Event Name"));
        }

        return ok(organization.render(eventList));
    }
    public Result orgCompleteProfile(){
        return ok(ofillprofile.render());
    }

    public boolean sendEmail(String emailID,String text,String heading){
        String FROM = "am4586@columbia.edu";
        String TO = emailID;
        String BODY = text;
        String SUBJECT = heading;
        AWSCredentials credentials = null;

        // Construct an object to contain the recipient address.
        Destination destination = new Destination().withToAddresses(new String[]{TO});

        // Create the subject and body of the message.
        Content subject = new Content().withData(SUBJECT);
        Content textBody = new Content().withData(BODY);
        Body body = new Body().withText(textBody);

        // Create a message with the specified subject and body.
        Message message = new Message().withSubject(subject).withBody(body);

        // Assemble the email.
        SendEmailRequest request = new SendEmailRequest().withSource(FROM).withDestination(destination).withMessage(message);

        try
        {
            System.out.println("Attempting to send an email through Amazon SES by using the AWS SDK for Java...");

            try {
                credentials = new ProfileCredentialsProvider().getCredentials();
            } catch (Exception e) {
                throw new AmazonClientException(
                        "Cannot load the credentials from the credential profiles file. " +
                                "Please make sure that your credentials file is at the correct " +
                                "location (~/.aws/credentials), and is in valid format.",
                        e);
            }


            AmazonSimpleEmailServiceClient client = new AmazonSimpleEmailServiceClient();
            Region REGION = Region.getRegion(Regions.US_EAST_1);
            client.setRegion(REGION);
            client.sendEmail(request);
            System.out.println("Email sent!");
            return true;
        }
        catch (Exception ex)
        {
            System.out.println("The email was not sent.");
            System.out.println("Error message: " + ex.getMessage());
            return false;
        }
    }

    public Result orgLogin(){
        return ok(orgLogin.render());
    }

    public Result checkOrgLogin() throws IOException, org.json.simple.parser.ParseException {
        System.out.println("inside checkkkk!");
        DynamicForm orgLoginData = formFactory.form().bindFromRequest();
        String email = orgLoginData.get("orgEmail");

        /////////////////////////////////////////////////////////////////////////////
        /////// GET ALL ORG Data from ES (Abhijeet) /////////////////////////////////
        ///////Store into an array so that I can send this to Org Profile page///////
        /////////////////////////////////////////////////////////////////////////////
        ArrayList<Event> eventList = new ArrayList<Event>();
        try {
            HttpURLConnection con = (HttpURLConnection) new URL("http://search-angelmatch-6k3puk6rfr3ks6deaxk6qmgfgm.us-east-1.es.amazonaws.com/data_org/organization/_search").openConnection();
            con.setRequestMethod("GET");
            con.setDoOutput(true);
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("Accept", "application/json");
            con.connect();

            String query = "{ \"query\": { \"term\":{ \"email\": \"" + email + "\"} } }";
            byte[] outputBytes = query.getBytes("UTF-8");
            OutputStream os = con.getOutputStream();
            os.write(outputBytes);

            os.close();
            System.out.println(con.getResponseMessage());
            BufferedReader br = new BufferedReader(new InputStreamReader((con.getInputStream())));
            StringBuilder sb = new StringBuilder();
            String output;
            while ((output = br.readLine()) != null) {
                sb.append(output);
            }
            String responseString = sb.toString();

            JSONParser parser = new JSONParser();
            JSONObject json = (JSONObject) parser.parse(responseString);
            JSONObject hitsInner = (JSONObject) json.get("hits");
            JSONArray dataArray = (JSONArray) hitsInner.get("hits");
            Organization[] oArray = new Organization[dataArray.size()];
            for(int i=0;i<dataArray.size();i++){
                JSONObject firstObject = (JSONObject) dataArray.get(i);
                JSONObject data = (JSONObject) firstObject.get("_source");
                if(data.containsKey("time_from")){
                    String[] date_from = convertfromMillis(Long.parseLong(data.get("time_from").toString()));
                    String[] date_to = convertfromMillis(Long.parseLong(data.get("time_to").toString()));
                    eventList.add(new Event(date_from[1],date_to[1],date_from[0],data.get("skills").toString(),data.get("location").toString(),data.get("name").toString()));
                }

                System.out.println(data.size());
            }
//            System.out.println(data.toString());

        }catch (Exception e){
            e.printStackTrace();
        }


        return ok(organization.render(eventList));
    }

    public String pushToS3(String jsonContent,String fileName){
        String existingBucketName  = "angelmatch";
        String keyName             = fileName;
        AWSCredentials credentials = null;
        try {
            credentials = new ProfileCredentialsProvider().getCredentials();
        } catch (Exception e) {
            throw new AmazonClientException(
                    "Cannot load the credentials from the credential profiles file. " +
                            "Please make sure that your credentials file is at the correct " +
                            "location (~/.aws/credentials), and is in valid format.",
                    e);
        }
        AmazonS3 s3Client = new AmazonS3Client(credentials);
//        s3Client.putObject(new PutObjectRequest(existingBucketName, keyName,
//                new File("C:\\Users\\akshay\\Desktop\\testS3.json")).withCannedAcl(CannedAccessControlList.PublicRead));
        String onlineFilePath = "https://s3.amazonaws.com/angelmatch/" + keyName;
        Boolean sqsStatus = pushtoSqs("Computer|Python","Women Empowerment|Homeless","12345678",onlineFilePath);
        System.out.println("SQS Status: "+sqsStatus);
        return onlineFilePath;
    }

    public boolean pushtoSqs(String skills,String causes, String id,String url){

        AWSCredentials credentials = null;
        try {
            credentials = new ProfileCredentialsProvider().getCredentials();
        } catch (Exception e) {
            throw new AmazonClientException(
                    "Cannot load the credentials from the credential profiles file. " +
                            "Please make sure that your credentials file is at the correct " +
                            "location (~/.aws/credentials), and is in valid format.",
                    e);
        }

        AmazonSQS sqs = new AmazonSQSClient(credentials);
        String messageToSend = skills+","+causes+","+url;
        try{
            sqs.sendMessage(new SendMessageRequest("https://sqs.us-east-1.amazonaws.com/021959201754/angelpush", messageToSend));
            return true;
        }catch (AmazonServiceException ase) {
            System.out.println("Caught an AmazonServiceException, which means your request made it " +
                    "to Amazon SQS, but was rejected with an error response for some reason.");
            System.out.println("Error Message:    " + ase.getMessage());
            System.out.println("HTTP Status Code: " + ase.getStatusCode());
            System.out.println("AWS Error Code:   " + ase.getErrorCode());
            System.out.println("Error Type:       " + ase.getErrorType());
            System.out.println("Request ID:       " + ase.getRequestId());
            return false;
        }catch (AmazonClientException ace) {
            System.out.println("Caught an AmazonClientException, which means the client encountered " +
                    "a serious internal problem while trying to communicate with SQS, such as not " +
                    "being able to access the network.");
            System.out.println("Error Message: " + ace.getMessage());
            return false;
        }
    }

    public Result rankedVolunteers(){
        return ok(rankedVolunteers.render());
    }

    public String pullfromSqs(){
        AWSCredentials credentials = null;
        try {
            credentials = new ProfileCredentialsProvider().getCredentials();
        } catch (Exception e) {
            throw new AmazonClientException(
                    "Cannot load the credentials from the credential profiles file. " +
                            "Please make sure that your credentials file is at the correct " +
                            "location (~/.aws/credentials), and is in valid format.",
                    e);
        }

        AmazonSQS sqs = new AmazonSQSClient(credentials);
        ReceiveMessageRequest receiveMessageRequest = new ReceiveMessageRequest("https://sqs.us-east-1.amazonaws.com/021959201754/machinepull");
        List<com.amazonaws.services.sqs.model.Message> messages;
        while(true){
            messages = sqs.receiveMessage(receiveMessageRequest).getMessages();
            if(!messages.isEmpty()){
                break;
            }
        }

        com.amazonaws.services.sqs.model.Message message = messages.get(0);
        String messageData = message.getBody();

        // Delete a message
        System.out.println("Deleting a message.\n");
        String messageReceiptHandle = messages.get(0).getReceiptHandle();
        sqs.deleteMessage(new DeleteMessageRequest()
                .withQueueUrl("https://sqs.us-east-1.amazonaws.com/021959201754/machinepull")
                .withReceiptHandle(messageReceiptHandle));

        return messageData;
    }

}

