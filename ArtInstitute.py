import requests 
import bs4 
import os
import urllib

#where to store the files
mydirectory = 'Modernism'
os.makedirs(mydirectory, exist_ok=True)

#the search results from the Art Institute that we want to grab
url = 'https://www.artic.edu/collection?is_public_domain=1&style_ids=Modernism'

res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'lxml')

#everything we are interested in is in a <li class="m-listing"> tag
for item in soup.find_all('li', class_='m-listing'):
    #not all artworks have an artist listed
    artist = ''
    #link = item.find('a', href=True)

    #imgsrc = item.find('img')
    try: 
        #the image link is in an IMG attribute called "data-iiifid"
        item.img.get("data-iiifid")
        imglink = item.img.get("data-iiifid")
        fulllink = imglink + '/full/4000,/0/default.jpg'
        print(fulllink)

        #the title is wrapped in <strong> tags
        title = item.strong.text

        #the artist name is in a <span class="subtitle">
        artistspan = item.find('span', class_='subtitle')
        if artistspan:
            artist = artistspan.text

        #rename the file with the title and artist
        filename = title + ' -- ' + artist + '.jpg'
        print(filename)

        #download the file
        print('Downloading image %s...' % (fulllink))
        res = requests.get(fulllink)
        res.raise_for_status()

        #save the file
        imageFile = open(os.path.join(mydirectory, os.path.basename(filename)), 'wb')
        for chunk in res.iter_content(1000000):
            imageFile.write(chunk)
        imageFile.close()

    except:
        print('## Not a valid image file')
        continue