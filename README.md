
# Cardio Analyx

It is a django-web application which can be used to detect cardiomegaly disease from a chest X-ray. We made it as a part of UNESCO India Africa Hackathon 2022




## Model files

To run this project, you will need to add download the following .pkl file:
200_6_23.pkl
https://drive.google.com/file/d/1aBaBs_Deu6v4hRLK3TSBp7hOp5wdalkY/view?usp=share_link

and place as following,

`cardioAnalyx/dashboard/`



## Installation

Clone the project

```bash
  git clone https://github.com/harshavb08/cardioAnalyx.git
```

Go to the project directory

```bash
  cd cardioAnalyx
```
Create virtual environment and install required packages


```bash
   pip install -r requirements.txt
```

Here are the few screenshots of the website,

**Home Page**

![homePage](https://user-images.githubusercontent.com/73329321/215339479-a02a6e65-0325-4802-bd3c-aa60b198826a.png)

**Dashboard**

![userDashboard](https://user-images.githubusercontent.com/73329321/215339564-c441a726-eb17-4aab-8c44-7d5a64100165.png)

**Result**
![result](https://user-images.githubusercontent.com/73329321/215339537-4515fc30-900d-439d-9fb2-b27a727d0d0e.png)

** Questionnaire**
![questionare](https://user-images.githubusercontent.com/73329321/215339581-fdb2bec4-3693-41cc-aca9-394ccf9b0034.png)

**Nearest Doctors**
![nearestDoctors](https://user-images.githubusercontent.com/73329321/215339613-f0a0e5ac-65c3-4d34-a3cd-699a66943267.png)

**Multiple Languages**
![multilanguage](https://user-images.githubusercontent.com/73329321/215339665-c304d087-041d-49f0-9ee6-ac13d19b9611.png)



## Technology

The Website is built with 

- Django
- SQLite
- Bootstrap
- CNN Resnet125

## Features

- User Authentication
- Multilingual
- Shows nearest cardiologist 
- Previous test history
- Symptom questionnaire test (can be used if x-ray is not available)
