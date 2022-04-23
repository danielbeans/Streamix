# Streamix

A playlist aggregator that allows users to migrate playlists from major streaming platforms.

## Features

- Users can sign up, log in, and log out of Streamix
  - Implemented with JWTs and storing user info (encrypted) in a MongoDB database
- Users can login and authenticate with Spotify and YouTube to sync their playlists
  - Implemented with Spotify and YouTube API, storing auth info in MongoDB with auto refreshing
- Users can migrate playlists from one platform to the other, selecting which songs they want
  - Implemented with Spotify and YouTube API and Vue composables

## Getting Started

There are a few steps you'll need to follow to get the application running on your machine. In order to fully run the application, you will need to run both the client and server simultaneously.

[Set up the client](./client/README.md)<br>
[Set up the server](./server/README.md)

Visit http://localhost:3000/ to login or sign up

## Testing

You can use the Vue SPA (Single Page Application) client or use a tool like [Postman]("https://www.postman.com") to query the Streamix API.

Example Streamix API requests:

```js
POST 'http://localhost:8000/api/auth/signup'    // Returns an access token
/*
    body = {
        "username": "danielbeans",
        "password": "password",
        "name": "Daniel",
        "email": "test@gmail.com"
    }
*/
GET 'http://localhost:8000/api/auth/spotify/'   // Redirects to Spotify authentication URL
/*
    header = {
        "Authorization": "Bearer " + access_token
    }
*/
POST 'http://localhost:8000/api/playlist/create/spotify/'   // Create a playlist on Spotify with body parameters
/*
    header = {
        "Authorization": "Bearer " + access_token
    }
    body = {
        "tracks": [
            {"name": "Don't Stop Me Now"}
        ],
        "playlist_name": "playlist #19",
    }
*/
```

## Python Libraries Used

- Django
- Django Rest Framework
- Google-API client, HTTP, and oauth Libraries
- Oauthlib
- PyJWT
- PyMongo
- Requests
- Urllib3

## Other Resources Used

- Vue
  - Element-Plus
- Vite
- Axios
- Tailwind

## Divison of Labor

Daniel Williams

- Backend
  - Developed and implemented Streamix API Django backend with MongoDB database functionality
- DevOps
  - Depolyed front end and back end on Netlify and Heroku respectively

Emmanuel Ayala

- Frontend
  - Exception handling

Miguel Quezada

- Frontend
  - Developed and implemented Vue frontend with queries to Streamix API backend
- Backend
  - Implemented controller logic and fixed logical or syntactical errors in the code base
