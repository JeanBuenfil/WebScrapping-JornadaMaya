from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

#Función para obtener la sección con los url de los meses con noticias del 2018
def get_2018_months_tag(url):
    url_jornada_maya = url
    data = requests.get(url_jornada_maya).text 
    soup = BeautifulSoup(data, "html5lib")
    #La clase years maya contiene la lista de links a los meses según el año, por lo que se usa el string 2018
    #para especificar el año
    year_2018_li = soup.find("li", class_="years maya", string="2018")
    year_2018_ul = year_2018_li.find_next("ul")
    return year_2018_ul

#Función para obtener los blogs de cada mes en un año
def get_month_blogs(ul_tag):
    year_2018_ul = ul_tag
    month_url = ""
    blogs_list = []

    for link in year_2018_ul.find_all("a", href=True):
        month_url = link["href"]
        data = requests.get(month_url).text
        soup = BeautifulSoup(data, "html5lib")
        #La clase single-blog-area blog-style-2 mb-15 wow fadeInUp contiene el link y título de la noticia
        blogs = soup.find_all("div", class_="single-blog-area blog-style-2 mb-15 wow fadeInUp")

        for blog in blogs:
            time.sleep(2)
            fecha = blog.find_all(class_="maya")
            headline_tag = blog.find("a", class_="post-headline") 
            headline = headline_tag.text.strip()
            link_ref = headline_tag["href"]
            #Existen dos div con la clase maya en cada noticia, por lo que se usa [-1]
            #porque el último div con esa clase es el que contiene la fecha
            fecha_noticia = fecha[-1].text.strip()
            content = get_post_content(link_ref)
            blogs_list.append((headline,link_ref, fecha_noticia, content))
    return blogs_list
    

#Función que utilize get_month_blogs para obtener el contenido de una noticia
def get_post_content(post_href):
    blog_url = post_href
    data = requests.get(blog_url).text
    soup = BeautifulSoup(data,"html5lib")
    blog_content_div = soup.find_all("div", class_="single-blog-content")
    #Existen dos div con la clase single-blog-content en cada noticia, por lo que se usa [-1] 
    #porque el útlimo div con esa clase es el que contiene el texto de la noticia
    blog_content_div = blog_content_div[-1]
    #Se eliminan secciones no deseadas de la noticia
    for meta in blog_content_div.find_all(["div", "a", "h1", "h6", "figcaption"]):
        meta.extract()  
    noticia = blog_content_div.get_text(separator="\n").strip()
    return noticia


url_jornada_maya = "https://www.lajornadamaya.mx/k'iintsil/archivo"
year_2018_ul = get_2018_months_tag(url_jornada_maya)
blogs_list = get_month_blogs(year_2018_ul)
df = pd.DataFrame(blogs_list)
df.to_csv("noticias.csv", index=False, header=False)