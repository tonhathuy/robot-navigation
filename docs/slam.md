# List of contents

>- [Introdution SLAM](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/slam.md#introdutions-slam)
>- [Classification SLAM](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/slam.md#classification-methods)
>- [Evaluation and Comparation](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/slam.md#evaluation-and-comparation)
>   + [Lidar SLAM methos](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/slam.md#lidar-slam-methods)
>   + [Monocular SLAM methods](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/slam.md#monocular-slam-methods)
>   + [Stereo SLAM methods](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/slam.md#stereo-slam-methods)
>- [Conclusion](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/slam.md#conclusion)

# Introdutions SLAM

- Simultaneous localization and mapping (SLAM) is the process of determining the positions and orientation of a sensor with respect to its surrounding, while simultaneously mapping the environment around that sensor. 

- There are some sensors can be used to sovle that problem which commonly is 2D lidar, a monocular and ZED stereo cameras, . . .


# Classification methods

- There are several different types of SLAM methods was developed to sensing like:

    + 2D lidar-based: GMapping, Hector SLAM, Cartographer, . . . 

    + Monoluar camera-based: LSD SLAM, ORB SLAM, DSO, . . .

    + Stereo camera-based: ZEDfu, RTAB map, ORB SLAM, S-PTAM, . . . 


# Evaluation and Comparation

## Lidar SLAM methods

|Methods |Advantage |Disadvantage |
|:--- |:---: |:---: |
|GMapping| |Cannot represent the real map of the environment |
|Hector SLAM |<ul><li>Can represent the real map of the environment</li><li>Best fit for tracking</li></ul> | |
|Cartographer |<ul><li> Best fit from 2D Lidar maps to the real environment</li><li>Can be use for tracking</li><li>Using global map optimization cycle and local probabilistic map updates</li></ul> | |

![2D SLAM methods](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/img/SLAM/2DLidar.png)

## Monocular SLAM methods

|Methods |Advantage |Disadvantage |
|:--- |:---: |:---: |
|PTAM| Fast | <ul><li>Cannot represent the real map of the environment</li><li>Lost the track when robot had a turn</li></ul>|
|SVO and DPPTAM| | <ul><li>Cannot represent the real map of the environment</li><li>Lost the track when robot had a turn</li></ul>|
|LSD SLAM| <ul><li> Provide dense point cloud maps and allow to make 3D scene recovery and object detection</li><li> Create a 3D dense map</li><li>Can be used for solving localization problem with an additional module for scale recovery</li></ul>| Lost the track when robot had a turn|
|ORB SLAM| <ul><li>Can solve navigation problems</li><li>Good enough for solving navigation problems</li></ul>| <ul><li>Lost the track when robot had a turn</li><li> Difficulties to make 3D scene recovery</li></ul>|
|DSO| <ul><li> Provide dense point cloud maps and allow to make 3D scene recovery and object detection</li><li> Create the best 3D dense map</li><li>Can be used for solving localization problem with an additional module for scale recovery</li></ul>| Lost the track when robot had a turn|

![Monocular SLAM methods](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/img/SLAM/Monocular.png)

## Stereo SLAM methods

|Methods |Advantage |Disadvantage |
|:--- |:---: |:---: |
|ZEDfu| Can use in term of robot pose tracking| The trajectory is not accurate|
|RTAB map| <ul><li>Can solve localization problem with accuracy comparable with Lidar methods without additional manipulations</li><li>One of the best method in terms of RMSE for mobile robot localization problem in homogeneous indoor office environment</li></ul>| The system sometimes has the problem with pose estimation when the robot moves closer to monotonous walls|
|ORB SLAM| Create sparse 3D map| The trajectory is not accurate|
|S-PTAM| <ul><li>Robust in terms of pose tracking</li><li>Have the spare map</li></ul>| The localization accuracy can be not enough for robot navigation|

![Stereo SLAM methods](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/img/SLAM/Stereo.png)

# Conclusion

![Map generted](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/img/SLAM/MapsGenerated.png)

- 2D lidar SLAM systems: Hector SLAM and Cartographer provide accurate solutions for UGV localization and map building. The methods provide almost the same results with RMSE of
Absolute Trajectory Error (ATE) at 0.024 m. Both trajectories coincide with the marked line on the floor. However, since Cartographer uses global map optimization cycle and local probabilistic map updates, it makes this system more robust to environmental changes.
- Monocular visual SLAM systems: Parallel Tracking and Mappping (PTAM), Semi-direct Visual Odometry (SVO), Dense Piecewise Parallel Tracking and Mapping (DPPTAM) failed the experiments since they lost track due to lack of features.
- Monocular visual SLAM systems: Large Scale Direct monocular SLAM (LSD SLAM), ORB SLAM, Direct Sparse Odometry (DSO) can be used for solving localization problem with an additional module for scale recovery.
- No monocular SLAM system could handle scale ambiguity problem without additional information about environment for scale recovery.
- Stereo visual SLAM systems: ZEDfu, Real-Time AppearanceBased Mapping (RTAB map), ORB SLAM, Stereo Parallel Tracking and Mapping (S-PTAM) provide metric information about localization without additional scaling modules, also building 3D metric point cloud.
- Visual SLAM system: RTAB map demonstrated the best results for localization problem in our experiments with RMSE ATE of 0.163 m, but it has the problem with the track lost close to
monochrome walls. The most robust and stable between tested system is ORB SLAM with RMSE ATE of 0.190 m

![Trajectoruy error base on Hector](https://github.com/tonhathuy/robot-navigation/blob/dev/docs/img/SLAM/TrajectoryErrorBaseOnHector.png)
