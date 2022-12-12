# Indeed-Apply-Bot
## Bot to automatically apply to jobs on Indeed.com, written in Python using Selenium.
---
This Bot is to automate job search and application on Indeed.com . You will need the Selenium library installed. Open a terminal : 

**pip install selenium**

Selenium needs a driver to interact with your web browser. I used chromedriver. Download this from Google [HERE](https://chromedriver.chromium.org/downloads).

**Use:**

Clone/Download this repo.

Edit config.json.example with your relevant information. Email etc. Delete ".example" from the end of the file.

Run with terminal command : 

python (or python3) main.py

---

This code is my first real attempt at anything interactive with webpages. It is updated and hopefully improved intermittently. Feel free to fork, clone , and tinker as you wish. Hopefully it helps someone out .

---
**This code is no longer supported or updated. Indeed's DOM is constantly changing and is made in such a way to prevent bots like this. I managed to overcome some of these issues by using PyAutoGUI. These changes are on the branch "Auto" should you wish to use them. You will have to configure locations of clicks via pixels for your own display size if you wish to use this method.**

I am leaving the repo up as an example of this being the first thing I really wrote and to help others who may wish to speed up their job search via botting . Necessity is the mother of invention.
