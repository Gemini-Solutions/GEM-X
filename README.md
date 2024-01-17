# GEM-X
Gem-X is a Python utility that revolutionizes the process of generating XPath files for any given URL within seconds.

## Why do we need Gem-X at all?
In recent years of our automation, we observed that a significant amount, approximately 20%-30% of our valuable time, is wasted in creating locators for UI elements. While existing extensions in the market offer some assistance, they come with their own set of limitations:
* These extensions often require manual intervention, requiring the user to open the URL and select elements one by one to create locators
* The creation of locators is limited to individual elements, presenting a time-consuming hurdle
* When the goal is to generate a locator file, existing extensions fall short. Only a limited number of them facilitate this, and they do not organize locators according to variable names, which again require additional manual effort on the user's part
Gem-X addresses these challenges seamlessly, offering an efficient solution to streamline the process of creating locators for UI elements.

## Features of Gem-X
* Gem-X simplifies the process of generating xpath files by only taking URL as input and asking the user to authorize the application manually if needed
* Gem-X keeps track of all the xpath files generated, thus providing a resource-efficient solution
* Gem-X uses Selenium and BeautifulSoup to extract the DOM structure. This robust approach ensures the generation of XPath locators for virtually every element available on UI
* Gem-X eliminates redundant XPaths and adds indexes to elements, enhancing the correctness of the generated locators. This feature allows for a more refined and optimized xpath outputs

## Prequisite
To use this utility, please make sure that you have **Python** and **pip** installed on your system

## Steps to use this utility
- Clone the repository by using git clone command:
  ```https://github.com/Gemini-Solutions/GEM-X.git```
- Create a virtual environment using the command given below. Click [here](https://stackoverflow.com/a/71086705/9985849) to learn why we need a virtual python environment.
  ```python -m venv <name of your virtual environment>```
- Activate virtual environment by using the command:
  ```<name of your virtual environment>\Scripts\activate```
  **Note** If you are getting UnauthorizedAccessError like ![UnauthorizedAccessError](https://github.com/Gemini-Solutions/GEM-X/blob/main/media/VirtualEnvError.png)
, run command ```Set-ExecutionPolicy Unrestricted -Scope Process``` before activating your virtual environment. On Gemini machines, you may have retrictions to Set Exacution policy for the current sesion only, so make sure to execute this command each time before activating your virtual environment```
- Run ```pip install -r config/requirements.txt```. This command will install all the requirements needed to run this utility
- Run XPathGenerator.py file by passing a valid URL

  ## Technology used to create this utility:
  I used the following tech-stack to create this utility
  1. Python
  2. Selenium
  3. BeautifulSoup

## Future Plans:
The Gem-X utility will be enhanced significantly in the upcoming days with features, including but not limited to:
1. **PyPI Package Integration:** Users will be able to use Gem-X seamlessly by downloading all its features with a single, convenient pip command
2. **Java Migration for Integration:** I am actively working on migrating Gem-X to Java, facilitating seamless integration with GemJar and Quantic frameworks, thereby broadening its compatibility and utility
3. **Human-Readable Element Names:** With added OpenAI libraries, Gem-X will generate more human-readable names for the created xpaths
4. **Customization Options:** Gem-X will empower users with the flexibility to customize the utility according to their specific needs. This feature ensures that the tool aligns perfectly with individual requirements, offering a tailored and user-centric experience.
