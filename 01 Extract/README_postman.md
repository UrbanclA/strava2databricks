# Postman collection is synced to this GitHub repository.
To-be-added are some notes and how I managed to create a working restAPI configuration, however it still isn´t smooth, which I have to tend to.

At least all changes I make in Postman collection are synced automatically in the [postman json file](https://github.com/UrbanclA/strava2databricks/blob/9435ed7c8006271ad0446b087d64e3c9fab1f092/01%20Extract/postman.json), which can hopefully make some sense to you, the reader :D 

## For import-related notebooks
Go to [02 Transform](https://github.com/UrbanclA/strava2databricks/tree/d434935ef9afdd27cdff0723b3d12e7f6d7fb0ca/02%20Transform)

Feel free to reach out for any questions!

Here is a clean, structured Markdown version of your guide. I’ve organized it into logical steps and added formatting to make it easier to read.

---

# How to Extract Data from the Strava API

> **Note:** This is a preliminary guide. The automation part is still a work in progress, but these steps cover the initial setup and manual extraction process.

### Prerequisites

* A Strava Account
* [Postman](https://www.postman.com/downloads/) installed, or you can use their web version, which worked for me also!

---

### Step 1: Create a Strava App

1. Log in to [Strava](https://www.strava.com/).
2. Navigate to the [Strava Developers Settings](https://developers.strava.com/).
3. Create a new Application.
4. **Crucial:** Locate your **Client ID** and **Client Secret**. You will need to save these for the next steps.

### Step 2: Configure Postman

I recommend using **Postman** to manage the API calls. You can follow the visual guide in this [YouTube Video](https://www.youtube.com/watch?v=nutXnXSyRLY).

**Setup Instructions:**

1. **Create an Environment:** Set up a Postman Environment (e.g., named "Strava").
2. **Add Variables:** Store your `Client ID` and `Client Secret` as variables in this environment. Also add `refreshToken` and `accessToken` variables which you can leave empty, since they will populate once you authorize
3. **Import Collection:** Create a collection that references these environment variables.
* *Resource:* For detailed guidance on setting up the Postman environment and collection, refer to this link (Steps 1-4) [Strava Slack Challenge Overview](https://www.postman.com/carson-hunter-team/strava-slack-challenge/overview).



### Step 3: Authorization (OAuth 2.0)

This is the manual step required to generate your access tokens.

1. **Construct the Authorization URL:** Create the specific URL using your Client ID and scopes (as defined in your Postman setup).
2. **Browser Authorization:** Paste this URL into your web browser.
3. **Authorize App:** Click "Authorize" on the Strava page.
4. **Extract the Code:** You will be redirected to a page (likely your `localhost`). It may look like an error page—**this is expected.**
5. Look at the URL in your browser address bar. Find the part that says `&code=...`. Copy that code.
6.  <img width="815" height="57" alt="image" src="https://github.com/user-attachments/assets/3cc20f3f-4641-4bba-8f9e-9e5272faee65" />


### Step 3.5: Exchange Code & Automate Token Storage

Once you have the `authorizationCode` from the browser URL, you need to exchange it for your actual access tokens.

1. Create a **POST** request in Postman (e.g., named "User data" or "Token Exchange") to `https://www.strava.com/oauth/token`.
2. Add the query parameters as shown in your screenshot (`client_id`, `client_secret`, `code`, `grant_type`).
3. **Automate Variable Updates:** To avoid manually copying the token every time you log in, go to the **Scripts** tab, select **Post-response**, and paste the code below. This script listens for a successful response and automatically saves the new `accessToken` and `refreshToken` into your Postman environment.

```javascript
let jsonResponse = pm.response.json();

// Check for successful response (HTTP 200)
// Note: Use '===' for comparison
if(pm.response.code === 200) {
    pm.environment.set("refreshToken", jsonResponse.refresh_token);
    pm.environment.set("accessToken", jsonResponse.access_token);
}

```

### Step 4: Fetching Data

Once you have exchanged the code for an Access Token in Postman, you can start fetching data.

* **Current Method:** Retrieving the last **60 activities** using parameter `per_page = 60`
* **Endpoint:** `GET /athlete/activities`

---

### Future Roadmap & Automation Ideas

* **Date filtering:** Investigate limiting the fetch to the last 2 months.
* **Scheduled Updates:** Redeploy the script every month to fetch new data chunks.
* **Pagination:** Review API documentation to refine how we handle pagination (using `page` and `per_page` parameters vs timestamps).
