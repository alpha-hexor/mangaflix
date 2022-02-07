import requests
from bs4 import BeautifulSoup
from termcolor import colored
import random
import os
from tqdm import tqdm
import img2pdf

#global things
url = "https://mangakakalot.com/search/story/"

manga_names = []
manga_links = []
download_header = {'Referer': 'https://readmanganato.com'}

#make download directory
if not os.path.exists("downloads"):
    os.mkdir("downloads")

#clear screen function
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#function for color print
def colored_print(message):
    colors = ['red','green','blue','yellow','magenta','cyan']
    color = random.choice(colors)
    print(colored(message,color,attrs=["bold"]))



#function to search manga
def search(name):
    if len(name) > 1:
        name = name.replace(" ","_")
    search_url = url + name
    r = requests.get(search_url)
    src = r.content
    soup = BeautifulSoup(src, "lxml")
    hrs = soup.find('div',attrs={'class':'panel_story_list'})

    for h in hrs:
        x = h.find('a')
        try:
            manga_links.append(x.get('href'))
            manga_names.append(x.img.get('alt'))
        except:pass

#function to search chapters
def search_chapter(manga_link):
    print(manga_link)
    r=requests.get(manga_link)
    src = r.content
    soup = BeautifulSoup(src, "lxml")
    h=soup.find('div',attrs={'class':'panel-story-chapter-list'})
    x=h.find_all('li',attrs={'class':'a-h'})
    l = len(x)
    first_element = x[0].find('a').get('href')
    last_element = x[l-1].find('a').get('href')

    #first chapter
    first_chapter = last_element.split('/')[-1].split('-')[-1]

    #last chapter
    last_chapter = first_element.split('/')[-1].split('-')[-1]

    return (first_chapter,last_chapter)

#function to download manga
def download_manga(path,final_link):
    image_links = []
    r=requests.get(final_link)
    src = r.content
    soup = BeautifulSoup(src, "lxml")
    h=soup.find('div',attrs={'class':'container-chapter-reader'})
    x = h.find_all('img')
    for i in x:
        image_links.append(i.get('src'))
    
    #tqdm progress bar to download images

    # for i in tqdm(image_links):
    #     r=requests.get(i,headers=download_header)
    #     src = r.content
    #     with open(path+"/"+i.split('/')[-1],"wb") as f:
    #         f.write(src)
    #     f.close()

    #list all the jpgs in the directory in sorted order
    ext = ".jpg"
    jpgs = []
    for i in range(1,len(image_links)+1):
        jpgs.append(str(i)+ext)

    #print(jpgs)
    #create pdf
    colored_print("[*]Creating PDF")
    os.chdir(path)
    name = path.split('/')[-1] + ".pdf"
    with open(name, "wb") as f:
        f.write(img2pdf.convert([i for i in jpgs]))
    f.close()
    colored_print("[*]Done")
    os.system("start "+name)


def main():
    name = str(input("Enter the name of the manga: "))
    search(name)

    #take user input
    for i in range(len(manga_names)):
        colored_print("{}. {}".format(i+1,manga_names[i]))
    
    s = int(input("Enter index of the manga: "))
    manga_to_download = manga_links[s-1]
    first,last = search_chapter(manga_to_download)
    colored_print("[*]Available chapters: [{}-{}]".format(first,last))

    #take manga chapter number
    x= input("Enter the chapter number: ")

    if int(x) < int(first) or int(x) > int(last):
        colored_print("[!]Invalid chapter number")
        exit()

    final_link = manga_to_download + "/" + "chapter-"+x
    n = manga_names[s-1]

    #remove : if any
    n = n.replace(":","")
    #remove spaces
    n = n.replace(" ","-")

    path = "downloads/" + n + "/" + "chapter-"+x
    if not os.path.exists(path):
        os.makedirs(path)
    clear()
    colored_print("[*]Downloading {} chapter {}".format(manga_names[s-1],x))
    download_manga(path,final_link)

main()  


