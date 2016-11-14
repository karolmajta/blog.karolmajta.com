Title: Let's buy a flat! Part 1
Subtitle: Scraping Web for Fun and Profit
Author: Karol Majta
Date: 2016-11-03 22:30
Tags: Python, Bokeh, Scrapy, Web Scrapping, Plots

I've been planning to play with some basic web scrapping, analyzing and visualizing data
for a while now. Question was - how to pick the right data to play with. I wanted to do
something useful, if not for common audience, then at least for me. Finally I've decided
to reach for property data, a fairly low-hanging fruit amongst what's available to squeeze
out of the web. It turns out that one of the biggest Polish real estate sites
[otodom.pl](https://otodom.pl) is well suited for scraping and provides decent amount
of data on rental and sales prices. It also gives data on geographical location of particular
offers, as well as address and district data. I grabbed a great python web scraping framework
[Scrapy](https://scrapy.org/), an awesome python/js visualization toolkit
[Bokeh](http://bokeh.pydata.org/en/latest/), and with some basic knowledge of
[numpy](http://www.numpy.org/) and [scipy](https://www.scipy.org/) came to some results
and nice plots. You can get the whole source code of the project at
[github.com/karolmajta/propertycrawl](https://github.com/karolmajta/propertycrawl), feel free to clone it, play with it
and get some results yourself (you can modify cities for which reports are generated
just by modifying the makefile). Installation and usage require some rudimentary
python knowledge. If you want to get some insight on how to roll stuff like this yourself,
keep reading...

## Scrapy is your new API

Let's face it. Most companies will not share you their stuff if they don't get something
in return. That's often the case when you try to collect interesting data - it's often
published on web pages, but rarely available through an easily consumable API. This is
because whoever owns it wants to get your eyes on the ads, wants to sell you something,
or just doesn't know that sharing is caring. Fortunately [Scrapy](https://scrapy.org/)
allows you to (almost) treat any webpage as source of structured information. Also, it's
dead simple to use.

### Peek behing the curtain

Of course getting data in a form we want requires some preparation. It's best to start

