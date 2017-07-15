#! /usr/bin/python

import cgi
import cgitb

cgitb.enable()

import urllib
import urllib2
import json


HTML_HEADER = 'Content-type: text/html\n\n'

Top_HTML='''
<html>
<head>
<title>Search Results</title>
      <style>
      body {font-family: "Trebuchet MS", Helvetica, sans-serif;}
      div.transbox {
        margin: 30px;
        background-color: #ffffff;
        border: 1px solid black;
        opacity: 0.8;
        filter: alpha(opacity=60);
      }
    </style>
</head>
<body background="results.gif">
<div class="transbox">
<center><h1>Here are your search results!</h1></center>
<center><p>(NOTE: click the links to get better and more detailed recipes)</p></center>
<h3>Your previous inputs:<h3>
'''
Bottom_HTML='<FORM><INPUT Type="button" VALUE="Back" onClick="history.go(-1);return true;"></FORM> </div></div></body></html>'

def searchRecipe():
    elements = cgi.FieldStorage()
    print HTML_HEADER
    print Top_HTML
    keys=elements.keys()
    for akey in keys:
        if akey == 'time':
            time=str(elements.getvalue(akey))+'%20'
            print 'Time of Day: ' + str(elements.getvalue(akey))+'<br><br>'
        if akey == 'flavor':
            flavor=str(elements.getvalue(akey))+'%20'
            print 'Flavor: '+ str(elements.getvalue(akey))+'<br><br>'
        if akey=='ingredient':
            if str(elements.getvalue(akey)) != '':
                ingredient=str(elements.getvalue(akey)).replace(' ', '%20')+'%20'
            else:
                ingredient='cheese'
            print 'The chosen one [ingredient]: '+ str(elements.getvalue(akey))+'<br><br>'
        if akey=='isdessert':
            if str(elements.getvalue(akey))=='nah':
                dessert=''
                print "It's not a dessert"+'<br><br>'
            else:
                print "It is a dessert"+'<br><br>'
                dessert='dessert'
    if 'flavor' not in keys:
        flavor=''
        print 'Flavor: None specified'+'<br><br>'
    if 'time' not in keys:
        time=''
        print 'Time of Day: None specified'+'<br><br>'
    if 'ingredient' not in keys:
        ingredient=''
        print 'The chosen one [ingredient]: None specified'+'<br><br>'
    if 'isdessert' not in keys:
        dessert=''
        print 'Dessert-ness not specified'+'<br><br>'
    final=ingredient+time+flavor+dessert
    print'Generated these results: '+'<br><br>'
    API_KEY='de39c04491ac7b525f9a7de0a2e366a0'
    request = urllib2.Request('http://food2fork.com/api/search?key=de39c04491ac7b525f9a7de0a2e366a0&q='+final)
    handle=urllib2.urlopen(request)
    content=json.load(handle)
    if content.has_key('error'):
        if content["error"]=="limit":
            print "<center> The maximum amount of searches have been conducted today. Please come back tomorrow!! </center>"
            return
    for item in content["recipes"]:
        try:
            if item['title']=='All Recipes':
                pass
            else:
                print '<center><a href='+item["f2f_url"]+'>'+item['title']+'</a></center>'+'<br>'
                image=item["image_url"]
                print '<center><img src='+image+' height=200 width=300></center>'+'<br><br>'
                newreq=urllib2.Request('http://food2fork.com/api/get?key=de39c04491ac7b525f9a7de0a2e366a0&q&rId='+item["recipe_id"])
                newhandle=urllib2.urlopen(newreq)
                newcontent=json.load(newhandle)
                print 'Ingredients: <br>'
                for i in newcontent["recipe"]["ingredients"]:
                    print str(i)+'<br>'
        except:
            pass
    if content['count']==0:
        print "We've searched high and low for a recipe to meet your requests... None have been found. <br><br> Tip: if you constantly do not get results, don't be too specific about the food (this may entail leaving some sections blank) OR do not put flavor or ingredient combinations that do not make sense."
    print Bottom_HTML

searchRecipe()


