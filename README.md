# CuttingSwap

#### Description:

CuttingSwap is a website implemented with the Flask framework
whose purpose is to connect people who love plants and want to
exchange some plant cuttings with other people.

## Features

The website has an authentication mechanism, and users may log in and register.
Most functionalities are unavailable to non-logged-in users.
Users have profiles that contains their name, location, general info, offers that are made by them.
The website contains two main parts. One for submitting and searching for offers,
and the second one for messaging between users.


The website uses the Flask framework, as well as some Flask plug-ins.
The database is sqlite, accessed through an ORM called SQLAlchemy.
SQLAlchemy is used through a Flask plug-in called Flask-SQLAlchemy.
I used other Flask plug-ins for email, login and session management,
database migration, datetime localization, HTML form generation, etc.

## Project organization

The project is split up into Flask's so called *Blueprints*.
There are blueprints for index page, authentication, user-related things,
offer-related things, messages.

I will describe the funcionality of each blueprint.

### Login

Login is where registration, email verification, logging in and password changes are performed.
It's neccessary for the users to be logged in for using the funcionalities of the website.

### Users

Users contains endpoints for viewing and editing user data.
A user may edit only their own profile, unless they are an administrator. Administrators may edit any profile.
There is also an endpoint for listing all users which is avilable only to administrators.

### Offers

'Offers' has endpoints for listing all offers (optionally filtered), adding new offers and viewing offers.
Beside a description and title, the offers include images which are uploaded to the server and stored (by filename) in the database.
Offer should contain a title, description, location, picture(s). Once the pictures are uploaded they are presented as a carousel.
When the offer is submitted the user will see its own post. At the Offers page the user can see the list of all the posts (by clicking on 
'show own posts' including their posts or not). By clicking on the title of the offer or at the picture, the user can see a single offer.
By clicking on the single offer the user can see the button 'Send Message' which would directly lead them to the conversation with another user 
about that particular offer.

### Messages

'Messages' contains endpoints for starting conversations regarding an offer or free-form conversations with a subject.
It also contains endpoints for viewing and listing said conversations and sending new messages.
So, when the user is at a single offer, there is a possibility to send a message to another user about particular offer, but
once there is a conversation listed with the title of that offer there is no way for starting another conversation about the same offer. 
If there already is a conversation about some offer by slicking 'send message' the user will be send to the existing conversation.
As it is already said, there is a possibility to send a message which is not considered about any particular offer. But there always should be
a title of the conversation.
THe user can see the list of all the conversations by going on 'Messages' page. There are listed all the existing conversations, regardless
of the sbject concerned. They are listed by timestamp, the newest are at the top off the list.
