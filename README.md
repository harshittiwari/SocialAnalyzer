# SocialAnalyzer
includes code for making custom wordclouds and keyboard heatmaps and code for the bot

A Twitter bot that can build a word cloud image from the tweets of a Twitter user. The images are uploaded on Imgur. We support only english right now.

You can see it in action at https://twitter.com/social_visualiz

tweet "@social_visualiz #wordcloud" To generate wordcloud of your tweets.
tweet "@social_visualiz #wordcloud @user" To generate wordcloud of another user's tweets.

If you have a public facebook page and want us to include words from your fb post include your fb page id in the request. For example:
tweet "@social_visualiz #wordcloud @espn fb=espn"
You can change text color and background color of the image too. Try:
@social_visualiz #wordcloud @twitter fb=twitterinc bg=white tc=blue

fb, bg and tc parameters are optional and can be in any order.

*acceptable colors: http://www.w3schools.com/colors/colors_names.asp
**I run the bot on my computer and hence it may take some time to build your wordcloud. Thank you for your patience. We will be moving the bot to a server soon.

Bot runs in Handler.py and makes calls to SocailVisualizer based on the requests.
