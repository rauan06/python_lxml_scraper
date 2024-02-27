import requests
import lxml.html
import json

# Getting the queriable html code from the website using lxml.html.fromstring
url = requests.get('https://store.steampowered.com/explore/new')
doc = lxml.html.fromstring(url.content)

# Searching for scpecific div's with specific classes
# // before div means: Search for every div on this website, 
# / would mean searcing for only one corresponding div
new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]

# Searching for attributes: title, price, tags, platforms
# . before double slash means: Search for the child of this html tag
# /text() extracts the text from the tag
title = new_releases.xpath('.//div[@class="tab_item_name"]/text()')
price = new_releases.xpath('.//div[@class="discount_final_price"]/text()')

# text_content() extracts all the text between chosen hmtl tag
tags = []
for tag in new_releases.xpath('.//div[@class="tab_item_top_tags"]'):
    tags.append(tag.text_content())

# ['Apple, Banana', 'Fish, Foo'] -> [[Apple, Banana], [Fish, Foo]]
tags = [tag.split(', ') for tag in tags]


platforms_div = new_releases.xpath('.//div[@class="tab_item_details"]')
total_platforms = []
for game in platforms_div:
    # Don't forget about using contains(), 
    # this method checks if the class has the given string, 
    # for instance: class="platform_img img" won't be found without contains()
    temp = game.xpath('.//span[contains(@class, "platform_img")]')
    platforms = [t.get('class').split(' ')[-1] for t in temp]
    if 'hmd_separator' in platforms:
        platforms.remove('hmd_separator')
    total_platforms.append(platforms)

output = []
# zip function to iterate over all of those lists in parallel
for info in zip(title, price, tags, total_platforms):
    resp = {}
    resp['title'] = info[0]
    resp['price'] = info[1]
    resp['tags'] = info[2]
    resp['platforms'] = info[3]
    output.append(resp)

# abing results as a JSON file
with open('data.json', 'w') as f:
  json.dump(output, f)

print(output)