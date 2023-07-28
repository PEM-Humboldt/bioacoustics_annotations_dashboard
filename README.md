# Bioacoustics Annotations Dashboard (BADASH 🐸)

BADASH is a streamlit app for visualization of bounding box annotations used for training machine learning models in Bioacoustics. Badash can be used to visualize annotations results and to check the consistency of codes defined in the annotation protocol.

## How to play with BADASH 🐸?

1. Open this [link](https://jscanass-bioacoustics-annotations-dashboard-app-fs3l8h.streamlit.app/) to use BADASH 🐸. 

2. Upload a set of annotations. You can use [these](https://github.com/juansulloa/soundclim_annotations/tree/master/bounding_boxes/INCT41) annotations to play with BADASH 🐸. 

## How to use BADASH 🐸 in my project?

### 1. Installing and Running


1. Clone this repo in your computer:
```shell
git clone https://github.com/jscanass/bioacoustics_annotations_dashboard.git
```

2. Use a [virtual environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) to avoid tampering other Python installations in your system. BADASH 🐸 works with Python versions 3.7. Install requirements and environment:

```shell
cd bioacoustics_annotations_dashboard
conda create --name badash_env python=3.10
conda activate badash_env
pip install -r requirements.txt
```

3. Run streamlit app:
```shell
streamlit run app.py
```

Feel free to modify the code of BADASH 🐸

### 2. Annotations

Follow the same format for annotations in your project as [examples](https://github.com/juansulloa/soundclim_annotations/tree/master/bounding_boxes/INCT41). The name of each file follow this structure: {SITE}_{DATE}.txt

### 3. Dictionary

Modify the species and quality dictionary following the same structure of the Species_code_Annotations.xlsx file. 

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
The authors acknowledge financial support from the intergovernmental Group on Earth Observations (GEO) and Microsoft, under the GEO-Microsoft Planetary Computer Programme (October 2021).

## Contact

- Juan Sebastián Ulloa (julloa@humboldt.org.co, [juansulloa](https://github.com/juansulloa))
- Juan Sebastián Cañas (jcanas@humboldt.org.co, [jscanass](https://github.com/jscanass))


