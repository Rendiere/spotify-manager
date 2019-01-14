# Spotify Playlist Manager

_Automatically add liked songs from Discover weekly to a specified playlist_

This work was inspired by Zach Johnson's [blog post](https://www.zachjohnsondev.com/posts/managing-spotify-library/), where he did something similar, just a tad fancier.

## Setup

**0. Install repo locally**

First things first...
1. clone this repo somewhere sensible
2. create a virtual environment - I recommend using [virtualenv](https://virtualenv.pypa.io/en/latest/)
3. Activate virtual env
4. Install dependencies: `pip install -r requirements.txt`
5. (TODO) run tests

**1. Register an app through Spotify**

The main goal of this is to get your `client ID` and `client secret` keys to fill out `.env`.

To get these:
* Go to the [Spotify Dev Dashboard](https://developer.spotify.com/dashboard/), and log in. All you need is a normal Spotify account. 
* Once logged in, click on "Create a Client ID"
* Fill in the details...
    - The names aren't important,
    - Pick "I Don't Know""
    - Select all the consent boxes
* Once finished, on the app dashboard, click "Edit Setting"
* In "Redirect URIs", add `http://www.google.com/`
* done...

**2. Set environment variables in `.env`**

While still on the app dashboard, click "SHOW CLIENT SECRET"

Now, copy and paste this information into the .env file. 

It should look like this:
```.env
SPOTIPY_CLIENT_ID='<YOUR CLIENT ID>'
SPOTIPY_CLIENT_SECRET='<YOUR CLIENT SECRET>'
SPOTIPY_REDIRECT_URI='http://www.google.com/'
SPOTIPY_USERNAME='<YOUR USERNAME>'
SPOTIPY_PLAYLIST='<DESTINATION PLAYLIST'
SPOTIPY_CACHE='<FILL IN LATER>'
```


TIP:
>If you're having trouble getting your username, use [this example](https://developer.spotify.com/console/get-current-user/) to get your user profile, then use the value in the `id` property of the returned JSON.


**3. Run single auth cycle**

Now that all the variables in the `.env` file are set, we need to start the app once for `spotipy` to perform an auth flow. 

With your virtual environment active, run:
```bash
(spotipy_env)$ python main.py
```

This wil start take you through the [client credentials flow](https://spotipy.readthedocs.io/en/latest/#authorization-code-flow) to get an auth token. An OAuth prompt should open up in your browser, authenticate the request, then copy and paste the link to which you get redirected into the terminal. These steps are also shown in the terminal by spotipy.

Once you've pasted this link into the terminal, the app should run normally and spotipy will have created a cache file in your root directory named `.cache-<USERNAME>`. 

If you can see this cache file, go to the next step. Else, retry from the beginning until you get the auth process done. [This guy](https://www.youtube.com/watch?v=tmt5SdvTqUI) shows the process quite clearly. 

**4. Copy cache into `.env`**

Stop the app, and copy the contents of `.cache-<USERNAME>` into .`env`.

It should look something like this (note the single ticks):

```.env
SPOTIPY_CACHE='{"access_token": "<YOUR TOKEN>"...}'
```

**5. Run app again locally**

Confirm that everything is working properly by _deleting the cache file_, and running `python main.py` again. 

The app should automatically create the .cache file again using the data in `.env` - this is exactly what will happen once we deploy the file to Heroku.

## Deployment

I chose to use Heroku for deploying this app, and will assume you've created and account and set up the [heroku cli](https://devcenter.heroku.com/articles/heroku-cli) locally before continuing. 

Using the Heroku dashboard, create a new app and follow the deploy instructions. You should be doing the following steps:

1. Create a remote to the repo: `heroku git:remote -a <YOUR HEROKU APP NAME>`
2. Set the config variables (in `.env`) on heroku using a custom script*: `python heroku_config.py` 
3. Push the code to Heroku: `git push heroku master`
4. View the logs to see the app running: `heroku logs --tail`

\* Note, you can set all the variables manually using the heroku dashboard. This is also a great way to change the destination playlist later on.


## Try it out

Go ahead and "love" a song on your Discover Weekly and see it pop up in your desired playlist.


**TODOs**

* Write unittests
* Integrate tests into setup
* Better deployment strategy - Lambda etc
* Server to handle login first login
* 