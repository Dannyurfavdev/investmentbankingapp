jQuery(document).ready(function(){const launchTime=script_args_launch_timer.launchTime
if(!launchTime){return}
let timerData=[]
if(launchTime&&launchTime.length>0){setInterval(()=>{const future=new Date(launchTime)
let now=new Date()
if(future<now){return false}
let difference=Math.floor((future-now)/1000);let seconds=fixIntTimer(difference%60);difference=Math.floor(difference/60);let minutes=fixIntTimer(difference%60);difference=Math.floor(difference/60);let hours=fixIntTimer(difference%24);difference=Math.floor(difference/24);let days=difference;timerData.minToLaunch=minutes
timerData.dayToLaunch=days
timerData.secToLaunch=seconds
timerData.hoursToLaunch=hours
setLaunchTime(timerData)},1000)}})
function fixIntTimer(integer)
{if(integer<0)
integer=0;if(integer<10)
return "0"+integer;return ""+integer;}
function setLaunchTime(launchData){const elLaunchTimer=document.getElementById('days-launch')
if(elLaunchTimer){document.getElementById('days-launch').innerHTML=`${launchData.dayToLaunch}`
document.getElementById('hours-launch').innerHTML=`${launchData.hoursToLaunch}`
document.getElementById('minutes-launch').innerHTML=`${launchData.minToLaunch}`
document.getElementById('seconds-launch').innerHTML=`${launchData.secToLaunch}`}}