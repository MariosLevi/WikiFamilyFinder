import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#types of family: Father, Mother, Children, Spouses, Parents, Partners, Relatives, Family
#This code only works if the familial relations are put into the infobox


my_url = 'https://en.wikipedia.org/wiki/Elizabeth_II'

multiple_relatives = []
relative = []

def scraping(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    global page_soup
    page_soup = soup(page_html, "html.parser")
    
def family_finder(relacion):
    #trying the two formats that wikipedia has for their infoboxes
    relative = []
    multiple_relatives = []
    try:
        page_infobox = page_soup.find("table",{"class":"infobox vcard"}).findAll("tr")
    except:
        page_infobox = page_soup.find("table",{"class":"infobox biography vcard"}).findAll("tr")
    for i in range(len(page_infobox)):
        #"th",{"scope":"row" is the bolded subsections of the infobox
        if relacion in str(page_infobox[i].find("th",{"scope":"row"})):
            #wikipedia uses this sometimes for seperating lines, indicator for if there are multiple people (like Spouses)
            space = "line-height:normal;margin-top:1px;white-space:normal;"
            #the way to list everybody in one relacion in a simple list
            all_sub_relacions = page_infobox[i].find("td").findAll("a")
            if space in str(page_infobox[i]):
                for x in range(len(page_infobox[i].find("td").findAll("div",{"style":"display:inline-block;" + space}))):        
                    relative_name = page_infobox[i].find("td").findAll("div",{"style":"display:inline-block;" + space})[x].get_text() 
                    multiple_relatives.append(relative_name)
                return multiple_relatives
            elif len(all_sub_relacions) > 1:
                for x in range(len(all_sub_relacions)):
                    multiple_relatives.append(all_sub_relacions[x].get_text())
                return multiple_relatives
            else:
                relative_name = page_infobox[i].find("td").find("a").get_text()
                relative.append(relative_name)
            return relative


#need to make NLP to find the parents based on Biography

def family_tree_finder(url):
    scraping(url)
    spouse = family_finder("Spouse")
    if spouse:
        print("Spouse is " + str(spouse))
    #relative.clear()
    #multiple_relatives.clear()


    father = family_finder("Father")
    if father:
        print("Father is " + str(father))
    #relative.clear()

    mother = family_finder("Mother")
    if mother:
        print("Mother is " + str(mother))
    #relative.clear()

    parents = family_finder("Parent")
    if parents:
        print("Parents are " + str(parents))
    #relative.clear()
    #multiple_relatives.clear()

    children = family_finder("Children")
    if children:
        print("Children are " + str(children))
    #relative.clear()
    #multiple_relatives.clear()

family_tree_finder(my_url)
