Created By: Ghelbere Vlad, Nistor Andrei, Lazea Iosua, Totan Gabriel
Note: Some of the Amazon configurations like the API Gateway and a lot of JS & CSS from the front-end is missing from this repository, serving only as a guide with samples.

# Meeting Room Monitor

Meeting rooms are sometimes booked in advance but not used and not released. This problem gets more expensive and time consuming the larger a company gets. Our project aims to solve this inconvenience once and for all.

# Tools

The tools we used to build our website and back-end are all Amazon WS tools:
- API Gateway
- Lambda
- DynamoDB
- Cognito
- S3
- Route 53
- Certificate Managaer
- CloudFront

For our Raspberry script, we used Python 3, our Lambda functions are
written in Node.js 8.10 and most of our website scripts are in JavaScript. 

# Project's Purpose

The main objective of this project is to make things easier for companies
when they want to schedule a meeting. How does the project help with that?
The project's main purpose is to monitor several meeting rooms of a company
at the same time, therefore making more reliable meeting schedules.

# What you will need

- A Raspberry Pi 3 Model B+
- A Webcam (you can also use a Raspberry Camera with some code adjustments)

# The System

Our architecture begins with a Raspberry Pi, placed into a meeting room that we want to monitor. The Raspberry Pi has a camera attached to it, and is running a motion detection algorithm. Each time the algorithm considers that a person is moving inside the room, it takes keeps track of how many persons are inside the room, and which room they are currently inside, then it sends information to two tables from our database, the first table, called ROOMS, stores each room number, the Raspberry Pi state (Online/Offline/Unknown) and the room status (Occupied/Unoccupied) for that room number. The second table, called LOGS, stores a unique ID, the current date, the exact moment at which the motion detection algorithm was triggered, and the moment at which the movement stopped. Also, the room in which the activity took place and the highest number of persons detected at once. Data from the ROOMS table is updated each time someone enters the room, and new entries are added to the LOGS table each time a meeting is done. 

Now for the more technical part, let us see how does everything we mentioned above happens. First, we must keep in mind that all the data we send is packed into a JSON. So, to update the ROOMS tables from the DynamoDB, we send the room name, the Raspberry Pi state and the room status using a POST request towards an API Gateway. Once received, a Lambda function gets called, to handle the JSON. The function opens up the database, splits the JSON into strings, and updates the data inside the table. For a better understanding of the process, see the Data Flow Diagram down below.

# The User

Our user wants to check a room's status, he accesses our website and is instantly prompted with an authentication menu. For a user to be able to access our website, he needs to be part of our Cognito user pool. We suppose that upon joining the company, the user is instantly registered with a username, email adress and a password into our user pool. He also needs to verify the account using his email adress. We did not add a register feature for obvious security reasons. After the email adress has been verified, the user becomes part of the user pool and he can authorize successfully on the website. Once the authorization is made successfully, the user is redirected to the main page, the "Dashboard". Here, he can see each room's status. He can also check the logs, and see which rooms were mostly used. Data from the logs can also be analyzed and used to optimize the usage of the meeting rooms. For example, a room with 10 seats, usually used by 4 to 6 people, is not the optimal solution, therefore we could suggest users meeting rooms based on previous knowledge. For a better understanding of the back-end that is running on our website, see the Client-Server Interactions Diagram down below.

# Performance

Performance wise the script is quite demanding, as it needs to analyze real-time frames and decide if there is someone in the frame and if it should do something about it or not. We tested it on a Raspberry Pi Zero W and concluded that a 1.0 GHz processor is too weak to handle these tasks. After we switched to a Raspberry Pi 3 B, we saw some real improvements even when running only on 1 of the 4 cores of the 3B. Once we started using all of them, the script had no other problems. 

# Costs

The upkeep costs, especially for a big company, can vary depending on how often the app is used, and how many rooms need to be managed as Amazon Cloud Services usually charge you based on how many requests were sent, how many times functions get called and so on. The hardware cost and set-up is quite cheap and also using such a small computer results in small electricity bills.
