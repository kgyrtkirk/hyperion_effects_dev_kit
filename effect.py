import hyperion, time, datetime
import math

n=hyperion.ledCount
u=18
v=11
maxIntensity=128

a=[]

#
#  0 x x x
#  x
#  x
#  0 x x x
def	ledDirs():
	pos=[]
	for i in range(hyperion.ledCount):
		l=i%(u+v)
		if l < u:
			x,y=l+1,0
		else:
			x,y=u+1,l-u +1
		
		if i>= u+v:
			x,y=1+u-x,1+v-y

		x,y=x,-y
		x-=(u+1)/2.0
		y+=(v+1)/2.0
		phi=math.atan2(x,y)
		if phi<0:
			phi+=2*math.pi
		phi/=2*math.pi
		#pos+=[[x,y]]
		pos+=[phi]
	return pos

pos=ledDirs()

def ringDist(a,b):
	if a>b:
		return ringDist(b,a)
	# a<b
	return min(b-a,a+1-b)

def dist2intensity(v,scale):
	return int(((1-v)**40) *scale* maxIntensity)

# effect loop
while not hyperion.abort():
	now = datetime.datetime.now()

	c = (now.second + now.microsecond/1e6) / 60.0
	b = (now.minute + c) / 60.0
	a = ((now.hour % 12) + b ) / 12.0
	led_data = bytearray()
	#print a

	for i in range(hyperion.ledCount):

		#off=(i/1.0/hyperion.ledCount+0/8.0)%1.0
		off=pos[i]
		dC = ringDist(off,c)
		dB = ringDist(off,b)
		dA = ringDist(off,a)
#		print off
#		print dA
		led_data += bytearray(( dist2intensity(dC,.3),dist2intensity(dB,.6),dist2intensity(dA,1) ))
		#led_data += bytearray(( dist2intensity(dC),int(0),int(0) ))
		#led_data += bytearray(( int((i*now.second)%255),int((i*now.second)%255),int((i*now.second)%255)))

	#bFill(led_data,hyperion.ledCount,c,0)

	hyperion.setColor(led_data)


	hyperion.setColor(led_data)
	time.sleep(0.1)
