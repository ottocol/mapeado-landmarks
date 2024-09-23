#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import math, rospy
from visualization_msgs.msg import Marker, MarkerArray
from sensor_msgs.msg import LaserScan
import tf2_ros
import tf2_geometry_msgs

def crear_marker(pos, id):
    marker = Marker()
    marker.header.frame_id = "map"  # Sistema de coordenadas de referencia
    marker.header.stamp = rospy.Time.now()
    marker.ns = "landmarks"  # Namespace
    marker.id = id  # Identificación única de cada marcador
    marker.type = Marker.SPHERE  # Tipo de marker (esfera para el landmark)
    marker.action = Marker.ADD
    # Posición del landmark
    marker.pose.position.x = pos[0]
    marker.pose.position.y = pos[1]
    marker.pose.position.z = pos[2]
    # Orientación del landmark
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    # Escala del marker (tamaño)
    marker.scale.x = 0.5
    marker.scale.y = 0.5
    marker.scale.z = 0.5
    # Color del marker (RGB + Alpha)
    marker.color.r = 1.0 
    marker.color.g = 1.0
    marker.color.b = 1.0
    marker.color.a = 1.0  # Transparencia
    # Duración (0 significa que será permanente)
    marker.lifetime = rospy.Duration(0)
    return marker

def callback_laser(msg):
    global tfBuffer
     
    #FALTA la parte en que se analizan las lecturas del laser para detectar los landmarks
    #esto imprime la lectura a mayor distancia, pero solo para ver cómo se trabaja con las lecturas
    masLejano = 0
    numRayos = len(msg.ranges)
    for index in range(0, numRayos):
        dist  = msg.ranges[index]
        if dist>masLejano:
            ang = msg.angle_min + index*msg.angle_increment
            lect_x = dist*math.cos(ang)
            lect_y = dist*math.sin(ang)
            masLejano = dist    
    # Este print (de Python 3) debería funcionar en Python 2 por el "from __future__ ..." del comienzo
    print('más lejano:', masLejano, ' x:', lect_x, ' y:', lect_y) 
    
    # crear y publicar el mapa con los landmarks. En ROS podemos representar un landmark con un Marker
    # un marker array no es más que una lista de landmarks
    marker_array = MarkerArray()
    # Definir posiciones para los landmarks. De momento son fijas
    # Tendréis que sacarlas de los datos del laser
    # ADEMÁS habrá que transformar las coordenadas de los landmark
    # que serán relativas al robot  ('base_laser_link') al sistema 'map'
    positions = [
        (2.0, 2.0, 0.0),
        (-2.0, 2.0, 0.0),
        (2.0, -2.0, 0.0),
        (-2.0, -2.0, 0-0)
    ]
    
    for i, pos in enumerate(positions):
        # Añadir el marcador al MarkerArray
        marker_array.markers.append(crear_marker(pos,i))

    # Publicar el MarkerArray
    marker_pub.publish(marker_array)


rospy.init_node('Mapeado_landmarks')
sub = rospy.Subscriber('/base_scan', LaserScan, callback_laser)
marker_pub = rospy.Publisher('/mapa_landmarks', MarkerArray, queue_size=10)
#el tfBuffer es el que nos servirá para transformar las coordenadas de un sistema a otro
tfBuffer = tf2_ros.Buffer()
# para que el tfBuffer funcione es necesario inicializar este listener aunque luego no lo usaremos directamente
listener = tf2_ros.TransformListener(tfBuffer)
rospy.spin()