
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
		
	return ''.join(res)

import math
def entropy(pdic):
	e=0.0
	t=0.0
	for p in pdic:
		w=len(pdic[p])
		e += w*math.log(w,2)
		t += w
	return math.log(t,2) - e/t


	
def fndopt(initguess):
	pguess={}
	pdic = {}
	for wrd in dic5:
		p = evgs(wrd,initguess)
		pdic[p] = pdic.get(p,[])+[wrd]
	pdicl = [(p,len(pdic[p])) for p in pdic]
	pdicl.sort(key = lambda x:-x[1])
	if pdicl[0][1]<250:
		print(initguess,pdicl[:3])
	#Step thru the 10 most common patterns for this initial guess
	sm=0.0
	for pat,c in pdicl[:10]:
		cdic = pdic[pat]
		sm += len(cdic)
		mxe=0
		for gu2 in dic5:
			pdic2 = {}
			for wrd in cdic:
				p = evgs(wrd,gu2)
				pdic2[p] = pdic2.get(p,0)+1
			e = math.log(len(cdic)) - sum([pdic2[p]*math.log(pdic2[p]) for p in pdic2])/len(cdic)
			if e > mxe:
				mxe = e
				owrd = gu2
		pguess[pat] = owrd
		#print(gu,pat,owrd,len(cdic),sm/len(dic5))
	return pguess


def mp_handler():
	p = multiprocessing.Pool(4)
	return p.map(fndopt,dic5)

if __name__ == '__main__':
	bst = mp_handler()
	bstguess= {dic5[k]:bst[k] for k in range(len(bst))}
	with open('bstguess.json', 'w') as f:
		json.dump(bstguess, f)
