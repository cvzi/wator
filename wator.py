"""

Stable:

config = {'predator': 141,
          'prey': 596,
          'gestation_predator': 10,
          'gestation_prey': 3,
          'starve_predator': 3,
          'width' : 32,
          'height' : 32,
          'showPlot' : True,
          'showText' : False }


"""

config = {
          'days' : 100,
          'predator': 50,
          'prey': 200,
          'gestation_predator': 10,
          'gestation_prey': 3,
          'starve_predator': 3,
          'width' : 32,
          'height' : 32,
          'showPlot' : True,            # Show plot
          'showRelativePlot' : True,    # Show relative plot
          'showText' : True,            # Show the evolution on the field
          'usetoxin' : False            # Kill have the population after 50 days
          }



"""#######################################################"""



import random,time,os


def cls(i=0):
     if not i == 0:
          time.sleep(i)
     #os.system('CLS')
class animal:
     def __init__(self,type,energy,gesture=1):
         self.type = type # 1 == predator, 2 == prey
         self.gesture = gesture
         self.energy = energy
         self.hunger = 0
     def t(self):
         return '0' if self.type == 2 else '+'


class simulation:
    # config
    age = 0
    global config

    #parameters
    initialValue_predator = config['predator']
    initialValue_prey = config['prey']
    initialValue_gestation_predator = config['gestation_predator']
    initialValue_gestation_prey = config['gestation_prey']
    initialValue_starve_predator = config['starve_predator']
    initialValue_width = config['width']
    initialValue_height = config['height']
    initialValue_gesture = 1



    # Create Field with '0' values
    field = list()
    for y in range(0,initialValue_height):
        field.append( list() )
        for x in range(0,initialValue_width):
            field[y].append( 0 )

    max_width = initialValue_width - 1
    max_height = initialValue_height - 1

    # Spill predators
    for i in range(0,initialValue_predator):
        x = random.randint(0, max_width)
        y = random.randint(0, max_height)
        while not field[y][x] == 0:
            x = random.randint(0, max_width)
            y = random.randint(0, max_height)
        gesture = 1
        energie = 1
        field[y][x] = animal(1,energie,gesture)

    # Spill prey
    for i in range(0,initialValue_prey):
        x = random.randint(0, max_width)
        y = random.randint(0, max_height)
        while not field[y][x] == 0:
            x = random.randint(0, max_width)
            y = random.randint(0, max_height)
        gesture = 1
        energie = 1
        field[y][x] = animal(2,energie,gesture)


    def move(self,field,x,y):
            re = self.findNextField(x,y)
            nx = re[0]
            ny = re[1]
            if x == nx and y == ny:
                 #nothing happends, no field empty
                 dummy = 1
            elif self.field[ny][nx] == 0:
                 self.field[ny][nx] = self.field[y][x]
                 self.field[y][x] == 0
                 if self.field[ny][nx].type == 1:
                      self.field[ny][nx].hunger += 1
                 else:
                      self.field[ny][nx].energy += 1
            elif self.field[ny][nx].type == 2 and field.type == 1:
                 self.field[y][x].energy += self.field[ny][nx].energy
                 self.field[ny][nx] = self.field[y][x]
                 self.field[y][x] == 0
            elif self.field[ny][nx].type  == 1 and field.type == 2:
                 self.field[ny][nx].energy += self.field[y][x].energy
                 self.field[y][x] = self.field[ny][nx]
                 self.field[ny][nx] == 0
            return nx,ny

    def findNextField(self,x,y):

        #get the four possible fields:
        width = self.initialValue_width - 1
        height = self.initialValue_height - 1

        if self.field[y][x] == 0:
             type = 0
        else:
             type = self.field[y][x].type

        doable_fields = list()

        tmp_y = y-1 if y-1 >= 0 else height
        north = self.field[tmp_y][x]
        north_xy = (x,tmp_y)
        if north == 0:
             doable_fields.append(north_xy)
        elif not north.type == type:
             doable_fields.append(north_xy)

        tmp_x = x+1 if x+1 < width else 0
        east = self.field[y][tmp_x];
        east_xy = (tmp_x,y)
        if east == 0:
             doable_fields.append(east_xy)
        elif not east.type == type:
             doable_fields.append(east_xy)

        tmp_y = y+1 if y+1 < height else 0
        south = self.field[tmp_y][x]
        south_xy = (x,tmp_y)
        if south == 0:
             doable_fields.append(south_xy)
        elif not south.type == type:
             doable_fields.append(south_xy)

        tmp_x = x-1 if x-1 >= 0 else width
        west = self.field[y][tmp_x];
        west_xy = (tmp_x,y)
        if west == 0:
             doable_fields.append(west_xy)
        elif not west.type == type:
             doable_fields.append(west_xy)

        found = False

        if type == 1:
             # Predator goes to prey
             for i in doable_fields:
                  f = self.field[ i[0] ][ i[1] ]
                  if not f == 0:
                       if f.type == 2:
                            found = [i[0],i[1]]
                            break

        #Random field
        if found == False and len(doable_fields)-1 != -1:
             r = random.randint(0, len(doable_fields)-1)
             found = doable_fields[r]
        elif found == False:
             found = [x,y]
        return found

    def createJuvenile(self,field,x,y,nx,ny):
        half = int(field.energy / 2)
        self.field[y][x] = animal(field.type,half)
        self.field[ny][nx].energy = half
        self.field[ny][nx].gesture = 1

    def kill(self,x,y):
        self.field[y][x] = 0


    def tick(self):
        x = 0
        y = 0
        for row in self.field:
            for field in row:
                if not field == 0:
                    field.gesture += 1

                    # deserves to die?
                    if field.hunger > self.initialValue_starve_predator:
                        self.kill(x,y)

                    if not self.field[y][x] == 0: # if not dead
                         # move
                         nx,ny = self.move(field,x,y)

                         # childbirth?
                         if field.type == 1 and field.gesture >= self.initialValue_gestation_predator:
                              self.createJuvenile(field,x,y,nx,ny)
                         elif field.type == 2 and field.gesture >= self.initialValue_gestation_prey:
                              self.createJuvenile(field,x,y,nx,ny)


                x += 1
            y += 1
            x = 0
        self.age += 1
        return self.age


    def getStats(self):
        predators = 0
        prey = 0
        for row in self.field:
            for field in row:
                if not field == 0:
                    if field.type == 1:
                        predators += 1
                    elif field.type == 2:
                        prey +=1
        return [self.age,predators,prey]


    def implantToxin(self,every):
        x = 0
        y = 0
        for row in self.field:
            for field in row:
                if not field == 0:
                    if random.randint(0, every) == 0:
                        self.kill(x,y)
                x += 1
            y += 1
            x = 0

print 'Calculate simulation'

simu = simulation()

showText = config['showText']
showPlot = config['showPlot']
showRelativePlot = config['showRelativePlot']
usetoxin = config['usetoxin']
days = config['days']

stats = list()
screens = list()
i = 0
for x in range(0,days):
    if showPlot or showRelativePlot:
         stats.append( simu.getStats() )
    print simu.tick()

    cls()
    if (showText):
         res = ''
         for a in simu.field:
              for b in a:
                   if b == 0:
                        res += ' '
                   else:
                        res += b.t()
              res += '\n'
         screens.append(res)
    if usetoxin and i == 50:
         simu.implantToxin(2)
         print 'setToxin'
    i += 1

if showText:
     print '\nShow field:'
     raw_input('Press Enter');
     i = 0
     for a in screens:
          cls(0.1)
          print i,'\n',a,'\n'
          i += 1



if showPlot:
     print '\nShow absolute plot'
     raw_input('Press Enter');
     # absolute Plot
     age = list()
     predator = list()
     prey = list()
     for a in stats:
          age.append(a[0])
          predator.append(a[1])
          prey.append(a[2])
     from pylab import *
     plot(age,prey,label='Prey',linewidth=2)
     x = plot(age,predator,label='Predator',linewidth=2)
     legend()
     show()

if showRelativePlot:
     print '\nShow relative plot'
     raw_input('Press Enter');

     # relative Plot


     # first find average level
     total_predator = 0
     total_prey = 0
     for a in stats:
          total_predator += a[1]
          total_prey += a[2]

     quotient_predator = (total_predator / float(days)) / 100.0
     quotient_prey = (total_prey / float(days)) / 100.0


     age = list()
     predator = list()
     prey = list()
     for a in stats:
          age.append(a[0])
          predator.append(a[1] / quotient_predator)
          prey.append(a[2] / quotient_prey)
     from pylab import *
     plot(age,prey,label='Prey',linewidth=2)
     x = plot(age,predator,label='Predator',linewidth=2)
     legend()
     show()

print 'End.'



