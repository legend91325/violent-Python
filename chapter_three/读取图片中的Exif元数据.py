from urllib import request
import optparse
from bs4 import BeautifulSoup
from os.path import basename
import os
from urllib.parse import urlsplit, urlparse
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS

def findImages(url):
    print("Finding images on "+ url)
    urlContent = request.urlopen(url).read()
    # soup = BeautifulSoup(urlContent,features="html5lib")
    soup = BeautifulSoup(urlContent)
    imgTages = soup.findAll("img")
    return imgTages

def downloadImage(imgTag):
    try:
        print("Downloading image ...")
        imgSrc = imgTag["src"]
        imgContent = request.urlopen(imgSrc).read()
        imgFileName = basename(urlsplit(imgSrc)[2])
        imgFile = open(imgFileName,"wb")
        imgFile.write(imgContent)
        imgFile.close()
        return imgFileName
    except Exception as e:
        print(str(e))
        return ''


def testForExif(imgFileName):
    try:
        exifData={}
        imgFile = Image.open(imgFileName)
        info = imgFile._getexif()
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag,tag)
                # GPSTAGS.get(tag)
                exifData[decoded] = value
            exifGPS = exifData.get("GPSInfo")
            if exifGPS:
                print(imgFileName+ " contains GPS MetaData "+exifGPS)
    except Exception as e:
        print("testForExif  "+str(e))
        pass

def main():
    try:
        parser = optparse.OptionParser("usage: %prog -u <target url>")
        parser.add_option("-u", dest="url", type="string", help="specify url address")
        (options,args) = parser.parse_args()
        url = options.url
        if url == None:
            print(parser.usage)
            exit(0)
        else:
            imgTags = findImages(url)
            for imgTag in imgTags:
                imgFileName = downloadImage(imgTag)
                testForExif(imgFileName)
                if os.path.exists(imgFileName):
                    os.remove(imgFileName)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()



