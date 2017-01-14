default_entities = [
    {
        'id':          '0x1000',
        'description': 'The great and venerable you. How are the wife and kids?',
        'slug':        'entity_player',
        'type':        'player',
        'meta': { 'health': 100 }
    },
    {
        'id':          '0x1001',
        'description': 'The air feels somehow less substantial here. Say, do you remember feeling this light?',
        'slug':        'entity_portal',
        'type':        'portal'
    },
    {
        'id':          '0x2000',
        'name':        'Primordial Ooze',
        'description': 'Sluggish beastie. Nasty things.',
        'slug':        'entity_enemy_slime',
        'type':        'enemy',
        'events':       {
            'enter': '__log("HELLO I AM A SLIME! Here is my ID:" + $this.id); __log("Player location: " + $entity_nearest_player.location.x + ", " + $entity_nearest_player.location.y); __log("Nearest enemy that isn\'t me: " + $entity_nearest_enemy.location.x + ", " + $entity_nearest_enemy.location.y);',
            'timestep': 'var player=$entity_nearest_player;var self=$this;var playerNearby=(__distance(player.location,self.location)<6);if(playerNearby){self.meta.chaseDistance=self.meta.chaseDistance||0;self.meta.roamProgress=0;self.meta.roamDistance=0;self.meta.roamPath=[];if(self.meta.chaseDistance%2==0){var newLocation=__moveTo({\'location\':self.location,\'target\':player.location});if(newLocation[0]!==undefined){self.location.x=newLocation[0].x;self.location.y=newLocation[0].y}}self.meta.chaseDistance=self.meta.chaseDistance+1}else{self.meta.chaseDistance=0;self.meta.roamProgress=self.meta.roamProgress||0;self.meta.roamDistance=self.meta.roamDistance||[];self.meta.roamPath=self.meta.roamPath||[];if((self.meta.roamProgress+1)>(self.meta.roamPath.length-1)){self.meta.roamProgress=0;self.meta.roamDistance=0;var isObstacle=true;var targetLocation;while(isObstacle){targetLocation={\'x\':self.location.x-__rand(-10,10),\'y\':self.location.y-__rand(-10,10)};if(!__isObstacle(targetLocation)){if(__distance(self.location,targetLocation)>2){isObstacle=false}}}self.meta.targetLocation=targetLocation;self.meta.roamPath=__moveTo({\'location\':self.location,\'target\':targetLocation})}var newLocation=self.meta.roamPath[self.meta.roamProgress];self.meta.roamDistance=self.meta.roamDistance+0.7;self.meta.roamProgress=Math.floor(self.meta.roamDistance);if(newLocation!==undefined){self.location.x=newLocation.x;self.location.y=newLocation.y}}'
        },
        'meta':        {}
    },
    {
        'id':          '0x3000',
        'description': 'Ah, the classic three-timber dungeon door. Generic, but quite homely. You can\'t deny that it has an almost...adoorable look to it.',
        'slug':        'entity_door',
        'type':        'door',
        'meta':        { 'locked': False }
    },
    {
        'id':          '0x3001',
        'description': 'Look, a train! ...Ha! Chest kidding.',
        'slug':        'entity_chest',
        'type':        'chest',
        'meta':        { 'locked': False }
    }
]
