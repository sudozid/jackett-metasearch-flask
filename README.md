##Jakett Manual Search Flask
This is a Python Flask based program for searching stuff using Jackett Manual Search API.One of the problems with sudozid/jackett-metasearch is that its just a frontend mod for Jackett. So everything is accessible, someone can change Jackett settings very easily. There is zero security. 

What I wanted to do was to make it so that API Key and other stuff is not accessible to end users. 

It communicates with Jackett directly, so you don't have to setup individual indexers here.

I will be honest, my coding skills aren't very great so if you are a experienced programmer, you may look at my code and puke. I don't know how much security issues there are with this but if you find this project interesting, you can fork it and make all the modifications you want. 

How to start this?

1. You need Python 3 installed on your system and install all the modules flask, flask_wtf, wtforms,pandas,requests,json etc
2. Change the API Key and Domain Name variables in apiscrape.py 5th and 6th line . If you don't have your Jackett setup behind a nginx reverse proxy, you can just use the IP Address along with port like 120.120.120.120:9117 


4. Just run app.py 

You can now access it at 127.0.0.1:5000

If you want to make it publicly accessible (I won't recommend as I don't know the security of my code) you can either use Nginx reverse proxy or change host variable in app.py 10th line.

Here is how the UI Looks like ik its kinda ugly, I haven't done the CSS.

![jfjsd](https://user-images.githubusercontent.com/67092879/132982665-84297341-4631-42f8-a91c-0b159a3ef938.PNG)

I don't know if I will work on this project further as NZBHydra2 has an amazing UI with Administrator login and direct Jackett integration for manual search. Anyways, feel free to modify whatever you want.
