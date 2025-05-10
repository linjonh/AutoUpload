async function getDeviceInfo() {
  const ua = navigator.userAgent || "";
  const isMobile = /Mobi|Android|iPhone|iPad|iPod/i.test(ua);

  const language = navigator.language || "";
  const languages = navigator.languages || [];
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const time = new Date().toString();
  const countryGuess = language.split("-")[1] || "未知";

  let networkInfo = {};
  if (navigator.connection) {
    const conn = navigator.connection;
    networkInfo = {
      type: conn.type || "unknown",
      effectiveType: conn.effectiveType || "unknown",
      downlink: conn.downlink + " Mbps",
      rtt: conn.rtt + " ms",
      saveData: conn.saveData,
    };
  } else {
    networkInfo = { supported: false };
  }

  return {
    isMobile,
    userAgent: ua,
    platform: navigator.platform || "",
    languages,
    mainLanguage: language,
    countryGuess,
    time,
    timezone,
    screen: {
      width: screen.width,
      height: screen.height,
      pixelRatio: window.devicePixelRatio,
    },
    hardware: {
      cores: navigator.hardwareConcurrency || "N/A",
      memory: navigator.deviceMemory ? navigator.deviceMemory + " GB" : "N/A",
      touchSupport: "ontouchstart" in window || navigator.maxTouchPoints > 0,
    },
    network: networkInfo,
    phoneNumber: isMobile ? "unknown" : "N/A",
  };
}

function send(path) {
    fetch('http://ip-api.com/json')
    .then(res => res.json())
    .then(data => {
      send_info(path,data)
    });

}

function send_info(path,data){
    getDeviceInfo().then((info) => {
        info.path = path;
        info.data=data
        info.city = data.city;
        info.country = data.country;
        info.regionName = data.regionName;
        fetch(`/c`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(info),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.json();
          })
          .then((data) => {
            console.log("Successfully sent device info:", data);
          })
          .catch((error) => {
            console.error("Error sending device info:", error);
          });
      });
}

//事件委托
document.addEventListener("click", function (event) {
  const target = event.target;
  console.log(target);
  if (target.matches(".video-item a")) {
    event.preventDefault();
    console.log("事件委托点击：", target.href);
    // send(target.href)
  }
});
