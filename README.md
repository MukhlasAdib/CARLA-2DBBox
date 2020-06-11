# CARLA Vehicle 2D Bounding Box Annotation Module

<head> This repo contains several python file that can be used to automatically create 2D counding box for vehicles from a camera view point in CARLA Simulator. To  use this, you need to import `carla_vehicle_annotator.py` to your python code and use the available functions. The other provided files are used to do supporting tasks that will be explained in this file.

Some parts of the provided code are not made by me and copied from CARLA example code. CARLA Simulator and its example code are licenced under the terms of MIT Licence. For more information about CARLA, I highly recommend you to visit their website https://carla.org.

## `carla_vehicle_annotator.py`

There are several functions that is provided in this module. However, you only need these main functions to make this module works properly.

### `result, removed = auto_annotate(vehicles, camera, depth_img, max_dist=100, depth_margin=-1, patch_ratio=0.5, resize_ratio=0.5, json_path=None)`

This function process the vehicles and image information and retrieve the 2D bounding box pixel coordinates for each visible vehicle with the corresponding vehicle’s class

Arguments:
- **`vehicles` (list of `carla.Actor`):** list that contain vehicle actors that you want to consider. You can pass list of all vehicles that have been spawned in Carla world.
- **`camera` (`carla.Sensor`):** the RGB camera object (carla sensor).
- **`depth_img` (`float` 2D numpy array):** the depth map taken from the same view of RGB camera in meter unit. You can get it from the output of depth camera manually or by using `extract_depth( )` function.
- **`max_dist` (`float` ; default 100):** the maximum distance parameter for distance filter. Increasing this value will allow the function to return vehicles that is located in greater distance, and thus with smaller bounding box. 
- **`depth_margin` (`float` ; defaullt -1):** the depth margin parameter for occlusion filter. If you pass negative value, the depth margin will be vary according to the vehicle’s dimension. Increasing this value can increase the number of positive results, but with more chance of having false positive result.
- **`patch_ratio` (`float` [0,1] ; default 0.5):** the patch ratio parameter for occlusion filter. Incresing this value might reduce the number of positive results, but with more cance of having false negative results.
- **`resize_ratio` (`float` [0,1] ; default 0.5):** the resize ratio parameter for occlusion filter. Set this to 1 if you don’t want to resize the bounding box for depth measurement.
- **`json_path` (`string` ; default None):** the JSON .txt path that contains vehicle types classification (ex: *‘/vehicle_class_json_file.txt’*). This argument must be filled if you want to assign a class label to each vehicle. Read explanation about vehicle_class_json_creator.py for information about labeling. Set this to None if you don’t need the label.

Return:
- **`result` (dictionary):** python dictionary that contains the bounding boxes, vehicle actors, and the corresponding label of the visible vehicles.
- **`removed` (dictionary):** python dictionary that contains the bounding boxes, vehicle actor, and the corresponding label of the vehicles that are removed by the occlusion filter. 

The result and removed dictionaries contain the following keys - values:
- key: `vehicles` - value (list of `carla.Actor`): the list of vehicle actors.
- key: `bbox` - value (list of `int` 2D numpy array): the list of bounding boxes where each bounding box represented by two (min and max) corner points (in (x,y) format) of the box. The i-th element of the list is the bounding box for i-th vehicle in `vehicles`.
- key: `class` - value (list of `int`): the list of vehicle class. The i-th element of the list is the class label for i-th vehicle in `vehicles`.

Notes:
- Make sure that the depth camera and RGB camera have the same attributes and transformation, and their data are taken in the same time.
- You might wonder why you need the removed bounding boxes. The occlusion filter is not 100% accurate. Therefore, you might want to have the list bounding boxes removed by the occlusion filter so that you can return the removed bounding box if you find that it is a false removal.
- For a quick review about how the algorithm works, I recommend you to visit this site.

### `void save_output(carla_img, bboxes, vehicle_class=None, old_bboxes=None, old_vehicle_class=None, cc_rgb=carla.ColorConverter.Raw, path=‘’, save_patched=False, add_data=None, out_format=‘pickle’)`

Use this function to save the result of `auto_annotate( )` into your local directory. This function will save the RGB image and RGB image with drawn bounding boxes in .jpg format and the bounding boxes information in JSON .txt or pickle format.

Arguments:
- **`carla_img` (`carla.Image`):** object (carla image) returned by the RGB camera at the time the bounding boxes are calculated.
- **`bboxes` (list of `float` 2D numpy array):** list of bounding boxes coordinates that you want to save. You can get it from the returned value `result` of `auto_annotate( )` with key `bbox`.
- **`vehicle_class` (list of `int` ; default None):** the list of visible vehilcles’ class. You can get it from the returned value `result` of `auto_annotate( )` with key `class`. Set this to None if you don’t want to save this information. 
- **`old_bboxes` (list of `int` 2D numpy array ; default None):** list of bounding boxes that are removed by the occlusion filter. You can get it from the returned value `removed` of `auto_annotate( )` with key `bbox`. Set this to None if you don’t want to save this information.
- **`old_vehicle_class` (list of `int` ; default None):** the list of vehicles’ class that are removed by the occlusion filter. You can get it from the returned value `removed` of `auto_annotate( )` with key `class`. Set this to None if you don’t want to save this information.
- **`cc_rgb` (`carla.ColorConverter` ; default `carla.ColorConverter.Raw`):** image color style that you want to use for the RGB image.
- **`path` (string ; default ‘’)**: the folder path where you want to save the result (ex: *‘/this/path/‘*).
- **`save_patched` (`bool` ; default False):** set this to True if you want to save the image with drawn bounding boxes.
- **`add_data` (any ; default None)**: fill this argument if you want to save any other additional information.
- **`out_format` (string ; default ‘pickle’)**: the file format to save the result and removed bounding boxes and class and also the additional information `add_data`. Only support *‘json’* (.txt) and *‘pickle’* (.pkl). Any format you choose, this information will be packed as python dictionary when you import the file to your python program.

This function will create three folders in `path`, which are *out_rgb* that contains RGB image, *out_bbox* that contains bounding boxes and other data formatted in pickle or JSON, and *out_rgb_bbox* that contains RGB image with drawn bounding boxes. Folder *out_rgb_bbox* will only be created if you set parameter `save_patched` to True. Data taken from the same moment are named with the same name in these three folders, so that you can find which bounding boxes file that corresponds to which image easily. Information that packed in *out_bbox*’s files are packed as python dictionary. This dictionary contains these keys - values:
- key: `bboxes` - value: data passed to `bboxes` argument
- key: `vehicle_class` - value: data passed to `vehicle_class` argument
- key: `removed_bboxes` - value: data passed to `old_bboxes` argument
- key: `removed_vehicle_class` - value: data passed to `old_vehicle_class` argument
- key: `others` - value: data passed to `add_data` argument

Notes:
- Make sure you put ending slash *‘/‘* behind the folder path that you pass into `path` argument.
- If you want to save bounding boxes data in JSON format, make sure data that you passed to `add_data` argument (if any) is compatible with JSON format.

### `depth_meter = extract_depth(depth_img)`

Use this function to convert depth `carla.Image` that you get from depth camera into depth map in meter unit, so that you can pass it to `auto_annotate( )` function.

Argument:
- **`depth_img` (`carla.Image`)**: carla image object that come from depth sensor measurement

Return:
- **`depth_meter` (`float` 2D numpy array)**: depth map of the corresponding input in meter unit.

Implementation example, assuming that world and the actors have been set.

```python
import carla_vehicle_annotator as cva
import queue
...
cameraQueue = queue.Queue()
depthQueue = queue.Queue()
camera.listen(cameraQueue.put())
depth.listen(depthQueue.put())

while True:
  world.tick()
  vehicles = world.get_actors().filter(‘vehicle.*’)
  if not cameraQueue.empty() and not depthQueue.empty():
    camera_data = cameraQueue.get()
    depth_data = depthQueue.get()
    depth_map = cva.extract_depth(depth_data)
    result , removed = cva.auto_annotate(vehicles, camera, depth_map)
    cva.save_output(camera_data, result[‘bbox’])
...
```

## `test_draw_bb.py`

Run this program to test how the algorithm works. This program will load interactive window that contains view from a car camera perspective. You can control the car manually so that you can evaluate the performance of the algorithm directly. You can change the values of filter parameters and see how changing these parameters can effect the performance of the filter.

## `vehicle_class_json_creator.py`

Run this program to create *vehicle_class_json_file.txt*. This file is a JSON formatted data that map each vehicle types available in Carla to one integer label. Definition of each label is also packed in the JSON file. The default label mapping file has been provided in my repo. But you can create your own label mapping file by running and edit this program.

This program has two variables that you can modify. One of them is `autoFill`, which if you set to True, the program will automatically create mapping file that maps all vehicle types to class label 0. The other one is `class_ref`, which is a dictionary that defines the definition of each class label. After you run the program (if `autoFill` is set to False), check your Carla window and it will show each vehicle types. All you have to do is type the vehicle’s class in your python window. I think it is quite intuitive.

That’s all I have for you. Have fun with CARLA and keep supporting CARLA project. Thank you.

