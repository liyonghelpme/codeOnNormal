power = [0, 0, 0, 0]
myPow = raw_read('myPow')
enePow = raw_read('enepow')
myPurePow = raw_read('my pure power')
enePurePow = raw_read('ene pure power')
att = raw_read('att')

myPow = int(myPow)
enePow = int(enePow)
myPurePow = int(myPurePow)
enePurePow = int(enePurePow)
att = int(att)
#attack suc fail
attackLost = [[40, 50, 70, 90], [15, 20, 20, 20]]
defenceLost = [[35, 35, 35, 35], [20, 30, 45, 45]]

if myPow > enePow:
    power[0] = myPow
    power[1] = enePow
    power[2] = myPurePow
    power[3] = enePurePow
else:
    power[0] = enePow
    power[1] = myPow
    power[2] = myPurePow
    power[3] = enePurePow
res = 0 #attack suc=def fail att fail1 = def suc3 % 2
if myPow < enePow
    att = (att+1)%2
#defence suc
#0 att suc 1 def suc
#0->1   1->0
#who won
if power[0] <= 2*power[1]:
    situation = 0
elif power[0] <= 10*power[1]:
    situation = 1
elif power[0] <= 100*power[1]:
    situation = 2
else
    situation = 3
won = 0
#attack won or defence
lost = [0, 0]
    lost[att] = int((power[1+att]*attackLost[][situation]+attackLost[0][situation]-1)/100)
    lost[1] = int((power[2]*defenceLost[0][situation]+defenceLost[0][situation]-1)/100)

