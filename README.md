
---  
  
  
---  
  
<blockquote>  
<h1 id="welcome-to-resiliency-challenge">Welcome to Resiliency Challenge!</h1>  
<p>In this hackathon, we are going to develop an AI-based chatbot on Facebook messenger and Whatsapp, which is expected to propagate the information of 2020 US Census and COVID-19 to everyone in need, especially the non English speaking immigrants. This repository contains the code for the Whatsapp version of the chatbot  
</p>  
<h2 id="requirement">Requirement</h2>  
<p>Python3.6 ( Python 3.7 won’t work in some places)<br>  
Flask==1.1.2<br>  
langdetect==1.0.8<br>  
nltk<br>  
pandas<br>  
sklearn<br>  
twilio<br>  
ngrok</p>  
</blockquote>  
<blockquote>  
<h2 id="tutorial">Tutorial</h2>  
<ol>  
<li>Install <a href="%5Bhttps://devcenter.heroku.com/articles/heroku-cli#download-and-install%5D(https://devcenter.heroku.com/articles/heroku-cli#download-and-install)">heroku</a></li>  
</ol>  
<blockquote>  
<p>Example (Ubuntu)</p>  
</blockquote>  
<pre><code>$ sudo snap install --classic heroku  
</code></pre>  
<ol start="2">  
<li><a href="%5Bhttps://devcenter.heroku.com/articles/heroku-cli#getting-started%5D(https://devcenter.heroku.com/articles/heroku-cli#getting-started)">Login to heroku account</a></li>  
</ol>  
<pre><code>$ heroku login  
</code></pre>  
<ol start="3">  
<li><a href="%5Bhttps://devcenter.heroku.com/articles/creating-apps#creating-a-named-app%5D(https://devcenter.heroku.com/articles/creating-apps#creating-a-named-app)">Create a heorku app</a></li>  
</ol>  
<pre><code>$ heroku create example  
</code></pre>    
<ol start="4">  
<li>  
<p>Create and setup a <a href="https://www.twilio.com/try-twilio">Twilio Account</a></p>    
</li>  
<li>  
<p>Activate the Sandbox feature, Home > Programmable SMS > Whatsapp > Sandbox </p>  
</li>  
</ol>   
<p><img src="https://github.com/adamisetty/Whatsapp-chatbot-for-2020-Census-and-Immigrant-Consults/blob/master/images/Twilio_sandbox.png" alt="alt text"></p>
<ol start="6">
<li>Replace the "WHEN A MESSAGE COMES IN" url with that from your heroku app </li>
The URL should be in the format "https://(insert name of heroku app).herokuapp.com/"
</ol>
<ol start = "7">
<li> Connect your heroku app to your Forked version of this repo. 
<p><img src="https://github.com/adamisetty/Whatsapp-chatbot-for-2020-Census-and-Immigrant-Consults/blob/master/images/Heroku_screenshot.png" alt="alt text"></p>
</li>
<li> Deploy this repo on heroku </li>
<li> Now follow the messaging instructions on Sandbox. Text the given Twilio number the given code.
</ol>
</blockquote>  
<blockquote>  
  
<h2 id="demo">DEMO</h2>
<p><img src="https://github.com/adamisetty/Whatsapp-chatbot-for-2020-Census-and-Immigrant-Consults/blob/master/images/english_convo.png" alt="alt text"></p>
<p><img src="https://github.com/adamisetty/Whatsapp-chatbot-for-2020-Census-and-Immigrant-Consults/blob/master/images/spanish_convo.png" alt="alt text"></p>
</blockquote>