define({ "api": [
  {
    "type": "get",
    "url": "/channel",
    "title": "Channel",
    "name": "Channel",
    "group": "Channel",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success Response",
          "content": "HTTP/1.1 200 OK\n{\n  \"created_on\": true,\n  \"created_by\": \"test\",\n  \"channel_name\" : \"test_channel\",\n  \"channel_type\" : \"public\",\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Invalid Params Provided",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"PUB-INVALID-PARAM\"\n  }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "healthify/resources/channel.py",
    "groupTitle": "Channel",
    "sampleRequest": [
      {
        "url": "http://localhost:3434/channel"
      }
    ]
  },
  {
    "type": "post",
    "url": "/channel/create",
    "title": "Create Channel",
    "name": "Channel",
    "group": "Channel",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "channel_name",
            "description": "<p>Channel Name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "type",
            "description": "<p>Channel type</p>"
          }
        ]
      }
    },
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success Response",
          "content": "HTTP/1.1 200 OK\n{\n  \"channel_name\" : \"test_channel\",\n  \"channel_type\" : \"public\",\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Channel Name not Provided",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"CHANNEL-REQ-NAME\"\n  }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "healthify/resources/channel.py",
    "groupTitle": "Channel",
    "sampleRequest": [
      {
        "url": "http://localhost:3434/channel/create"
      }
    ]
  },
  {
    "type": "post",
    "url": "/channel/unsubscribe",
    "title": "Unsubscribe Channel",
    "name": "Unsubscribe_Channel",
    "group": "Channel",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "channel_name",
            "description": "<p>Channel Name</p>"
          }
        ]
      }
    },
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success Response",
          "content": "HTTP/1.1 200 OK\n{\n  \"channel_name\" : \"test_channel\",\n  \"channel_type\" : \"public\",\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Channel Name not Provided",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"CHANNEL-REQ-NAME\"\n  }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "healthify/resources/channel.py",
    "groupTitle": "Channel",
    "sampleRequest": [
      {
        "url": "http://localhost:3434/channel/unsubscribe"
      }
    ]
  },
  {
    "type": "get",
    "url": "/channel/{channel_name}",
    "title": "Fetch Channel",
    "name": "Unsubscribe_Channel",
    "group": "Channel",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success Response",
          "content": "HTTP/1.1 200 OK\n{\n    \"channel_id\": \"channel.id\",\n    \"channel_name\": \"channel_name\",\n    \"channel_type\": \"public\",\n    \"created_by\": \"test_user\",\n    \"created_on\": \"some date\",\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Invalid params Provided",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"GET-CHANNEL-INVALID-PARAM\"\n  }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "healthify/resources/channel.py",
    "groupTitle": "Channel",
    "sampleRequest": [
      {
        "url": "http://localhost:3434/channel/{channel_name}"
      }
    ]
  },
  {
    "type": "post",
    "url": "/message/delete",
    "title": "Delete Messages",
    "name": "Delete_Message",
    "group": "Chat",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "channel_name",
            "description": ""
          }
        ]
      }
    },
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success Response",
          "content": "HTTP/1.1 200 OK\n{\n    \"chat_deleted\": True,\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Channel NameMissing",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"MSG-DELETE-REQ-CHANNEL\"\n  }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "healthify/resources/chat.py",
    "groupTitle": "Chat",
    "sampleRequest": [
      {
        "url": "http://localhost:3434/message/delete"
      }
    ]
  },
  {
    "type": "post",
    "url": "/message",
    "title": "Fetch Messages",
    "name": "Fetch_Message",
    "group": "Chat",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "channel_name",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "page_num",
            "description": ""
          }
        ]
      }
    },
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success Response",
          "content": "HTTP/1.1 200 OK\n{\n    \"message_id\": \"11010f-1344-1345-acf42245\",\n    \"published_by_name\": \"Rahul\",\n    \"message_text\": \"THis is a test message\",\n    \"created_on\": \"2016-10-31\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Page Num Missing",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"MSG-FETCH-REQ-PAGE-NUM\"\n  }\n}",
          "type": "json"
        },
        {
          "title": "Channel NameMissing",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"MSG-FETCH-REQ-CHANNEL\"\n  }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "healthify/resources/chat.py",
    "groupTitle": "Chat",
    "sampleRequest": [
      {
        "url": "http://localhost:3434/message"
      }
    ]
  },
  {
    "type": "post",
    "url": "/message/publish",
    "title": "Publish/Broadcasts Message",
    "name": "Publish_Message",
    "group": "Chat",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "channel_name",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "message",
            "description": ""
          }
        ]
      }
    },
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success Response",
          "content": "HTTP/1.1 200 OK\n{\n    \"message_id\": \"11010f-1344-1345-acf42245\",\n    \"message_published\": \"True\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Message Payload Missing",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"PUB-REQ-MESSAGE\"\n  }\n}",
          "type": "json"
        },
        {
          "title": "Channel NameMissing",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"PUB-REQ-CHANNEL\"\n  }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "healthify/resources/chat.py",
    "groupTitle": "Chat",
    "sampleRequest": [
      {
        "url": "http://localhost:3434/message/publish"
      }
    ]
  },
  {
    "type": "post",
    "url": "/auth",
    "title": "Authentication",
    "name": "Authentication_Login",
    "group": "User",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Content-Type",
            "description": "<p>Should be application/json for /auth</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>Username of the user</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>Password of the user</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "access_code",
            "description": "<p>JWT</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success Response",
          "content": "HTTP/1.1 200 OK\n{\n  \"access_token\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6IjM5MDA4MGExLWY0ZjctMTFlNS04NTRkLTI4ZDI0NDQyZDNlNyIsImlhdCI6MTQ1OTE3ODE0NSwibmJmIjoxNDU5MTc4MTQ1LCJleHAiOjE0NTkxNzg0NDV9.nx_1a4RmvJ7Vlf1CvnMzqoTfzChcuJnDb1Tjy1_FnXw\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Invalid Credentials",
          "content": "{\n  \"description\": \"Invalid credentials\",\n  \"error\": \"Bad Request\",\n  \"status_code\": 401\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "healthify/functionality/auth.py",
    "groupTitle": "User",
    "sampleRequest": [
      {
        "url": "http://localhost:3434/auth"
      }
    ]
  },
  {
    "type": "post",
    "url": "/signup",
    "title": "User Signup",
    "name": "Signup",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>Username</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>Password</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "first_name",
            "description": "<p>First Name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "last_name",
            "description": "<p>Last Name</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>Created user</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success Response",
          "content": "HTTP/1.1 200 OK\n{\n  \"created\": true,\n  \"username\": \"test@test.com\",\n  \"user_id\" : \"010c1f06-3971-4e43-bf27-a03b9f5d1e70\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Username is required",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"SIGNUP-REQ-USERNAME\"\n  }\n}",
          "type": "json"
        },
        {
          "title": "Username already exists",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"SIGNUP-EXISTS-USERNAME\"\n  }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "healthify/resources/auth.py",
    "groupTitle": "User",
    "sampleRequest": [
      {
        "url": "http://localhost:3434/signup"
      }
    ]
  },
  {
    "type": "get",
    "url": "/user",
    "title": "User",
    "name": "Signup",
    "group": "User",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success Response",
          "content": "HTTP/1.1 200 OK\n{\n  \"created_on\": true,\n  \"username\": \"test@test.com\",\n  \"first_name\" : \"test\",\n  \"last_name\" : \"test\",\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Bad Username Provided",
          "content": "HTTP/1.1 400 Bad Request\n{\n  \"message\": {\n    \"username\": \"BAD-USER-ID\"\n  }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "healthify/resources/auth.py",
    "groupTitle": "User",
    "sampleRequest": [
      {
        "url": "http://localhost:3434/user"
      }
    ]
  }
] });
