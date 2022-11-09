First Assignment of Research Track I
================================

The idea is to search and choose the closest silver box in the enviroment, then the robot put that block close to the closest golden box to it. Getting the boxes distributed in pairs at the end.

Installing and running
----------------------

The assignment run on a simulator that requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

To run it:
```bash
$ python2 run.py assignment.py
```

How works
----------------------
At the start the robot revolves around itself to search, mesaure and save every block he can see. Then it choose the closest silver box and go to reach it. After reached the closest silver box, the robot grabs the block and go to reach the closest gold one to pair them. 
To kown the correct distance during its job, the robot measure and save any block it see while moving around the map. 

## Pseudocode

```
discover(silver_list :list(), gold_list : list())
        do the robot revolves around itself
        markers <- markers seen by robot at that time
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
        int i <- contains(list, m)
        if( i != -1) Then
                list(i).dist <- m.dist
                list(i).rot_y <- m.rot_y

disable_token(list :list(), code :int)
        int i <- contains(list, m)
        list.removeAt(i)

contains(list :list(), code :int) :int 
        int i <- 0
        foreach marker in list
                i <- i + 1
                if(marker.code == code) Then
                        return i
        return -1
        
reach_block_code(code :int, type :string, last_rot_y :int ,m_dst :int,silver_list :list(), gold_list : list())
        int dst <- 0
        int rot_y <- 0
        while(dst == 0)
                if(last_rot_y < -a_th) Then
                        turn left
                ELse 
                        turn right
                if(last_rot_y == 0)
                        turn right
                markers <- markers seen by robot at that time
                foreach marker in markers
                        if(marker.info.code == code AND m.info.type == type) Then
                                dist <- m.dist
                                rot_y <- m.rot_y
                        if(marker.info.type == "gold-token") Then
                                update_distance(gold_list, m)
                        else
                                update_distance(silver_list, m)
        foreach marker in markers 
                if(marker.info.code == code AND m.info.type == type) Then
                        dist <- m.dist
                        rot_y <- m.rot_y
                        while(dist < m_dst)
                                if(-a_th<= rot_y <= a_th) Then
                                        go straight
                                else if(rot_y < -a_th) Then
                                        turn left
                                else
                                        turn right
                                markers <- markers seen by robot at that time
                                        if(marker.info.code == code AND m.info.type == type) Then
                                                rot_y = m.rot_y	
						dist = m.dist	
                                        else
                                                if(marker.info.type == "gold-token") Then
                                                        update_distance(gold_list, m)
                                                else
                                                        update_distance(silver_list, m)
                                                
gold_tokens <- list()
silver_tokens <- list()
discover(silver_tokens, gold_tokens)
while(len(gold_tokens) + len(silver_tokens) > 0)
	get code and last_rot_y from chose_closer_token(silver_tokens)
	reach_block_code(code, "silver-token" , last_rot_y, d_th, silver_tokens, gold_tokens)
	grab the block
	disable_token(silver_tokens, code)
	get code and last_rot_y from chose_closer_token(gold_tokens)
	reach_block_code(code, "gold-token" , last_rot_y, 1.5*d_th, silver_tokens, gold_tokens)
	release the block
	disable_token(gold_tokens, code)	
	go back for a while 
        
```
Possible Improvement
----------------------
A possible improvement could be the implementation of record new blocks during the job.        
        
