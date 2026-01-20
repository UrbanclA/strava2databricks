# Postman collection is synced to this GitHub repository.
Below is a preliminary guide on how I managed to create a working restAPI configuration, however the solution is far from being smooth or automated. 
I will tackle this issue in accordance with my roadmap.

At least all changes I make in my Postman project are synced automatically in the [postman json file](https://github.com/UrbanclA/strava2databricks/blob/9435ed7c8006271ad0446b087d64e3c9fab1f092/01%20Extract/postman.json), which can probably be imported in your own environment. 
I realize some of my tokens are therefore public through this json file but I don't mind you gathering that data.

## For import-related notebooks, overall data transformation process
Go to [02 Transform](https://github.com/UrbanclA/strava2databricks/tree/d434935ef9afdd27cdff0723b3d12e7f6d7fb0ca/02%20Transform)

Feel free to reach out for any questions!

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

1. **Create an Environment:** Set up a Postman Environment (e.g., named "Strava")
2. **Add Variables:** Store your `clientId` and `clientSecret` from the app as variables in this environment.
3. **Add Empty Variables:** Also add `authorizationCode`, `refreshToken` and `accessToken` variables which you can leave empty since we will populate them in later steps (step 3.5).
4. **Import Collection:** Create a collection that references these environment variables.
* *Resource:* For detailed guidance on setting up the Postman environment and collection, refer to this link (Steps 1-4) [Strava Slack Challenge Overview](https://www.postman.com/carson-hunter-team/strava-slack-challenge/overview).

<img width="2280" height="404" alt="image" src="https://github.com/user-attachments/assets/f85c55e6-04be-4b35-a24f-4802b889faa6" />


### Step 3: Authorization (OAuth 2.0)

This is the manual step required to generate your access tokens.

1. **Construct the Authorization URL:** Create the specific URL using your Client ID and scopes (as defined in your Postman setup).
   
<img width="2288" height="652" alt="image" src="https://github.com/user-attachments/assets/bd48b14a-dd47-459c-988a-e642edd71830" />


2. **Browser Authorization:** Paste this URL into your web browser.
3. **Authorize App:** Click "Authorize" on the Strava page.
4. **Extract the Code:** You will be redirected to a page (likely your `localhost`). It may look like an error page—**this is expected.**
5. Look at the URL in your browser address bar. Find the part that says `&code=...` - Copy that code.

<img width="815" height="57" alt="image" src="https://github.com/user-attachments/assets/3cc20f3f-4641-4bba-8f9e-9e5272faee65" />


### Step 3.5: Exchange Code & Automate Token Storage

Once you have the `authorizationCode` from the browser URL, you need to exchange it for your actual access tokens.

1. Insert  `authorizationCode` you copied from browser into Strava-postman environment variable.
2. Create a **POST** request in Postman (e.g., named "User data" or "Token Exchange") to `https://www.strava.com/oauth/token`.
3. Add the query parameters (`client_id`, `client_secret`, `code`, `grant_type`).

<img width="2286" height="601" alt="image" src="https://github.com/user-attachments/assets/f7d4cd90-f50c-4857-ba8a-c9e54007ef6b" />


4. **Automate Variable Updates:** To avoid manually copying the token every time you log in, go to the **Scripts** tab, select **Post-response**, and paste the code below. This script listens for a successful response and automatically saves the new `accessToken` and `refreshToken` into your Postman environment.

```javascript
let jsonResponse = pm.response.json();

// Check for successful response (HTTP 200)
// Note: Use '===' for comparison
if(pm.response.code === 200) {
    pm.environment.set("refreshToken", jsonResponse.refresh_token);
    pm.environment.set("accessToken", jsonResponse.access_token);
}

```
5. It should look something like this at the end:

<img width="1384" height="275" alt="image" src="https://github.com/user-attachments/assets/a314214d-dd33-456f-9421-f0f2883969c3" />


### Step 4: Fetching Data

Once you have exchanged the code for an Access Token in Postman, you can start fetching data.
* Create a **GET** request with parameters from the picture below, for now.
* **Current Method:** Retrieving the last **60 activities** using parameter `per_page = 60`
* **Endpoint:** `GET /athlete/activities` - since we need actual data we can visualize, we can start directly with acivities. Later we will fetch also data through athlete, gear, achievement and sport endpoints.

<img width="2289" height="588" alt="image" src="https://github.com/user-attachments/assets/4bafeb76-9f3c-43a9-81cd-022d1c62f872" />

### Step 5: PRESS SEND AND HOPEFULLY YOU GET BACK A RESPONSE in JSON.
* save the file and import it to Databricks volume and continue to [02 Transform](https://github.com/UrbanclA/strava2databricks/tree/d434935ef9afdd27cdff0723b3d12e7f6d7fb0ca/02%20Transform) module!

---

### Future Roadmap & Automation Ideas

* **Login refresh automation:** Figure out login refresh to be more 1 click rather than manual copy and pasting. - in progress as seen on pictures
* **Date filtering:** Investigate limiting the fetch to the last 2 months.
* **Scheduled Updates:** Redeploy the script every month to fetch new data chunks.
* **Pagination:** Review API documentation to refine how we handle pagination (using `page` and `per_page` parameters vs timestamps).
