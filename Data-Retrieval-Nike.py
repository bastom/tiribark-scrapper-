
import requests
import json

def scrap_data_from(json):
  for obj in json:
    product = {
    'id': obj['publishedContent']['properties']['productCard']['properties']['squarishURL'].split('/')[-1].split('.')[0],
    'name': obj['productInfo'][0]['merchProduct']['labelName'],
    'price' : obj['productInfo'][0]['merchPrice']['fullPrice'],
    'image': obj['productInfo'][0]['imageUrls']['productImageUrl'],
    'link': "https://www.nike.com/de/t/"+ obj['publishedContent']['properties']['productCard']['properties']['squarishURL'].split('/')[-1].split('.')[0]
    }
    products.append(product)

link = "https://api.nike.com/product_feed/rollup_threads/v2?filter=marketplace%28DE%29&filter=language%28de%29&filter=employeePrice%28true%29&filter=attributeIds%280f64ecc7-d624-4e91-b171-b83a03dd8550%2C16633190-45e5-4830-a068-232ac7aea82c%29&anchor=72&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24"
products = []
while True:
  try:
    request = requests.get(link)
    json_reponse = json.loads(request.content)
    scrap_data_from(json_reponse['objects'])
    link = "https://api.nike.com/"+ json_reponse['pages']['next']
    
  except:
    break

#Save data into a json file  
with open('man.json', 'w') as fp:
    json.dump(products, fp)
