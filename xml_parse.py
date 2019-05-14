import requests
import csv
import xml.etree.ElementTree as ET


def loadRSS():
    url = 'http://www.hindustantimes.com/rss/topnews/rssfeed.xml'

    resp = requests.get(url)

    with open('topnewsfeed.xml', 'wb') as f:
        f.write(resp.content)


def parseXML(XMLfile):
    tree = ET.parse(XMLfile)
    root = tree.getroot()
    newsitem = []
    for item in root.findall('./channel/item'):
        news = {}
        for child in item:
            if child.tag == '{http://search.yahoo.com/mrss/}content':
                news['media'] = child.attrib['url']
            else:
                news[child.tag] = child.text.encode('utf8')

        newsitem.append(news)
    return newsitem


def savetoCSV(newsitems, filename):

    # specifying the fields for csv file
    fields = ['guid', 'title', 'pubDate', 'description', 'link', 'media']

    # writing to csv file
    with open(filename, 'w') as csvfile:

        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(newsitems)


def main():
    # load rss from web to update existing xml file
    loadRSS()

    # parse xml file
    newsitems = parseXML('topnewsfeed.xml')
    savetoCSV(newsitems, 'newsfile.csv')
    # store news items in a csv file


if __name__ == "__main__":

    # calling main function
    main()
