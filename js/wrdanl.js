var toggler = document.getElementsByTagName('td');
var i;
var curPos=0
var r1Hst;
var colorMap={'*':"404040",'o':"CCCC00",'g':"009900"}
toggler[curPos].style.color="red";

function getWrd(row) {
	var st=""
	for(var i=0;i<5;i++){
		st = st + toggler[row*5+i].innerHTML.toLowerCase();
	}
	return st
}

function setWrd(row,wrd) {
	if (!wrd)
		wrd = "-----"
	for(var i=0;i<5;i++){
		toggler[row*5+i].innerHTML=wrd[i].toUpperCase();
	}
}

function setPat(row,pat) {
	if (!pat)
		pat = "*****"
	for(var i=0;i<5;i++){
		toggler[row*5+i].bgColor=colormap[pat[i]];
	}
}


function getPat(row) {
	var st=""
	for(var i=0;i<5;i++){
		if (toggler[row*5+i].bgColor=="404040")
			st = st + "*";
		else if (toggler[row*5+i].bgColor=="CCCC00")
			st = st + "o";
		else
			st = st + 'g';
	}
	return st
}

function logKey(e) {
	// console.log(e.key);
	toggler[curPos].innerHTML = e.key.toUpperCase();
	toggler[curPos].style.color="white";
	curPos = curPos + 1;
	if (curPos==5) {
		// console.log(getWrd(0),getPat(0),bstGuess[getWrd(0)][getPat(0)]);
		r1Hst=wrdhst(getWrd(0),ansDict);
		setWrd(1,bstGuess[getWrd(0)][getPat(0)]);
	}
	if (curPos==30) curPos=0;
	toggler[curPos].style.color="red";
}

document.onkeypress=logKey;

for (i = 0; i < toggler.length; i++) {
  toggler[i].cid = i
  toggler[i].addEventListener("click", function() {
	//   console.log(parseInt(this.cid/5),this.cid%5);
	if (curPos!=this.cid) {
		toggler[curPos].style.color="white";
		curPos=this.cid;
		this.style.color="red"
	}
	else {
	  if (this.bgColor==="404040") this.bgColor="CCCC00";
	  else if (this.bgColor==="CCCC00") this.bgColor="009900";
	  else this.bgColor="404040";
	  if (this.cid<5) {
		var wrd=getWrd(0)
		var pat=getPat(0)
		if ((wrd in bstGuess) && !(pat in bstGuess[wrd]))
			bstGuess[wrd][pat]=optguess(ansDict,r1Hst[pat]);
	  	setWrd(1,bstGuess[wrd][pat])
	  }
	} 
  });
}

function evgs(wrd,guess) {
	var letr = [...wrd].reduce((a, e) => { a[e] = a[e] ? a[e] + 1 : 1; return a }, {});
	var res =['*','*','*','*','*'];
	var uas = [];

	for(var k=0;k<5;k++) 
		if (wrd.charAt(k)==guess.charAt(k)) {
			res[k]='g';
			letr[wrd[k]] -=1;
		}
		else if (wrd.includes(guess.charAt(k)))
			uas.push(k)
	for(const k of uas)
		if (letr[guess.charAt(k)]>0) {
			res[k]='o';
			letr[guess.charAt(k)]-=1;
		}
	return res.join('');
}

function wrdhst(guess,dict) {
	var res = {}
	for(const wrd in dict) {
		p=evgs(dict[wrd],guess);
		if (p in res)
			res[p].push(dict[wrd]);
		else
			res[p]=[dict[wrd]];
	}
	return res
}

function mxHst(hist) {
	mx=0
	var res=""
	for(const pat in hist)
		if (hist[pat].length>mx) {
			mx=hist[pat].length;
			res=pat;
		}
	return res
}


function cnthst(guess,dict) {
	var res = {}
	for(const wrd in dict) {
		p=evgs(dict[wrd],guess);
		if (p in res)
			res[p]+=1;
		else
			res[p]=1;
	}
	return res
}


function entropy(hst) {
	var res=0.0
	var tl=0
	var le=0
	for(const pat in hst){
		le = Array.isArray(hst[pat]) ? hst[pat].length() : hst[pat];
		res += le*Math.log2(le);
		tl += le;
	}
	return Math.log2(tl) - res/tl;
}

function optguess(guesses,dict) {
	mxe=0
	bstWord=""
	for(const gu in guesses){
		e = entropy(cnthst(guesses[gu],dict));
		if (e>mxe) {
			mxe=e;
			bstWord=guesses[gu];
		}
	}
	return bstWord;
}