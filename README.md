# terrapseudo_dataset

[Dataset](https://uofi.app.box.com/folder/249397004985) </br>

The name of this dataset is terrapseudo, from "terrasentia" and "pseudolabeling". 

## Collection

This dataset was extracted from the `.bag` files of [this dataset](https://github.com/jrcuaranv/terrasentia-dataset). </br>
For this, the scripts of [rosbag2csv](https://github.com/thomas-woehrle/rosbag2csv) and [dataset_creation](https://github.com/thomas-woehrle/dataset_creation) were used. A detailed description of the workflow can be found in their respective README files. 

## Structure

The dataset folders mirror and extend the structure of the dataset mentioned above. </br>
Specifically, this is the structure:

```
terrapseudo_dataset
/<field_name> f.e. cornfield1
    /<day_name> f.e. 20220603_cornfield
        /<run_name> f.e. ts_2022_06_03_02h54m54s
            /left_cam
                <some_picture>.png
                ...
                labels.csv
            /right_cam
                <some_other_picture>.png
                ...
                labels.csv
            rosbag.csv
```
</br>
The labels.csv files are structured like this:


| image_name                       | vp           | ll           | lr           |
|----------------------------------|--------------|--------------|--------------|
| 20220603-025500-0805.png         | (132, 104)   | (49, 223)    | (319, 217)   |
| 20220603-025502-0767.png         | (132, 104)   | (54, 223)    | (319, 217)   |
| ...         | ...   | ...    | ...   |

NOTE: Not all `ll` have `y=223` and not all `lr` have `x=319`. But all* of ll and lr are on the frame.</br>

It is important to note that not all pictures in the `left_cam` or `right_cam` directories have a corresponding row in their `labels.csv` file. See [Caveats](##Caveats) section below. 

</br>

The `rosbag.csv` files contain the output of the rosbag2csv script mentioned above. It was run from one of the dataset_creation scripts mentioned above like so: 
```
python3 rosbag2csv.py "$bagfile" 1 ./topics.json -o "$output_folder/$bagfile_name/"
```
with `topics.json` being like the topics.json in this repository. 

## Image shape & Preprocessing 
The images have a shape of `832×468`. The labels exist in the dimension of `320×224`, because of the properties of the ML model used. </br>
The function `process_image()` in `utils.py` is used to move an image from its `832×468` into a `320×224` dimensionality (without stretching), where the labels can be applied. 

## Visualization 
The `test_visual.py` file can be used to visualize the labels of a specific cam. 

## Caveats
As described in the dataset_creation repository, this dataset was created using pseudo labeling, where humans manually delete bad labels. This brings 2 main caveats:
1. Dataset size: only around 1/3 of all pictures available are labeled, meaning that the number of images in `left_cam` is roughly 3 times the number of rows in `left_cam/labels.csv`. Same for `right_cam`. See the `cleanup_info.txt` files inside the <run_name> folders starting end of July for more information on this.

2. Dataset quality: It is reasonable to assume that the 1/3 of pictures is not a random third, but that there is a concentration among a certain kind of picture. Specifically, it seems like images that are further from the norm i.e. images where the robot isn't looking directly towards the vanishing point, are underrepresented in the labels files.

The one pro this pseudolabeling approach has is that it is faster than complete manual labeling. 
