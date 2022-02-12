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
def fndopt(initguess):
	pguess={}
	pdic = [[] for k in range(243)]
	for wk in range(len(dic5)):
		p = ega[wk][initguess]
		pdic[p].append(wk)
	pdicl = [(p,len(pdic[p])) for p in range(243)]
	pdicl.sort(key = lambda x:-x[1])
	if pdicl[0][1]<len(dic5)/10:
		print(initguess,dic5[initguess],[(patlst[p],c) for p,c in pdicl[:5]])
	#Step thru the 10 most common patterns for this initial guess
	sm=0.0
	for pat,c in pdicl[:10]:
		cdic = pdic[pat]
		sm += len(cdic)
		mxe=0
		for guk2 in range(len(dic5)):
			pdic2 = [0]*243
			for wrd in cdic:
				p = ega[wrd][guk2]
				pdic2[p] += 1
			e = math.log(len(cdic)) - sum([pdic2[p]*math.log(pdic2[p]) for p in range(243) if pdic2[p]>0])/len(cdic)
			if e > mxe:
				mxe = e
				owrd = dic5[guk2]
		pguess[patlst[pat]] = owrd
		#print(gu,pat,owrd,len(cdic),sm/len(dic5))
	return pguess
 
 
def mp_handler():
	p = multiprocessing.Pool(4)
	return p.map(fndopt,range(len(dic5)))
 
if __name__ == '__main__':
	bst = mp_handler()
	bstguess= {dic5[k]:bst[k] for k in range(len(bst))}
	print(bstguess['raise'])
	#with open('bstguess.json', 'w') as f:
	#   json.dump(bstguess, f)
