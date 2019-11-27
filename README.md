# Setup

## Step 1 setup Trello credentials
Login to [Trello Developer API Keys](https://trello.com/app-key), copy your API KEY and Secret. Then set their values to environment variables:
```bash
export TRELLO_API_KEY=<your API Key>
export TRELLO_TOKEN=<your secret>
```

## Step 2 setup YouTube credentials
1. Login to [Google Developer Console](https://console.developers.google.com/apis/credentials)
2. Click on **Create OAuth client ID**
3. Choose **Other**
4. Give it a name
5. Click **Create**. You will be redirected to a page that lists all your keys.
6. Find your credentials under **OAuth 2.0 client IDs** 
7. Click on download icon (which is most right)
8. Put that `client_secret.json` file in to the root of the project.

# Run
