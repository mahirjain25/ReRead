# ReRead
Web application to proofread documents and derive research-oriented insights. 


### Dependencies

**Sumy Summarizer**

`pip install git+git://github.com/miso-belica/sumy.git`

**PyTorch**

`pip3 install http://download.pytorch.org/whl/cpu/torch-0.4.1-cp36-cp36m-linux_x86_64.whl`

`pip3 install torchvision`

**Django Widget Tweaks**  

`pip3 install django-widget-tweaks`

**Gensim**  
`pip3 install gensim`

**Language-check**  
`pip3 install language-check`

### Instructions to set up server
+ Clone the repository
+ Run `python3 manage.py migrate`
+ Run `python3 manage.py makemigrations`
+ Run server using `python3 manage.py runserver` and navigate to localhost:8000


### Features
+ Grammar Error Correction
+ Keyword Extraction and Associated Literature References
+ Abstract Summarisation
