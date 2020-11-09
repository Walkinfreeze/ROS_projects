;; Auto-generated. Do not edit!


(when (boundp 'laser_scan_matcher::Num)
  (if (not (find-package "LASER_SCAN_MATCHER"))
    (make-package "LASER_SCAN_MATCHER"))
  (shadow 'Num (find-package "LASER_SCAN_MATCHER")))
(unless (find-package "LASER_SCAN_MATCHER::NUM")
  (make-package "LASER_SCAN_MATCHER::NUM"))

(in-package "ROS")
;;//! \htmlinclude Num.msg.html


(defclass laser_scan_matcher::Num
  :super ros::object
  :slots (_num ))

(defmethod laser_scan_matcher::Num
  (:init
   (&key
    ((:num __num) 0.0)
    )
   (send-super :init)
   (setq _num (float __num))
   self)
  (:num
   (&optional __num)
   (if __num (setq _num __num)) _num)
  (:serialization-length
   ()
   (+
    ;; float64 _num
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _num
       (sys::poke _num (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _num
     (setq _num (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get laser_scan_matcher::Num :md5sum-) "f942a3e0cbd340847b2a0e5b31a783fe")
(setf (get laser_scan_matcher::Num :datatype-) "laser_scan_matcher/Num")
(setf (get laser_scan_matcher::Num :definition-)
      "float64 num

")



(provide :laser_scan_matcher/Num "f942a3e0cbd340847b2a0e5b31a783fe")


