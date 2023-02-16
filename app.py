import requests
import lxml.html


def prepare_text_to_print(incoming_list):
    new_text = incoming_list[0]

    new_text = new_text.replace("\r", "")
    new_text = new_text.replace("\n", "")
    new_text = new_text.replace("%", "")
    new_text = new_text.replace("°", "")
    new_text = new_text.replace("мм рт. ст.", "")
    new_text = new_text.strip()

    return new_text


html = requests.get('http://192.168.2.74/').content

tree = lxml.html.document_fromstring(html)
h1_text = tree.xpath('/html/body/h1/text()')
temp = tree.xpath('//*[@id="temp"]/text()')
humi = tree.xpath('//*[@id="humi"]/text()')
press = tree.xpath('//*[@id="press"]/text()')

print(prepare_text_to_print(h1_text))
print(prepare_text_to_print(temp))
print(prepare_text_to_print(humi))
print(prepare_text_to_print(press))
