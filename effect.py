import hyperion, time, datetime


n=hyperion.ledCount


def bFill(data,n,x,ch):
	i0=int(x*n)
	i1=(i0+1)%n
	t1=(x*n-i0)
	t0=1-t1
	print i0
	data[3*i0+ch]=int(t0*255);
	data[3*i1+ch]=int(t1*255);

def ringDist(a,b):
	if a>b:
		return ringDist(b,a)
	# a<b
	return min(b-a,a+1-b)

def dist2intensity(v):
	return int((1-v)**16 * 255)

# effect loop
while not hyperion.abort():
	now = datetime.datetime.now()

	c = (now.second + now.microsecond/1e6) / 60.0
	b = (now.minute + c) / 60.0
	a = ((now.hour % 12) + 0 ) / 12.0
	a=0
	led_data = bytearray()
	print a

	for i in range(hyperion.ledCount):
		off=(i/1.0/hyperion.ledCount+0/8.0)%1.0
		dC = ringDist(off,c)
		dB = ringDist(off,b)
		dA = ringDist(off,a)
		#led_data += bytearray(( dist2intensity(dC),dist2intensity(dB),dist2intensity(dA) ))
		led_data += bytearray(( dist2intensity(dA),int(0),int(0) ))
		#led_data += bytearray(( int((i*now.second)%255),int((i*now.second)%255),int((i*now.second)%255)))

	#bFill(led_data,hyperion.ledCount,c,0)

	hyperion.setColor(led_data)


	hyperion.setColor(led_data)
	time.sleep(0.2)
