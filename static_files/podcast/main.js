// podcast info objects
let playlist = {};
let tag_class = {};
let class_tag = {};
// DOM elements
let titleH1DOM = document.getElementById("titleH1");
let titleSpanDOM = document.getElementById("titleSpan");
let tagIndexDOM = document.getElementById("tagindex");
let indexBarDOM = document.getElementById("indexbar");
let unionSDOM = document.getElementById("unionSpan");
let tagADOM = document.getElementById("tagA");
let tagIDOM = document.getElementById("tagI");
let sortIDOM = document.getElementById("sortI");
let sortADOM = document.getElementById("sortA");
let sortMDOM = document.getElementById("sortM");
let moreIDOM = document.getElementById("moreI");
let colourIDOM = document.getElementById("colourI");
let colourADOM = document.getElementById("colourA");
let colourMDOM = document.getElementById("colourM");
let contraIDOM = document.getElementById("contraI");
let contraADOM = document.getElementById("contraA");
let contraMDOM = document.getElementById("contraM");
let tagBarDOM = document.getElementById("tagbar");
let tagListDOM = document.getElementById("taglist");
let shareRsDivDOM = document.getElementById("shareResultDiv");
let shareRsADOM = document.getElementById("shareResultA");
let shareLinkDOM = document.getElementById("shareLink");
let shareTagDOM = document.getElementById("shareTag");
let shareEpiDOM = document.getElementById("shareEpi");
let shareCutDOM = document.getElementById("shareCuT");
let tagSpanDOM = document.getElementById("tagSpan");
let cuTSpanDOM = document.getElementById("cuTSpan");
let shareContentDOM = document.getElementById("share_content");
let tagNoteDOM = document.getElementById("tagnote");
let trackTitleDOM = document.getElementById("tracktitle");
let morePageDOM = document.getElementById("morePage");
let epiListDOM = document.getElementById("playlistContain");
let playlistDOM = document.getElementById("playlist");
let detailPgDOM = document.getElementById("detailContain");
let playerDOM = document.getElementById("player");
let playerBarDOM = document.getElementById("playerbar");
let playBTN = document.getElementById("playBtn");
let pauseBTN = document.getElementById("pauseBtn");
let moveBTN = document.getElementById('movebtn');
let seekerDOM = document.getElementById("seeker");
let currentDOM = document.getElementById("currentTime");
let sliderDOM = document.getElementById("slider");
let totalDOM = document.getElementById("totalTimer");
let popADOM = document.getElementById("popA");
let popPipDOM = document.getElementById("popPiP");
let canvasDOM = document.createElement('canvas');
let videoDOM = document.createElement('video');
let contentDOM = document.getElementById("contentdiv");

let satPropertyValue = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sat"), 10);
let sarPropertyValue = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sar"), 10);
let sabPropertyValue = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sab"), 10);
let salPropertyValue = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sal"), 10);
let safeAreaInsetTop    = isNaN(satPropertyValue)? 0 : satPropertyValue;
let safeAreaInsetRight  = isNaN(sarPropertyValue)? 0 : sarPropertyValue;
let safeAreaInsetBottom = isNaN(sabPropertyValue)? 0 : sabPropertyValue;
let safeAreaInsetLeft   = isNaN(salPropertyValue)? 0 : salPropertyValue;
let permUpperTop = safeAreaInsetTop + remToPx(0.5);
let permUpperLeft = safeAreaInsetLeft + remToPx(0.5);
let permLowerTop = window.innerHeight - playerBarDOM.offsetHeight - safeAreaInsetBottom - remToPx(0.5);
let permLowerLeft = window.innerWidth - playerBarDOM.offsetWidth - safeAreaInsetRight - remToPx(0.5);
let storeTop = 0;
let storeLeft = 0;
let moveTop = 0;
let moveLeft = 0;
let newTop = 0;
let newLeft = 0;

// Local storage
let storage = window.localStorage;

// Fontawesome strings
let faTagStr = "fa-solid fa-tag fa-fw";
let selectedStr = "fa-solid fa-circle-check fa-fw";
let playingStr = "fa-solid fa-circle-play fa-fw"; // fa-spin fa-fw";
let pausedStr = "fa-solid fa-circle-pause fa-fw";
let stopStr = "fa-solid fa-circle-stop fa-fw";
let unionToggleOnStr = "fa-solid fa-toggle-on fa-fw";
let unionToggleOffStr = "fa-solid fa-toggle-off fa-fw";
let tagUpStr = "fa-solid fa-square-caret-up fa-fw";
let tagDownStr = "fa-solid fa-tags fa-fw";
let moreUpStr = "fa-solid fa-square-minus fa-fw";
let moreDownStr = "fa-solid fa-bars fa-fw";
let sortFaStr = "fa-solid fa-sort fa-fw";
let sortNewStr = "fa-solid fa-arrow-up-1-9 fa-fw";
let sortOldStr = "fa-solid fa-arrow-down-1-9 fa-fw";
let contrastOnStr = "fa-solid fa-circle-half-stroke fa-fw";
let contrastOffStr = "fa-solid fa-circle-half-stroke fa-fw fa-flip-horizontal";
let neutralColourStr = "fa-solid fa-cloud fa-fw";
let lightColourStr = "fa-solid fa-sun fa-fw";
let darkColourStr = "fa-solid fa-moon fa-fw";

// Default parameters
let sectionObj = {
"titlebar":{"pos":0,"dom":titleH1DOM,"on":"min-content"},
"more_option":{"pos":1,"dom":morePageDOM,"on":"1fr"},
"tags_list":{"pos":2,"dom":tagIndexDOM,"on":"1fr"},
"selected_tags":{"pos":3,"dom":tagBarDOM,"on":"min-content"},
"episodes_list":{"pos":4,"dom":epiListDOM,"on":"1fr"},
"episode_detail":{"pos":5,"dom":detailPgDOM,"on":"1fr"},
"player":{"pos":6,"dom":playerBarDOM,"on":"min-content"},
"audio":{"pos":7,"dom":playerDOM,"on":"0px"}
};
let themeObj = {"colour":0,"contrast":1};
let paramObj = {
"sort":{
"neutral":{"text":"排序","class":sortFaStr,"next":"oldest"},
"oldest":{"text":"最舊","class":sortOldStr,"next":"newest"},
"newest":{"text":"最新","class":sortNewStr,"next":"neutral"},
},
"colour":{
"position":0,
"neutral":{"text":"預設晝夜","class":neutralColourStr,"next":"light"},
"light":{"text":"白晝主題","class":lightColourStr,"next":"dark"},
"dark":{"text":"黑夜主題","class":darkColourStr,"next":"neutral"},
},
"contrast":{
"position":1,
"lowContrast":{"text":"低對比度","class":contrastOffStr,"next":"highContrast"},
"highContrast":{"text":"高對比度","class":contrastOnStr,"next":"lowContrast"},
},
};

let actionHandlers = [
['play' ,async () => {mixPlay();}],
['pause' ,() => {mixPause(); }],
['previoustrack',async () => {doPrev(); }],
['nexttrack' ,async () => {doNext(); }],
['stop' ,null ],
['seekbackward' ,(details) => {seakBack(details); }],
['seekforward' ,(details) => {seakForw(details); }],
['seekto' ,(details) => {seakGoTo(details); }],
];

// get option from url and save to local storage
let url = new URL(window.location.href);
let argueObj = new Object();

for (const [key,value] of url.searchParams.entries()) {
if (value.includes(",")) {
valueOriArr = value.split(",");
valueArr = Array();
for (let i = 0; i < valueOriArr.length; i++) {
(valueOriArr[i]=="")||valueArr.push(valueOriArr[i]);
}
argueObj[key] = valueArr;
} else if (value != "") {
argueObj[key] = [value];
};
};

let argueKey = Object.keys(argueObj);
let defaultObj = {"key":[],"now":"","currentTS":"","union":"false","sort":"neutral","colour":"neutral","contrast":"highContrast"};
let optionObj = {"key":[],"now":"","currentTS":"","union":"false","sort":"neutral","colour":"neutral","contrast":"highContrast"};
let optionKey = Object.keys(optionObj);

for (var ark = 0; ark < argueKey.length; ++ark) {
var key = argueKey[ark];
if (optionKey.includes(key)) {
var value = argueObj[key];
optionObj[key] = (key=="key")?value:value[0];
};
};

((optionObj["now"]!="")&&(optionObj["currentTS"]=="")&&storage.getItem(`${channel}_currentTS`))&&storage.setItem(`${channel}_currentTS`,"");

for (var opt = 0; opt < optionKey.length; ++opt) {
var key = optionKey[opt];
if (argueObj["do"]&&argueObj["do"][0]=="reset") {
optionObj[key]=defaultObj[key];
storage.setItem(`${channel}_${key}`,optionObj[key]);
} else {
var optionValue = (key=="key")?optionObj[key].join(","):optionObj[key];
var defaultValue = (key=="key")?"":defaultObj[key];
(optionValue==defaultValue)?((storage.getItem(`${channel}_${key}`))||storage.setItem(`${channel}_${key}`,optionValue)):storage.setItem(`${channel}_${key}`,optionValue);
};
};
  
(argueObj["do"])&&(argueObj["do"][0]=="reset")&&(window.location.href=`/${channel}/`);

// function to replace fontawesome key
function fontAwe(fontKey,fontID="") {
var fontI = document.createElement('i');
fontI.className = fontKey;
if (fontID) {fontI.id = fontID;};
return fontI;
};

// function to replace fontawesome key
function link(href,innerArr,jump = '',label = '') {
let classArr = new Array();
if (href == "") {
var tag = document.createElement('span');
classArr.push("hideBtn");
} else {
var tag = document.createElement('a');
classArr.push("linkDecor");
classArr.push("activeBtn");
tag.href = href;
if (jump) {tag.target = jump;};
};
if (label) {classArr.push(label);};
for (let ia = 0; ia < innerArr.length; ia++) {
if (typeof(innerArr[ia])=="string") {tag.append(innerArr[ia])};
if (typeof(innerArr[ia])=="object") {tag.appendChild(innerArr[ia])};
};
tag.className = classArr.join(" ");
return tag;
};

function compareLength(aArr,bArr) {
if (aArr.length > 0) {return aArr};
if (bArr.length > 0) {return bArr};
return bArr;
};

function getArr(inputStr) {return inputStr?inputStr.split(","):new Array();};
var keyArr = compareLength(optionObj['key'],getArr(storage.getItem(`${channel}_key`)));
storage.setItem(`${channel}_key`,keyArr.join(","));

function addTag(addStr) {
var addKeyArr = getArr(storage.getItem(`${channel}_key`));
if (!addKeyArr.includes(addStr)) {addKeyArr.push(addStr);};
storage.setItem(`${channel}_key`,addKeyArr.join(","));
var targetDOM = document.getElementById(addStr);
if (targetDOM) {
var tagClassEachASpan = link("",[fontAwe(faTagStr)," "+addStr],'','tagBorder');
tagClassEachASpan.id = addStr;
targetDOM.replaceWith(tagClassEachASpan);
};
var tagClassArr = tag_class[addStr];
if (tagClassArr) {
for (let tcai = 0; tcai < tagClassArr.length; tcai++) {
var textTagStr = tagClassArr[tcai]+addStr;
var targetDOM = document.getElementById(textTagStr);
if (targetDOM) {
var tagClassEachASpan = link("",[fontAwe(faTagStr)," "+addStr],'','tagBorder');
tagClassEachASpan.id = textTagStr;
targetDOM.replaceWith(tagClassEachASpan);
};
};
};
draw();
};

function removeTag(removeStr) {
var addKeyArr = getArr(storage.getItem(`${channel}_key`));
var altKeyArr = new Array();
for (let ka = 0; ka < addKeyArr.length; ka++) {
if (addKeyArr[ka] != removeStr) {altKeyArr.push(addKeyArr[ka]);};
};
storage.setItem(`${channel}_key`,altKeyArr.join(","));
var addTagStr = "javascript: void(addTag(\""+removeStr+"\"))";
var targetDOM = document.getElementById(removeStr);
if (targetDOM) {
var tagClassEachASpan = link(addTagStr,[fontAwe(faTagStr)," "+removeStr],'','tagBorder');
tagClassEachASpan.id = removeStr;
targetDOM.replaceWith(tagClassEachASpan);
};
var tagClassArr = tag_class[removeStr];
if (tagClassArr) {
for (let tcai = 0; tcai < tagClassArr.length; tcai++) {
var textTagStr = tagClassArr[tcai]+removeStr;
var targetDOM = document.getElementById(textTagStr);
if (targetDOM) {
var tagClassEachASpan = link(addTagStr,[fontAwe(faTagStr)," "+removeStr],'','tagBorder');
tagClassEachASpan.id = textTagStr;
targetDOM.replaceWith(tagClassEachASpan);
};
};
};
draw();
};

function fillIndex() {
var drawKeyArr = getArr(storage.getItem(`${channel}_key`));
indexBarDOM.innerText = "";
var tagClassArr = Object.keys(class_tag);
for (let tli = 0; tli < tagClassArr.length; tli++) {
var tagClassHeadP = document.createElement("div");
tagClassHeadP.className = "indexBar";
var tagClassMemberP = document.createElement("div");
tagClassMemberP.className = "memberBar";
var tagClassStr = tagClassArr[tli];
if (tagClassStr[0] == "#") {
var tagClassASpan = link("",[" "+tagClassStr],'','tagBorder');
tagClassASpan.id = tagClassStr;
tagClassHeadP.appendChild(tagClassASpan);
} else {
var addTagScriptStr = "javascript: void(addTag(\""+tagClassStr+"\"))";
var addTagStr = drawKeyArr.includes(tagClassStr)?"":addTagScriptStr;
tagClassASpan = link(addTagStr,[fontAwe(faTagStr)," "+tagClassStr],'','tagBorder');
tagClassASpan.id = tagClassStr;
tagClassHeadP.appendChild(tagClassASpan);
};
var tagClassEachArr = class_tag[tagClassArr[tli]];
for (let tcea = 0; tcea < tagClassEachArr.length; tcea++) {
var textTagStr = tagClassEachArr[tcea];
var addTagStr = drawKeyArr.includes(textTagStr)?"":"javascript: void(addTag(\""+textTagStr+"\"))";
var tagClassEachASpan = link(addTagStr,[fontAwe(faTagStr)," "+textTagStr],'','tagBorder');
tagClassEachASpan.id = tagClassArr[tli]+textTagStr;
tagClassMemberP.appendChild(tagClassEachASpan);
};
indexBarDOM.appendChild(tagClassHeadP);
indexBarDOM.appendChild(tagClassMemberP);
};
};

function filter() {
var sortStr = storage.getItem(`${channel}_sort`);
var filtered = new Array();
var filterKeyArr = getArr(storage.getItem(`${channel}_key`));
var playlistKeyArr = Object.keys(playlist);
// default: old to new (oldest) # in playlist
// true: new to old (newest)
// false: old to new (oldest)
// no filterKey (true) + "neutral":newest first (true)
// no filterKey (true) + "newest":newest first (true)
// no filterKey (true) + "oldest":oldest first (false)
// have filterKey (false) + "neutral":oldest first (false)
// have filterKey (false) + "newest":newest first (true)
// have filterKey (false) + "oldest":oldest first (false)
for (let nub = 0; nub < playlistKeyArr.length; nub++) {
var filteredBool = (filterKeyArr.length == 0);
var sortKeyBool = filteredBool?(sortStr != "oldest"):(sortStr == "newest");
ord = sortKeyBool?playlistKeyArr[playlistKeyArr.length - nub - 1] :playlistKeyArr[nub];
if (filteredBool) {
filtered.push(ord);
} else { // if filterKeyArr.length > 0
if (storage.getItem(`${channel}_union`) == 'true') {
var unionBool = false;
for (let pot = 0; pot < playlist[ord]["tag"].length; pot++) {
// tag key include track tag, include
if (filterKeyArr.includes(playlist[ord]["tag"][pot])) {unionBool = true;};
};
if (unionBool) {filtered.push(ord);};
} else {
var unionBool = true;
for (let oki = 0; oki < filterKeyArr.length; oki++) {
// track tag not include all tag key, reject
if (!playlist[ord]["tag"].includes(filterKeyArr[oki])) {unionBool = false;};
};
if (unionBool) {filtered.push(ord);};
};
};
};
storage.setItem(`${channel}_filtered`,filtered.join(","))
};

function draw() {
filter();
unionSDOM.innerHTML = "";
tagListDOM.innerHTML = "";
var drawKeyArr = getArr(storage.getItem(`${channel}_key`));
if (drawKeyArr.length > 0) {
toggleLayout("selected_tags","on")
shareTagDOM.style["display"] = "block";
tagSpanDOM.innerText = "："+drawKeyArr.join("、");
if (drawKeyArr.length > 1) {
tagNoteDOM.innerText = "：";
var drawUnionStr = storage.getItem(`${channel}_union`);
var unionToggleBool = (drawUnionStr == "true");
unionSDOM.appendChild(fontAwe(unionToggleBool?unionToggleOnStr:unionToggleOffStr));
unionSDOM.append(" ");
var unionA = document.createElement("a");
unionA.append(unionToggleBool?"聯集":"交集");
unionA.href = "javascript: void(toggleUnion())";
unionSDOM.appendChild(unionA);
} else {
tagNoteDOM.innerHTML = "";
tagNoteDOM.appendChild(fontAwe(faTagStr));
tagNoteDOM.append(" 已選：");
};
for (let oka = 0; oka < drawKeyArr.length; oka++) {
var removeTagStr = "javascript: void(removeTag(\""+drawKeyArr[oka]+"\"))";
okaArr = [fontAwe(faTagStr)," "+drawKeyArr[oka]+" ",fontAwe("fa-solid fa-delete-left fa-fw")];
tagListDOM.appendChild(link(removeTagStr,okaArr,'','tagBorder'));
};
} else {
toggleLayout("selected_tags","off")
shareTagDOM.style["display"] = "none";
tagSpanDOM.innerText = "";
};
playlistDOM.innerHTML = "";
var podObj = {};
var nowStr = storage.getItem(`${channel}_now`);
var storedArr = getArr(storage.getItem(`${channel}_filtered`));
var filteredArr = (nowStr&&!storedArr.includes(nowStr))?[nowStr].concat(storedArr):storedArr;
for (let nub = 0; nub < filteredArr.length; nub++) {
var tar = filteredArr[nub];
var entryPg = document.createElement('div');
entryPg.id = "entry"+tar;
entryPg.className = "entry";
var popDetailStr = "javascript: void(popDetail(\""+tar+"\"))";
var titlePdom = document.createElement("p");
titlePdom.className = "titletrack";
var titleAdom = document.createElement("a");
titleAdom.innerText = playlist[tar]['name'];
titleAdom.href = popDetailStr;
titlePdom.appendChild(titleAdom);
entryPg.appendChild(titlePdom);
var buttonPdom = document.createElement("p");
buttonPdom.className = "buttonPdom";
var playSpan = document.createElement('span');
playSpan.className = "tagBorder";
podObj[tar] = nub;
var playIdArr = [fontAwe("fa-solid fa-play fa-fw",fontID="playIco"+tar)];
playSpan.appendChild(link("javascript: void(goToPlay(\""+tar+"\"))",playIdArr));
buttonPdom.appendChild(playSpan);
var controlSpan = document.createElement('span');
controlSpan.className = "tagBorder";
if (show_apple) {
  controlSpan.appendChild(link(playlist[tar]["apple"],[fontAwe("fa-brands fa-apple fa-fw")],"podcast"));
}
if (show_google) {
  controlSpan.appendChild(link(playlist[tar]["google"],[fontAwe("fa-brands fa-google fa-fw")],"podcast"));
}
if (show_spotify) {
  controlSpan.appendChild(link(playlist[tar]["spotify"],[fontAwe("fa-brands fa-spotify fa-fw")],"podcast"));
}
if (show_youtube) {
  controlSpan.appendChild(link(playlist[tar]["youtube"],[fontAwe("fa-brands fa-youtube fa-fw")],"podcast"));
}
buttonPdom.appendChild(controlSpan);
var shareSpan = document.createElement('span');
shareSpan.className = "tagBorder";
var shareStr = "javascript: void(shareNow(0,\""+tar+"\"))";
shareSpan.appendChild(link(popDetailStr,[fontAwe(faTagStr)],"","tagBtn"));
shareSpan.appendChild(link(popDetailStr,[fontAwe("fa-solid fa-circle-info fa-fw")]));
shareSpan.appendChild(link(shareStr,[fontAwe("fa-solid fa-share-from-square fa-fw")]));
buttonPdom.appendChild(shareSpan);
var tagsListSpan = document.createElement('span');
tagsListSpan.className = "tagList";
for (let tagi = 0; tagi < playlist[tar]["tag"].length; tagi++) {
var textTagStr = playlist[tar]["tag"][tagi];
var addTagStr = drawKeyArr.includes(textTagStr)?"":"javascript: void(addTag(\""+textTagStr+"\"))";
tagsListSpan.appendChild(link(addTagStr,[fontAwe(faTagStr)," "+textTagStr],'','tagBorder'));
}
buttonPdom.appendChild(tagsListSpan);
entryPg.appendChild(buttonPdom);
playlistDOM.appendChild(entryPg);
storage.setItem(`${channel}_podcast`,JSON.stringify(podObj));
};
doQueue(storage.getItem(`${channel}_now`));
};

async function doNext() {
afterPause();
var queueObj = JSON.parse(storage.getItem(`${channel}_queue`)||"{}");
var nowStr = storage.getItem(`${channel}_now`);
mixPause();
var nextStr = queueObj[nowStr];
if (nextStr) {
doQueue(nextStr);
await doPlay(nextStr);
} else {
afterStop();
};
};

async function doPrev() {
afterPause();
var antiQueueObj = JSON.parse(storage.getItem(`${channel}_anti-queue`)||"{}");
var nowStr = storage.getItem(`${channel}_now`);
mixPause();
var prevStr = antiQueueObj[nowStr];
if (prevStr) {doQueue(prevStr); await doPlay(prevStr);};
};

function updatePositionState() {
if (navigator.mediaSession.metadata) {
navigator.mediaSession.setPositionState({
duration:playerDOM.duration,
playbackRate:playerDOM.playbackRate,
position:playerDOM.currentTime
});
};
storage.setItem(`${channel}_currentTS`,playerDOM.currentTime.toString())
};

function changeIcon(targetName,targetValue) {
var icoDOM = document.getElementById(targetName);
if (icoDOM) {icoDOM.className = targetValue};
};

function afterPause() {
navigator.mediaSession.playbackState = 'paused';
var nowStr = storage.getItem(`${channel}_now`)||"";
changeIcon("playIco"+nowStr,'fa-solid fa-play fa-fw');
if (nowStr!="") {
trackTitleDOM.innerHTML = "";
trackTitleDOM.appendChild(fontAwe(pausedStr));
trackTitleDOM.append(" 暫停：");
trackTitleDOM.append(playlist[nowStr]['name']);
shareEpiDOM.style["display"] = "block";
shareCutDOM.style["display"] = "block";
};
playBTN.style["display"] = "block";
pauseBTN.style["display"] = "none";
};

function afterStop() {
trackTitleDOM.innerHTML = "";
trackTitleDOM.appendChild(fontAwe(stopStr));
trackTitleDOM.append(" 播放完成：請點選任意集數開始播放");
shareEpiDOM.style["display"] = "none";
shareCutDOM.style["display"] = "none";
};

function afterPlay() {
navigator.mediaSession.playbackState = 'playing';
var nowStr = storage.getItem(`${channel}_now`)||"";
changeIcon("playIco"+nowStr,'fa-solid fa-pause fa-fw');
var nowDOM = document.getElementById("entry"+nowStr);
if (nowDOM) {nowDOM.scrollIntoView({ behavior:'smooth' })};
if (nowStr!="") {
trackTitleDOM.innerHTML = "";
trackTitleDOM.appendChild(fontAwe(playingStr));
trackTitleDOM.append(" 播放：");
trackTitleDOM.append(playlist[nowStr]['name']);
shareEpiDOM.style["display"] = "block";
shareCutDOM.style["display"] = "block";
};
playBTN.style["display"] = "none";
pauseBTN.style["display"] = "block";
let nameStr = playlist[storage.getItem(`${channel}_now`)]['image'];
popPipDOM.style['background-image'] = `url("https://klo.lt/p/${nameStr}/512.png")`;
navigator.mediaSession.metadata = new MediaMetadata({
title:playlist[storage.getItem(`${channel}_now`)]['name'],
artist:final_artist_str,
album:playlist[storage.getItem(`${channel}_now`)]['tag'].join(" "),
artwork:[
{ src:`https://klo.lt/p/${nameStr}/96.png`,sizes:'96x96',type:'image/png' },
{ src:`https://klo.lt/p/${nameStr}/128.png`,sizes:'128x128',type:'image/png' },
{ src:`https://klo.lt/p/${nameStr}/192.png`,sizes:'192x192',type:'image/png' },
{ src:`https://klo.lt/p/${nameStr}/256.png`,sizes:'256x256',type:'image/png' },
{ src:`https://klo.lt/p/${nameStr}/384.png`,sizes:'384x384',type:'image/png' },
{ src:`https://klo.lt/p/${nameStr}/512.png`,sizes:'512x512',type:'image/png' },
]
});
};

function seakBack(details) {
const skipTime = details.seekOffset || 10;
playerDOM.currentTime = Math.max(playerDOM.currentTime - skipTime,0);
};
function seakForw(details) {
const skipTime = details.seekOffset || 10;
playerDOM.currentTime = Math.min(playerDOM.currentTime+skipTime,playerDOM.duration);
};
function seakGoTo(details) {playerDOM.currentTime = details.seekTime;};
function jumpTo() {(storage.getItem(`${channel}_currentTS`)=="")||(playerDOM.currentTime = storage.getItem(`${channel}_currentTS`))};

async function doPlay(inputStr) {
initPlay(inputStr);
storage.setItem(`${channel}_currentTS`,"");
await mixPlay();
};

function initPlay(inputStr) {
playerDOM.src = playlist[inputStr]['feed'];
storage.setItem(`${channel}_now`,inputStr);
trackTitleDOM.innerHTML = "";
trackTitleDOM.appendChild(fontAwe(selectedStr));
trackTitleDOM.append(" 已選：");
trackTitleDOM.append(playlist[inputStr]['name']);
var nowDOM = document.getElementById("entry"+inputStr);
if (nowDOM) {nowDOM.scrollIntoView({ behavior:'smooth' })};
};

function doQueue(inputStr) {
var gpPodObj = JSON.parse(storage.getItem(`${channel}_podcast`)||"{}");
var gpPodArr = Object.keys(gpPodObj);
var gpQueueObj = {};
var gpAntiQueueObj = {};
var inputBool = Object.keys(gpPodObj).includes(inputStr);
if (!inputBool) {gpQueueObj[inputStr] = gpPodArr[0];};
var targetInt = inputBool?parseInt(gpPodObj[inputStr]):0;
for (let qa = targetInt; qa < gpPodArr.length - 1; qa++) {
gpQueueObj[gpPodArr[qa]] = gpPodArr[qa+1];
};
if (targetInt) {
for (let qa = 0; qa < targetInt; qa++) {
gpAntiQueueObj[gpPodArr[qa+1]] = gpPodArr[qa];
};
};
storage.setItem(`${channel}_queue`,JSON.stringify(gpQueueObj));
storage.setItem(`${channel}_anti-queue`,JSON.stringify(gpAntiQueueObj));
};

async function goToPlay(targetStr) {
afterPause();
doQueue(targetStr);
var nowStr = storage.getItem(`${channel}_now`);
if (nowStr === targetStr) {
playerDOM.paused?await mixPlay():mixPause();
} else {
await doPlay(targetStr);
};
};

function convertTimer(inputSeconds) {
var seconds = Math.floor(inputSeconds % 60);
if (seconds < 10) {seconds = "0"+seconds};
var minutes = Math.floor(inputSeconds / 60);
return minutes+":"+seconds;
};

async function doPiP() {
await updatePiP();
videoDOM.srcObject = canvasDOM.captureStream();
await videoDOM.play();
await videoDOM.requestPictureInPicture();
};

async function updatePiP() {
canvasDOM.getContext('2d').clearRect(0,0,512,512);
let nameStr = playlist[storage.getItem(`${channel}_now`)]['image'];
const image = new Image();
image.crossOrigin = true;
image.src = `https://klo.lt/p/${nameStr}/512.png`;
await image.decode();
canvasDOM.getContext('2d').drawImage(image,0,0,512,512);
};

async function mixPlay() {
let nowStr = storage.getItem(`${channel}_now`);
let nameStr = playlist[nowStr]['image'];
popPipDOM.style['background-image'] = `url("https://klo.lt/p/${nameStr}/512.png")`;
if (document.pictureInPictureEnabled) {popADOM.href = "javascript: void(doPiP())";};
var playPromise = playerDOM.play();
if (playPromise !== undefined) {
playPromise.then(_ => {
if (document.pictureInPictureElement&&(!window.matchMedia('(display-mode: standalone)').matches)) {
updatePiP();
if (videoDOM.paused) {videoDOM.play()};
};
jumpTo();
for (const [action,handler] of actionHandlers) {
try {
navigator.mediaSession.setActionHandler(action,handler);
} catch (error) {
console.log(`The media session action "${action}" is not supported yet.`);
};
};
}).catch(error => {
mixPause();
setTimeout(() => {
console.error(error);
mixPlay();
},"2000")
});
};
};

async function mixPause() {
playerDOM.pause();
if (document.pictureInPictureElement) {
if (!videoDOM.paused) {videoDOM.pause()};
};
};

function toggleLayout(sectionStr,modeStr) {
var positionInt = sectionObj[sectionStr]["pos"];
var targetDOM = sectionObj[sectionStr]["dom"];
var onStr = sectionObj[sectionStr]["on"];
var layoutArr = contentDOM.style['grid-template-rows'].split(" ");
var beforeStr = layoutArr[positionInt];
var offBool = (beforeStr=="0px");
var conditionBool = false;
if (modeStr=="toggle") {
layoutArr[positionInt] = offBool?onStr:"0px";
targetDOM.style["visibility"] = offBool?"visible":"hidden";
conditionBool = offBool?true:false;
} else if (modeStr=="on") {
layoutArr[positionInt] = onStr;
targetDOM.style["visibility"] = "visible";
conditionBool = true;
} else if (modeStr=="off") {
layoutArr[positionInt] = "0px";
targetDOM.style["visibility"] = "hidden";
conditionBool = false;
} else if (modeStr=="check") {
conditionBool = offBool?false:true;
};
contentDOM.style['grid-template-rows'] = layoutArr.join(" ");
return conditionBool;
};

function toggleTag() {
// hide other sections
toggleLayout("more_option","off");
moreIDOM.className = moreDownStr;
toggleLayout("episode_detail","off");
// toggle index
var toggleTagBool = toggleLayout("tags_list","toggle");
tagIDOM.className = toggleTagBool?tagUpStr:tagDownStr;
resizeDiv();
};

function toggleMoreOpt() {
// hide other sections
toggleLayout("tags_list","off")
tagIDOM.className = tagDownStr;
toggleLayout("episode_detail","off");
// toggle option
var toggleMoreOptBool = toggleLayout("more_option","toggle");
moreIDOM.className = toggleMoreOptBool?moreUpStr:moreDownStr;
resizeDiv();
clearShare();
};

function closeDetail() {
toggleLayout("episode_detail","off");
resizeDiv();
};

function popDetail(tar) {
// hide other sections
toggleLayout("more_option","off");
moreIDOM.className = moreDownStr;
toggleLayout("tags_list","off")
tagIDOM.className = tagDownStr;
toggleLayout("episode_detail","on");
resizeDiv();
//
var drawKeyArr = getArr(storage.getItem(`${channel}_key`));
var entryPg = document.createElement('div');
entryPg.id = "entry"+tar;
entryPg.className = "entryDetail";
var topPdom = document.createElement("p");
topPdom.className = "entryDetailMove";
var topAdom = document.createElement("a");
topAdom.href = "javascript: void(closeDetail())";
topAdom.appendChild(fontAwe("fa-solid fa-circle-info fa-fw"));
topAdom.append(" 單集細節·");
topAdom.append("點此關閉 ");
topAdom.appendChild(fontAwe("fa-solid fa-square-xmark fa-fw"));
topPdom.appendChild(topAdom);
entryPg.appendChild(topPdom);
var titleHdom = document.createElement("h3");
titleHdom.className = "titletrack";
titleHdom.append(playlist[tar]['name']);
entryPg.appendChild(titleHdom);
var tagsListSpan = document.createElement("p");
for (let tagi = 0; tagi < playlist[tar]["tag"].length; tagi++) {
var textTagStr = playlist[tar]["tag"][tagi];
var haveKeyBool = drawKeyArr.includes(textTagStr);
var addTagStr = haveKeyBool?"":"javascript: void(addTag(\""+textTagStr+"\"))";
var tagLink = document.createElement(haveKeyBool?"span":"a");
tagLink.className = haveKeyBool?"detailTag hideBtn":"detailTag";
tagLink.href = addTagStr;
tagLink.appendChild(fontAwe(faTagStr));
tagLink.append(" "+textTagStr);
tagsListSpan.appendChild(tagLink);
tagsListSpan.append(" ");
// tagsListSpan.appendChild(link(addTagStr,[fontAwe(faTagStr),textTagStr]));
};
entryPg.appendChild(tagsListSpan);
// entryPg.appendChild(document.createElement("p"));
var buttonPdom = document.createElement("p");
buttonPdom.className = "buttonBar";
var playSpan = document.createElement('span');
playSpan.className = "tagBorder";
var playIdArr = [fontAwe("fa-solid fa-play fa-fw",fontID="playIco"+tar)];
playSpan.appendChild(link("javascript: void(goToPlay(\""+tar+"\"))",playIdArr));
buttonPdom.appendChild(playSpan);
var controlSpan = document.createElement('span');
controlSpan.className = "tagBorder";
if (show_apple) {
  controlSpan.appendChild(link(playlist[tar]["apple"],[fontAwe("fa-brands fa-apple fa-fw")],"podcast"));
}
if (show_google) {
  controlSpan.appendChild(link(playlist[tar]["google"],[fontAwe("fa-brands fa-google fa-fw")],"podcast"));
}
if (show_spotify) {
  controlSpan.appendChild(link(playlist[tar]["spotify"],[fontAwe("fa-brands fa-spotify fa-fw")],"podcast"));
}
if (show_youtube) {
  controlSpan.appendChild(link(playlist[tar]["youtube"],[fontAwe("fa-brands fa-youtube fa-fw")],"podcast"));
}
controlSpan.appendChild(link(playlist[tar]["feed"],[fontAwe("fa-solid fa-file-audio fa-fw")],"podcast"));
buttonPdom.appendChild(controlSpan);
var shareSpan = document.createElement('span');
shareSpan.className = "tagBorder";
var shareStr = "javascript: void(shareNow(0,\""+tar+"\"))";
shareSpan.appendChild(link(shareStr,[fontAwe("fa-solid fa-share-from-square fa-fw")]));
buttonPdom.appendChild(shareSpan);
entryPg.appendChild(buttonPdom);
// entryPg.appendChild(document.createElement("p"));
var extraArr = Object.keys(playlist[tar]["extra"]);
if (extraArr.length > 0) {
for (let ind = 0; ind < extraArr.length; ind++) {
var extraKey = extraArr[ind];
var extraValue = playlist[tar]["extra"][extraKey];
var extraP = document.createElement("p");
extraP.className = "extraLink entryDetailMove";
var extraA = document.createElement('a');
extraA.appendChild(fontAwe("fa-brands fa-youtube fa-fw"));
extraA.append(" ",extraKey);
extraA.href = extraValue;
extraA.target = "extra";
extraP.appendChild(extraA);
entryPg.appendChild(extraP);
};
};
var tagDivP = document.createElement("p");
tagDivP.className = "descripBar";
tagDivP.innerHTML = playlist[tar]['description'];
entryPg.appendChild(tagDivP);
detailPgDOM.innerHTML = "";
detailPgDOM.appendChild(entryPg);
};

function toggleUnion() {
var nowUnionStr = storage.getItem(`${channel}_union`);
var nextUnionStr = (nowUnionStr == "true")?"false":"true";
storage.setItem(`${channel}_union`,nextUnionStr);
draw();
};

function toggleBtn(sectionStr) {
var sectionNowStr = storage.getItem(`${channel}_${sectionStr}`);
var nextStr = paramObj[sectionStr][sectionNowStr]['next'];
storage.setItem(`${channel}_${sectionStr}`,nextStr);
};
function updateTxtNBtn(sectionStr,targetADOM,targetIDOM,targetMDOM) {
var sectionNowStr = storage.getItem(`${channel}_${sectionStr}`);
targetADOM.innerText = paramObj[sectionStr][sectionNowStr]["text"];
targetIDOM.className = paramObj[sectionStr][sectionNowStr]["class"];
targetMDOM.className = paramObj[sectionStr][sectionNowStr]["class"];
};
function updateTheme(sectionStr) {
var positionInt = paramObj[sectionStr]["position"];
var nowThemeStr = storage.getItem(`${channel}_${sectionStr}`);
var layoutArr = document.body.className.split(" ");
layoutArr[positionInt]=nowThemeStr;
document.body.className = layoutArr.join(" ");
}
    
function toggleSort() {
toggleBtn("sort");
updateTxtNBtn("sort",sortADOM,sortIDOM,sortMDOM);
draw();
};
function toggleTheme(sectionStr,targetADOM,targetIDOM,targetMDOM) {
toggleBtn(sectionStr);
updateTheme(sectionStr);
updateTxtNBtn(sectionStr,targetADOM,targetIDOM,targetMDOM);
};
function toggleColour() {toggleTheme("colour",colourADOM,colourIDOM,colourMDOM)};
function toggleContrast() {toggleTheme("contrast",contraADOM,contraIDOM,contraMDOM)};

function resizeDiv() {
var verticalBool = (window.visualViewport.height > window.visualViewport.width);
var smallHeightBool = window.visualViewport.height <= 800;
var epiDtalBool = toggleLayout("episode_detail","check");
var moreOptBool = toggleLayout("more_option","check");
var tagslstBool = toggleLayout("tags_list","check");
if (smallHeightBool) {
(epiDtalBool||moreOptBool||tagslstBool)?toggleLayout("episodes_list","off"):toggleLayout("episodes_list","on");
} else if (epiDtalBool) {
toggleLayout("episodes_list","off");
} else {
toggleLayout("episodes_list","on");
};
};

function shareTags() {
if (navigator.share) {
var drawKeyArr = getArr(storage.getItem(`${channel}_key`));
var targetUrl_str = final_root_path+"?key="+drawKeyArr.join(",");
var targetTitle_str = "【"+final_artist_str+"】標籤："+drawKeyArr.join("、");
navigatorShare(targetUrl_str,targetTitle_str);
} else {
clipboardShare(targetUrl_str);
};
};

function shareNow(t=0,at="") {
if (navigator.share) {
var drawKeyArr = getArr(storage.getItem(`${channel}_key`));
var nowStr = (at=="")?storage.getItem(`${channel}_now`):at;
var currentTsValue = storage.getItem(`${channel}_currentTS`);
var currentTsStr = (currentTsValue==""||t==0)?"":`&currentTS=${currentTsValue}`;
var targetUrl_str = `${final_root_path}?key=${drawKeyArr.join(",")}&now=${nowStr}${currentTsStr}`;
var targetTitle_str = `【${final_artist_str}】：${playlist[nowStr]['name']}`;
navigatorShare(targetUrl_str,targetTitle_str);
} else {
clipboardShare(targetUrl_str);
};
};

function clearShare() {shareRsDivDOM.style["display"] = "none";};

async function navigatorShare(targetUrl,targetTitle) {
var shareData = {
url:targetUrl,
title:final_title_str,
text:targetTitle,
};
shareRsDivDOM.style["display"] = "block";
shareRsADOM.textContent = "嘗試分享";
shareLinkDOM.href = targetUrl;
try {
await navigator.share(shareData);
shareRsADOM.textContent = "謝謝分享";
shareLinkDOM.href = targetUrl;
} catch (err) {
const { name,message } = err;
if (name === "AbortError") {
shareRsADOM.textContent = "取消分享";
shareLinkDOM.href = targetUrl;
} else {
shareRsADOM.textContent = err;
shareLinkDOM.href = targetUrl;
};
};
};

function clipboardShare(targetUrl) {
shareContentDOM.value = targetUrl;
shareContentDOM.setAttribute("type", "text");
shareContentDOM.select();
shareRsDivDOM.style["display"] = "block";
shareRsADOM.textContent = "嘗試分享";
shareLinkDOM.href = targetUrl;
try {
navigator.clipboard.writeText(targetUrl)
.then(() => {
alert(`${targetUrl} - 複製成功`);
shareRsADOM.textContent = "複製成功";
shareLinkDOM.href = targetUrl;
})
.catch(() => {
alert("複製失敗");
shareRsADOM.textContent = "複製失敗";
shareLinkDOM.href = targetUrl;
});
} catch (err) {
alert("無法複製");
shareRsADOM.textContent = "無法複製";
shareLinkDOM.href = targetUrl;
};
};

function remToPx(rem) {
let fontSize = getComputedStyle(document.documentElement).fontSize;
let rootFontSize = parseFloat(fontSize);
let pxValue = rem * rootFontSize;
return pxValue;
}

function dragMouseDown(e) {
e.preventDefault();
moveTop = e.clientY;
moveLeft = e.clientX;
document.onmouseup = closeDragElement;
document.onmousemove = elementDrag;
// playerBarDOM.style.border = "solid var(--ctbr)";
// playerBarDOM.style.position = "absolute";
// playerBarDOM.style.padding = ".5rem";
}

function dragTouchStart(e) {
e.preventDefault();
moveTop = e.touches[0].clientY;
moveLeft = e.touches[0].clientX;
document.ontouchend = closeDragElement;
document.ontouchmove = elementTouchDrag;
// playerBarDOM.style.border = "solid var(--ctbr)";
// playerBarDOM.style.position = "absolute";
// playerBarDOM.style.padding = ".5rem";
}

function applyDrag() {
var satPropertyValue = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sat"), 10);
var sarPropertyValue = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sar"), 10);
var sabPropertyValue = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sab"), 10);
var salPropertyValue = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sal"), 10);
var safeAreaInsetTop    = isNaN(satPropertyValue)? 0 : satPropertyValue;
var safeAreaInsetRight  = isNaN(sarPropertyValue)? 0 : sarPropertyValue;
var safeAreaInsetBottom = isNaN(sabPropertyValue)? 0 : sabPropertyValue;
var safeAreaInsetLeft   = isNaN(salPropertyValue)? 0 : salPropertyValue;
var permUpperTop  = safeAreaInsetTop  + remToPx(0.5);
var permUpperLeft = safeAreaInsetLeft + remToPx(0.5);
var permLowerTop  = window.innerHeight - playerBarDOM.offsetHeight - safeAreaInsetBottom - remToPx(0.5);
var permLowerLeft = window.innerWidth  - playerBarDOM.offsetWidth  - safeAreaInsetRight  - remToPx(0.5);
if (newTop  > permLowerTop ) newTop  = permLowerTop ;
if (newLeft > permLowerLeft) newLeft = permLowerLeft;
if (newTop  < permUpperTop ) newTop  = permUpperTop ;
if (newLeft < permUpperLeft) newLeft = permUpperLeft;

playerBarDOM.style.top = newTop + "px";
playerBarDOM.style.left = newLeft + "px";
playerBarDOM.style.bottom = "auto";
playerBarDOM.style.right = "auto";
// if (newTop >= permLowerTop) {
//     playerBarDOM.style.border = "solid var(--plbr)";
//     playerBarDOM.style.position = "static";
//     playerBarDOM.style.padding = ".25rem .5rem";
// };
}

function elementDrag(e) {
e.preventDefault();
storeTop = moveTop - e.clientY;
storeLeft = moveLeft - e.clientX;
moveTop = e.clientY;
moveLeft = e.clientX;

newTop = playerBarDOM.offsetTop - storeTop;
newLeft = playerBarDOM.offsetLeft - storeLeft;
applyDrag();
}

function elementTouchDrag(e) {
e.preventDefault();
storeTop = moveTop - e.touches[0].clientY;
storeLeft = moveLeft - e.touches[0].clientX;
moveTop = e.touches[0].clientY;
moveLeft = e.touches[0].clientX;

newTop = playerBarDOM.offsetTop - storeTop;
newLeft = playerBarDOM.offsetLeft - storeLeft;
applyDrag();
}

function closeDragElement() {
document.onmouseup = null;
document.onmousemove = null;
document.ontouchend = null;
document.ontouchmove = null;
console.log("permUpperTop: "+permUpperTop);
console.log("permUpperLeft: "+permUpperLeft);
console.log("permLowerTop: "+permLowerTop);
console.log("permLowerLeft: "+permLowerLeft);
console.log("newTop: "+newTop);
console.log("newLeft: "+newLeft);
console.log("playerBarDOM.offsetTop: "+playerBarDOM.offsetTop);
console.log("playerBarDOM.offsetLeft: "+playerBarDOM.offsetLeft);
}

// load json
let date = new Date();
let timestamp = date.getFullYear().toString().substr(-2) + ('0' + (date.getMonth() + 1)).slice(-2) + ('0' + date.getDate()).slice(-2) + ('0' + date.getHours()).slice(-2);
Promise.all([
fetch(`/${channel}-playlist.json?${timestamp}`)
.then(response => response.json())
.then(data  => {
playlist = data;
console.log('[playlist] length:', Object.keys(playlist).length);
})
.catch(error => console.error('[playlist] Error:', error)),
//
fetch(`/${channel}-tag_class.json?${timestamp}`)
.then(response => response.json())
.then(data  => {
tag_class = data;
console.log('[tag_class] length:', Object.keys(tag_class).length);
})
.catch(error => console.error('[tag_class] Error:', error)),
//
fetch(`/${channel}-class_tag.json?${timestamp}`)
.then(response => response.json())
.then(data  => {
class_tag = data;
console.log('[class_tag] length:', Object.keys(class_tag).length);
})
.catch(error => console.error('[class_tag] Error:', error))
]).then(() => {
(storage.getItem(`${channel}_now`)=="")||initPlay(storage.getItem(`${channel}_now`));
fillIndex();
updateTxtNBtn("sort",sortADOM,sortIDOM,sortMDOM);
updateTheme("colour");
updateTxtNBtn("colour",colourADOM,colourIDOM,colourMDOM);
updateTheme("contrast");
updateTxtNBtn("contrast",contraADOM,contraIDOM,contraMDOM);
draw();

playerDOM.addEventListener('play',afterPlay,false);
playerDOM.addEventListener('pause',afterPause,false);
playerDOM.addEventListener('ended',doNext,false);
playerDOM.addEventListener('loadedmetadata',function() {
totalDOM.innerHTML = convertTimer(playerDOM.duration);
if(storage.getItem(`${channel}_currentTS`)) {
currentDOM.innerHTML = convertTimer(storage.getItem(`${channel}_currentTS`))
} else {
currentDOM.innerHTML = convertTimer(playerDOM.currentTime);
};
cuTSpanDOM.innerText = "："+convertTimer(playerDOM.currentTime);
sliderDOM.max= playerDOM.duration;
sliderDOM.setAttribute("value",playerDOM.currentTime);
});
playerDOM.addEventListener('timeupdate',function() {
currentDOM.innerText = convertTimer(playerDOM.currentTime);
cuTSpanDOM.innerText = "："+convertTimer(playerDOM.currentTime);
sliderDOM.value = playerDOM.currentTime;
sliderDOM.setAttribute("value",playerDOM.currentTime);
updatePositionState();
});
sliderDOM.addEventListener("change",function () {
playerDOM.currentTime = sliderDOM.value;
updatePositionState();
});

videoDOM.addEventListener('play',() => {mixPlay()},false);
videoDOM.addEventListener('pause',() => {mixPause()},false);
canvasDOM.width = canvasDOM.height = 512;
videoDOM.muted = true;

moveBTN.onmousedown = dragMouseDown;
moveBTN.ontouchstart = dragTouchStart;

window.onresize = resizeDiv;
resizeDiv();
});
