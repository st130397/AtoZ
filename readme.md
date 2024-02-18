AtoZ Blogger:


Description - AtoZ Blogger is use to register the user either the admin or the author,apart from this it is use to create, view, edit, search and delete the content created by user.


Install all the dependencies using:
pip install -r requirements.txt


Endpoint - /api/register/
Functioning - This is used to register a new user
Method - POST
Payload - 
{
	"first_name": "Shivam",
	"last_name": "Tiwari",
	"username": "st.1303",
	"passkey": "Shivam",
	"email": "st.1303786@gmail.com",
	"mobile_number": 8291212213,
	"pincode": 400101,
	"role": "author"
}
Response - 
{
    "status": "success",
	"data": {
        "first_name": "Shivam",
        "last_name": "Tiwari",
        "username": "st.1303",
        "email": "st.1303786@gmail.com",
        "mobile_number": 8291212213,
        "pincode": 400101,
        "role": "author",
        "token": "<token>"
    }
}

Endpoint - /api/login/
Functioning - This is used to login the existing user
Method - POST
Payload - 
{
	"username": "st.1303",
	"passkey": "Shivam"
}
Response - 
{
    "status": "success",
	"data": {
        "first_name": "Shivam",
        "last_name": "Tiwari",
        "username": "st.1303",
        "email": "st.1303786@gmail.com",
        "mobile_number": 8291212213,
        "pincode": 400101,
        "role": "author"
   		"token":"<token>"
    }
}

Endpoint - /api/userDetail/?token=<token>
Functioning - This is used to view the details of the existing user
Method - GET
Response - 
{
    "status": "success",
	"data": {
        "first_name": "Shivam",
        "last_name": "Tiwari",
        "username": "st.1303",
        "email": "st.1303786@gmail.com",
        "mobile_number": 8291212213,
        "pincode": 400101,
        "role": "author"
    }
}

Endpoint - /api/content/
Functioning - This is used to create the data
Method - POST
Payload - 
{
	"title": "testing",
	"body": "checking that is the data is getting updloaded or not",
	"summary": "status: done",
	"category": "test",
	"createdBy": "st.1303",
	"token": "<token>"
}
Response - 
{
    "status": "success",
	"data": [
		{
			"title": "testing",
			"body": "checking that is the data is getting updloaded or not",
			"summary": "status: done",
			"category": "test",
			"createdBy": "st.1303",
		}
	]
}

Endpoint - /api/getContent/?token=<token>
Functioning - This is used to view the all existing data
Method - POST
Response - 
{
    "status": "success",
    "data": [
        {
            "title": "testing",
            "body": "checking that is the data is getting updloaded or not",
            "summary": "status: done",
            "category": "test",
            "createdBy": "st.1303"
        }
	]
}

Endpoint - /api/updateContent/?token=<token>&title=testing
Functioning - This is used to edit the existing data
Method - PATCH
Payload - 
{
	"title": "testing",
	"body": "checking that is the data is getting updloaded or not",
	"summary": "status: done",
	"category": "testedd",
	"createdBy": "st.1303"
}
Response - 
{
    "status": "success",
	"data": [
		{
			"title": "testing",
			"body": "checking that is the data is getting updloaded or not",
			"summary": "status: done",
			"category": "testedd",
			"createdBy": "st.1303"
		}
	]
}

Endpoint - /api/deleteContent/?token=<token>&title=<title>
Functioning - This is used to delete the existing data
Method - DELETE
Response - 
{
    "status": "success",
    "message": "Record Deleted"
}

Endpoint - /api/searchContent/?query=<query>
Functioning - This is used to search the data
Method - GET
Response - 
{
    "status": "success",
    "data": [
        {
            "title": "testing",
            "body": "checking that is the data is getting updloaded or not",
            "summary": "status: done",
            "category": "testedd",
            "createdBy": "st.1303"
        }
    ]
}
