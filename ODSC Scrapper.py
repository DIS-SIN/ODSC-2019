#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from bs4.element import Tag


# In[11]:


from typing import Optional, List, Mapping, Union


# In[12]:


import pandas as pd


# In[13]:


import urllib.parse
import urllib.request


# In[14]:


import datetime


# In[190]:


import json


# In[169]:


def get_html(url: str, 
             method: str, 
             data: Optional[dict] = None,
             headers: Optional[dict] = None) -> str:
    if method == "POST":
        if data is not None:
            data = urllib.parse.urlencode(data)
            data = data.encode("ascii")
            if headers is not None:
                req = urllib.request.Request(url, data, headers)
            else:
                req = urllib.request.Request(url, data)
        elif headers is not None:
            req = urllib.request.Request(url, headers)
        else:
            raise ValueError("Must provide data if making POST request")
    elif method == "GET":
        if data is not None:
            data = urllib.parse.urlencode(data)
            url = url + '?' + data
            if headers is not None:
                req = urllib.request.Request(url, headers)
        elif headers is not None:
            req = urllib.request.Request(url,headers)
        else:
            req = urllib.request.Request(url)
    else:
        raise ValueError(f"method {method} is not supported")
    
    with urllib.request.urlopen(req) as response:
        print(req.headers)
        page = response.read()
    return page


# In[16]:


def get_links_from_html(html: str) -> List[dict]:
    soup = BeautifulSoup(html, 'lxml')
    links = [{"parent": link.parent, **link.attrs} for link in soup.find_all('a')]
    return links
    


# In[446]:


class PageHTML:
    def __init__(self, url: str, **kwargs: Union[dict, int, str]) -> None:
        self.vals = {'url': url, **kwargs}
        self.url = url
    
    @property
    def url(self) -> str:
        return self._url
    @property
    def html(self) -> str:
        self.updated = False
        return self._html
    @property
    def soup(self) -> BeautifulSoup:
        self.updated = False
        return self._soup
    @url.setter
    def url(self, url) -> None:
        if hasattr(self, 'url'):
            if url != self.url:
                self._url = url
                self.vals['url'] = self._url
                self.html = self.vals
        else:
            self.vals['url'] = url
            self._url = url
            self.html = self.vals
    @html.setter
    def html(self, vals: Union[str, Mapping[str,Union[str,dict]]]) -> None:
        self.updated = True
        if isinstance(vals,str):
            req = urllib.request.Request(vals)
        else:
            if vals.get('url') is None:
                raise ValueError("When providing a dictionary the url field must be present")
            if vals.get('method') == "POST":
                if vals.get('data') is not None:
                    data = urllib.parse.urlencode(vals['data'])
                    data = data.encode('ascii')
                    if vals.get('headers') is not None:
                        req = urllib.request.Request(self.url, data, headers = vals.get('headers'))
                    else:
                        req = urllib.request.Request(self.url, data)
                else:
                    raise ValueError("When submitting a post request data field must not be none")
            else:
                if vals.get('data') is not None:
                    data = urllib.parse.urlencode(vals['data'])
                    self.url = url + '?' + data
                    if vals.get('headers') is not None:
                        req = urllib.request.Request(self.url, headers = vals.get('headers'))
                    else:
                        req = urllib.request.Request(self.url)
                elif vals.get('headers') is not None:
                    req = urllib.request.Request(self.url, headers = vals.get('headers'))
                else:
                    req = urllib.request.Request(self.url)
        self.request = req
        print(self.request.headers)
        with urllib.request.urlopen(req) as response:
            self._html = response.read()
            self.soup = self._html
    
    @soup.setter
    def soup(self, html):
        self._soup = BeautifulSoup(html, 'lxml')
    
    def refresh(self):
        self.html = self.vals


# In[474]:


class Position:
    def __init__(self, position: str) -> None:
        self.position = position
    @property
    def position(self) -> str:
        return self._position
    @position.setter
    def position(self, position: str) -> None:
        self._position = position
    def __repr__(self):
        return f"Position {self.position}"
    


# In[475]:


class Organization:
    def __init__(self, organization: str) -> None:
        self.organization = organization
    @property
    def organization(self) -> str:
        return self._organization
    @organization.setter
    def organization(self, organization: str) -> None:
        self._organization = organization
    def __repr__(self):
        return f"Organization {self.organization}"


# In[511]:


class Presenter:
    def __init__(self, parent: Tag) -> None:
        self.parent = parent
    @property
    def parent(self) -> Tag:
        return self._parent
    @property
    def artist_popover_element(self) -> Tag:
        return self._artist_popover_element
    @property
    def presenter_bio(self) -> str:
        return self._presenter_bio
    @property
    def artist_image_element(self):
        return self._artist_image_element
    @property
    def presenter_image(self):
        return self._presenter_image
    @property
    def artist_linkedin_element(self):
        return self._artist_linkedin_element
    @property
    def presenter_linkedin(self):
        return self._presenter_linkedin
    @property
    def artist_info_element(self):
        return self._artist_info_element
    @property
    def artist_title_element(self):
        return self._artist_title_element
    @property
    def artist_position_element(self):
        return self._artist_position_element
    @property
    def title(self):
        return self._title
    @property
    def name(self):
        return self._name
    @property
    def organizations(self):
        return self._organizations
    @property
    def positions(self):
        return self._positions
    @parent.setter
    def parent(self, parent: Tag) -> None:
        self.updated = True
        self._parent = parent
        if len(self._parent.find_all(class_ = "tcode-artist-popover")) > 0:
            self.artist_popover_element = self._parent.find_all(class_ = "tcode-artist-popover")[0]
        else:
            self.artist_content_element = None
            self.presenter_bio = None
        if len(self._parent.find_all(class_ = "tcode-es-artist-title-container")) > 0:
            self.artist_info_element = self._parent.find_all(class_ = "tcode-es-artist-title-container")[0]
        else:
            self._artist_info_element = None
            self._positions = None
            self._organizations = None
            self._title = None
            self._name = None
    @artist_info_element.setter
    def artist_info_element(self, artist_info_element: Tag) -> None:
        self.updated = True
        self._artist_info_element = artist_info_element
        if self._artist_info_element.find(class_="tcode-es-artist-title") is not None:
            self.artist_title_element = self._artist_info_element.find(class_ ="tcode-es-artist-title")
        else:
            self._name = None
            self._title = None
        if self._artist_info_element.find(class_ = "artist-position") is not None:
            self.artist_position_element = self._artist_info_element.find(class_ = "artist-position")
        else:
            self._organizations = None
            self._positions = None
    @artist_position_element.setter
    def artist_position_element(self, artist_position_element: Tag) -> None:
        self.updated = True
        self._artist_position_element = artist_position_element
        txt = self._artist_position_element.text
        txt = txt.strip()
        positions_organizations = txt.split('|')
        if len(positions_organizations) == 1:
            positions = positions_organizations[0]
            positions = positions.split(',')
            last_position = positions.pop(-1)
            if last_position.find('and') != -1:
                last_position = last_position.split('and')
                positions.extend(last_position)
            else:
                positions.append(last_position)
            self._positions = []
            for pos in positions:
                self._positions.append(Position(pos))
            self._organizations = None
        elif (len(positions_organizations) == 2 and 
              positions_organizations[-1] != '' or len(positions_organizations) == 3 and
              positions_organizations[-1] == ''):
            positions = positions_organizations[0]
            positions = positions.split(',')
            last_position = positions.pop(-1)
            if last_position.find('and') != -1:
                last_position = last_position.split('and')
                positions.extend(last_position)
            else:
                positions.append(last_position)
            self._positions = []
            for pos in positions:
                self._positions.append(Position(pos))
            organizations = positions_organizations[1]
            organizations = organizations.split(',')
            last_organization = organizations.pop(-1)
            if last_organization.find('and') != -1:
                last_organization = last_organization.split('and')
                organizations.extend(last_organization)
            else:
                organizations.append(last_organization)
            self._organizations = []
            for org in organizations:
                self._organizations.append(Organization(org))
        else:
            self._organizations = None
            self._positions = None
            
            
            
    @artist_title_element.setter
    def artist_title_element(self,artist_title_element: Tag) -> None:
        self.updated = True
        self._artist_title_element = artist_title_element
        txt = self._artist_title_element.text
        txt = txt.strip()
        name_title = txt.split(',')
        if len(name_title) == 1:
            self._name = name_title[0]
            self._title = None
        elif len(name_title) > 1:
            self._name = name_title[0]
            self._title = name_title[1]
    @artist_popover_element.setter
    def artist_popover_element(self, artist_popover_element: Tag) -> None:
        self.updated = True
        self._artist_popover_element = artist_popover_element
        if self._artist_popover_element.find(class_="artist-content") is not None:
            self._presenter_bio = self._artist_popover_element.find(class_="artist-content").text
        else:
            self._presenter_bio = None
        if self._artist_popover_element.find(class_="artist-image") is not None:
            self.artist_image_element = self._artist_popover_element.find(class_="artist-image")
        else:
            self._artist_image = None
            self._presenter_image = None
        if self._artist_popover_element.find(class_="tcode-ico-linkedin") is not None:
            self.artist_linkedin_element = self._artist_popover_element.find(class_="tcode-ico-linkedin")
        else:
            self._artist_linkedin_element = None
            self._presenter_linkedin = None
    @artist_image_element.setter
    def artist_image_element(self,artist_image_element: Tag) -> None:
        self.updated = True
        self._artist_image_element = artist_image_element
        if self._artist_image_element.find('img') is not None:
            self._presenter_image = self._artist_image_element.find('img').get('src')
        else:
            self._presenter_image = None
    @artist_linkedin_element.setter
    def artist_linkedin_element(self, artist_linkedin_element: Tag) -> None:
        self.updated = True
        self._artist_linkedin_element = artist_linkedin_element
        self._presenter_linkedin = self._artist_linkedin_element.get('href')
            
            
        
    


# In[512]:


class Category:
    def __init__(self, category: str) -> None:
        self.category = category
    @property
    def category(self):
        return self._category
    @category.setter
    def category(self, category: str) -> None:
        self.updated = True
        self._category = category
    def __repr__(self):
        return f"Category {self.category}"
    


# In[513]:


class ScheduleItem:
    def __init__(self, parent: Tag) -> None:
        self.parent = parent
    @property
    def parent(self) -> Tag:
        self.updated = False
        return self._parent
    @property
    def title_element(self) -> Tag:
        self.updated = False
        return self._title_element
    @property
    def time_element(self) -> Tag:
        self.updated = False
        return self._time_element
    @property
    def excerpt_element(self) -> Tag:
        return self._excerpt_element
    @property
    def excerpt_text_element(self) -> Tag:
        return self._excerpt_text_element
    @property
    def excerpt_p_elements(self) -> List[Tag]:
        return self._excerpt_p_element
    @property
    def excerpt_categories_element(self) -> Tag:
        return self._excerpt_category_element
    @property
    def categories_text(self) -> str:
        return self._categories_text
    @property
    def presenters_element(self) -> List[Tag]:
        return self._presenters_element
    @property
    def title(self) -> str:
        return self._title
    @property
    def day(self) -> str:
        return self._day
    @property
    def time(self) -> str:
        return self._time
    @property
    def datetime(self) -> datetime.datetime:
        month_day = self._day
        month_day = month_day.strip('st')
        month_day = month_day.strip('rd')
        month_day = month_day.strip('th')
        year_month_day = "2019-" + month_day
        if self._time is not None:
            year_month_day = year_month_day + " " + self._time
            return datetime.datetime.strptime(year_month_day, '%Y-%B-%d %H:%M')
        return datetime.datetime.strptime(year_month_day, '%Y-%B-%d')
    @property
    def excerpt(self) -> str:
        return self._excerpt
    @property
    def presenters(self) -> List[dict]:
        return self._presenters
    @property
    def categories(self) -> List['Category']:
        return self._categories
    @parent.setter
    def parent(self, parent) -> None:
        self.updated = True
        self._parent = parent
        self._day = parent.get('data-location')
        self.title_element = parent.find_all('div', class_ = 'event-title')[0]
        if len(parent.find_all('div', class_ = "event-time")) > 0:
            self.time_element = parent.find_all('div', class_ = "event-time")[0]
        else:
            self._time = None
            self._time_element = None
        if len(parent.find_all('div', class_ = "event-excerpt")) > 0:
            self.excerpt_element = parent.find_all('div', class_ = "event-excerpt")[0]
        else:
            self._excerpt_element = None
            self._excerpt_text_element = None
            self._excerpt_categories_element = None
            self._excerpt_p_elements = None
            self._categories_text = None
            self._presenters_element = None
            self._presenters = None
            self._excerpt = None
            self._categories = None
    @title_element.setter
    def title_element(self, title_element: Tag) -> None:
        self.updated = True
        self._title_element = title_element
        self._title = str(self._title_element.contents[0])
    @time_element.setter
    def time_element(self, time_element: Tag) -> None:
        self.updated = True
        self._time_element = time_element
        self._time = self._time_element.find_all(class_ = "time-starts")[0].text
    @excerpt_element.setter
    def excerpt_element(self, excerpt_element: Tag) -> None:
        self.updated = True
        self._excerpt_element = excerpt_element
        if len(excerpt_element.find_all(class_ = 'event-content')) > 0:
            self.excerpt_text_element = excerpt_element.find_all(class_ = 'event-content')[0]
        else:
            self._excerpt_text_element = None
            self._excerpt = None
            self._categories_text = None
            self._categories = None
            self._excerpt_categories_element
        if len(excerpt_element.find_all(class_ = "artist-row")) > 0:
            self.presenters_element = excerpt_element.find_all(class_ = "artist-row")
        else:
            self._presenters_element = None
            self._presenters = None
    @presenters_element.setter
    def presenters_element(self, presenters_element: List[Tag]) -> None:
        self.updated = True
        self._presenters_element = presenters_element
        self._presenters = []
        for elem in self._presenters_element:
            self._presenters.append(Presenter(elem))
    @excerpt_text_element.setter
    def excerpt_text_element(self, excerpt_text_element: Tag) -> None:
        self.updated = True
        self._excerpt_text_element = excerpt_text_element
        if len(excerpt_text_element.find_all('strong')) > 0:
            self.excerpt_categories_element = excerpt_text_element.find_all('strong')[0]
        else:
            self._excerpt_categories_element = None
            self._categories_text = None
            self._categories = None
        excerpt_p_elements = []
        for elem in excerpt_text_element.find_all('p'):
            if len(elem.find_all('strong')) == 0 or len(elem.select('strong a')) > 0:
                if elem.text != "&nbsp;":
                    excerpt_p_elements.append(elem)
        if len(excerpt_p_elements) >= 1:
            self.excerpt_p_elements = excerpt_p_elements
            
        else:
            self._excerpt_p_elements = None
            self._excerpt = None
    @excerpt_p_elements.setter
    def excerpt_p_elements(self, excerpt_p_elements: List[Tag]) -> None:
        self.updated = True
        self._excerpt_p_elements = excerpt_p_elements
        excerpt = ""
        for elem in self._excerpt_p_elements:
            if elem.find('span') is None:
                excerpt += elem.text + "\n"
            else:
                excerpt_span = elem.find('span')
                if excerpt_span.get('data-sheets-value') is not None:
                    excerpt = json.loads(excerpt_span.get('data-sheets-value'))['2']
                    break  
        excerpt = excerpt.lstrip("\n")
        self._excerpt = excerpt.replace('more details', '')
    @excerpt_categories_element.setter
    def excerpt_categories_element(self, excerpt_category_element: Tag) -> None:
        self.updated = True
        self._excerpt_category_element = excerpt_category_element
        self.categories_text = excerpt_category_element.text
    @categories_text.setter
    def categories_text(self, categories_text: Tag) -> None:
        self.updated = True
        self._categories_text = categories_text
        categories_list = [cat.strip(' ').replace('&nbsp;', '') for cat in self._categories_text.split('|')]
        self._categories = [Category(cat) for cat in categories_list]    


# In[514]:


class SchedulePage(PageHTML):
    def __init__(self, url: str, **kwargs: Union[dict, str, int]) -> None:
        if url.find('odsc.com') == -1:
            raise ValueError('url must be an odsc schedule page')
        elif url.find('schedule') == -1:
            raise ValueError('odsc link specified is not a schedule page!')
        super(SchedulePage, self).__init__(url, **kwargs)
    @property
    def items(self) -> List['ScheduleItem']:
        if self.updated == True:
            self.items = self.soup
        return self._items
    @items.setter
    def items(self, soup: BeautifulSoup) -> None:
        self._items_elements = self.soup.find_all(class_ = "scheduled-events")[0]
        self._items = []
        count = 0
        for child in self._items_elements.children:
            if (isinstance(child, Tag) and 
                child.has_attr('class') and
               'scheduled-event' in child['class']):
                count += 1
                item = ScheduleItem(child)
                self._items.append(item)
        


# In[515]:


page = SchedulePage('https://odsc.com/boston/east-2019-schedule',
                   headers = {
                       'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19"
                   })


# In[497]:


page.updated


# In[516]:


count = 0
for item in page.items:
    print("title " + item.title)
    print("day " + item.day)
    print("time " + str(item.time))
    print("datetime " + str(item.datetime))
    print("excerpt " + str(item.excerpt))
    for presenter in item.presenters:
        print("presenter_bio " + presenter.presenter_bio)
        print("presenter_image " + str(presenter.presenter_image))
        print("presenter_linkedin " + str(presenter.presenter_linkedin))
        print("presenter_title " + str(presenter.title))
        print("presenter_name " + str(presenter.name) )
        print("presenter_orgs " + str(presenter.organizations))
        print("presenter_positions " + str(presenter.positions))
    print("categories " + str(item.categories) + "\n")


# In[296]:


count = 0
for item in page.items:
    for presenter in item.presenters:
        if presenter.presenter_bio is None:
            print("title " + item.title)
            print("day " + item.day)
            print("time " + str(item.time))
            print("datetime " + str(item.datetime))
            print("excerpt " + str(item.excerpt))
            print("categories " + str(item.categories) + "\n")
            
        


# In[61]:


page.html


# In[54]:


page.updated


# In[55]:


page.soup


# In[188]:


"may-1st".strip('st')


# In[98]:


html = "<p>ligfiuewbfiuewbfiewfbwuebfwubfwbflwb<a href='#'></a></p>"
some_soup = BeautifulSoup(html, "lxml")
some_soup.p.contents


# In[417]:


[1,1,1,1,2].pop(-1)


# In[ ]:




