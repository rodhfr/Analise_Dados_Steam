(function(){"use strict";try{if(window.sessionStorage.getItem("browser_unsupported"))return}catch{}if(!["fetch","structuredClone","AbortController","BigInt","Clipboard","IntersectionObserver","Intl"].every(t=>t in window)||!("RelativeTimeFormat"in window.Intl)||!("noModule"in HTMLScriptElement.prototype)){const t=window.SteamDB.Alert("SteamDB may not work correctly in your browser. SteamDB uses modern features that your browser does not support.","Unsupported browser"),e=document.createElement("a");e.className="btn btn-sm btn-primary",e.href="https://browsehappy.com/",e.textContent="Update your browser",t.append(e),t.addEventListener("toast-close",()=>{try{window.sessionStorage.setItem("browser_unsupported","1")}catch{}})}})();