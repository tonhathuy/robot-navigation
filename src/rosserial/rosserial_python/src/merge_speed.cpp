#include <ros/ros.h>
#include <message_filters/subscriber.h>
#include <message_filters/time_synchronizer.h>
#include <geometry_msgs/Vector3.h>
#include <std_msgs/Float64>

void callback(const & std_msgs::Float64& speed_left, const & std_msgs::Float64& speed_right){
	speed_act_left = trunc(speed_left.data*100)/100;
	ROS_INFO("speed left : %f", speed_act_left);
}


int main(int argc, char** argv){
    ros::init(argc, argv, "merge_speed");
    ros::NodeHandle nh;
    // ros::Subscriber sub = n.subscribe("speed_left", 50, handle_speed);
    // ros::Subscriber sub = n.subscribe("speed_right", 50, handle_speed);

    message_filters::Subscriber speed_l_sub(nh, "speed_left", 1);
    message_filters::Subscriber speed_r_sub(nh, "speed_right", 1);
    //ros::Publisher odom_pub = n.advertise<nav_msgs::Odometry>("odom", 50);
    TimeSynchronizer sync(speed_l_sub, speed_r_sub, 10);
    sync.registerCallback(boost::bind(&callback, _1, _2));

    ros::spin();
    return 0;
}
