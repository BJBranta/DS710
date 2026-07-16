# Assignment 7 Reflection - Ben Branta

## 1. Describe the process of finding the data you need in page sourcecode.

**Answer:** To start the process we would first find a site, a particular item of interest, right click, and inspect the elements in the page sourcecode. I would look for element identifiers for searching later on. We would use the requests library to request the website and turn the response content into soup by providing an html parser. After having soup I would use find or find_all with an element type or identifier, such as table and wikitable. The method of finding the specific content will vary by what you are looking for.

---

## 2. Visit a site you frequent, probably a shopping site. Poke around in the sourcecode using the developer console. Describe what you see, and compare to source for Wikipedia pages.

**Answer:** I went to amazon to look around. As I was learning about BeautifulSoup I was also looking into web QA automation tools. What I was learning about was how many websites are now Javascript driven using React or other libraries. So with that in mind, on the Amazon page I see a lot of script element types. I believe that means these element load dynamically which would make sense for loading items specific to a user profile. When I look at a specific item though it does appear to be div so I'm not exactly sure how that loads dynamically. Compared to the wikipedia page amazon has much more content. The script element types are what stand out to me.

---

## 3. Discuss the ethics of webcrawling.

**Answer:** It is important to site and have approval to use data. It is someone elses work and the authors and owners of that work should get credit but also provide approval to use it. I've done a little more research into this topic and have found some processes to follow or consider. Review the web sites robots.txt file which is a standard used by websites to instruct web crawlers which parts of the site they are allowed to access. Use API's when they are available. Rate limit requests.

---

## 4. What did you find interesting or useful in this Lesson, and how might you use it in your future work.

**Answer:** I find the BeautifulSoup package interesting. It takes a difficult problem of parsing html and provides tools to help search through it. In my current work I do QA on a vehicle telematics data application which includes web test automation. I primarily have worked from the vehicle to data storage and have not gotten into the web automation tools but this fits the next step I need to take there. As I expand my data science role I see this as an opportunity to source more data. Data doesn't always show up as clean downloadable csv's and web scraping is one more tool I now have. 