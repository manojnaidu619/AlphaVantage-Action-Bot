# AlphaVantage-Action-Bot
### A github action to render real-time stocks/cryptocurrency charts inside readme 

![AlphaVantage-Action-Bot-Chart](./alphavantage/chart.png) 
**Realtime Stock/Crytpocurrency Chart📈  Rendered By [AlphaVantage-Action-Bot](https://github.com/manojnaidu619/AlphaVantage-Action-Bot) | Last updated the above chart on Sep 01, 2025(01:12:29) ** 

Hello programmers, hope you are all doing fantastic!🥳 .We all know that Readme file is crucial for any repository, it serves as a user manual and helps us in getting started. 

This action makes the best use of readme file to show the trajectory of stock prices in order to gauge your company’s general health.

📌 **Click on DEV logo below to view detailed article**

<a href="https://dev.to/manojnaidu619/alphavantage-action-bot-3d05">
  <img src="https://d2fltix0v2e0sb.cloudfront.net/dev-badge.svg" alt="Manoj Naidu's DEV Profile" height="100" width="100">
</a>

## What Is it?

**AlphaVantage Action Bot** is a Github action that renders the realtime chart of a stock/cryptocurrency inside the readme file. We will be using the [Alpha Vantage Public Stock APIs](https://www.alphavantage.co/) to build the action bot. You may also check out [this finance API guide](https://medium.com/@patrick.collins_58673/stock-api-landscape-5c6e054ee631) that surveys some of the popular stock and crypto data APIs in the market.

## Screenshots

* BITCOIN open price trajectory

![Bitcoin open trajectory](https://dev-to-uploads.s3.amazonaws.com/i/jtg3iiwe2f6ap5qzwx9d.png)

* close price trajectory of APPLE

![Apple close trajectory](https://dev-to-uploads.s3.amazonaws.com/i/xvdexkflg343fvhtmtzx.png)

* Market Capital(USD) of BTC

![BTC market capital](https://dev-to-uploads.s3.amazonaws.com/i/8m331eiavjx3531yd8r7.png)

## How to Setup?

This action could be adopted easily into your project in just 3 steps...

### *Step 1* - Adding script file into your repo.

This step is pretty simple, all you need to do is..
  - Create folder named `alphavantage` in the root of your repo.
  - Inside `alphavantage` folder, add a new python script file with name `alphavantage-bot.py` and paste the complete code below
  - [Link to Gist](https://gist.github.com/manojnaidu619/61809a103180f12a441d6de991b40a04 )

  - From line 8-50, the variables could be customized to requirements.
  
  > So now, your repo will contain a python script file, whose path is `YOUR_REPO_NAME/alphavantage/alphavantage-bot.py`. It should look like this...

![Script Path](https://dev-to-uploads.s3.amazonaws.com/i/jbn0ga6gokbg4x8qfmm0.png)

### *Step 2* - Adding AlphaVantage API key to repo secrets.

- Since we are using [AlphaVantage's](https://www.alphavantage.co/documentation/) API to get the data, we need to obtain API key from them to utilize their service. [Click here to get API key](https://www.alphavantage.co/support/#api-key).

After filling the basic details, you should get your API key instantly.

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/gc624m1ae2n6rd75bhq8.png)

- Now, paste the API key inside your repo secrets with the name `ALPHA_VANTAGE_KEY`.

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/dgaps49v9ni9qbbs32my.png)

### *Step 3* - Setup Workflow file(Final step, yay!).

Paste the below code inside
`REPO_ROOT/.github/workflows/AlphaVantage-Action-Bot.yml`
 
```yml

name: AlphaVantage-Action-Bot

on:
  schedule:
    - cron: "*/30 * * * *"  
    # Runs every 30th minute
    # Could be customized to requirement
    # To know more about crontabs refer https://crontab.guru/ 
     

jobs:
  alphavantage-render-chart:
    runs-on: ubuntu-latest
    steps:
      - name: checkout repo content
        uses: actions/checkout@v2 # checkout the repository content to github runner.
      - name: setup python
        uses: actions/setup-python@v2
        with:
           python-version: 3.8 #install the python needed
      - name: Install dependencies
        run: python -m pip install --upgrade pip matplotlib pandas alpha_vantage
      - name: execute python script 
        run: python ./alphavantage/alphavantage-bot.py
        env:
           ALPHA_VANTAGE_KEY: ${{ secrets.ALPHA_VANTAGE_KEY }}
      - name: Commit and push if changed
        run: |
         git add .
         git diff
         git config --global user.email "alphavantage-action-bot@example.com"
         git config --global user.name "AlphaVantage Action Bot"
         git commit -m "AlphaVantage Action Bot Updated README" -a || echo "No changes to commit"
         git push
```

Now, your workflow file's path should like something like this...

![Wokflow file path](https://dev-to-uploads.s3.amazonaws.com/i/eq55q4ho3ottmfnqn9l7.png)

##### Congrats! You have successfully set up the workflow 😎

### Additional Resources / Info

**Special Thanks to the AlphaVantage team for reaching me out on this project✌️**

* [Github Actions Docs](https://docs.github.com/en/actions)
* [What are Github actions?](https://www.youtube.com/watch?v=5ncuRFwnrdc&ab_channel=EddieJaoude)
