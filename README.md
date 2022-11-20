# conquerShot-backend

This is the repository of all backend implementation of the project [**ConquerShot**](devpost.com/software/conquershot) for [hackaTUM 2022](https://hack.tum.de/), contributed by [Mariz Samir Awad](https://github.com/marzi333), [Johannes Getzner](https://github.com/JohannesGetzner), [Zhuoling Li](https://github.com/joelynli0110) and [Melanie Maier](https://github.com/mmmaier). The project is submitted for the challenge "Open Digital Earth Reconstruction" which is sponsored by Huawei. 

## ML Models for OSM Feature Classification

You can find all ML-related implementation under ```./mlmodels``` , feel free to check out there:

```
cd ./mlmodels
```

### 1. Set up the Environment

Install all required packages and dependencies via:

```
pip install -r requirements.txt
```



### 2. Data Preparation

The training and evaluation of the model is basically implemented with [torchvision](https://pytorch.org/vision/stable/index.html). In order to load and proceed data with the library, the data should be organized as follows:

```
<dataset_name>
 ├── train
 │   ├── footway
 │   │   └── xxx.jpg
 │   └── primary
 │       └── xxx.jpg
 ├── val
 │   ├── footway
 │   │   └── xxx.jpg
 │   └── primary
 │       └── xxx.jpg
 └── issues
     ├── footway
     │   └── xxx.jpg
     └── primary
         └── xxx.jpg
```

For training the binary classifier for OSM features, we are provided the Huawei Challenge Dataset with following structure:

```
<huawei_dataset>
 ├── train
 │   ├── xxx.jpg
 |   ├── ...
 |   ├── labels.csv
 ├── val
 │   └── xxx.jpg
 |   └── ...
 |   └── labels.csv
 ├── issues
 │   └── xxx.jpg
 |   └── ...
 |   └── issues.csv
```

The following command is used to transform the Huawei dataset into the required structure (<split> can be train, val, issues, etc. ):

```
python prepare_data.py --split <split>
```

For training the classfier for road/non-road, we additionally sample the data from [MS-COCO dataset](https://cocodataset.org/#home) , with ensuring that a fair distribution of the training data (road and non-road). More details see [here](https://github.com/giddyyupp/coco-minitrain).



### 3. Training the model

The model is based on a pre-trained backbone from the torchvision library,  see [documentation](https://pytorch.org/vision/stable/models.html). In our case, the ```<backbone_name>``` is set by default as ```resnet18```, but feel free to try out other resnet variants like resnet50, resnet101, etc. 

Fine-tuning the model for road classification based on ```<backbone_name>```:

```
python fine_road_cls.py --backbone <backbone_name>
```

as well as fine-tuning the model for OSM classification based on ```<backbone_name>``` :

```
python finetune_osm_cls.py --backbone <backbone_name>
```

The fine-tuned models will be saved under ```./checkpoints/```.  We also upload our trained models (in pth. format) for both road classification and OSM classification [here](https://github.com/marzi333/conquerShot-backend/tree/main/mlmodels/checkpoints).  



### 4. Evaluating the model

 You can evaluate the model on the test set via following:

```
python evaluate.py --batch_size <batch_size> \
				   --input_size <input_size> \
				   --phase <phase> \
				   --cls_type <cls_type>
```

Note that ```<cls_type>``` specifies the classifier type to be evaluated. It can be either ```osm_cls``` or ```road_cls```.

The results will be output as csv.files containing the data in two columns (*img_id* and *prediction*), and stored under ```../results/```. 