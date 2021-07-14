from django.http import response
from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Create your views here.


links = dict()
links["github"] = "https://github.com/coachadebi/otyweatherforcaster"



def weather_search(city):

    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE

    #city = city.replace(" ", "+")
    search_find = session.get(f"https://www.google.com/search?q=weather+{city}").content
    
    
    return search_find
    
    

def home(request):


    filee = pd.read_csv("static/data/annual.csv")
    data = (filee.head(26))

    example = ColumnDataSource(data)
    example2 = ColumnDataSource(data)
    
    plot = figure(plot_width=370, plot_height=300)

    plot.circle(x="Year", y="Mean", source = example,size = 10, color = "red")
    
    plot2 = figure(plot_width=370, plot_height=300)

    plot2.circle(x="Year", y="Mean", source = example2,size = 10, color = "red")
    
    
    hover = HoverTool()
    hover.tooltips=[
    ("Source", "@Source"),
    ('Year', '@Year'),
    ('Mean Temperature', '@Mean')
]


    hover2 = HoverTool()
    hover2.tooltips=[
    ("Source", "@Source"),
    ('Year', '@Year'),
    ('Mean Temperature', '@Mean')
]

    plot.add_tools(hover)
    plot2.add_tools(hover2)
    script, div = components(plot)
    

    
    
    script2, div2 = components(plot2)
    
    #weather_data = None


    try:
    
        if request.method == "POST":
            city = request.POST.get("Search")

            contentt = weather_search(city)

            soup = BeautifulSoup(contentt, "html.parser")
            show = soup.prettify()
            #print(show)

            weather_data = dict()
            weather_data["location"] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
            weather_data["temperature"] = soup.find("div", attrs={"class":"BNeawe iBp4i AP7Wnd"}).text
            time_desc = soup.find("div", attrs={"BNeawe tAd8D AP7Wnd"}).text
            td = time_desc.split("\n")
            weather_data["desciption"] = td[1]
            weather_data["time_date"] = td[0]
            


            return render(request, "index.html", {"weather":weather_data, "script":script, "div":div, "script2":script2, "div2":div2,"links":links})
    
    
        else:

            return render(request, "index.html", {"script":script, "div":div, "script2":script2, "div2":div2, "links":links})
        
        
    except:
         return render(request, "index.html", {"script":script, "div":div, "script2":script2, "div2":div2, "links":links})   
        

def about(request):

    
        
        
    
    return render(request, "about.html", {"links":links})

         
        

         
         
         
         
         
         
         
