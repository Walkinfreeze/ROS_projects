#include <ros/ros.h>
#include <geometry_msgs/TwistStamped.h>
#include <tf/transform_datatypes.h>
#include <tf/transform_listener.h>
#include <tf/transform_broadcaster.h>
#include <std_msgs/Float64.h>
#include <rosbag/bag.h>
#include <rosbag/view.h>
#include <iostream>
#include <fstream>
#include <math.h> 

geometry_msgs::Twist vel_msg_;
geometry_msgs::Twist velf_msg_;
std_msgs::Float64 theta_msg_;
std_msgs::Float64 theta_msg2_;
std_msgs::Float64 beta_msg_;
std_msgs::Float64 delta_msg_;
std_msgs::Float64 deltaf_msg_;
ros::Publisher pub; 
ros::Publisher pub_f; 
ros::Publisher pub_theta; 
ros::Publisher pub_theta2; 
ros::Publisher pub_beta; 
ros::Publisher pub_delta; 
ros::Publisher pub_deltaf; 
double v_x_;
double v_y_;
double v_a_;
double v_x_f;
double v_y_f;
double v_a_f;
boost::shared_ptr<tf::TransformListener> tf_listener_;
tf::StampedTransform f2b_;
double th;
double th_lsm;
double beta_;
double delta_;
double beta_f;
double delta_f;
rosbag::Bag bag;
std::fstream myfile;
//std_msgs::Float64::ConstPtr th_lsm; 

void thetaCallback(const std_msgs::Float64 msg)
{
  th_lsm = msg.data;
}
 //velocity from alpha beta filter
void velfCallback(const geometry_msgs::TwistStamped::ConstPtr& twistf_msg){
 velf_msg_ = twistf_msg->twist;
 v_x_f=twistf_msg->twist.linear.x;
 v_y_f=twistf_msg->twist.linear.y;
 v_a_f=twistf_msg->twist.angular.z;
 velf_msg_.linear.x = v_x_f*cos(th_lsm)-v_y_f*sin(th_lsm);
 velf_msg_.linear.y = v_x_f*sin(th_lsm)+v_y_f*cos(th_lsm);
 velf_msg_.angular.z = v_a_f;
 pub_f.publish(velf_msg_);


 beta_f = atan(velf_msg_.linear.y/velf_msg_.linear.x); 
 delta_f = atan(2*tan(beta_f));

 
 deltaf_msg_.data = delta_f*180/M_PI;
 pub_deltaf.publish(deltaf_msg_);
}

void velCallback(const geometry_msgs::TwistStamped::ConstPtr& twist_msg){
 vel_msg_ = twist_msg->twist;
 v_x_=twist_msg->twist.linear.x;
 v_y_=twist_msg->twist.linear.y;
 v_a_=twist_msg->twist.angular.z;
 
  // Velocity transform to body frame
  th = tf::getYaw(f2b_.getRotation());
  vel_msg_.linear.x = v_x_*cos(th)-v_y_*sin(th);
  vel_msg_.linear.y = v_x_*sin(th)+v_y_*cos(th);
  vel_msg_.angular.z = v_a_;
  theta_msg_.data = th;
// theta_msg2_.data = th_lsm;

  // Calculate slip angle and steering angle
  beta_ = atan(vel_msg_.linear.y/vel_msg_.linear.x); 
  delta_ = atan(2*tan(beta_));

  beta_msg_.data = beta_*180/M_PI;
  delta_msg_.data = delta_*180/M_PI;


  //Publish here
  pub.publish(vel_msg_);
  pub_theta.publish(theta_msg_);
  pub_beta.publish(beta_msg_);
  pub_delta.publish(delta_msg_);
 // pub_theta2.publish(theta_msg2_);
}




int main(int argc, char **argv)
{
    ros::init(argc, argv, "velocity");
    tf_listener_.reset(new tf::TransformListener);
    ros::NodeHandle n;
   
    ros::Subscriber sub = n.subscribe("vel", 5, velCallback);
    ros::Subscriber f_sub = n.subscribe("twist_f", 5, velfCallback);
    ros::Subscriber theta_sub = n.subscribe("theta", 5, thetaCallback);
    pub = n.advertise<geometry_msgs::Twist>("vel_hec",5);
    pub_f = n.advertise<geometry_msgs::Twist>("vel_abf",5);
    pub_theta = n.advertise<std_msgs::Float64>("theta_hec",5);
    pub_beta = n.advertise<std_msgs::Float64>("beta",5);
    pub_delta = n.advertise<std_msgs::Float64>("delta",5);
    pub_deltaf = n.advertise<std_msgs::Float64>("delta_abf",5);
    //pub_theta2 = n.advertise<std_msgs::Float64>("theta_lsm",1);
    ros::Rate loop_rate(28.2); //same freq that LSM uses

    while (ros::ok()){ 

    /*bag.open("theta_lsm.bag");  // BagMode is Read by default

    for(rosbag::MessageInstance const m: rosbag::View(bag))
    {
      th_lsm = m.instantiate<std_msgs::Float64>();
      if (th_lsm != nullptr)
        std::cout << th_lsm->data << std::endl;
    }#include <math.h> 

    bag.close();*/
    
    ///////Save THETA TO TXT ////////////

     /*myfile.open("/home/marzhan/catkin_ws/theta_hec.txt", std::ios_base::app);

        if (!myfile)
        {
              ROS_INFO("Txt cannot be opened");
        }
          myfile << th; 
          myfile << '\n';
          
     myfile.close();*/
    
    tf::StampedTransform transform;
    try{

    tf_listener_->waitForTransform( "scanmatcher_frame", "map", ros::Time(0), ros::Duration(1.0));
    tf_listener_->lookupTransform ( "scanmatcher_frame", "map", ros::Time(0), transform);
  }
  catch (tf::TransformException ex)
  {
    ROS_WARN("Could not get initial transform from map to base frame, %s", ex.what());
  }
        f2b_ = transform;
        ros::spinOnce();
        loop_rate.sleep();
    }

}

