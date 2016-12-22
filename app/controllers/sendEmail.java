package controllers;

/**
 * Created by akshay on 12/22/2016.
 */

import java.io.IOException;

import com.amazonaws.AmazonClientException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.services.simpleemail.*;
import com.amazonaws.services.simpleemail.model.*;
import com.amazonaws.regions.*;

public class sendEmail {
    static final String FROM = "am4586@columbia.edu";
    static final String TO = "an2756@columbia.edu";
    static final String BODY = "This email was sent through Amazon SES by using the AWS SDK for Java.";
    static final String SUBJECT = "Amazon SES test (AWS SDK for Java)";

    public static void main(String[] args) throws IOException {

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
        }
        catch (Exception ex)
        {
            System.out.println("The email was not sent.");
            System.out.println("Error message: " + ex.getMessage());
        }
    }
}