import multiprocessing
import json

with open('wordledict.json') as f:
	wordleDicts = json.load(f)

dic5 = wordleDicts['answers']
#d5lset = dic5 + wordleDicts['guesses']

#d5lset = dic5 + wordleDicts['guesses']

#with open('words5.json') as f:
#    dic5 = json.load(f)

print(len(dic5))

import itertools

print 
patlst =[]
patdic = {}
cnt=0
for it in itertools.product('*og',repeat=5):
	patlst.append(''.join(it))
	patdic[''.join(it)]=cnt
	cnt+=1

import array

def evgs(wrd,guess):
	let={}
	for l in wrd:
		let[l] = let.get(l,0)+1
	res = ['*']*5
	nm=[]
	for k in range(5):  
		if guess[k]==wrd[k]:
			res[k] = 'g'
			let[guess[k]]-=1
		elif guess[k] in let:
			nm.append(k)
	for k in nm:
		if let[guess[k]]>0:
			res[k] = 'o'
			let[guess[k]]-=1 
		
	return patdic[''.join(res)]
	
ega=[]
for w in dic5:
	rd=array.array('B')
	for gu in dic5:
		p=evgs(w,gu)
		rd.append(p)
	ega.append(rd)

print('Done with evgs')


import math
def entropy(pdic):
	e=0.0
	t=0.0
	for p in pdic:
		w=len(pdic[p])
		if w>0:
			e += w*math.log(w,2)
			t += w
	return math.log(t,2) - e/t

wrdlu = {dic5[k]:k for k in range(len(dic5))}
allwrds = list(range(len(dic5)))

def fndopt(cdic,guesses):
	mxe=-1
	for gu in guesses:
		pdic2 = [0]*243
		for wrd in cdic:
			p = ega[wrd][gu]
			pdic2[p] += 1
		e = math.log(len(cdic)) - sum([pdic2[p]*math.log(pdic2[p]) for p in range(243) if pdic2[p]>0])/len(cdic)
		if e > mxe:
			mxe = e
			owrd = gu
	return owrd


guess=wrdlu['react']
gdic = [[] for k in range(243)]
for wrd in allwrds:
	gdic[ega[wrd][guess]] += [wrd]

bg1=[]
for g in gdic:
	if len(g)>0:
		bg1.append(fndopt(g,g+allwrds))
	else:
		bg1.append(-1)


def fndwrd(ans):
	if ans==guess:
		return 1
	apat=ega[ans][guess]
	gu = bg1[apat]
	cdic = gdic[apat]
	cnt=2
	while gu!=ans:
		apat = ega[ans][gu]
		cdic = [k for k in cdic if apat==ega[k][gu]]
		#print(gu,dic5[gu],len(cdic),patlst[apat])
		gu = fndopt(cdic,cdic+allwrds)
		cnt+=1
		
	if cnt==2 or cnt==6:
		print(ans,dic5[ans],cnt)
	return cnt

def mp_handler():
	p = multiprocessing.Pool(4)
	return p.map(fndwrd,range(len(dic5)))

"""
hist=[0]*7
for k in allwrds:
	hist[fndwrd(k)]+=1

for k in range(7):
	print(k,hist[k])


"""
if __name__ == '__main__':
	nguess = mp_handler()
	print(sum(nguess)/len(dic5))
	hist=[0]*7
	for n in nguess:
		hist[n]+=1
	for k in range(7):
		print(k,hist[k])
