# Bioacustics Annotations Dashboard (BADASH) 🐸

BADASH is a streamlit app for visulization of bounding box annotations. (Explain what is annotations in Bioacustics and add protocol) Exploratory Data Analysis
Fast and way to check the consistency of used codes for annotation

## How to play with BADASH 🐸?

1. Open this [link](https://github.com/) to use BADASH 🐸. 

2. Upload a set of annotations. You can use [these](https://github.com/juansulloa/soundclim_annotations/tree/master/bounding_boxes/INCT41) annotations to play with BADASH 🐸. 

## How to use BADASH in my project?

### 1. Installing and Running


1. Clone this repo in your computer:
```shell
git clone https://github.com/jscanass/annotations_eda_dashboard.git
```

2. Install requirements or environment. Use a [virtual environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) to avoid tampering other Python installations in your system. BADASH 🐸 works with Python versions 3.7.

```shell
conda create --name badash_env python=3.7
conda activate badash_env
pip install -r requirements.txt
```
OR:
```shell
conda env create -f environment.yml
conda activate badash_env
```

3. Run streamlit app:
```shell
streamlit run app.py
```

Feel free to modify the code of BADASH 🐸

### 2. Annotations:

Follow the same format for annotations in your project as [examples](https://github.com/juansulloa/soundclim_annotations/tree/master/bounding_boxes/INCT41). The name of each file follow this structure: {SITE}_{DATE}.txt

### 3. Dictionary

Modify the species and quality dictionary following the same structure of the Species_code_Annotations.xlsx file. 

## Authors and contributors

* Juan Sebastián Cañas - [jscanass](https://github.com/erikasv)

## License
This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.
