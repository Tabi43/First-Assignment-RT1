First Assignment of Research Track I
================================

This is my solution of the first Reaserach Track's Assignment. I tried to obtain a general high effincency solution for this job, in fact the idea is to search and choose the **closest** silver box in the enviroment, then it must put that block close to the **closest** golden box. Having at the end the boxes distributed in pairs.

How works
----------------------
At the start the robot revolves around itself to search, mesaure and save every block he can see. Then it choose the closest silver box and go to reach it. After reached the closest silver box, it grabs it and go to reach the closest gold one to pair them. 
To kown the corrects distance during its job, the robot measure and save any block it see while moving around the map. 

## Pseudocode

```
discover(silver_list :list(), gold_list : list())
        do the robot revolves around itself
        markers = markers seen by robot at that time
        for each markers
                code <- marker code
                color <- markers color 
                distance <- marker distance from the robot
                rotation <- marker rotation relative to the robot
                if (NOT gold_marker_list.contains(code)) AND color = 'gold' then
                        token <- (code, distance, rotation)
                        gold_marker_list.add(token)
                if (NOT silver_marker_list.contains(code)) AND color = 'silver' then
                        token <- (code, distance, rotation)
                        silver_marker_list.add(token)

chose_closest_token(color_marker_list: list()): (int, int)
        min_dst <- 0
        rotation <- 0
        for each markers in color_marker_list
                if (marker.distance < min_dts OR min_dst = 0) Then
                        choose that marker
                        min_dst <- marker.distance
                         rotation <- marker rotation relative to the robot
        return marker.code, rotation  

update_distance(list :list(), m :marker)
        
```          
              
              
        
